#!/usr/bin/env python
# coding: utf-8

########## Calling relevant libraries ##########
import  h5py, os

# local imports
import imelt.model as model
import imelt.utils as utils

import numpy as np
import pandas as pd
import rampy as rp
import matplotlib.pyplot as plt

import sklearn.model_selection as model_selection
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer
from sklearn.linear_model import HuberRegressor

#
# function definition
#

def prepare_raman(my_liste, output_file):
    """prepare the raman dataset for the ML model"""
    # Run
    nb_exp = my_liste.shape[0]
    print(nb_exp)
    roi_glass = my_liste.loc[:,"lb1":"hb2"]
    scaling_factor = 1000.   

    x = np.arange(400.,1250.,1.0) # our real x axis, for resampling
    spectra = np.ones((len(x),nb_exp))
    spectra_long = np.ones((len(x),nb_exp))

    xmin = np.ones((nb_exp,1))

    for i in range(nb_exp):
        file_name, file_extension=os.path.splitext(my_liste.loc[i,"nom"])
        
        if file_extension == ".txt" or file_extension == ".TXT":
            sp = np.genfromtxt("./data/raman/"+my_liste.loc[i,"nom"],skip_header=1)
        elif file_extension == ".csv":
            sp = np.genfromtxt("./data/raman/"+my_liste.loc[i,"nom"],skip_header=1,delimiter=",")
        else:
            raise InputError("Unsupported file extension")
        
        # we flip the spectra if necessary
        sp = rp.flipsp(sp)
        
        # we apply the long correction
        if my_liste.raw[i] == "yes":
            _, y_long, ese_long = rp.tlcorrection(sp[:,0], sp[:,1]-np.min(sp[sp[:,0]>600,1]), 23.0,
                                            my_liste.loc[i,"laserfreq"], normalisation="intensity")
        elif my_liste.raw[i] == "no":
            y_long = sp[:,1]-np.min(sp[sp[:,0]>600,1])
        else:
            raise ValueError("Check the column raw, should be yes or no.")
        
        # resampling 
        #y_resampled = rp.resample(sp[:,0], y_long.ravel(), x, fill_value="extrapolate") 
        # scaling x
        X_scaler = StandardScaler()
        x_scaled = X_scaler.fit_transform(sp[:,0].reshape(-1,1)) 
        # fit model
        model = make_pipeline(SplineTransformer(n_knots=100, degree=3), HuberRegressor()).fit(x_scaled, y_long)
        # predict on new x axis
        y_resampled = model.predict(X_scaler.transform(x.reshape(-1,1))).ravel()
        
        print("Spectra %i, checking array size: %i" % (i,sp.shape[0]))
        
        # we get the array position of the minima near 800 automatically
        #idx_min = np.where(y_resampled == np.min(y_resampled[(800<= x)&(x<=1000)]))[0]
        #xmin[i] = x[idx_min]
        
        # updating the BIR
        #bir = np.array([[xmin[i]-5,xmin[i]+5],[1230,1250]])
        
        # Fitting the background
        #y_bas, bas = rp.baseline(x, y_resampled,bir,"poly",polynomial_order=1)

        y_bas = (y_resampled-np.min(y_resampled))/(np.max(y_resampled)-np.min(y_resampled))
        
        # Assigning the spectra in the output array
        spectra_long[:,i] = y_bas.ravel()
        
        # Making a nice figure
        plt.figure()
        plt.suptitle(my_liste.loc[i,"product"])
        plt.subplot(1,2,1)
        plt.plot(sp[:,0], y_long, "k.")
        plt.plot(x, y_resampled, "b-")
        plt.plot(x, y_bas, "c-")
        
        plt.subplot(1,2,2)
        plt.plot(x,y_bas,"r-")
        plt.savefig("./figures/datasets/raman/{}.pdf".format(my_liste.loc[i,"product"]))
    
    # saving the spectra in HDF5
    TOTAL = my_liste.sio2 + my_liste.al2o3 + my_liste.na2o + my_liste.k2o + my_liste.mgo + my_liste.cao
    X = my_liste.loc[:,["sio2","al2o3","na2o","k2o","mgo","cao"]]/TOTAL.values.reshape(-1,1)
    X = utils.descriptors(X).values
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X,spectra_long.T,test_size=0.15, random_state=67) # train-test split
    with h5py.File(output_file, 'w') as f:
        f.create_dataset('X_raman_train', data=X_train)
        f.create_dataset('X_raman_test', data=X_test)
        f.create_dataset('y_raman_train', data=y_train)
        f.create_dataset('y_raman_test', data=y_test)

