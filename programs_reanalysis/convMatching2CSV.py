#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
CONVERT MATCHING .TXT TO CSV FILE (1 per observer/background condition/background pattern)
CONVERT ENTRIES OF TARGET/MATCH LUMINANCE TO BE IN RANGE [0,255]
get experimental data of Aguilar & Maertens 2020
convert entries to be in luminance range [0, 255]
convert .txt file to CSV file: 1 per background condition
"""

####################################################################################################################
"""IMPORT"""

import pandas as pd
import rea_constants as rc
import rea_utils as ru

####################################################################################################################
"""CONSTANTS"""

# define method
method = "Matching"

# path of experimental data of Aguilar2020
var_path = rc.p_exp_match  + "results/"     # variegated
hom_path = rc.p_exp_match  + "resultsSR/"   # homogeneous

####################################################################################################################
"""FUNCTIONS"""

"""
PREPROCESS DATA BEFORE SAVING INTO CSV
convert entries with target's reflectance to luminance
convert match's luminance range [0, 1] -> [0, 255]
INPUT:
    df  - dataframe to be processed
    c   - background condition (plain/dark/light)
RETURN:
    tarl, matl - target and match luminance
"""
def preprocess(df, c):
    # extract relevant columns
    df = df[['context', 'r', 'match_lum']]
    
    # extract relevant rows, only rows for particular condition
    dfc = df.loc[df['context'] == c]

    # target's reflectance to luminance
    tarl = ru.map_rl(dfc["r"], c)
    
    # convert match luminance values from [0,1] to [0, 255]
    matl = ru.conv_lut(dfc["match_lum"])
    dfc.loc[:, "match_lum"] = matl 
    
    return tarl, matl

####################################################################################################################
"""MAIN"""

"""
get experimental data for all observers & background conditions
create one csv file per background condition
"""
for bgc in rc.bg_cond:
    # iniliaze dictionary
    tmp_dict = {"tar_lum": [], 
                "mat_lum": [],
                "obs": [],
                "background": []}
    
    # load and add data for each observer
    for o in rc.obs:
        # filename for variegated/homogeneous data
        fn = o + ".txt"
        
        # path to data
        p_var_file = var_path + fn
        p_hom_file = hom_path + fn
        
        # load individual csv data
        var_data = pd.read_csv(p_var_file, sep = '\t')
        hom_data = pd.read_csv(p_hom_file, sep = '\t')
        
        # preprocess data, convert luminance values
        var_tar, var_mat = preprocess(var_data, bgc)
        hom_tar, hom_mat = preprocess(hom_data, bgc)
        
        # repliacte variegated/homogeneous label for creation of dataframe
        # each luminance value once in each experimental condition
        rep_var = [rc.var_cond] * len(var_tar)
        rep_hom = [rc.hom_cond] * len(hom_tar)
    
        # insert luminance values and cond labels in dictionary
        # variegated condition
        tmp_dict["tar_lum"].extend(var_tar)
        tmp_dict["mat_lum"].extend(var_mat)
        tmp_dict["background"].extend(rep_var)
        
        # insert homogeneous data
        tmp_dict["tar_lum"].extend(hom_tar)
        tmp_dict["mat_lum"].extend(hom_mat)
        tmp_dict["background"].extend(rep_hom)
        
        # number of entries, no. values for target in variegated & homogeneous condition
        n_entries = len(var_tar) + len(hom_tar)

        # replicate observer label for creation of dataframe
        rep_obs = [o] * n_entries
        tmp_dict["obs"].extend(rep_obs)
       
    # convert dictionary with data for all observers to dataframe
    comb_df = pd.DataFrame(tmp_dict, columns = ["tar_lum", "mat_lum",  "obs", "background"])
    
    # filename of combined csv file
    comb_csv = method + bgc + ".csv"
    
    # save to csv file
    p_tmp_csv = rc.p_csv_data + comb_csv
    comb_df.to_csv(p_tmp_csv, columns = ["tar_lum", "mat_lum",  "obs", "background"] , sep = ',', index = False)
    
    
        
        
        
        
        
        
        
        