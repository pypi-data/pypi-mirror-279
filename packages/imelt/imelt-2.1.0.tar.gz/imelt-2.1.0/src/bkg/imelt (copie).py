# (c) Charles Le Losq 2022
# see embedded licence file
# imelt V1.2

import numpy as np
import torch, time
import h5py
import pandas as pd
from sklearn.metrics import mean_squared_error
from scipy.constants import Avogadro, Planck

###
### FUNCTIONS FOR HANDLNG DATA
###

class data_loader():
    """custom data loader for batch training

    """
    def __init__(self, 
                 path_viscosity = "./data/NKCMAS_viscosity.hdf5", 
                 path_raman = "./data/NKCMAS_Raman.hdf5", 
                 path_density = "./data/NKCMAS_density.hdf5", 
                 path_ri = "./data/NKCMAS_optical.hdf5", 
                 path_cp = "./data/NKCMAS_cp.hdf5", 
                 scaling = False):
        """
        Inputs
        ------
        path_viscosity : string
            path for the viscosity HDF5 dataset

        path_raman : string
            path for the Raman spectra HDF5 dataset

        path_density : string
            path for the density HDF5 dataset

        path_ri : String
            path for the refractive index HDF5 dataset
        
        path_cp : String
            path for the liquid heat capacity HDF5 dataset

        scaling : False or True
            Scales the input chemical composition.
            WARNING : Does not work currently as this is a relic of testing this effect,
            but we chose not to scale inputs and Cp are calculated with unscaled values in the network.
        """
        
        f = h5py.File(path_viscosity, 'r')

        # List all groups
        self.X_columns = f['X_columns'][()]

        # Entropy dataset
        X_entropy_train = f["X_entropy_train"][()]
        y_entropy_train = f["y_entropy_train"][()]

        X_entropy_valid = f["X_entropy_valid"][()]
        y_entropy_valid = f["y_entropy_valid"][()]

        X_entropy_test = f["X_entropy_test"][()]
        y_entropy_test = f["y_entropy_test"][()]

        # Viscosity dataset
        X_train = f["X_train"][()]
        T_train = f["T_train"][()]
        y_train = f["y_train"][()]

        X_valid = f["X_valid"][()]
        T_valid = f["T_valid"][()]
        y_valid = f["y_valid"][()]

        X_test = f["X_test"][()]
        T_test = f["T_test"][()]
        y_test = f["y_test"][()]

        # Tg dataset
        X_tg_train = f["X_tg_train"][()]
        X_tg_valid= f["X_tg_valid"][()]
        X_tg_test = f["X_tg_test"][()]

        y_tg_train = f["y_tg_train"][()]
        y_tg_valid = f["y_tg_valid"][()]
        y_tg_test = f["y_tg_test"][()]

        f.close()

        # Raman dataset
        f = h5py.File(path_raman, 'r')
        X_raman_train = f["X_raman_train"][()]
        y_raman_train = f["y_raman_train"][()]
        X_raman_valid = f["X_raman_test"][()]
        y_raman_valid = f["y_raman_test"][()]
        f.close()

        # Raman axis is
        self.x_raman_shift = np.arange(400.,1250.,1.0)

        # grabbing number of Raman channels
        self.nb_channels_raman = y_raman_valid.shape[1]

        # Density dataset
        f = h5py.File(path_density, 'r')
        X_density_train = f["X_density_train"][()]
        X_density_valid = f["X_density_valid"][()]
        X_density_test = f["X_density_test"][()]

        y_density_train = f["y_density_train"][()]
        y_density_valid = f["y_density_valid"][()]
        y_density_test = f["y_density_test"][()]
        f.close()

        # Refractive Index (ri) dataset
        f = h5py.File(path_ri, 'r')
        X_ri_train = f["X_ri_train"][()]
        X_ri_valid = f["X_ri_valid"][()]
        X_ri_test = f["X_ri_test"][()]

        lbd_ri_train = f["lbd_ri_train"][()]
        lbd_ri_valid = f["lbd_ri_valid"][()]
        lbd_ri_test = f["lbd_ri_test"][()]

        y_ri_train = f["y_ri_train"][()]
        y_ri_valid = f["y_ri_valid"][()]
        y_ri_test = f["y_ri_test"][()]
        f.close()

        # Liquid heat capacity (cp) dataset
        f = h5py.File(path_cp, 'r')
        X_cpl_train = f["X_cp_l"][()]
        T_cpl_train = f["T_cp_l"][()]
        y_cpl_train = f["y_cp_l"][()]
        f.close()

        # preparing data for pytorch

        # Scaler
        # Warning : this was done for tests and currently will not work,
        # as Cp are calculated from unscaled mole fractions...
        if scaling ==  True:
            X_scaler_mean = np.mean(X_train, axis=0)
            X_scaler_std = np.std(X_train, axis=0)
        else:
            X_scaler_mean = 0.0
            X_scaler_std = 1.0

        # The following lines perform scaling (not needed, not active),
        # put the data in torch tensors and send them to device (GPU or CPU, as requested) not anymore

        # viscosity
        self.x_visco_train = torch.FloatTensor(self.scaling(X_train,X_scaler_mean,X_scaler_std))
        self.T_visco_train = torch.FloatTensor(T_train.reshape(-1,1))
        self.y_visco_train = torch.FloatTensor(y_train[:,0].reshape(-1,1))

        self.x_visco_valid = torch.FloatTensor(self.scaling(X_valid,X_scaler_mean,X_scaler_std))
        self.T_visco_valid = torch.FloatTensor(T_valid.reshape(-1,1))
        self.y_visco_valid = torch.FloatTensor(y_valid[:,0].reshape(-1,1))

        self.x_visco_test = torch.FloatTensor(self.scaling(X_test,X_scaler_mean,X_scaler_std))
        self.T_visco_test = torch.FloatTensor(T_test.reshape(-1,1))
        self.y_visco_test = torch.FloatTensor(y_test[:,0].reshape(-1,1))

        # entropy
        self.x_entro_train = torch.FloatTensor(self.scaling(X_entropy_train,X_scaler_mean,X_scaler_std))
        self.y_entro_train = torch.FloatTensor(y_entropy_train[:,0].reshape(-1,1))

        self.x_entro_valid = torch.FloatTensor(self.scaling(X_entropy_valid,X_scaler_mean,X_scaler_std))
        self.y_entro_valid = torch.FloatTensor(y_entropy_valid[:,0].reshape(-1,1))

        self.x_entro_test = torch.FloatTensor(self.scaling(X_entropy_test,X_scaler_mean,X_scaler_std))
        self.y_entro_test = torch.FloatTensor(y_entropy_test[:,0].reshape(-1,1))

        # tg
        self.x_tg_train = torch.FloatTensor(self.scaling(X_tg_train,X_scaler_mean,X_scaler_std))
        self.y_tg_train = torch.FloatTensor(y_tg_train.reshape(-1,1))

        self.x_tg_valid = torch.FloatTensor(self.scaling(X_tg_valid,X_scaler_mean,X_scaler_std))
        self.y_tg_valid = torch.FloatTensor(y_tg_valid.reshape(-1,1))

        self.x_tg_test = torch.FloatTensor(self.scaling(X_tg_test,X_scaler_mean,X_scaler_std))
        self.y_tg_test = torch.FloatTensor(y_tg_test.reshape(-1,1))

        # Glass density
        self.x_density_train = torch.FloatTensor(self.scaling(X_density_train,X_scaler_mean,X_scaler_std))
        self.y_density_train = torch.FloatTensor(y_density_train.reshape(-1,1))

        self.x_density_valid = torch.FloatTensor(self.scaling(X_density_valid,X_scaler_mean,X_scaler_std))
        self.y_density_valid = torch.FloatTensor(y_density_valid.reshape(-1,1))

        self.x_density_test = torch.FloatTensor(self.scaling(X_density_test,X_scaler_mean,X_scaler_std))
        self.y_density_test = torch.FloatTensor(y_density_test.reshape(-1,1))

        # Optical
        self.x_ri_train = torch.FloatTensor(self.scaling(X_ri_train,X_scaler_mean,X_scaler_std))
        self.lbd_ri_train = torch.FloatTensor(lbd_ri_train.reshape(-1,1))
        self.y_ri_train = torch.FloatTensor(y_ri_train.reshape(-1,1))

        self.x_ri_valid = torch.FloatTensor(self.scaling(X_ri_valid,X_scaler_mean,X_scaler_std))
        self.lbd_ri_valid = torch.FloatTensor(lbd_ri_valid.reshape(-1,1))
        self.y_ri_valid = torch.FloatTensor(y_ri_valid.reshape(-1,1))

        self.x_ri_test = torch.FloatTensor(self.scaling(X_ri_test,X_scaler_mean,X_scaler_std))
        self.lbd_ri_test = torch.FloatTensor(lbd_ri_test.reshape(-1,1))
        self.y_ri_test = torch.FloatTensor(y_ri_test.reshape(-1,1))

        # Raman
        self.x_raman_train = torch.FloatTensor(self.scaling(X_raman_train,X_scaler_mean,X_scaler_std))
        self.y_raman_train = torch.FloatTensor(y_raman_train)

        self.x_raman_valid = torch.FloatTensor(self.scaling(X_raman_valid,X_scaler_mean,X_scaler_std))
        self.y_raman_valid = torch.FloatTensor(y_raman_valid)

        # Liquid heat capacity
        self.x_cpl_train = torch.FloatTensor(self.scaling(X_cpl_train,X_scaler_mean,X_scaler_std))
        self.T_cpl_train = torch.FloatTensor(T_cpl_train.reshape(-1,1))
        self.y_cpl_train = torch.FloatTensor(y_cpl_train.reshape(-1,1))

    def recall_order(self):
        print("Order of chemical components is sio2, al2o3, na2o, k2o, mgo, cao, then descriptors")

    def scaling(self,X,mu,s):
        return(X-mu)/s

    def print_data(self):
        """print the specifications of the datasets"""

        print("################################")
        print("#### Dataset specifications ####")
        print("################################")

        # print splitting
        size_train = self.x_visco_train.unique(dim=0).shape[0]
        size_valid = self.x_visco_valid.unique(dim=0).shape[0]
        size_test = self.x_visco_test.unique(dim=0).shape[0]
        size_total = size_train+size_valid+size_test
        self.size_total_visco = size_total

        print("")
        print("Number of unique compositions (viscosity): {}".format(size_total))
        print("Number of unique compositions in training (viscosity): {}".format(size_train))
        print("Dataset separations are {:.2f} in train, {:.2f} in valid, {:.2f} in test".format(size_train/size_total,
                                                                                    size_valid/size_total,
                                                                                    size_test/size_total))

        # print splitting
        size_train = self.x_entro_train.unique(dim=0).shape[0]
        size_valid = self.x_entro_valid.unique(dim=0).shape[0]
        size_test = self.x_entro_test.unique(dim=0).shape[0]
        size_total = size_train+size_valid+size_test
        self.size_total_entro = size_total

        print("")
        print("Number of unique compositions (entropy): {}".format(size_total))
        print("Number of unique compositions in training (entropy): {}".format(size_train))
        print("Dataset separations are {:.2f} in train, {:.2f} in valid, {:.2f} in test".format(size_train/size_total,
                                                                                    size_valid/size_total,
                                                                                    size_test/size_total))

        size_train = self.x_ri_train.unique(dim=0).shape[0]
        size_valid = self.x_ri_valid.unique(dim=0).shape[0]
        size_test = self.x_ri_test.unique(dim=0).shape[0]
        size_total = size_train+size_valid+size_test
        self.size_total_ri = size_total

        print("")
        print("Number of unique compositions (refractive index): {}".format(size_total))
        print("Number of unique compositions in training (refractive index): {}".format(size_train))
        print("Dataset separations are {:.2f} in train, {:.2f} in valid, {:.2f} in test".format(size_train/size_total,
                                                                                    size_valid/size_total,
                                                                                    size_test/size_total))

        size_train = self.x_density_train.unique(dim=0).shape[0]
        size_valid = self.x_density_valid.unique(dim=0).shape[0]
        size_test = self.x_density_test.unique(dim=0).shape[0]
        size_total = size_train+size_valid+size_test
        self.size_total_density = size_total

        print("")
        print("Number of unique compositions (glass density): {}".format(size_total))
        print("Number of unique compositions in training (glass density): {}".format(size_train))
        print("Dataset separations are {:.2f} in train, {:.2f} in valid, {:.2f} in test".format(size_train/size_total,
                                                                                    size_valid/size_total,
                                                                                    size_test/size_total))

        size_train = self.x_raman_train.unique(dim=0).shape[0]
        size_valid = self.x_raman_valid.unique(dim=0).shape[0]
        size_total = size_train+size_valid
        self.size_total_raman = size_total

        print("")
        print("Number of unique compositions (Raman): {}".format(size_total))
        print("Number of unique compositions in training (Raman): {}".format(size_train))
        print("Dataset separations are {:.2f} in train, {:.2f} in valid".format(size_train/size_total,
                                                                                    size_valid/size_total))


        # training shapes
        print("")
        print("This is for checking the consistency of the dataset...")

        print("Visco train shape")
        print(self.x_visco_train.shape)
        print(self.T_visco_train.shape)
        print(self.y_visco_train.shape)

        print("Entropy train shape")
        print(self.x_entro_train.shape)
        print(self.y_entro_train.shape)

        print("Tg train shape")
        print(self.x_tg_train.shape)
        print(self.y_tg_train.shape)

        print("Density train shape")
        print(self.x_density_train.shape)
        print(self.y_density_train.shape)

        print("Refactive Index train shape")
        print(self.x_ri_train.shape)
        print(self.lbd_ri_train.shape)
        print(self.y_ri_train.shape)

        print("Raman train shape")
        print(self.x_raman_train.shape)
        print(self.y_raman_train.shape)

        # testing device
        print("")
        print("Where are the datasets? CPU or GPU?")

        print("Visco device")
        print(self.x_visco_train.device)
        print(self.T_visco_train.device)
        print(self.y_visco_train.device)

        print("Entropy device")
        print(self.x_entro_train.device)
        print(self.y_entro_train.device)

        print("Tg device")
        print(self.x_tg_train.device)
        print(self.y_tg_train.device)

        print("Density device")
        print(self.x_density_train.device)
        print(self.y_density_train.device)

        print("Refactive Index device")
        print(self.x_ri_test.device)
        print(self.lbd_ri_test.device)
        print(self.y_ri_test.device)

        print("Raman device")
        print(self.x_raman_train.device)
        print(self.y_raman_train.device)