def prepare_cp(dataset,output_file, rand_state=60):
    """prepare the dataset of liquid heat capacity for the ML model"""
    # control dataset
    dataset = model.chimie_control(dataset)
    
    # grab what we are interested in
    X_cp_l = utils.descriptors(dataset.loc[:, ["sio2","al2o3","na2o","k2o","mgo","cao"]])
    T_cp_l = dataset.loc[:, ["T"]]
    y_cp_l = dataset.loc[:, ["Cp_l"]]
    
    # Cp_l is only used as a regularization parameter during training
    # dataset is too small for ML
    # therefore no splitting is done here
    # writing the data in HDF5 file for later call
    with h5py.File(output_file, 'w') as f:
        f.create_dataset('X_cp_l', data=X_cp_l)
        f.create_dataset('T_cp_l', data=T_cp_l)
        f.create_dataset('y_cp_l',  data=y_cp_l)
        
    print("Done.")

def prepare_density(dataset,output_file, rand_state=60):
    """prepare the dataset of glass density for the ML model"""
    
    # control dataset
    dataset = model.chimie_control(dataset)
    
    # grab what we are interested in
    X_d = dataset.loc[:, ["sio2","al2o3","na2o","k2o","mgo","cao"]]
    X_d = utils.descriptors(X_d)
    y_d = dataset.loc[:, ["d"]]
    
    # Density dataset has a very low number of duplicates, so data leakage is not a problem
    # we thus use directly the model_selection.train_test_split function
    # train-valid-test split 70-15-15   
    X_train, X_vt, y_train, y_vt = model_selection.train_test_split(X_d, y_d, test_size=0.20, random_state=rand_state)
    X_valid, X_test, y_valid, y_test = model_selection.train_test_split(X_vt, y_vt, test_size=0.5, random_state=rand_state)
    
    # writing the data in HDF5 file for later call
    with h5py.File(output_file, 'w') as f:
        f.create_dataset('X_density_train', data=X_train)
        f.create_dataset('X_density_valid', data=X_valid)
        f.create_dataset('X_density_test',  data=X_test)

        f.create_dataset('y_density_train', data=y_train)
        f.create_dataset('y_density_valid', data=y_valid)
        f.create_dataset('y_density_test',  data=y_test)
        
    print("Done.")
 
