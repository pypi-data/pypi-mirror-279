import os
import time
import random
import itertools
from tqdm import tqdm
from typing import Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
from torch import nn, autograd

from scmidas import models, utils
from scmidas.datasets import MultiDatasetSampler, MultimodalDataset, GetDataInfo
from scmidas.sample import BallTreeSubsample

class MIDAS():
    def __init__(self, data:Union[list, GetDataInfo], status:Union[list, None] = None):
        """
        Args:
            data (list): A list of 'ReadData' objects or a single 'ReadData' object. For a list input, the order of the items influences the order of batch ID distribution to them. If a list is provided, 'current' is always assigned after 'replay'.
            Status (:obj:'list', optional): A list containing 'current' and 'replay' to indicate the property of data to be trained. If not given, 'current' is assigned to all input batches.
            
        Examples:
            for offline integration
            >>> model = MIDAS([ReadData1, ReadData2])

            for continual integration
            >>> model = MIDAS([ReadData1, ReadData2, ReadData3], ['replay', 'replay', 'current'])
        """
        if type(data) is not list:
            data = [data]
        self.data = data
        self.batch_num_rep = 0
        self.batch_num_curr = 0
        self.mods = []
        if not status:
            status = ['current' for i in range(len(self.data))] 
        for i, d in enumerate(data):
            if status[i] == 'replay':
                self.batch_num_rep += d.num_subset
            else:
                self.batch_num_curr += d.num_subset
            self.mods += list(d.mods.values())
        self.total_num = self.batch_num_rep + self.batch_num_curr
        self.s_joint = [[i] for i in range(self.total_num)]
        self.s_joint, self.combs, self.s, self.dims_s = utils.gen_all_batch_ids(self.s_joint, [self.mods])
        self.reference_features = {}
        self.dims_x = {}
        self.dims_chr = []
        self.dims_rep = {}
        for i, d in enumerate(data):
            # d.info()
            for k in d.mod_combination:
                if k == 'atac':
                    self.dims_x['atac'] = d.feat_dims['atac']
                    self.reference_features[k] = d.features['atac']
                    self.dims_chr = d.dims_chr
                    if (status[i] == 'replay') and (k not in self.dims_rep):
                        self.dims_rep[k] = d.feat_dims[k]
                else:
                    if k not in self.reference_features:
                        self.reference_features[k] = d.features[k]
                    else:
                        self.reference_features[k], _ = utils.merge_features(self.reference_features[k].copy(), d.features[k].copy())
                    if status[i] == 'replay':
                        if k not in self.dims_rep:
                            self.dims_rep[k] = d.feat_dims[k]
                        else:
                            self.dims_rep[k], _  = utils.merge_features(self.dims_rep[k], d.feat_dims[k])

        for k in ['atac', 'rna', 'adt']:
            if k in self.reference_features:
                self.dims_x[k] = len(self.reference_features[k])
        
        self.mods = utils.ref_sort(np.unique(np.concatenate(self.mods).flatten()).tolist(), ['atac', 'rna','adt'])
    
    def init_model(
            self, 
            # training related
            train_mod:str = 'offline', 
            lr:float = 1e-4, 
            drop_s:int = 0, 
            s_drop_rate:float = 0.1, 
            grad_clip:int = -1, 
            # structure related
            dim_c:int = 32, 
            dim_b:int = 2, 
            dims_enc_s:list = [16,16], 
            dims_enc_chr:list = [128,32], 
            dims_enc_x:list = [1024,128], 
            dims_discriminator:list = [128,64],
            norm:str = "ln", 
            drop:float = 0.2, 
            disc_train:int = 3,
            # loss related
            loss_s_recon:float = 1000.0,
            loss_mod_alignment:float = 50.0,
            loss_disc:float = 30.0, 
            # checkpoint related
            model_path:Union[str, None] = None,
            log_path:Union[str, None] = None,
            # continual integration related
            continual_from:Union[str, None] = None
            ):
        """Initialize the model structure.

        Args:
            train_mod (str): 'offline': Classic training method (See MIDAS). 'continual': Reciprocal integration method.
            lr (float): Learning rate for training.
            drop_s (float): Whether to force dropping s (batch ID) during training.
            s_drop_rate (float): Dropout rate for s (batch ID).
            grad_clip (int): Whether to clip gradients during training.
            dim_c (list): Dimension of the variable c (biological information).
            dim_b (list): Dimension of the variable b (batch information).
            dims_enc_s (list): List of dimensions for the encoder layers for s (batch ID).
            dims_enc_chr (list): List of dimensions for the encoder layers for chromosomes (used when there is ATAC data).
            dims_enc_x (list): List of dimensions for the encoder layers for data (except ATAC).
            dims_discriminator (list): List of dimensions for the discriminator layers.
            norm (str): Type of normalization. 'ln' or 'bn'.
            drop (float): Dropout rate for the hidden layers.
            disc_train (int): Number of training iterations for the discriminator.
            loss_s_recon (float): Scaling factor for s (batch ID) reconstruction loss.
            loss_mod_alignment (float): Scaling factor for modality alignment loss.
            loss_disc  (float): Scaling factor for the loss used to train the discriminator.
            model_path (str): Path to save the model weights (a ".pt" file).
            log_path (str): Path to save the training status (a ".toml" file).
            continual_from (str): Path to the model weights when using 'continual' training mode (a ".pt" file). This is used only when train_mod == 'continual'.
        """

        assert not (train_mod == 'continual' and continual_from==None), 'Missing weight path to initialize the model when trying to implement continual integration'
        dims_h = {}
        self.train_mod = train_mod
        for m, dim in self.dims_x.items():
            dims_h[m] = dim if m != "atac" else dims_enc_chr[-1] * 22

        self.log = {
            "train_loss": [],
            "test_loss": [],
            "foscttm": [],
            "epoch_id_start": 0,
            }

        self.o = utils.simple_obj({
            # data related
            'mods' : self.mods,
            'dims_x' : self.dims_x,
            'ref_mods': self.mods, # no meanings here
            's_joint' : self.s_joint,
            'combs' : self.combs, 
            's' : self.s, 
            'dims_s' : self.dims_s,
            'dims_chr' : self.dims_chr,
            # model hyper-parameters
            'drop' : drop,
            'drop_s' : drop_s,
            's_drop_rate' : s_drop_rate,
            'grad_clip' : grad_clip,
            'norm' : norm,
            'lr' : lr,
            # model structure
            'dim_c' : dim_c, 
            'dim_b' : dim_b, 
            'dim_s' : self.dims_s["joint"], 
            'dim_z' : dim_c + dim_b, 
            'dims_enc_s' : dims_enc_s, 
            'dims_enc_chr' : dims_enc_chr, 
            'dims_enc_x' : dims_enc_x, 
            'dims_dec_x' : dims_enc_x[::-1],
            'dims_dec_s' : dims_enc_s[::-1],
            'dims_dec_chr' : dims_enc_chr[::-1],
            "dims_h" : dims_h,
            'dims_discriminator' : dims_discriminator,
            "disc_train" : disc_train,
            # loss related
            "loss_s_recon" : loss_s_recon,
            "loss_mod_alignment" : loss_mod_alignment,
            "loss_disc": loss_disc, 
            })

        self.net = models.Net(self.o).cuda()
        self.discriminator = models.Discriminator(self.o).cuda()
        self.optimizer_net = torch.optim.AdamW(self.net.parameters(), lr=self.o.lr)
        self.optimizer_disc = torch.optim.AdamW(self.discriminator.parameters(), lr=self.o.lr)
        
        # initialization for continual learning
        # model structure adaptation
        if self.train_mod == 'continual':
            print('load an old model from', continual_from)
            savepoint = torch.load(continual_from)
            dims_h_rep = {}
            for m, dim in self.dims_rep.items():
                dims_h_rep[m] = dim if m != "atac" else dims_enc_chr[-1] * 22
            self.net = utils.update_model(savepoint, dims_h_rep, self.o.dims_h, self.net)
            self.discriminator = models.Discriminator(self.o).cuda()
            self.optimizer_net = torch.optim.AdamW(self.net.parameters(), lr=self.o.lr)
            self.optimizer_disc = torch.optim.AdamW(self.discriminator.parameters(), lr=self.o.lr)
        # start training from a breakpoint
        if model_path is not None:
            print('load a pretrained model from', model_path)
            savepoint = torch.load(model_path)
            self.net.load_state_dict(savepoint['net_states'])
            self.discriminator.load_state_dict(savepoint['disc_states'])
            self.optimizer_net.load_state_dict(savepoint['optim_net_states'])
            self.optimizer_disc.load_state_dict(savepoint['optim_disc_states'])
        if log_path is not None:
            savepoint_toml = utils.load_toml(log_path)
            self.log.update(savepoint_toml['log'])

        net_param_num = sum([param.data.numel() for param in self.net.parameters()])
        disc_param_num = sum([param.data.numel() for param in self.discriminator.parameters()])
        print('Parameter number: %.3f M' % ((net_param_num+disc_param_num) / 1e6))

    
    def __forward_net__(self, inputs):
        return self.net(inputs)


    def __forward_disc__(self, c, s):
        return self.discriminator(c, s)
    
    def __update_disc__(self, loss):
        self.__update__(loss, self.discriminator, self.optimizer_disc)


    def __update_net__(self,loss):
        self.__update__(loss, self.net, self.optimizer_net)


    def __update_disc__(self,loss):
        self.__update__(loss, self.discriminator, self.optimizer_disc)
        

    def __update__(self,loss, model, optimizer):
        optimizer.zero_grad()
        loss.backward()
        if self.o.grad_clip > 0:
            nn.utils.clip_grad_norm_(model.parameters(), self.o.grad_clip)
        optimizer.step()
        
    def __run_iter__(self, split, epoch_id, inputs, rnt=1):
        inputs = utils.convert_tensors_to_cuda(inputs)
        if split == "train":
            with autograd.set_detect_anomaly(self.debug == 1):
                loss_net, c_all = self.__forward_net__(inputs)
                self.discriminator.epoch = epoch_id
                for _ in range(self.o.disc_train):
                    loss_disc = self.__forward_disc__(utils.detach_tensors(c_all), inputs["s"])
                    loss_disc = loss_disc * rnt
                    self.__update_disc__(loss_disc)
                loss_adv = self.__forward_disc__(c_all, inputs["s"])
                loss_adv = -loss_adv
                loss = loss_net + loss_adv
                loss = rnt * loss
                self.__update_net__(loss)
            
        else:
            with torch.no_grad():
                loss_net, c_all = self.__forward_net__(inputs)
                loss_adv = self.__forward_disc__(c_all, inputs["s"])
                loss_adv = -loss_adv
                loss = loss_net + loss_adv
        return loss.item()

    def __run_epoch__(self, data_loader, split, epoch_id=0):
        start_time = time.time()
        if split == "train":
            self.net.train()
            self.discriminator.train()
        elif split == "test":
            self.net.eval()
            self.discriminator.eval()
        else:
            assert False, "Invalid split: %s" % split
        loss_total = 0
        if self.train_mod == 'continual':
            assert type(data_loader) is list, "Wrong type of dataloader for continual learning."
            current_dataloader = data_loader[1]
            replay_dataloader = data_loader[0]
            for _, data in enumerate(zip(current_dataloader, replay_dataloader)):
                data1, data2 = data[0], data[1]
                rnt_ = self.batch_num_curr / (self.batch_num_rep + self.batch_num_curr)
                loss = self.__run_iter__(split, epoch_id, data1, rnt_)
                loss_total += loss
                rnt_ = self.batch_num_rep / (self.batch_num_rep  + self.batch_num_curr)
                loss = self.__run_iter__(split, epoch_id, data2, rnt_)
                loss_total += loss
            loss_avg = loss_total / len(current_dataloader) / 2
        elif self.train_mod == 'offline':
            rnt_ = 1
            for _, data in enumerate(data_loader):
                loss = self.__run_iter__(split, epoch_id, data, rnt_)
                loss_total += loss
            loss_avg = loss_total / len(data_loader)

        epoch_time = (time.time() - start_time) / 3600 / 24
        self.log[split+'_loss'].append((float(epoch_id), float(loss_avg)))
        return loss_avg, epoch_time
    
    def train(
            self, 
            n_epoch:int = 2000, 
            mini_batch_size:int = 256, 
            shuffle:bool = True, 
            save_epochs:int = 10, 
            debug:int = 0, 
            save_path:str = './result/experiment/'
            ):
        """Train the model.
        
        Args:
            n_epoch (int): Number of training epochs.
            mini_batch_size (int): Size of mini-batches for training.
            shuffle (bool): Whether to shuffle the training data during each epoch.
            save_epochs (int): Frequency to save the latest weights and logs during training.
            debug (int): If True, print intermediate variables for debugging purposes.
            save_path (str): Path to save the trained model and related files.

        """
        print("Training ...")
        self.save_epochs = save_epochs
        self.debug = debug
        self.o.debug = debug
        if self.train_mod == 'continual':
            datasets = self.gen_datasets(self.data)
            replay_datasets = list(datasets[:self.batch_num_rep])
            current_datasets = list(datasets[-self.batch_num_curr:])
            replay_datasets = torch.utils.data.dataset.ConcatDataset(replay_datasets)
            current_datasets = torch.utils.data.dataset.ConcatDataset(current_datasets)
            replay_sampler = MultiDatasetSampler(replay_datasets, batch_size=mini_batch_size, shuffle=shuffle)
            current_sampler = MultiDatasetSampler(current_datasets, batch_size=mini_batch_size, shuffle=shuffle)
            self.data_loader = [
                torch.utils.data.DataLoader(replay_datasets, batch_size=mini_batch_size, sampler=replay_sampler, num_workers=64, pin_memory=True),
                torch.utils.data.DataLoader(current_datasets, batch_size=mini_batch_size, sampler=current_sampler, num_workers=64, pin_memory=True)
            ]
        elif self.train_mod == 'offline':
            datasets = self.gen_datasets(self.data)
            sampler = MultiDatasetSampler(torch.utils.data.dataset.ConcatDataset(datasets), batch_size=mini_batch_size, shuffle=shuffle)
            self.data_loader = torch.utils.data.DataLoader(torch.utils.data.dataset.ConcatDataset(datasets), batch_size=mini_batch_size, sampler=sampler, num_workers=64, pin_memory=True)
        with tqdm(total=n_epoch) as pbar:
            pbar.update(self.log['epoch_id_start'])
            for epoch_id in range(self.log['epoch_id_start'], n_epoch):
                loss_avg, epoch_time = self.__run_epoch__(self.data_loader, "train", epoch_id)
                self.__check_to_save__(epoch_id, n_epoch, save_path)
                pbar.update(1)
                pbar.set_description("Loss: %.4f" % loss_avg)
        
    def predict(self, 
                save_dir:str = './result/experiment/predict/', 
                joint_latent:bool = True, 
                mod_latent:bool = False, 
                impute:bool = False, 
                batch_correct:bool = False, 
                translate:bool = False, 
                input:bool = False, 
                mini_batch_size:int = 256
                ):
        """Predict the embeddings or their imputed expression.

        Args:
            save_dir (str): The path to save the predicted files.
            joint_latent (bool): Whether to generate the joint embeddings.
            impute (bool): Whether to generate the imputed expression data.
            batch_correct (bool): Whether to generate the batch-corrected expression data.
            translate (bool): Whether to generate the translated expressions.
            input (bool): Whether to generate the input data.
            mini_batch_size (bool): The mini-batch size for saving. Influence the cell number in the csv file.
        """
        if translate:
            mod_latent = True
        print("Predicting ...")
        self.o.pred_dir = save_dir
        if not os.path.exists(self.o.pred_dir):
            os.makedirs(self.o.pred_dir)
        dirs = utils.get_pred_dirs(self.o, joint_latent, mod_latent, impute, batch_correct, translate, input)
        parent_dirs = list(set(map(os.path.dirname, utils.extract_values(dirs))))
        utils.mkdirs(parent_dirs, remove_old=True)
        utils.mkdirs(dirs, remove_old=True)
        datasets = self.gen_datasets(self.data)
        data_loaders = {k:torch.utils.data.DataLoader(datasets[k], batch_size=mini_batch_size, \
            num_workers=64, pin_memory=True, shuffle=False) for k in range(self.batch_num_curr+self.batch_num_rep)}
        # data_loaders = get_dataloaders("test", train_ratio=0)
        self.net.eval()
        with torch.no_grad():
            for subset_id, data_loader in data_loaders.items():
                print("Processing subset %d: %s" % (subset_id, str(self.o.combs[subset_id])))
                fname_fmt = utils.get_name_fmt(len(data_loader))+".csv"
                
                for i, data in enumerate(tqdm(data_loader)):
                    data = utils.convert_tensors_to_cuda(data)
                    
                    # conditioned on all observed modalities
                    if joint_latent:
                        x_r_pre, _, _, _, z, _, _, *_ = self.net.sct(data)  # N * K
                        utils.save_tensor_to_csv(z, os.path.join(dirs[subset_id]["z"]["joint"], fname_fmt) % i)
                    if impute:
                        x_r = models.gen_real_data(x_r_pre, sampling=False)
                        for m in self.o.mods:
                            utils.save_tensor_to_csv(x_r[m], os.path.join(dirs[subset_id]["x_impt"][m], fname_fmt) % i)
                    if input:  # save the input
                        for m in self.o.combs[subset_id]:
                            utils.save_tensor_to_csv(data["x"][m].int(), os.path.join(dirs[subset_id]["x"][m], fname_fmt) % i)

                    # conditioned on each individual modalities
                    if mod_latent:
                        for m in data["x"].keys():
                            input_data = {
                                "x": {m: data["x"][m]},
                                "s": data["s"], 
                                "e": {}
                            }
                            if m in data["e"].keys():
                                input_data["e"][m] = data["e"][m]
                            x_r_pre, _, _, _, z, c, b, *_ = self.net.sct(input_data)  # N * K
                            utils.save_tensor_to_csv(z, os.path.join(dirs[subset_id]["z"][m], fname_fmt) % i)
                            if translate: # single to double
                                x_r = models.gen_real_data(x_r_pre, sampling=False)
                                for m_ in set(self.o.mods) - {m}:
                                    utils.save_tensor_to_csv(x_r[m_], os.path.join(dirs[subset_id]["x_trans"][m+"_to_"+m_], fname_fmt) % i)
                    
                    if translate: # double to single
                        for mods in itertools.combinations(data["x"].keys(), 2):
                            m1, m2 = utils.ref_sort(mods, ref=self.o.mods)
                            input_data = {
                                "x": {m1: data["x"][m1], m2: data["x"][m2]},
                                "s": data["s"], 
                                "e": {}
                            }
                            for m in mods:
                                if m in data["e"].keys():
                                    input_data["e"][m] = data["e"][m]
                            x_r_pre, *_ = self.net.sct(input_data)  # N * K
                            x_r = models.gen_real_data(x_r_pre, sampling=False)
                            m_ = list(set(self.o.mods) - set(mods))[0]
                            utils.save_tensor_to_csv(x_r[m_], os.path.join(dirs[subset_id]["x_trans"][m1+"_"+m2+"_to_"+m_], fname_fmt) % i)

            if batch_correct:
                print("Calculating b_centroid ...")
                pred = utils.load_predicted(self.o)
                b = torch.from_numpy(pred["z"]["joint"][:, self.o.dim_c:])
                s = torch.from_numpy(pred["s"]["joint"])

                b_mean = b.mean(dim=0, keepdim=True)
                b_subset_mean_list = []
                for subset_id in s.unique():
                    b_subset = b[s == subset_id, :]
                    b_subset_mean_list.append(b_subset.mean(dim=0))
                b_subset_mean_stack = torch.stack(b_subset_mean_list, dim=0)
                dist = ((b_subset_mean_stack - b_mean) ** 2).sum(dim=1)
                self.net.sct.b_centroid = b_subset_mean_list[dist.argmin()]
                self.net.sct.batch_correction = True
                
                print("Batch correction ...")
                for subset_id, data_loader in data_loaders.items():
                    print("Processing subset %d: %s" % (subset_id, str(self.o.combs[subset_id])))
                    fname_fmt = utils.get_name_fmt(len(data_loader))+".csv"
                    
                    for i, data in enumerate(tqdm(data_loader)):
                        data = utils.convert_tensors_to_cuda(data)
                        x_r_pre, *_ = self.net.sct(data)
                        x_r = models.gen_real_data(x_r_pre, sampling=True)
                        for m in self.o.mods:
                            utils.save_tensor_to_csv(x_r[m], os.path.join(dirs[subset_id]["x_bc"][m], fname_fmt) % i)
    
    def read_embeddings(
            self, 
            emb_path:str = None, 
            joint_latent:bool = True, 
            mod_latent:bool = False, 
            impute:bool = False, 
            batch_correct:bool = False, 
            translate:bool = False, 
            input:bool = False, 
            group_by:str = "modality") -> dict:
        """Get embeddings or other outputs from a specified path.

        Args:
            emb_path (str): The path from which to retrieve the embeddings. If not provided, it uses the path from the previous `predict()` function call, if available.
            joint_latent (bool): Whether to retrieve the joint embeddings.
            impute (bool): Whether to retrieve the imputed expression data.
            batch_correct (bool): Whether to retrieve the batch-corrected expression data.
            translate (bool): Whether to retrieve the translated expressions.
            input (bool): Whether to retrieve the input data.
            group_by (bool): Specify how to group the data: "modality" or "batch".
            
        Returns:
            Embeddings or other outputs obtained from the specified path.
        """

        if emb_path is not None:
            self.o.pred_dir = emb_path
        pred = utils.load_predicted(self.o, joint_latent=joint_latent, mod_latent=mod_latent, impute=impute, batch_correct=batch_correct, 
                   translate=translate, input=input, group_by=group_by)
        return pred
    
    def gen_datasets(self, data:list) -> list:
        """ Generate dataset object
        Args:
            data (list): A list of GetDataInfo containing information about the dataset.

        Returns:
            A list containing torch Dataset objects.
        """
        datasets = []
        n = 0
        for d in data:
            for i in range(d.num_subset):
                datasets.append(MultimodalDataset(d, subset=i, s_subset=self.s[n], reference_features=self.reference_features))
                n += 1
        return datasets

    def viz_loss(self):
        """ 
        Visualize the loss.
        """
        plt.figure(figsize=(4,2))
        plt.plot(np.array(self.log['train_loss'])[:, 0]+1, np.array(self.log['train_loss'])[:, 1])
        plt.xlabel('Training epoch')
        plt.ylabel('Loss')
        plt.title('Loss curve')

    def pack(self, 
             output_task_name:str = 'pack', 
             des_dir:str = './data/processed/', 
             n_sample:int = 100000, 
             pred_dir:Union[str, None] = None):
        """ Pack the data for training or sharing.
    
        Args:
            output_task_name (str): The name of the output. It will be concatenated with 'des_dir' to form the output path.
            des_dir (str): The directory path where the data will be saved.
            n_sample (int): The desired number of samples to be packed. Use the balltree sampling to implement it.
            pred_dir (str): The directory path where the embeddings are stored.
        """

        if pred_dir is None:
            pred_dir = self.o.pred_dir
        else:
            self.o.pred_dir = pred_dir
        print("Packing ...")

        if not os.path.exists(os.path.join(des_dir, output_task_name)):
            os.makedirs(os.path.join(des_dir, output_task_name, 'feat'))

        # load info
        datasets = self.gen_datasets(self.data)
        data_loaders = {k:torch.utils.data.DataLoader(datasets[k], batch_size=1, \
            num_workers=64, pin_memory=True, shuffle=False) for k in range(self.batch_num_curr+self.batch_num_rep)}
        
        emb = self.read_embeddings()
        # print(emb)
        cell_names = {}
        cell_names_sampled = {}
        cell_nums = []
        n = 0
        for d in self.data:
            for k in range(d.num_subset):
                cell_names_sampled[n] = d.cell_names['subset_%d'%k]
                cell_names[n] = d.cell_names_orig['subset_%d'%k]
                cell_nums.append(len(cell_names[n]))
                n += 1

        # cell_nums = np.concatenate([d.subset_cell_num.values for d in self.data]).flatten().tolist()

        # for i in range(self.batch_num_rep):
            # cell_names[i] = pd.read_csv(os.path.join(self.data_path, self.replay_task, 'subset_%d'%i, 'cell_names.csv'), index_col=0)
            # cell_nums.append(len(cell_names[i]))
            # if os.path.exists(os.path.join(self.data_path, self.replay_task, 'subset_%d'%i, 'cell_names_sampled.csv')):
                # cell_names_sampled[i] = pd.read_csv(os.path.join(self.data_path, self.replay_task, 'subset_%d'%i, 'cell_names_sampled.csv'), index_col=0)
        # for i in range(self.batch_num_curr):
            # cell_names[i+self.batch_num_rep] = pd.read_csv(os.path.join(self.data_path, self.current_task, 'subset_%d'%i, 'cell_names.csv'), index_col=0)
            # cell_nums.append(len(cell_names[i+self.batch_num_rep]))
            # if os.path.exists(os.path.join(self.data_path, self.current_task, 'subset_%d'%i, 'cell_names_sampled.csv')):
                # cell_names_sampled[i] = pd.read_csv(os.path.join(self.data_path, self.current_task, 'subset_%d'%i, 'cell_names_sampled.csv'), index_col=0)

        if sum(cell_nums) > n_sample:
            rate = (np.array(cell_nums) / sum(cell_nums)  * n_sample).astype(int)
        else:
            rate = [len(i) for i in datasets]
        sample_preserve = {}
        if not os.path.exists(os.path.join(des_dir, output_task_name, 'feat')):
            os.makedirs(os.path.join(des_dir, output_task_name, 'feat'))
        for i in range(self.batch_num_rep+self.batch_num_curr):
            emb_subset = emb['z']['joint'][emb['s']['joint']==i]
            sample_preserve['subset_%d'%i] = BallTreeSubsample(emb_subset, rate[i])
            sample_preserve['subset_%d'%i].sort()
            # print(sample_preserve['subset_%d'%i])

            if not os.path.exists(os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'mask')):
                os.makedirs(os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'mask'))
            if i in cell_names_sampled:
                # print(i)
                pd.DataFrame(cell_names_sampled[i][sample_preserve['subset_%d'%i]]).to_csv(os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'cell_names_sampled.csv'))
                pd.DataFrame(cell_names[i]).to_csv(os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'cell_names.csv'))
            else:
                pd.DataFrame(cell_names[i][sample_preserve['subset_%d'%i]]).to_csv(os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'cell_names_sampled.csv'))
                pd.DataFrame(cell_names[i]).to_csv(os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'cell_names.csv'))
            fname_fmt = utils.get_name_fmt(rate[i])+".csv"
            n = 0
            for k, data in enumerate(data_loaders[i]):
                if k in sample_preserve['subset_%d'%i]:
                    for m in self.o.combs[i]:
                        if not os.path.exists(os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'vec', m)):
                            os.makedirs(os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'vec', m))
                        utils.save_tensor_to_csv(data["x"][m].int(), os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'vec', m, fname_fmt) % n)
                    n += 1
            for k, data in enumerate(data_loaders[i]):
                for m in self.o.combs[i]:
                    if m != 'atac':
                        pd.DataFrame(utils.convert_tensor_to_list(data["e"][m].int())).to_csv(os.path.join(des_dir, output_task_name, 'subset_%d'%i, 'mask', '%s.csv'%m))
                break

        features_dims = {}
        if self.dims_chr != []:
            features_dims['atac'] = self.dims_chr
        for m in self.reference_features:
            if m != 'atac':
                features_dims[m] = [self.dims_x[m] for i in range(22)]
            pd.DataFrame(self.reference_features[m]).to_csv(os.path.join(des_dir, output_task_name, 'feat','feat_names_%s.csv'%m))
        pd.DataFrame(features_dims).to_csv(os.path.join(des_dir, output_task_name, 'feat','feat_dims.csv'))


    def __check_to_save__(self, epoch_id, epoch_num, save_path):
        if (epoch_id+1) % self.save_epochs == 0 or epoch_id+1 == epoch_num:
            self.__save_training_states__(epoch_id, "sp_%08d"%(epoch_id+1), save_path)
            self.__save_training_states__(epoch_id, "sp_latest", save_path)
    
    def __save_training_states__(self, epoch_id, filename,save_path):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        self.log['epoch_id_start'] = epoch_id + 1
        utils.save_toml({"o": vars(self.o), "log": self.log}, os.path.join(save_path, filename+".toml"))
        torch.save({"net_states": self.net.state_dict(),
                "disc_states": self.discriminator.state_dict(),
                "optim_net_states": self.optimizer_net.state_dict(),
                "optim_disc_states": self.optimizer_disc.state_dict()
                }, os.path.join(save_path, filename+".pt"))
        
    