###
### MODEL
###
class PositionalEncoder(torch.nn.Module):
    """
    From:
    https://towardsdatascience.com/how-to-make-a-pytorch-transformer-for-time-series-forecasting-69e073d4061e
    Adapted from:
    https://pytorch.org/tutorials/beginner/transformer_tutorial.html
    https://github.com/LiamMaclean216/Pytorch-Transfomer/blob/master/utils.py
    """

    def __init__(self, dropout: float = 0.1, max_seq_len: int = 5000, d_model: int = 512):

        """
        Args:
            dropout: the dropout rate
            max_seq_len: the maximum length of the input sequences
            d_model: The dimension of the output of sub-layers in the model
                     (Vaswani et al, 2017)
        """

        super().__init__()

        self.d_model = d_model

        self.dropout = torch.nn.Dropout(p=dropout)

        # Create constant positional encoding matrix with values
        # dependent on position and i
        position = torch.arange(max_seq_len).unsqueeze(1)

        exp_input = torch.arange(0, d_model, 2) * (-np.log(10000.0) / d_model)

        div_term = torch.exp(exp_input) # Returns a new tensor with the exponential of the elements of exp_input

        pe = torch.zeros(max_seq_len, d_model)

        pe[:, 0::2] = torch.sin(position * div_term)

        pe[:, 1::2] = torch.cos(position * div_term) # torch.Size([target_seq_len, dim_val])

        pe = pe.unsqueeze(0).transpose(0, 1) # torch.Size([target_seq_len, input_size, dim_val])

        # register that pe is not a model parameter
        self.register_buffer('pe', pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Tensor, shape [batch_size, enc_seq_len, dim_val]
        """

        add = self.pe[:x.size(1), :].squeeze(1)

        x = x + add

        return self.dropout(x)

class model(torch.nn.Module):
    """i-MELT model

    """
    def __init__(self, input_size, hidden_size = 300, num_layers = 4, nb_channels_raman = 800, 
                 p_drop=0.2, activation_function = torch.nn.ReLU(), 
                 shape="rectangle", dropout_pos_enc=0.01, n_heads=4):
        """Initialization of i-MELT model

        Parameters
        ----------
        input_size : int
            number of input parameters

        hidden_size : int
            number of hidden units per hidden layer

        num_layers : int
            number of hidden layers

        nb_channels_raman : int
            number of Raman spectra channels, typically provided by the dataset

        p_drop : float (optinal)
            dropout probability, default = 0.2

        activation_function : torch.nn activation function (optional)
            activation function for the hidden units, default = torch.nn.ReLU()
            choose here : https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity

        shape : string (optional)
            either a rectangle network (same number of neurons per layer, or triangle (regularly decreasing number of neurons per layer))
            default = rectangle
            
        dropout_pos_enc & n_heads are experimental features, do not use...
        """
        super(model, self).__init__()

        # init parameters
        self.input_size = input_size
        self.hidden_size  = hidden_size
        self.num_layers  = num_layers
        self.nb_channels_raman = nb_channels_raman
        self.shape = shape

        # get constants
        #self.constants = constants()

        # network related torch stuffs
        self.activation_function = activation_function
        self.p_drop = p_drop
        self.dropout = torch.nn.Dropout(p=p_drop)

        # for transformer
        self.dropout_pos_enc = dropout_pos_enc
        self.n_heads = n_heads

        # general shape of the network
        if self.shape == "rectangle":

            self.linears = torch.nn.ModuleList([torch.nn.Linear(input_size, self.hidden_size)])
            self.linears.extend([torch.nn.Linear(self.hidden_size, self.hidden_size) for i in range(1, self.num_layers)])

        if self.shape == "triangle":

            self.linears = torch.nn.ModuleList([torch.nn.Linear(self.input_size, int(self.hidden_size/self.num_layers))])
            self.linears.extend([torch.nn.Linear(int(self.hidden_size/self.num_layers*i),
                                                 int(self.hidden_size/self.num_layers*(i+1))) for i in range(1,
                                                                                                         self.num_layers)])
        if self.shape == "transformer":

            # Creating the three linear layers needed for the model
            self.encoder_input_layer = torch.nn.Linear(
                in_features=1,
                out_features=self.hidden_size
                )

            # Create positional encoder
            self.positional_encoding_layer = PositionalEncoder(
                d_model=self.hidden_size,
                dropout=self.dropout_pos_enc,
                max_seq_len=self.hidden_size
                )

            # The encoder layer used in the paper is identical to the one used by
            # Vaswani et al (2017) on which the PyTorch module is based.
            encoder_layer = torch.nn.TransformerEncoderLayer(
                d_model=self.hidden_size,
                nhead=self.n_heads,
                dropout=self.p_drop,
                batch_first=True
                )

            # Stack the encoder layers in nn.TransformerDecoder
            # It seems the option of passing a normalization instance is redundant
            # in my case, because nn.TransformerEncoderLayer per default normalizes
            # after each sub-layer
            # (https://github.com/pytorch/pytorch/issues/24930).
            self.encoder = torch.nn.TransformerEncoder(
                encoder_layer=encoder_layer,
                num_layers=self.num_layers,
                norm=None
                )


        # output layers
        if self.shape == "transformer":
            self.out_thermo = torch.nn.Linear(self.hidden_size*self.input_size, 30) # Linear output, 22 without Cp
            self.out_raman = torch.nn.Linear(self.hidden_size*self.input_size, self.nb_channels_raman) # Linear output
        else:
            self.out_thermo = torch.nn.Linear(self.hidden_size, 30) # Linear output, 22 without Cp
            self.out_raman = torch.nn.Linear(self.hidden_size, self.nb_channels_raman) # Linear output

        # the model will also contains parameter for the losses
        #self.log_vars = torch.nn.Parameter(torch.zeros((6)))

        # we are going to determine better values for
        # the aCpl and bCpl coefficients
        # self.Cp_coefs = torch.nn.Parameter(
        #     torch.tensor(
        #     [np.log(81.37), np.log(85.78), np.log(100.6), np.log(50.13), np.log(85.78), np.log(86.05), 
        #      np.log(0.09428), np.log(0.01578)]), 
        #      requires_grad=True
        #     )
        

    def output_bias_init(self):
        """bias initialisation for self.out_thermo

        positions are Tg, Sconf(Tg), Ae, A_am, density, fragility (MYEGA one)
        """
        self.out_thermo.bias = torch.nn.Parameter(data=torch.tensor([np.log(1000.),np.log(8.), # Tg, ScTg
                                                                     -3.5, -3.5, -3.5, -4.5, # A_AG, A_AM, A_CG, A_TVF
                                                                     np.log(715.), np.log(61.), np.log(500.), # To_CG, C_CG, C_TVF
                                                                     np.log(27.29), np.log(36.66), np.log(29.65), np.log(47.28), np.log(12.66), np.log(20.66), # molar volumes of SiO2, al2o3, na2o, k2o, mgo, cao
                                                                     np.log(44.0), # fragility
                                                                     .90,.20,.98,0.6,0.2,1., # Sellmeier coeffs B1, B2, B3, C1, C2, C3
                                                                     np.log(81.37),np.log(130.2), np.log(100.6), np.log(50.13), np.log(85.78), np.log(86.05), np.log(0.03), np.log(0.01578)
                                                                     #np.log(0.09428), np.log(0.01578)
                                                                     #np.log(1500.) # liquidus
                                                                     ]))

    def use_pretrained_model(self, pretrained_name, same_input_size=False):
        """to use a pretrained model
        """
        if same_input_size == False :
            pretrained_model = torch.load(pretrained_name)
            pretrained_model['old_linear.0.weight'] = pretrained_model.pop('linears.0.weight')
            self.load_state_dict(pretrained_model, strict=False)
        else :
            pretrained_model = torch.load(pretrained_name)
            self.load_state_dict(pretrained_model, strict=False)

    def forward(self, x):
        """foward pass in core neural network"""
        if self.shape != "transformer":
            for layer in self.linears: # Feedforward
                x = self.dropout(self.activation_function(layer(x)))
            return x
        else:
            x = self.encoder_input_layer(x.unsqueeze(2))
            x = self.positional_encoding_layer(x)
            x = self.encoder(x)
            return x.flatten(start_dim=1)

    def at_gfu(self,x):
        """calculate atom per gram formula unit

        assumes first columns are sio2 al2o3 na2o k2o mgo cao
        """
        out = 3.0*x[:,0] + 5.0*x[:,1] + 3.0*x[:,2] + 3.0*x[:,3] + 2.0*x[:,4] + 2.0*x[:,5]
        return torch.reshape(out, (out.shape[0], 1))

    def aCpl(self,x):
        """calculate term a in equation Cpl = aCpl + bCpl*T

        Partial molar Cp are from Richet 1985, etc.

        assumes first columns are sio2 al2o3 na2o k2o mgo cao
        """
        # Richet 1985
        # out = (81.37*x[:,0] # Cp liquid SiO2
        #        + 130.2*x[:,1] # Cp liquid Al2O3 (Courtial R. 1993)
        #        + 100.6*x[:,2] # Cp liquid Na2O (Richet 1985)
        #        + 50.13*x[:,3] + x[:,0]*(x[:,3]*x[:,3])*151.7 # Cp liquid K2O (Richet 1985)
        #        + 85.78*x[:,4] # Cp liquid MgO (Richet 1985)
        #        + 86.05*x[:,5] # Cp liquid CaO (Richet 1985)
        #       )
        
        # solution with a_cp values from neural net
        a_cp = torch.exp(self.out_thermo(self.forward(x))[:,22:28])
        out = (a_cp[:,0]*x[:,0] + # Cp liquid SiO2, fixed value from Richet 1984
               a_cp[:,1]*x[:,1] + # Cp liquid Al2O3
               a_cp[:,2]*x[:,2] + # Cp liquid Na2O
               a_cp[:,3]*x[:,3] + # Cp liquid K2O
               a_cp[:,4]*x[:,4] + # Cp liquid MgO
               a_cp[:,5]*x[:,5] # Cp liquid CaO)
              )
        
        # solution with a_cp values as global parameters
        # out = (torch.exp(self.Cp_coefs[0])*x[:,0] + # Cp liquid SiO2
        #        torch.exp(self.Cp_coefs[1])*x[:,1] + # Cp liquid Al2O3
        #        torch.exp(self.Cp_coefs[2])*x[:,2] + # Cp liquid Na2O
        #        torch.exp(self.Cp_coefs[3])*x[:,3] + # Cp liquid K2O
        #        torch.exp(self.Cp_coefs[4])*x[:,4] + # Cp liquid MgO
        #        torch.exp(self.Cp_coefs[5])*x[:,5] # Cp liquid CaO)
        #       )
        
        return torch.reshape(out, (out.shape[0], 1))

    def bCpl(self,x):
        """calculate term b in equation Cpl = aCpl + bCpl*T

        assumes first columns are sio2 al2o3 na2o k2o mgo cao

        only apply B terms on Al and K
        """
        # Richet 1985
        #out = 0.09428*x[:,1] + 0.01578*x[:,3]

        # solution with a_cp values from neural net
        b_cp = torch.exp(self.out_thermo(self.forward(x))[:,28:])
        out = b_cp[:,0]*x[:,1] + b_cp[:,1]*x[:,3]

        # solution with a_cp values as global parameters
        #out = torch.exp(self.Cp_coefs[6])*x[:,1] + torch.exp(self.Cp_coefs[7])*x[:,3]

        return torch.reshape(out, (out.shape[0], 1))

    def cpg_tg(self,x):
        """Glass heat capacity at Tg calculated from Dulong and Petit limit
        """
        return 3.0*8.314462*self.at_gfu(x)
    
    def cpl(self,x,T):
        """Liquid heat capacity at T
        """
        out = self.aCpl(x) + self.bCpl(x)*T
        return torch.reshape(out, (out.shape[0], 1))

    def ap_calc(self,x):
        """calculate term ap in equation dS = ap ln(T/Tg) + b(T-Tg)
        """
        out = self.aCpl(x) - self.cpg_tg(x)
        return torch.reshape(out, (out.shape[0], 1))

    def dCp(self,x,T):
        out = self.ap_calc(x)*(torch.log(T)-torch.log(self.tg(x))) + self.bCpl(x)*(T-self.tg(x))
        return torch.reshape(out, (out.shape[0], 1))

    def raman_pred(self,x):
        """Raman predicted spectra"""
        return self.out_raman(self.forward(x))

    def tg(self,x):
        """glass transition temperature Tg"""
        out = torch.exp(self.out_thermo(self.forward(x))[:,0])
        return torch.reshape(out, (out.shape[0], 1))

    def sctg(self,x):
        """configurational entropy at Tg"""
        out = torch.exp(self.out_thermo(self.forward(x))[:,1])
        return torch.reshape(out, (out.shape[0], 1))

    def ae(self,x):
        """Ae parameter in Adam and Gibbs and MYEGA"""
        out = self.out_thermo(self.forward(x))[:,2]
        return torch.reshape(out, (out.shape[0], 1))

    def a_am(self,x):
        """A parameter for Avramov-Mitchell"""
        out = self.out_thermo(self.forward(x))[:,3]
        return torch.reshape(out, (out.shape[0], 1))

    def a_cg(self,x):
        """A parameter for Free Volume (CG)"""
        out = self.out_thermo(self.forward(x))[:,4]
        return torch.reshape(out, (out.shape[0], 1))

    def a_tvf(self,x):
        """A parameter for VFT"""
        out = self.out_thermo(self.forward(x))[:,5]
        return torch.reshape(out, (out.shape[0], 1))

    def to_cg(self,x):
        """To parameter for Free Volume (CG)"""
        out = torch.exp(self.out_thermo(self.forward(x))[:,6])
        return torch.reshape(out, (out.shape[0], 1))

    def c_cg(self,x):
        """C parameter for Free Volume (CG)"""
        out = torch.exp(self.out_thermo(self.forward(x))[:,7])
        return torch.reshape(out, (out.shape[0], 1))

    def c_tvf(self,x):
        """C parameter for VFT"""
        out = torch.exp(self.out_thermo(self.forward(x))[:,8])
        return torch.reshape(out, (out.shape[0], 1))

    def vm_glass(self,x):
        """partial molar volume of sio2 in glass"""
        out = torch.exp(self.out_thermo(self.forward(x))[:,9:15])
        return torch.reshape(out, (out.shape[0], 6))
    
    def density_glass(self, x):
        """glass density
        
        assumes X first columns are sio2 al2o3 na2o k2o mgo cao
        """
        vm_ = self.vm_glass(x) # partial molar volumes
        w = molarweights() # weights

        # calculation of glass molar volume
        v_g = (vm_[:,0]*x[:,0] + vm_[:,1]*x[:,1] + # sio2 + al2o3
                  vm_[:,2]*x[:,2] + vm_[:,3]*x[:,3] + # na2o + k2o
                  vm_[:,4]*x[:,4] + vm_[:,5]*x[:,5]) # mgo + cao
        
        # glass mass for one mole of oxides
        XMW_SiO2 	= x[:,0] * w["sio2"]
        XMW_Al2O3 	= x[:,1] * w["al2o3"]
        XMW_Na2O 	= x[:,2] * w["na2o"]
        XMW_K2O 	= x[:,3] * w["k2o"]
        XMW_MgO 	= x[:,4] * w["mgo"]
        XMW_CaO 	= x[:,5] * w["cao"]

        XMW_tot = XMW_SiO2 + XMW_Al2O3 + XMW_Na2O + XMW_K2O + XMW_MgO + XMW_CaO
        XMW_tot = XMW_tot.reshape(-1,1)
        
        out = XMW_tot / v_g.reshape(-1,1) 
        return torch.reshape(out,(out.shape[0],1))

    def density_melt(self, x, T, P=1):
        """melt density, calculated as in DensityX"""

        # grab constants
        d_cts = constants()
        w = molarweights()

        # mass for one mole of oxides
        XMW_SiO2 	= x[:,0] * w["sio2"]
        XMW_Al2O3 	= x[:,1] * w["al2o3"]
        XMW_Na2O 	= x[:,2] * w["na2o"]
        XMW_K2O 	= x[:,3] * w["k2o"]
        XMW_MgO 	= x[:,4] * w["mgo"]
        XMW_CaO 	= x[:,5] * w["cao"]

        XMW_tot = XMW_SiO2 + XMW_Al2O3 + XMW_Na2O + XMW_K2O + XMW_MgO + XMW_CaO
        XMW_tot = XMW_tot.reshape(-1,1)
        
        # calculation of corrected VM
        c_Vm_Tref = (x[:,0] * d_cts.c_sio2 + 
                   x[:,1] * d_cts.c_al2o3 + 
                   x[:,2] * d_cts.c_na2o +
                   x[:,3] * d_cts.c_k2o +
                   x[:,4] * d_cts.c_mgo +
                   x[:,5] * d_cts.c_cao)
        
        # calculation of alphas
        alpha_ = (x[:,0] * d_cts.dVdT_SiO2  * (T - d_cts.Tref_SiO2) +
                   x[:,1] * d_cts.dVdT_Al2O3 * (T - d_cts.Tref_Al2O3) + 
                   x[:,2] * d_cts.dVdT_Na2O  * (T - d_cts.Tref_Na2O) +
                   x[:,3] * d_cts.dVdT_K2O   * (T - d_cts.Tref_K2O) +
                   x[:,4] * d_cts.dVdT_MgO   * (T - d_cts.Tref_MgO) +
                   x[:,5] * d_cts.dVdT_CaO   * (T - d_cts.Tref_CaO))
        
        d_g = self.density_glass(x) # glass density
        v_g = XMW_tot/d_g # glass volume
        # melt volume estimated from glass plus deviation from T ref
        v_l = v_g.reshape(-1,1) + c_Vm_Tref.reshape(-1,1) + alpha_.reshape(-1,1)
        out = XMW_tot / v_l # output melt density
        return torch.reshape(out,(out.shape[0],1))

    def fragility(self,x):
        """melt fragility"""
        out = torch.exp(self.out_thermo(self.forward(x))[:,15])
        return torch.reshape(out, (out.shape[0], 1))

    def S_B1(self,x):
        """Sellmeir B1"""
        out = self.out_thermo(self.forward(x))[:,16]
        return torch.reshape(out, (out.shape[0], 1))

    def S_B2(self,x):
        """Sellmeir B2"""
        out = self.out_thermo(self.forward(x))[:,17]
        return torch.reshape(out, (out.shape[0], 1))

    def S_B3(self,x):
        """Sellmeir B3"""
        out = self.out_thermo(self.forward(x))[:,18]
        return torch.reshape(out, (out.shape[0], 1))

    def S_C1(self,x):
        """Sellmeir C1, with proper scaling"""
        out = 0.01*self.out_thermo(self.forward(x))[:,19]
        return torch.reshape(out, (out.shape[0], 1))

    def S_C2(self,x):
        """Sellmeir C2, with proper scaling"""
        out = 0.1*self.out_thermo(self.forward(x))[:,20]

        return torch.reshape(out, (out.shape[0], 1))

    def S_C3(self,x):
        """Sellmeir C3, with proper scaling"""
        out = 100*self.out_thermo(self.forward(x))[:,21]
        return torch.reshape(out, (out.shape[0], 1))

    #def tl(self,x):
    #    """liquidus temperature, K"""
    #    out = torch.exp(self.out_thermo(self.forward(x))[:,17])
    #    return torch.reshape(out, (out.shape[0], 1))

    def a_theory(self,x):
        """Theoretical high T viscosity limit
        
        see Le Losq et al. 2017, JNCS 463, page 184
        and references cited therein
        """
        
        # attempt with theoretical calculation
        vm_ = self.vm_glass(x) # partial molar volumes

        # calculation of glass molar volume
        # careful with the units, we want m3/mol
        v_g = 1e-6*(vm_[:,0]*x[:,0] + vm_[:,1]*x[:,1] + # sio2 + al2o3
                  vm_[:,2]*x[:,2] + vm_[:,3]*x[:,3] + # na2o + k2o
                  vm_[:,4]*x[:,4] + vm_[:,5]*x[:,5]) # mgo + cao
        
        # calculation of theoretical A
        out = torch.log10(Avogadro*Planck/v_g)
        return torch.reshape(out, (out.shape[0], 1))

    def b_cg(self, x):
        """B in free volume (CG) equation"""
        return 0.5*(12.0 - self.a_cg(x)) * (self.tg(x) - self.to_cg(x) + torch.sqrt( (self.tg(x) - self.to_cg(x))**2 + self.c_cg(x)*self.tg(x)))

    def b_tvf(self,x):
        """B in VFT equation"""
        return (12.0-self.a_tvf(x))*(self.tg(x)-self.c_tvf(x))

    def be(self,x):
        """Be term in Adam-Gibbs equation given Ae, Tg and Scong(Tg)"""
        return (12.0-self.ae(x))*(self.tg(x)*self.sctg(x))

    def ag(self,x,T):
        """viscosity from the Adam-Gibbs equation, given chemistry X and temperature T
        """
        return self.ae(x) + self.be(x) / (T* (self.sctg(x) + self.dCp(x, T)))

    def myega(self,x, T):
        """viscosity from the MYEGA equation, given entries X and temperature T
        """
        return self.ae(x) + (12.0 - self.ae(x))*(self.tg(x)/T)*torch.exp((self.fragility(x)/(12.0-self.ae(x))-1.0)*(self.tg(x)/T-1.0))

    def am(self,x, T):
        """viscosity from the Avramov-Mitchell equation, given entries X and temperature T
        """
        return self.a_am(x) + (12.0 - self.a_am(x))*(self.tg(x)/T)**(self.fragility(x)/(12.0 - self.a_am(x)))

    def cg(self,x, T):
        """free volume theory viscosity equation, given entries X and temperature T
        """
        return self.a_cg(x) + 2.0*self.b_cg(x)/(T - self.to_cg(x) + torch.sqrt( (T-self.to_cg(x))**2 + self.c_cg(x)*T))

    def tvf(self,x, T):
        """Tamman-Vogel-Fulscher empirical viscosity, given entries X and temperature T
        """
        return self.a_tvf(x) + self.b_tvf(x)/(T - self.c_tvf(x))

    def sellmeier(self, x, lbd):
        """Sellmeier equation for refractive index calculation, with lbd in microns
        """
        return torch.sqrt( 1.0 + self.S_B1(x)*lbd**2/(lbd**2-self.S_C1(x))
                             + self.S_B2(x)*lbd**2/(lbd**2-self.S_C2(x))
                             + self.S_B3(x)*lbd**2/(lbd**2-self.S_C3(x)))

###
### TRAINING FUNCTIONS
###

class loss_scales():
    """loss scales for everything"""
    def __init__(self):
        # scaling coefficients for loss function
        # viscosity is always one
        self.entro = 1.
        self.raman = 20.
        self.density = 1000.
        self.ri = 5000.
        self.tg = 0.001
        self.A_scale = 1e4 # 1e-6 potentiellement bien
        self.cpl = 1e-2 # 1e-2 for strong constraints

def training(neuralmodel, ds, 
             criterion, optimizer, 
             save_switch=True, save_name="./temp", 
             nb_folds=1, train_patience=50, min_delta=0.1, 
             verbose=True,  mode="main", device='cuda'):
    """train neuralmodel given a dataset, criterion and optimizer

    Parameters
    ----------
    neuralmodel : model
        a neuravi model
    ds : dataset
        dataset from data_loader()
    criterion : pytorch criterion
        the criterion for goodness of fit
    optimizer : pytorch optimizer
        the optimizer to use
    

    Options
    -------
    save_switch : bool
        if True, the network will be saved in save_name
    save_name : string
        the path to save the model during training
    nb_folds : int, default = 10
        the number of folds for the K-fold training
    train_patience : int, default = 50
        the number of iterations
    min_delta : float, default = 0.1
        Minimum decrease in the loss to qualify as an improvement,
        a decrease of less than or equal to `min_delta` will count as no improvement.
    verbose : bool, default = True
        Do you want details during training?
    device : string, default = "cuda"
        the device where the calculations are made during training

    Returns
    -------
    neuralmodel : model
        trained model
    record_train_loss : list
        training loss (global)
    record_valid_loss : list
        validation loss (global)
    """

    if verbose == True:
        time1 = time.time()

    # scaling coefficients for loss function
    # viscosity is always one
    ls = loss_scales()
    entro_scale = ls.entro
    raman_scale = ls.raman
    density_scale = ls.density
    ri_scale = ls.ri
    tg_scale = ls.tg
    cpl_scale = ls.cpl

    # we will do mixed-precision training
    # https://pytorch.org/blog/accelerating-training-on-nvidia-gpus-with-pytorch-automatic-mixed-precision/
    # for a need for speed, we will use the torch.cuda.amp package
    # Creates once at the beginning of training
    scaler = torch.cuda.amp.GradScaler()

    #put model in train mode
    neuralmodel.train()

    # for early stopping
    epoch = 0
    best_epoch = 0
    val_ex = 0

    # for recording losses
    record_train_loss = []
    record_valid_loss = []

    # new vectors for the K-fold training (each vector contains slices of data separated)
    slices_x_visco_train = [ds.x_visco_train[i::nb_folds] for i in range(nb_folds)]
    slices_y_visco_train = [ds.y_visco_train[i::nb_folds] for i in range(nb_folds)]
    slices_T_visco_train = [ds.T_visco_train[i::nb_folds] for i in range(nb_folds)]

    slices_x_raman_train = [ds.x_raman_train[i::nb_folds] for i in range(nb_folds)]
    slices_y_raman_train = [ds.y_raman_train[i::nb_folds] for i in range(nb_folds)]

    slices_x_density_train = [ds.x_density_train[i::nb_folds] for i in range(nb_folds)]
    slices_y_density_train = [ds.y_density_train[i::nb_folds] for i in range(nb_folds)]

    slices_x_entro_train = [ds.x_entro_train[i::nb_folds] for i in range(nb_folds)]
    slices_y_entro_train = [ds.y_entro_train[i::nb_folds] for i in range(nb_folds)]

    slices_x_tg_train = [ds.x_tg_train[i::nb_folds] for i in range(nb_folds)]
    slices_y_tg_train = [ds.y_tg_train[i::nb_folds] for i in range(nb_folds)]

    slices_x_ri_train = [ds.x_ri_train[i::nb_folds] for i in range(nb_folds)]
    slices_y_ri_train = [ds.y_ri_train[i::nb_folds] for i in range(nb_folds)]
    slices_lbd_ri_train = [ds.lbd_ri_train[i::nb_folds] for i in range(nb_folds)]

    while val_ex <= train_patience:

        #
        # TRAINING
        #
        
        loss = 0 # initialize the sum of losses of each fold

        for i in range(nb_folds): # loop for K-Fold training to reduce memory footprint

            # training dataset is not on device yet and needs to be sent there
            x_visco_train = slices_x_visco_train[i].to(device)
            y_visco_train = slices_y_visco_train[i].to(device)
            T_visco_train = slices_T_visco_train[i].to(device)

            x_raman_train = slices_x_raman_train[i].to(device)
            y_raman_train = slices_y_raman_train[i].to(device)

            x_density_train = slices_x_density_train[i].to(device)
            y_density_train = slices_y_density_train[i].to(device)

            x_entro_train = slices_x_entro_train[i].to(device)
            y_entro_train = slices_y_entro_train[i].to(device)

            x_tg_train = slices_x_tg_train[i].to(device)
            y_tg_train = slices_y_tg_train[i].to(device)

            x_ri_train = slices_x_ri_train[i].to(device)
            y_ri_train = slices_y_ri_train[i].to(device)
            lbd_ri_train = slices_lbd_ri_train[i].to(device)

            # Forward pass on training set
            y_ag_pred_train = neuralmodel.ag(x_visco_train,T_visco_train)
            y_myega_pred_train = neuralmodel.myega(x_visco_train,T_visco_train)
            y_am_pred_train = neuralmodel.am(x_visco_train,T_visco_train)
            y_cg_pred_train = neuralmodel.cg(x_visco_train,T_visco_train)
            y_tvf_pred_train = neuralmodel.tvf(x_visco_train,T_visco_train)
            y_raman_pred_train = neuralmodel.raman_pred(x_raman_train)
            y_density_pred_train = neuralmodel.density_glass(x_density_train)
            y_entro_pred_train = neuralmodel.sctg(x_entro_train)
            y_tg_pred_train = neuralmodel.tg(x_tg_train)
            y_ri_pred_train = neuralmodel.sellmeier(x_ri_train,lbd_ri_train)
            y_clp_pred_train = neuralmodel.cpl(ds.x_cpl_train.to(device), ds.T_cpl_train.to(device))

            # Precisions
            precision_visco = 1.0#1/(2*torch.exp(-neuralmodel.log_vars[0]))
            precision_raman = raman_scale #1/(2*torch.exp(-neuralmodel.log_vars[1]))
            precision_density = density_scale #1/(2*torch.exp(-neuralmodel.log_vars[2]))
            precision_entro = entro_scale#1/(2*torch.exp(-neuralmodel.log_vars[3]))
            precision_tg = tg_scale#1/(2*torch.exp(-neuralmodel.log_vars[4]))
            precision_ri = ri_scale#1/(2*torch.exp(-neuralmodel.log_vars[5]))
            precision_cpl = cpl_scale#1/(2*torch.exp(-neuralmodel.log_vars[6]))

            # initialise gradient
            optimizer.zero_grad() 

            # Casts operations to mixed precision
            with torch.cuda.amp.autocast():
                # Compute Loss
                loss_ag = precision_visco * criterion(y_ag_pred_train, y_visco_train) #+ neuralmodel.log_vars[0]
                loss_myega = precision_visco * criterion(y_myega_pred_train, y_visco_train) #+ neuralmodel.log_vars[0]
                loss_am = precision_visco * criterion(y_am_pred_train, y_visco_train) #+ neuralmodel.log_vars[0]
                loss_cg = precision_visco * criterion(y_cg_pred_train, y_visco_train) #+ neuralmodel.log_vars[0]
                loss_tvf = precision_visco * criterion(y_tvf_pred_train, y_visco_train) #+ neuralmodel.log_vars[0]
                loss_raman = precision_raman * criterion(y_raman_pred_train,y_raman_train) #+ neuralmodel.log_vars[1]
                loss_density = precision_density * criterion(y_density_pred_train,y_density_train) #+ neuralmodel.log_vars[2]
                loss_entro = precision_entro * criterion(y_entro_pred_train,y_entro_train) #+ neuralmodel.log_vars[3]
                loss_tg = precision_tg * criterion(y_tg_pred_train,y_tg_train) #+ neuralmodel.log_vars[4]
                loss_ri = precision_ri * criterion(y_ri_pred_train,y_ri_train) #+ neuralmodel.log_vars[5]
                loss_cpl = precision_cpl * criterion(y_clp_pred_train,ds.y_cpl_train.to(device)) #+ neuralmodel.log_vars[6]

                # L2 regularization of the A parameters
                # reg_A = torch.sum(ls.A_scale * neuralmodel.ae(x_visco_train)**2 + 
                #          ls.A_scale * neuralmodel.a_am(x_visco_train)**2 +
                #          ls.A_scale * neuralmodel.a_cg(x_visco_train)**2 + 
                #          ls.A_scale * neuralmodel.a_tvf(x_visco_train)**2)
                            
                # pretrain deprecated, we can directly train now
                #if mode == "pretrain":
                #    loss_fold = loss_tg + loss_raman + loss_density + loss_entro + loss_ri
                #else:
                loss_fold = (loss_ag + loss_myega + loss_am + loss_cg + loss_tvf +
                            loss_raman + loss_density + loss_entro + loss_ri + loss_cpl)

            # Scales the loss, and calls backward()
            # to create scaled gradients
            scaler.scale(loss_fold).backward()

            # Unscales gradients and calls
            # or skips optimizer.step()
            scaler.step(optimizer)

            # Updates the scale for next iteration
            scaler.update()
            #loss_fold.backward() # backward gradient determination
            #optimizer.step() # optimiser call and step

            loss += loss_fold.item() # add the new fold loss to the sum

        # record global loss (mean of the losses of the training folds)
        record_train_loss.append(loss/nb_folds)

        #
        # MONITORING VALIDATION SUBSET
        #
        with torch.set_grad_enabled(False):

            # Precisions
            precision_visco = 1.0#1/(2*torch.exp(-neuralmodel.log_vars[0]))
            precision_raman = raman_scale #1/(2*torch.exp(-neuralmodel.log_vars[1]))
            precision_density = density_scale #1/(2*torch.exp(-neuralmodel.log_vars[2]))
            precision_entro = entro_scale#1/(2*torch.exp(-neuralmodel.log_vars[3]))
            precision_tg = tg_scale#1/(2*torch.exp(-neuralmodel.log_vars[4]))
            precision_ri = ri_scale#1/(2*torch.exp(-neuralmodel.log_vars[5]))

            # on validation set
            y_ag_pred_valid = neuralmodel.ag(ds.x_visco_valid.to(device),ds.T_visco_valid.to(device))
            y_myega_pred_valid = neuralmodel.myega(ds.x_visco_valid.to(device),ds.T_visco_valid.to(device))
            y_am_pred_valid = neuralmodel.am(ds.x_visco_valid.to(device),ds.T_visco_valid.to(device))
            y_cg_pred_valid = neuralmodel.cg(ds.x_visco_valid.to(device),ds.T_visco_valid.to(device))
            y_tvf_pred_valid = neuralmodel.tvf(ds.x_visco_valid.to(device),ds.T_visco_valid.to(device))
            y_raman_pred_valid = neuralmodel.raman_pred(ds.x_raman_valid.to(device))
            y_density_pred_valid = neuralmodel.density_glass(ds.x_density_valid.to(device))
            y_entro_pred_valid = neuralmodel.sctg(ds.x_entro_valid.to(device))
            y_tg_pred_valid = neuralmodel.tg(ds.x_tg_valid.to(device))
            y_ri_pred_valid = neuralmodel.sellmeier(ds.x_ri_valid.to(device), ds.lbd_ri_valid.to(device))

            # validation loss
            loss_ag_v = precision_visco * criterion(y_ag_pred_valid, ds.y_visco_valid.to(device)) #+ neuralmodel.log_vars[0]
            loss_myega_v = precision_visco * criterion(y_myega_pred_valid, ds.y_visco_valid.to(device)) #+ neuralmodel.log_vars[0]
            loss_am_v = precision_visco * criterion(y_am_pred_valid, ds.y_visco_valid.to(device)) #+ neuralmodel.log_vars[0]
            loss_cg_v = precision_visco * criterion(y_cg_pred_valid, ds.y_visco_valid.to(device)) #+ neuralmodel.log_vars[0]
            loss_tvf_v = precision_visco * criterion(y_tvf_pred_valid, ds.y_visco_valid.to(device)) #+ neuralmodel.log_vars[0]
            loss_raman_v = precision_raman * criterion(y_raman_pred_valid,ds.y_raman_valid.to(device)) #+ neuralmodel.log_vars[1]
            loss_density_v = precision_density * criterion(y_density_pred_valid,ds.y_density_valid.to(device)) #+ neuralmodel.log_vars[2]
            loss_entro_v = precision_entro * criterion(y_entro_pred_valid,ds.y_entro_valid.to(device)) #+ neuralmodel.log_vars[3]
            loss_tg_v = precision_tg * criterion(y_tg_pred_valid,ds.y_tg_valid.to(device)) #+ neuralmodel.log_vars[4]
            loss_ri_v = precision_ri * criterion(y_ri_pred_valid,ds.y_ri_valid.to(device)) #+ neuralmodel.log_vars[5]

            # L2 regularization of the A parameters
            # reg_A = torch.sum(ls.A_scale * neuralmodel.ae(ds.x_visco_valid.to(device))**2 + 
            #          ls.A_scale * neuralmodel.a_am(ds.x_visco_valid.to(device))**2 +
            #          ls.A_scale * neuralmodel.a_cg(ds.x_visco_valid.to(device))**2 + 
            #          ls.A_scale * neuralmodel.a_tvf(ds.x_visco_valid.to(device))**2)

            # pretrain deprecated, we can directly train now
            #if mode == "pretrain":
            #    loss_v = loss_tg_v + loss_raman_v + loss_density_v + loss_entro_v + loss_ri_v
            #else:
            loss_v = (loss_ag_v + loss_myega_v + loss_am_v + loss_cg_v + loss_tvf_v + 
                        loss_raman_v + loss_density_v + loss_entro_v + loss_ri_v)

            record_valid_loss.append(loss_v.item())

        #
        # Print info on screen
        #
        if verbose == True:
            if (epoch % 20 == 0):
                print('Epoch {} => loss train {:.2f}, valid {:.2f}; reg A: {:.6f}'.format(epoch, loss/nb_folds, loss_v.item(), 0))

        #
        # calculating ES criterion
        #
        if epoch == 0:
            val_ex = 0
            best_loss_v = loss_v.item()
        elif loss_v.item() <= best_loss_v - min_delta: # if improvement is significant, this saves the model
            val_ex = 0
            best_epoch = epoch
            best_loss_v = loss_v.item()

            if save_switch == True: # save best model
                torch.save(neuralmodel.state_dict(), save_name)
        else:
            val_ex += 1

        epoch += 1

    # print outputs if verbose is True
    if verbose == True:
        time2 = time.time()
        print("Running time in seconds:", time2-time1)
        print("Scaled loss values are:")
        print("--- Train ---")
        print('Tg: {:.2f}, Raman: {:.2f}, d: {:.2f}, Sc: {:.2f}, ori: {:.2f}, visco: {:.2f}, cpl: {:.2f}'.format(
        loss_tg, loss_raman, loss_density, loss_entro,  loss_ri, loss_ag, loss_cpl
        ))
        print("--- Valid ---")
        print('Tg: {:.2f}, Raman: {:.2f}, d: {:.2f}, Sc: {:.2f}, ori: {:.2f}, visco: {:.2f}'.format(
        loss_tg_v, loss_raman_v, loss_density_v, loss_entro_v,  loss_ri_v, loss_ag_v
        ))

    return neuralmodel, record_train_loss, record_valid_loss

def RMSE_viscosity_bydomain(bagged_model, ds, method="ag", boundary=7.0):
    """return the RMSE between predicted and measured viscosities

    Parameters
    ----------
    bagged_model : bagged model object
        generated using the bagging_models class
    ds : ds dataset
        contains all the training, validation and test viscosity datasets
    method : str
        method to provide to the bagged model
    boundary : float
        boundary between the high and low viscosity domains (log Pa s value)

    Returns
    -------
    total_RMSE : list
        RMSE between predictions and observations, three values (train-valid-test)
    high_RMSE : list
        RMSE between predictions and observations, above the boundary, three values (train-valid-test)
    low_RMSE : list
        RMSE between predictions and observations, below the boundary, three values (train-valid-test)

    """
    y_pred_train = bagged_model.predict(method,ds.x_visco_train,ds.T_visco_train).mean(axis=1).reshape(-1,1)
    y_pred_valid = bagged_model.predict(method,ds.x_visco_valid,ds.T_visco_valid).mean(axis=1).reshape(-1,1)
    y_pred_test = bagged_model.predict(method,ds.x_visco_test,ds.T_visco_test).mean(axis=1).reshape(-1,1)

    y_train = ds.y_visco_train
    y_valid = ds.y_visco_valid
    y_test = ds.y_visco_test

    total_RMSE_train = mean_squared_error(y_pred_train,y_train,squared=False)
    total_RMSE_valid = mean_squared_error(y_pred_valid,y_valid,squared=False)
    total_RMSE_test = mean_squared_error(y_pred_test,y_test,squared=False)

    high_RMSE_train = mean_squared_error(y_pred_train[y_train>boundary],y_train[y_train>boundary],squared=False)
    high_RMSE_valid = mean_squared_error(y_pred_valid[y_valid>boundary],y_valid[y_valid>boundary],squared=False)
    high_RMSE_test = mean_squared_error(y_pred_test[y_test>boundary],y_test[y_test>boundary],squared=False)

    low_RMSE_train = mean_squared_error(y_pred_train[y_train<boundary],y_train[y_train<boundary],squared=False)
    low_RMSE_valid = mean_squared_error(y_pred_valid[y_valid<boundary],y_valid[y_valid<boundary],squared=False)
    low_RMSE_test = mean_squared_error(y_pred_test[y_test<boundary],y_test[y_test<boundary],squared=False)

    out1 = [total_RMSE_train, total_RMSE_valid, total_RMSE_test]
    out2 = [high_RMSE_train, high_RMSE_valid, high_RMSE_test]
    out3 = [low_RMSE_train, low_RMSE_valid, low_RMSE_test]

    if method =="ag":
        name_method = "Adam-Gibbs"
    elif method == "cg":
        name_method = "Free Volume"
    elif method == "tvf":
        name_method = "Vogel Fulcher Tamman"
    elif method == "myega":
        name_method = "MYEGA"
    elif method == "am":
        name_method = "Avramov Milchev"


    print("Using the equation from {}:".format(name_method))
    print("    RMSE on the full range (0-15 log Pa s): train {0:.2f}, valid {1:.2f}, test {2:.2f}".format(total_RMSE_train,
                                                                                        total_RMSE_valid,
                                                                                        total_RMSE_test))
    print("    RMSE on the -inf - {:.1f} log Pa s range: train {:.2f}, valid {:.2f}, test {:.2f}".format(boundary,
                                                                                      low_RMSE_train,
                                                                                        low_RMSE_valid,
                                                                                        low_RMSE_test))
    print("    RMSE on the {:.1f} - +inf log Pa s range: train {:.2f}, valid {:.2f}, test {:.2f}".format(boundary,
                                                                                      high_RMSE_train,
                                                                                        high_RMSE_valid,
                                                                                        high_RMSE_test))
    print("")
    return out1, out2, out3

def record_loss_build(path, list_models, ds, shape='rectangle'):
    """build a Pandas dataframe with the losses for a list of models at path

    """
    # scaling coefficients for global loss function
    # viscosity is always one
    # check lines 578-582 in imelt.py
    entro_scale = 1.
    raman_scale = 20.
    density_scale = 1000.
    ri_scale = 10000.

    nb_exp = len(list_models)

    record_loss = pd.DataFrame()

    record_loss["name"] = list_models

    record_loss["nb_layers"] = np.zeros(nb_exp)
    record_loss["nb_neurons"] = np.zeros(nb_exp)
    record_loss["p_drop"] = np.zeros(nb_exp)

    record_loss["loss_ag_train"] = np.zeros(nb_exp)
    record_loss["loss_ag_valid"] = np.zeros(nb_exp)

    record_loss["loss_am_train"] = np.zeros(nb_exp)
    record_loss["loss_am_valid"] = np.zeros(nb_exp)

    record_loss["loss_am_train"] = np.zeros(nb_exp)
    record_loss["loss_am_valid"] = np.zeros(nb_exp)

    record_loss["loss_Sconf_train"] = np.zeros(nb_exp)
    record_loss["loss_Sconf_valid"] = np.zeros(nb_exp)

    record_loss["loss_d_train"] = np.zeros(nb_exp)
    record_loss["loss_d_valid"] = np.zeros(nb_exp)

    record_loss["loss_raman_train"] = np.zeros(nb_exp)
    record_loss["loss_raman_valid"] = np.zeros(nb_exp)

    record_loss["loss_train"] = np.zeros(nb_exp)
    record_loss["loss_valid"] = np.zeros(nb_exp)

    # Loss criterion
    criterion = torch.nn.MSELoss()

    # Load dataset
    for idx,name in enumerate(list_models):

        # Extract arch
        nb_layers = int(name[name.find("l")+1:name.find("_")])
        nb_neurons = int(name[name.find("n")+1:name.find("p")-1])
        p_drop = float(name[name.find("p")+1:name.find("s")-1])

        # Record arch
        record_loss.loc[idx,"nb_layers"] = nb_layers
        record_loss.loc[idx,"nb_neurons"] = nb_neurons
        record_loss.loc[idx,"p_drop"] = p_drop

        # Declare model
        neuralmodel = neuravi.model(6,nb_neurons,nb_layers,ds.nb_channels_raman,p_drop=p_drop, shape=shape)
        neuralmodel.load_state_dict(torch.load(path+'/'+name, map_location='cpu'))
        neuralmodel.eval()

        # PREDICTIONS

        with torch.set_grad_enabled(False):
            # train
            y_ag_pred_train = neuralmodel.ag(ds.x_visco_train,ds.T_visco_train)
            y_myega_pred_train = neuralmodel.myega(ds.x_visco_train,ds.T_visco_train)
            y_am_pred_train = neuralmodel.am(ds.x_visco_train,ds.T_visco_train)
            y_cg_pred_train = neuralmodel.cg(ds.x_visco_train,ds.T_visco_train)
            y_tvf_pred_train = neuralmodel.tvf(ds.x_visco_train,ds.T_visco_train)
            y_raman_pred_train = neuralmodel.raman_pred(ds.x_raman_train)
            y_density_pred_train = neuralmodel.density_glass(ds.x_density_train)
            y_entro_pred_train = neuralmodel.sctg(ds.x_entro_train)
            y_ri_pred_train = neuralmodel.sellmeier(ds.x_ri_train, ds.lbd_ri_train)

            # valid
            y_ag_pred_valid = neuralmodel.ag(ds.x_visco_valid,ds.T_visco_valid)
            y_myega_pred_valid = neuralmodel.myega(ds.x_visco_valid,ds.T_visco_valid)
            y_am_pred_valid = neuralmodel.am(ds.x_visco_valid,ds.T_visco_valid)
            y_cg_pred_valid = neuralmodel.cg(ds.x_visco_valid,ds.T_visco_valid)
            y_tvf_pred_valid = neuralmodel.tvf(ds.x_visco_valid,ds.T_visco_valid)
            y_raman_pred_valid = neuralmodel.raman_pred(ds.x_raman_valid)
            y_density_pred_valid = neuralmodel.density_glass(ds.x_density_valid)
            y_entro_pred_valid = neuralmodel.sctg(ds.x_entro_valid)
            y_ri_pred_valid = neuralmodel.sellmeier(ds.x_ri_valid, ds.lbd_ri_valid)

            # Compute Loss

            # train
            record_loss.loc[idx,"loss_ag_train"] = np.sqrt(criterion(y_ag_pred_train, ds.y_visco_train).item())
            record_loss.loc[idx,"loss_myega_train"]  = np.sqrt(criterion(y_myega_pred_train, ds.y_visco_train).item())
            record_loss.loc[idx,"loss_am_train"]  = np.sqrt(criterion(y_am_pred_train, ds.y_visco_train).item())
            record_loss.loc[idx,"loss_cg_train"]  = np.sqrt(criterion(y_cg_pred_train, ds.y_visco_train).item())
            record_loss.loc[idx,"loss_tvf_train"]  = np.sqrt(criterion(y_tvf_pred_train, ds.y_visco_train).item())
            record_loss.loc[idx,"loss_raman_train"]  = np.sqrt(criterion(y_raman_pred_train,ds.y_raman_train).item())
            record_loss.loc[idx,"loss_d_train"]  = np.sqrt(criterion(y_density_pred_train,ds.y_density_train).item())
            record_loss.loc[idx,"loss_Sconf_train"]  = np.sqrt(criterion(y_entro_pred_train,ds.y_entro_train).item())
            record_loss.loc[idx,"loss_ri_train"]  = np.sqrt(criterion(y_ri_pred_train,ds.y_ri_train).item())

            # validation
            record_loss.loc[idx,"loss_ag_valid"] = np.sqrt(criterion(y_ag_pred_valid, ds.y_visco_valid).item())
            record_loss.loc[idx,"loss_myega_valid"] = np.sqrt(criterion(y_myega_pred_valid, ds.y_visco_valid).item())
            record_loss.loc[idx,"loss_am_valid"] = np.sqrt(criterion(y_am_pred_valid, ds.y_visco_valid).item())
            record_loss.loc[idx,"loss_cg_valid"]  = np.sqrt(criterion(y_cg_pred_valid, ds.y_visco_valid).item())
            record_loss.loc[idx,"loss_tvf_valid"]  = np.sqrt(criterion(y_tvf_pred_valid, ds.y_visco_valid).item())
            record_loss.loc[idx,"loss_raman_valid"] = np.sqrt(criterion(y_raman_pred_valid,ds.y_raman_valid).item())
            record_loss.loc[idx,"loss_d_valid"] = np.sqrt(criterion(y_density_pred_valid,ds.y_density_valid).item())
            record_loss.loc[idx,"loss_Sconf_valid"] = np.sqrt(criterion(y_entro_pred_valid,ds.y_entro_valid).item())
            record_loss.loc[idx,"loss_ri_valid"]  = np.sqrt(criterion(y_ri_pred_valid,ds.y_ri_valid).item())

            record_loss.loc[idx,"loss_train"] = (record_loss.loc[idx,"loss_ag_train"] +
                                                 record_loss.loc[idx,"loss_myega_train"] +
                                                 record_loss.loc[idx,"loss_am_train"] +
                                                 record_loss.loc[idx,"loss_cg_train"] +
                                                 record_loss.loc[idx,"loss_tvf_train"] +
                                                 raman_scale*record_loss.loc[idx,"loss_raman_train"] +
                                                 density_scale*record_loss.loc[idx,"loss_d_train"] +
                                                 entro_scale*record_loss.loc[idx,"loss_Sconf_train"] +
                                                 ri_scale*record_loss.loc[idx,"loss_ri_train"])

            record_loss.loc[idx,"loss_valid"] = (record_loss.loc[idx,"loss_ag_valid"] +
                                                 record_loss.loc[idx,"loss_myega_valid"] +
                                                 record_loss.loc[idx,"loss_am_valid"] +
                                                 record_loss.loc[idx,"loss_cg_valid"] +
                                                 record_loss.loc[idx,"loss_tvf_valid"] +
                                                 raman_scale*record_loss.loc[idx,"loss_raman_valid"] +
                                                 density_scale*record_loss.loc[idx,"loss_d_valid"] +
                                                 entro_scale*record_loss.loc[idx,"loss_Sconf_valid"] +
                                                 ri_scale*record_loss.loc[idx,"loss_ri_valid"])

    return record_loss

###
### BAGGING
###

class bagging_models:
    """custom class for bagging models and making predictions

    Parameters
    ----------
    path : str
        path of models

    name_models : list of str
        names of models

    device : str
        cpu or gpu

    activation_function : torch.nn.Module
        activation function to be used, default is ReLU

    Methods
    -------
    predict : function
        make predictions

    """
    def __init__(self, path, name_models, ds, device, activation_function=torch.nn.ReLU()):

        self.device = device
        self.n_models = len(name_models)
        self.models = [None for _ in range(self.n_models)]

        for i in range(self.n_models):
            name = name_models[i]

            # Extract arch
            nb_layers = int(name[name.find("l")+1:name.find("_n")])
            nb_neurons = int(name[name.find("n")+1:name.rfind("_p")])
            p_drop = float(name[name.find("p")+1:name.rfind("_m")])

            self.models[i] = model(ds.x_visco_train.shape[1],nb_neurons,nb_layers,ds.nb_channels_raman,
                                   p_drop=p_drop, activation_function=activation_function)
            self.models[i].load_state_dict(torch.load(path+name,map_location='cpu'))
            self.models[i].eval()

    def predict(self, method, X, T=[1000.0], lbd= [500.0], sampling=False, n_sample = 10):
        """returns predictions from the n models

        Parameters
        ----------
        method : str
            the property to predict. See imelt code for possibilities. Basically it is a string handle that will be converted to an imelt function.
            For instance, for tg, enter 'tg'.
        X : pandas dataframe
            chemical composition for prediction
        T : list of floats
            temperatures for predictions, default = [1000.0]
        lbd : list of floats
            lambdas for Sellmeier equation, default = [500.0]
        sampling : Bool
            if True, dropout is activated and n_sample random samples will be generated per network. 
            This allows performing MC Dropout on the ensemble of models.
        """

        X = torch.Tensor(X).to(self.device)
        T = torch.Tensor(T).to(self.device)
        lbd = torch.Tensor(lbd).to(self.device)

        #
        # we activate dropout if necessary for error sampling
        #
        if sampling == True:
            for i in range(self.n_models):
                self.models[i].train()

        with torch.no_grad():
            if method == "raman_pred":
                #
                # For Raman spectra generation
                #
                if sampling == True:
                    out = np.zeros((len(X),850,self.n_models,n_sample)) # problem is defined with a X raman shift of 850 values
                    for i in range(self.n_models):
                        for j in range(n_sample):
                            out[:,:,i,j] = getattr(self.models[i],method)(X).cpu().detach().numpy()        
                    
                    # reshaping for 3D outputs
                    out = out.reshape((out.shape[0], out.shape[1], out.shape[2]*out.shape[3]))
                else:
                    out = np.zeros((len(X),850,self.n_models)) # problem is defined with a X raman shift of 850 values
                    for i in range(self.n_models):
                        out[:,:,i] = getattr(self.models[i],method)(X).cpu().detach().numpy()
            else:
                #
                # Other parameters (latent or real)
                #
                if sampling == True:
                    out = np.zeros((len(X),self.n_models, n_sample))
                    if method in frozenset(('ag', 'myega', 'am', 'cg', 'tvf','density_melt')):
                        for i in range(self.n_models):
                            for j in range(n_sample):
                                out[:,i,j] = getattr(self.models[i],method)(X,T).cpu().detach().numpy().reshape(-1)
                    elif method == "sellmeier":
                        for i in range(self.n_models):
                            for j in range(n_sample):
                                out[:,i,j] = getattr(self.models[i],method)(X,lbd).cpu().detach().numpy().reshape(-1)
                    else:
                        for i in range(self.n_models):
                            for j in range(n_sample):
                                out[:,i,j] = getattr(self.models[i],method)(X).cpu().detach().numpy().reshape(-1)
                    
                    # reshaping for 2D outputs
                    out = out.reshape((out.shape[0], out.shape[1]*out.shape[2]))
                else:
                    out = np.zeros((len(X),self.n_models))
                    if method in frozenset(('ag', 'myega', 'am', 'cg', 'tvf','density_melt')):
                        for i in range(self.n_models):
                            out[:,i] = getattr(self.models[i],method)(X,T).cpu().detach().numpy().reshape(-1)
                    elif method == "sellmeier":
                        for i in range(self.n_models):
                            out[:,i] = getattr(self.models[i],method)(X,lbd).cpu().detach().numpy().reshape(-1)
                    else:
                        for i in range(self.n_models):
                            out[:,i] = getattr(self.models[i],method)(X).cpu().detach().numpy().reshape(-1)
            
        #
        # Before leaving this function, we make sure we freeze again the dropout
        #
        for i in range(self.n_models):
                self.models[i].eval() # we make sure we freeze dropout if user does not activate sampling
        
        #
        # returning our sample
        #
        return out

def load_pretrained_bagged(path_viscosity="./data/NKCMAS_viscosity.hdf5", 
                            path_raman="./data/NKCMAS_Raman.hdf5", 
                            path_density="./data/NKCMAS_density.hdf5", 
                            path_optical="./data/NKCMAS_optical.hdf5",
                            path_cp="./data/NKCMAS_cp.hdf5", 
                            path_models = "./model/best/", 
                            device=torch.device('cpu'),
                            activation_function=torch.nn.ReLU()):
    """loader for the pretrained bagged i-melt models

    Parameters
    ----------
    path_viscosity : str
        Path for the melt viscosity HDF5 dataset (optional)
    path_raman : str
        Path for the glass Raman HDF5 dataset (optional)
    path_density : str
        Path for the glass density HDF5 dataset (optional)
    path_optical : str
        Path for the glass optical refractive index HDF5 dataset (optional)
    path_models : str
        Path for the models
    device : torch.device()
        CPU or GPU device, default = 'cpu' (optional)

    Returns
    -------
    bagging_models : object
        A bagging_models object that can be used for predictions
    """
    import pandas as pd
    ds = data_loader(path_viscosity,path_raman,path_density,path_optical,path_cp)
    name_list = pd.read_csv(path_models+"best_list.csv").loc[:,"name"]
    return bagging_models(path_models, name_list, ds, device, activation_function=activation_function)

def molarweights():
	"""returns a partial table of molecular weights for elements and oxides that can be used in other functions

    Returns
    =======
    w : dictionary
        containing the molar weights of elements and oxides:

        - si, ti, al, fe, li, na, k, mg, ca, ba, o (no upper case, symbol calling)

        - sio2, tio2, al2o3, fe2o3, feo, li2o, na2o, k2o, mgo, cao, sro, bao (no upper case, symbol calling)

    """
	w = {"si": 28.085}

    # From IUPAC Periodic Table 2016, in g/mol
	w["ti"] = 47.867
	w["al"] = 26.982
	w["fe"] = 55.845
	w["h"] = 1.00794
	w["li"] = 6.94
	w["na"] = 22.990
	w["k"] = 39.098
	w["mg"] = 24.305
	w["ca"] = 40.078
	w["ba"] = 137.327
	w["sr"] = 87.62
	w["o"] = 15.9994

	w["ni"] = 58.6934
	w["mn"] = 54.938045
	w["p"] = 30.973762

	# oxides
	w["sio2"] = w["si"] + 2* w["o"]
	w["tio2"] = w["ti"] + 2* w["o"]
	w["al2o3"] = 2*w["al"] + 3* w["o"]
	w["fe2o3"] = 2*w["fe"] + 3* w["o"]
	w["feo"] = w["fe"] + w["o"]
	w["h2o"] = 2*w["h"] + w["o"]
	w["li2o"] = 2*w["li"] +w["o"]
	w["na2o"] = 2*w["na"] + w["o"]
	w["k2o"] = 2*w["k"] + w["o"]
	w["mgo"] = w["mg"] + w["o"]
	w["cao"] = w["ca"] + w["o"]
	w["sro"] = w["sr"] + w["o"]
	w["bao"] = w["ba"] + w["o"]

	w["nio"] = w["ni"] + w["o"]
	w["mno"] = w["mn"] + w["o"]
	w["p2o5"] = w["p"]*2 + w["o"]*5
	return w # explicit return

def wt_mol(data):

	"""to convert weights in mol fraction

	Parameters
	==========
	data: Pandas DataFrame
		containing the fields sio2,tio2,al2o3,fe2o3,li2o,na2o,k2o,mgo,cao,feo

	Returns
	=======
	chemtable: Pandas DataFrame
		contains the fields sio2,tio2,al2o3,fe2o3,li2o,na2o,k2o,mgo,cao,feo in mol%
	"""

	chemtable = data.copy()
	w = molarweights()

	# conversion to mol in 100 grammes
	sio2 = chemtable["sio2"]/w["sio2"]
	al2o3 = chemtable["al2o3"]/w["al2o3"]
	na2o = chemtable["na2o"]/w["na2o"]
	k2o = chemtable["k2o"]/w["k2o"]
	mgo = chemtable["mgo"]/w["mgo"]
	cao = chemtable["cao"]/w["cao"]
	# renormalisation

	tot = sio2+al2o3+na2o+k2o+mgo+cao

	chemtable["sio2"]=sio2/tot
	chemtable["al2o3"]=al2o3/tot
	chemtable["na2o"]=na2o/tot
	chemtable["k2o"]=k2o/tot
	chemtable["mgo"]=mgo/tot
	chemtable["cao"]=cao/tot

	return chemtable

def R_Raman(x,y, lb = 670, hb = 870):
    """calculates the R_Raman parameter of a Raman signal y sampled at x.

    y can be an NxM array with N samples and M Raman shifts.
    """
    A_LW =  np.trapz(y[:,x<lb],x[x<lb],axis=1)
    A_HW =  np.trapz(y[:,x>hb],x[x>hb],axis=1)
    return A_LW/A_HW

class constants():
    def __init__(self):
        self.V_g_sio2 = (27+2*16)/2.2007
        self.V_g_al2o3 = (26*2+3*16)/3.009
        self.V_g_na2o = (22*2+16)/2.686
        self.V_g_k2o = (44*2+16)/2.707
        self.V_g_mgo = (24.3+16)/3.115
        self.V_g_cao = (40.08+16)/3.140
        
        self.V_m_sio2 = 27.297 # Courtial and Dingwell 1999, 1873 K
        self.V_m_al2o3 = 36.666 # Courtial and Dingwell 1999
        #self.V_m_SiCa = -7.105 # Courtial and Dingwell 1999
        self.V_m_na2o = 29.65 # Tref=1773 K (Lange, 1997; CMP)
        self.V_m_k2o = 47.28 # Tref=1773 K (Lange, 1997; CMP)
        self.V_m_mgo = 12.662 # Courtial and Dingwell 1999
        self.V_m_cao = 20.664 # Courtial and Dingwell 1999
        
        #dV/dT values
        self.dVdT_SiO2 = 1.157e-3 # Courtial and Dingwell 1999 
        self.dVdT_Al2O3 = -1.184e-3 # Courtial and Dingwell 1999
        #self.dVdT_SiCa = -2.138 # Courtial and Dingwell 1999
        self.dVdT_Na2O = 0.00768 # Table 4 (Lange, 1997)
        self.dVdT_K2O = 0.01208 # Table 4 (Lange, 1997)
        self.dVdT_MgO = 1.041e-3 # Courtial and Dingwell 1999
        self.dVdT_CaO = 3.786e-3 # Courtial and Dingwell 1999
        
        # melt T reference
        self.Tref_SiO2 = 1873.0 # Courtial and Dingwell 1999
        self.Tref_Al2O3 = 1873.0 # Courtial and Dingwell 1999
        self.Tref_Na2O = 1773.0 # Tref=1773 K (Lange, 1997; CMP)
        self.Tref_K2O = 1773.0 # Tref=1773 K (Lange, 1997; CMP)
        self.Tref_MgO = 1873.0 # Courtial and Dingwell 1999
        self.Tref_CaO = 1873.0 # Courtial and Dingwell 1999
        
        # correction constants between glass at Tambient and melt at Tref
        self.c_sio2 = self.V_m_sio2 - self.V_g_sio2
        self.c_al2o3 = self.V_m_al2o3 - self.V_g_al2o3
        self.c_na2o = self.V_m_na2o - self.V_g_na2o
        self.c_k2o = self.V_m_k2o - self.V_g_k2o
        self.c_mgo = self.V_m_mgo - self.V_g_mgo
        self.c_cao = self.V_m_cao - self.V_g_cao

class density_constants():

    def __init__(self):
        #Partial Molar Volumes
        self.MV_SiO2 = 27.297 # Courtial and Dingwell 1999
        self.MV_TiO2 = 28.32 # TiO2 at Tref=1773 K (Lange and Carmichael, 1987)
        self.MV_Al2O3 = 36.666 # Courtial and Dingwell 1999
        self.MV_Fe2O3 = 41.50 # Fe2O3 at Tref=1723 K (Liu and Lange, 2006)
        self.MV_FeO = 12.68 # FeO at Tref=1723 K (Guo et al., 2014)
        self.MV_MgO = 12.662 # Courtial and Dingwell 1999
        self.MV_CaO = 20.664 # Courtial and Dingwell 1999
        self.MV_SiCa = -7.105 # Courtial and Dingwell 1999
        self.MV_Na2O = 29.65 # Tref=1773 K (Lange, 1997; CMP)
        self.MV_K2O = 47.28 # Tref=1773 K (Lange, 1997; CMP)
        self.MV_H2O = 22.9 # H2O at Tref=1273 K (Ochs and Lange, 1999)

        #Partial Molar Volume uncertainties
        #value = 0 if not reported
        self.unc_MV_SiO2 = 0.152 # Courtial and Dingwell 1999
        self.unc_MV_TiO2 = 0.0
        self.unc_MV_Al2O3 = 0.196 # Courtial and Dingwell 1999
        self.unc_MV_Fe2O3 = 0.0
        self.unc_MV_FeO = 0.0
        self.unc_MV_MgO = 0.181 # Courtial and Dingwell 1999
        self.unc_MV_CaO = 0.123 # Courtial and Dingwell 1999
        self.unc_MV_SiCa = 0.509 # Courtial and Dingwell 1999
        self.unc_MV_Na2O = 0.07
        self.unc_MV_K2O = 0.10
        self.unc_MV_H2O = 0.60

        #dV/dT values
        #MgO, CaO, Na2O, K2O Table 4 (Lange, 1997)
        #SiO2, TiO2, Al2O3 Table 9 (Lange and Carmichael, 1987)
        #H2O from Ochs & Lange (1999)
        #Fe2O3 from Liu & Lange (2006)
        #FeO from Guo et al (2014)
        self.dVdT_SiO2 = 1.157e-3 # Courtial and Dingwell 1999 
        self.dVdT_TiO2 = 0.00724
        self.dVdT_Al2O3 = -1.184e-3 # Courtial and Dingwell 1999
        self.dVdT_Fe2O3 = 0.0
        self.dVdT_FeO = 0.00369
        self.dVdT_MgO = 1.041e-3 # Courtial and Dingwell 1999
        self.dVdT_CaO = 3.786e-3 # Courtial and Dingwell 1999
        self.dVdT_SiCa = -2.138 # Courtial and Dingwell 1999
        self.dVdT_Na2O = 0.00768
        self.dVdT_K2O = 0.01208
        self.dVdT_H2O = 0.0095

        #dV/dT uncertainties
        #value = 0 if not reported
        self.unc_dVdT_SiO2 = 0.0007e-3 # Courtial and Dingwell 1999
        self.unc_dVdT_TiO2 = 0.0
        self.unc_dVdT_Al2O3 = 0.0009e-3 # Courtial and Dingwell 1999
        self.unc_dVdT_Fe2O3 = 0.0
        self.unc_dVdT_FeO = 0.0
        self.unc_dVdT_MgO = 0.0008 # Courtial and Dingwell 1999
        self.unc_dVdT_CaO = 0.0005e-3 # Courtial and Dingwell 1999
        self.unc_dVdT_SiCa = 0.002e-3 # Courtial and Dingwell 1999
        self.unc_dVdT_Na2O = 0.0
        self.unc_dVdT_K2O = 0.0
        self.unc_dVdT_H2O = 0.0008

        #dV/dP values
        #Anhydrous component data from Kess and Carmichael (1991)
        #H2O data from Ochs & Lange (1999)
        self.dVdP_SiO2 = -0.000189
        self.dVdP_TiO2 = -0.000231
        self.dVdP_Al2O3 = -0.000226
        self.dVdP_Fe2O3 = -0.000253
        self.dVdP_FeO = -0.000045
        self.dVdP_MgO = 0.000027
        self.dVdP_CaO = 0.000034
        self.dVdP_Na2O = -0.00024
        self.dVdP_K2O = -0.000675
        self.dVdP_H2O = -0.00032

        #dV/dP uncertainties
        self.unc_dVdP_SiO2 = 0.000002
        self.unc_dVdP_TiO2 = 0.000006
        self.unc_dVdP_Al2O3 = 0.000009
        self.unc_dVdP_Fe2O3 = 0.000009
        self.unc_dVdP_FeO = 0.000003
        self.unc_dVdP_MgO = 0.000007
        self.unc_dVdP_CaO = 0.000005
        self.unc_dVdP_Na2O = 0.000005
        self.unc_dVdP_K2O = 0.000014
        self.unc_dVdP_H2O = 0.000060

        #Tref values
        self.Tref_SiO2 = 1873.0 # Courtial and Dingwell 1999
        self.Tref_TiO2 = 1773.0
        self.Tref_Al2O3 = 1873.0 # Courtial and Dingwell 1999
        self.Tref_Fe2O3 = 1723.0
        self.Tref_FeO = 1723.0
        self.Tref_MgO = 1873.0 # Courtial and Dingwell 1999
        self.Tref_CaO = 1873.0 # Courtial and Dingwell 1999
        self.Tref_Na2O = 1773.0
        self.Tref_K2O = 1773.0
        self.Tref_H2O = 1273.0


###
### Functions for ternary plots (not really needed with mpltern)
###

def polycorners(ncorners=3):
    '''
    Return 2D cartesian coordinates of a regular convex polygon of a specified
    number of corners.
    Args:
        ncorners (int, optional) number of corners for the polygon (default 3).
    Returns:
        (ncorners, 2) np.ndarray of cartesian coordinates of the polygon.
    '''

    center = np.array([0.5, 0.5])
    points = []

    for i in range(ncorners):
        angle = (float(i) / ncorners) * (np.pi * 2) + (np.pi / 2)
        x = center[0] + np.cos(angle) * 0.5
        y = center[1] + np.sin(angle) * 0.5
        points.append(np.array([x, y]))

    return np.array(points)

def bary2cart(bary, corners):
    '''
    Convert barycentric coordinates to cartesian coordinates given the
    cartesian coordinates of the corners.
    Args:
        bary (np.ndarray): barycentric coordinates to convert. If this matrix
            has multiple rows, each row is interpreted as an individual
            coordinate to convert.
        corners (np.ndarray): cartesian coordinates of the corners.
    Returns:
        2-column np.ndarray of cartesian coordinates for each barycentric
        coordinate provided.
    '''

    cart = None

    if len(bary.shape) > 1 and bary.shape[1] > 1:
        cart = np.array([np.sum(b / np.sum(b) * corners.T, axis=1) for b in bary])
    else:
        cart = np.sum(bary / np.sum(bary) * corners.T, axis=1)

    return cart

def CLR(input_array):
    """Transform chemical composition in colors

    Inputs
    ------
    input_array: n*4 array
        4 chemical inputs with sio2, al2o3, k2o and na2o in 4 columns, n samples in rows

    Returns
    -------
    out: n*3 array
        RGB colors
    """
    XXX = input_array.copy()
    XXX[:,2] = XXX[:,2]+XXX[:,3] # adding alkalis
    out = np.delete(XXX,3,1) # remove 4th row
    # min max scaling to have colors in the full RGB scale
    out[:,0] = (out[:,0]-out[:,0].min())/(out[:,0].max()-out[:,0].min())
    out[:,1] = (out[:,1]-out[:,1].min())/(out[:,1].max()-out[:,1].min())
    out[:,2] = (out[:,2]-out[:,2].min())/(out[:,2].max()-out[:,2].min())
    return out

def make_ternary(ax,t,l,r, z,labelt,labell,labelr,levels, levels_l, c_m, norm,boundaries_SiO2,annotation = "(a)"):

    ax.plot([1.0,0.5],[0.,0.5],[0.,0.5],"--",color="black")

    ax.tricontourf(t,l,r,z,
                levels=levels, cmap=c_m, norm=norm)

    tc = ax.tricontour(t,l,r,z,
                    levels=levels_l,colors='k', norm=norm)

    ax.clabel(tc, inline=1, fontsize=7, fmt="%1.1f")

    ax.set_tlabel(labelt)
    #ax.set_llabel(labell)
    #ax.set_rlabel(labelr)

    ax.taxis.set_label_rotation_mode('horizontal')
    #ax.laxis.set_tick_rotation_mode('horizontal')
    #ax.raxis.set_label_rotation_mode('horizontal')

    make_arrow(ax, labell, labelr)

    ax.raxis.set_ticks([])

    # Using ``ternary_lim``, you can limit the range of ternary axes.
    # Be sure about the consistency; the limit values must satisfy:
    # tmax + lmin + rmin = tmin + lmax + rmin = tmin + lmin + rmax = ternary_scale
    ax.set_ternary_lim(
        boundaries_SiO2[0], boundaries_SiO2[1],  # tmin, tmax
        0.0, boundaries_SiO2[0],  # lmin, lmax
        0.0, boundaries_SiO2[0],  # rmin, rmax
    )

    ax.annotate(annotation, xy=(-0.1,1.0), xycoords="axes fraction", fontsize=12)

    ax.spines['tside'].set_visible(False)

    #ax.annotate(labell, xy=(-0.1,-0.07), xycoords="axes fraction", ha="center")
    #ax.annotate(labelr, xy=(1.1,-0.07), xycoords="axes fraction", ha="center")

    ax.tick_params(labelrotation='horizontal')

def make_arrow(ax, labell, labelr, sx1 = -0.1, sx2 = 1.02, fontsize = 9, linewidth = 2):
    ax.annotate('', xy=(sx1, 0.03), xycoords='axes fraction', xytext=(sx1+0.08, 0.18),
            arrowprops=dict(arrowstyle="->", color='k',linewidth=linewidth))

    ax.annotate(labell, xy=(sx1+0.03
                                  ,0.08), xycoords="axes fraction",
                ha="center",rotation=60,fontsize = fontsize)

    ax.annotate('', xy=(sx2, 0.18), xycoords='axes fraction', xytext=(sx2+0.08, 0.03),
                arrowprops=dict(arrowstyle="<-", color='k',linewidth=linewidth))

    ax.annotate(labelr, xy=(sx2+0.05,0.08), xycoords="axes fraction",
                ha="center",rotation=-60, fontsize = fontsize)

def plot_loss(ax, loss, legends, scale="linear"):
    for count,i in enumerate(loss):
        ax.plot(i,label=legends[count])

    ax.legend()
    ax.set_yscale(scale)
    ax.set_xlabel("Epoch")