def prepare_viscosity(dataset,output_file, rand_state=67):
    """prepare the dataset of glass-forming melt viscosity for the ML model"""
    print('Reading data...')
    # reading the Pandas dataframe
    dataset = model.chimie_control(dataset)

    #
    # For viscosity
    #
    
    # train-valid-test split
    print("Splitting datasets...\n")
    # 80 % of the data for training
    train_sub, tv_sub, idxtrain_sub, idxtv_sub = rp.chemical_splitting(dataset,'Name',
                                                                             split_fraction=0.20, 
                                                                             rand_state=rand_state)
    
    # 10% for test, 10% for validation
    valid_sub, test_sub, idxvalid_sub, idxtest_sub = rp.chemical_splitting(tv_sub,'Name',
                                                                     split_fraction=0.5, 
                                                                     rand_state=rand_state)
    
    # composition
    X_columns = ["sio2","al2o3","na2o","k2o","mgo","cao"]
    X_train = train_sub.loc[:,X_columns]
    X_valid = valid_sub.loc[:,X_columns]
    X_test = test_sub.loc[:,X_columns]

    # temperature
    T_train = train_sub.loc[:,"T"].values
    T_valid = valid_sub.loc[:,"T"].values
    T_test = test_sub.loc[:,"T"].values

    # add descriptors
    X_train = utils.descriptors(X_train).values
    X_valid = utils.descriptors(X_valid).values
    X_test  = utils.descriptors(X_test).values
    
    y_train = train_sub["viscosity"].values.reshape(-1,1)
    y_valid = valid_sub["viscosity"].values.reshape(-1,1)
    y_test = test_sub["viscosity"].values.reshape(-1,1)
    
    #
    # For entropy
    #
    # we drop all rows without entropy values and get only one value per composition
    #
    dataset_entropy = dataset.dropna(subset=['Sc']).copy()
    dataset_entropy.drop_duplicates(subset ="Name",keep = "first", inplace = True)

    # 80-10-10 split
    train_entropy, tv_entropy = model_selection.train_test_split(dataset_entropy, test_size=0.20, random_state=rand_state)
    test_entropy, valid_entropy = model_selection.train_test_split(tv_entropy, test_size=0.5, random_state=rand_state)
    
    X_columns = ["sio2","al2o3","na2o","k2o","mgo","cao"] # for output
    X_entropy_train = train_entropy.loc[:,X_columns]
    X_entropy_valid = valid_entropy.loc[:,X_columns]
    X_entropy_test = test_entropy.loc[:,X_columns]

    # add descriptors
    X_entropy_train = utils.descriptors(X_entropy_train).values
    X_entropy_valid = utils.descriptors(X_entropy_valid).values
    X_entropy_test  = utils.descriptors(X_entropy_test).values
    
    y_entropy_train = train_entropy.loc[:,"Sc"].values
    y_entropy_valid = valid_entropy.loc[:,"Sc"].values
    y_entropy_test = test_entropy.loc[:,"Sc"].values
    
    #
    # for Tg
    # we grab the Tgs associated with the train-valid-test split of viscosity data
    # (as Tg is not used for training per se)
    #
     
    # we drop the values at 0 (Tg not determined)
    train_tg = train_sub[train_sub.tg != 0]
    valid_tg = valid_sub[valid_sub.tg != 0]
    test_tg = test_sub[test_sub.tg != 0]
    
    # for output
    X_tg_train = train_tg.loc[:,["sio2","al2o3","na2o","k2o","mgo","cao"]]
    X_tg_valid = valid_tg.loc[:,["sio2","al2o3","na2o","k2o","mgo","cao"]]
    X_tg_test = test_tg.loc[:,["sio2","al2o3","na2o","k2o","mgo","cao"]]
    
    # add descriptors
    X_tg_train = utils.descriptors(X_tg_train)
    # last time we do it so we now record the columns
    X_columns = X_tg_train.columns.values
    # and we convert to numpy and continue
    X_tg_train = X_tg_train.values
    X_tg_valid = utils.descriptors(X_tg_valid).values
    X_tg_test  = utils.descriptors(X_tg_test).values

    y_tg_train = train_tg.loc[:,"tg"].values
    y_tg_valid = valid_tg.loc[:,"tg"].values
    y_tg_test = test_tg.loc[:,"tg"].values

    # Figure of the datasets
    plt.figure()
    plt.subplot(121)
    plt.plot(10000/T_train,y_train,"k.", label="train")

    plt.subplot(121)
    plt.plot(10000/T_valid,y_valid,"b.", label="valid")

    plt.subplot(121)
    plt.plot(10000/T_test,y_test,"r.", label="test")
    plt.savefig(output_file+".pdf")
    plt.close()

    print("Size of viscous training subsets:\n")
    print(X_train.shape)
    
    # writing the data in HDF5 file for later call
    with h5py.File(output_file, 'w') as f:
        f.create_dataset('X_columns', data=X_columns)#data=np.array(X_columns, dtype="S10"))

        f.create_dataset('X_entropy_train', data=X_entropy_train)
        f.create_dataset('y_entropy_train', data=y_entropy_train.reshape(len(y_entropy_train),1))
        
        f.create_dataset('X_entropy_valid', data=X_entropy_valid)
        f.create_dataset('y_entropy_valid', data=y_entropy_valid.reshape(len(y_entropy_valid),1))
        
        f.create_dataset('X_entropy_test', data=X_entropy_test)
        f.create_dataset('y_entropy_test', data=y_entropy_test.reshape(len(y_entropy_test),1))
        
        f.create_dataset('X_tg_train',data=X_tg_train)
        f.create_dataset('X_tg_valid',data=X_tg_valid)
        f.create_dataset('X_tg_test',data=X_tg_test)
        
        f.create_dataset('y_tg_train',data=y_tg_train.reshape(len(y_tg_train),1))
        f.create_dataset('y_tg_valid',data=y_tg_valid.reshape(len(y_tg_valid),1))
        f.create_dataset('y_tg_test',data=y_tg_test.reshape(len(y_tg_test),1))

        f.create_dataset('X_train', data=X_train)
        f.create_dataset('T_train', data=T_train)
        f.create_dataset('y_train', data=y_train)
        
        f.create_dataset('X_valid', data=X_valid)
        f.create_dataset('T_valid', data=T_valid)
        f.create_dataset('y_valid', data=y_valid)
        
        f.create_dataset('X_test', data=X_test)
        f.create_dataset('T_test', data=T_test)
        f.create_dataset('y_test', data=y_test)

def prepare_ri(dataset,output_file, rand_state=81):
    """prepare the optical refractive index data for the ML model"""
    # Control data
    dataset = model.chimie_control(dataset)
    
    # train-valid-test split
    # below the split fractions are not 0.15 0.15 strictly 
    # because the second value is relative to the remaining tv_sub dataset size...
    # At the end, this was adjusted to get splits of 80-10-10 by composition
    print("Splitting datasets...\n")
    train_sub, tt_sub, idxtrain_sub, idxtt_sub = rp.chemical_splitting(dataset,'Name',
                                                                             split_fraction=0.20, 
                                                                             rand_state=rand_state)
    valid_sub, test_sub, idxvalid_sub, idxtest_sub = rp.chemical_splitting(tt_sub,'Name',
                                                                     split_fraction=0.5, 
                                                                     rand_state=rand_state)
    
    
    X_columns = ["sio2","al2o3","na2o","k2o","mgo","cao"] # for output
    X_train = train_sub.loc[:,X_columns]
    X_valid = valid_sub.loc[:,X_columns]
    X_test = test_sub.loc[:,X_columns]

    # add descriptors
    X_train = utils.descriptors(X_train).values
    X_valid = utils.descriptors(X_valid).values
    X_test  = utils.descriptors(X_test).values
    
    lbd_train = train_sub["lbd"].values.reshape(-1,1)*1e-3
    lbd_valid = valid_sub["lbd"].values.reshape(-1,1)*1e-3
    lbd_test = test_sub["lbd"].values.reshape(-1,1)*1e-3
    
    y_train = train_sub["ri"].values.reshape(-1,1)
    y_valid = valid_sub["ri"].values.reshape(-1,1)
    y_test = test_sub["ri"].values.reshape(-1,1)
       
    # writing the data in HDF5 file for later call
    with h5py.File(output_file, 'w') as f:
        f.create_dataset('X_ri_train', data=X_train)
        f.create_dataset('X_ri_valid', data=X_valid)
        f.create_dataset('X_ri_test',  data=X_test)

        f.create_dataset('lbd_ri_train', data=lbd_train)
        f.create_dataset('lbd_ri_valid', data=lbd_valid)
        f.create_dataset('lbd_ri_test',  data=lbd_test)

        f.create_dataset('y_ri_train', data=y_train)
        f.create_dataset('y_ri_valid', data=y_valid)
        f.create_dataset('y_ri_test',  data=y_test)

    print("Done.")

if __name__=="__main__":

    # ask which dataset needs to be prepared:
    print("Which dataset do you want to prepare?")
    print("Type:\n    v for viscosity")
    print("    r for Raman spectroscopy")
    print("    o for optical refractive index")
    print("    d for density")
    print("    c for liquid heat capacity")

    good = False
    while good == False:
        user_input = input("Enter the desired value:")
        if user_input in ["v","r","o","d","c"]:
            good = True
    
    if user_input == "v":
        # Viscosity preparation
        print("Preparing the viscosity datasets...")
        dataset = pd.read_excel("./data/Database_IPGP.xlsx",sheet_name="VISCO")
        print(dataset.columns)

        #fractions_valid = [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80]
        #prefix= ["_0p10val","_0p20val","_0p30val","_0p40val","_0p50val","_0p60val","_0p70val","_0p80val"]

        #for indice,value in enumerate(fractions_valid):
        #prepare_viscosity(dataset,"./data/NKCMAS_viscosity"+prefix[indice]+".hdf5", rand_state=67)
        prepare_viscosity(dataset,"./data/NKCMAS_viscosity.hdf5", rand_state=61)

    if user_input == "d":
        # Density preparation
        print("Preparing the density dataset...")
        prepare_density(pd.read_excel("./data/Database_IPGP.xlsx",sheet_name="DENSITY"),"./data/NKCMAS_density.hdf5")

    if user_input == "o":
        # Refractive Index preparation
        print("Preparing the optical refractive index dataset...")
        prepare_ri(pd.read_excel("./data/Database_IPGP.xlsx",sheet_name="OPTICAL"),"./data/NKCMAS_optical.hdf5", rand_state=60)

    if user_input == "r":
        # Raman spectra preparation
        print("Preparing the Raman spectra dataset...")
        prepare_raman(pd.read_excel("./data/Database_IPGP.xlsx", "RAMAN"), './data/NKCMAS_Raman.hdf5')

    if user_input == "c":
        # Heat capacity preparation
        print("Preparing the heat capacity dataset...")
        prepare_cp(pd.read_excel("./data/Database_IPGP.xlsx", "CP"), './data/NKCMAS_cp.hdf5')