#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
CONVERT MLDS/MLCM OBJECT TO CSV FILE (1 per observer/background condition/background pattern)
NORMALIZE MLDS/MLCM DATA AND SAVE THESE INTO ONE CSV FILE PER BACKGROUND CONDITION (plain/dark/light)
get experimental data of Aguilar & Maertens 2020
convert MLDS/MLCM object to CSV file
normalize pscale & confidence intervals to make data comparable among obsververs
"""

####################################################################################################################
"""IMPORT"""
import numpy as np
import pandas as pd
import subprocess as sp                             
import rea_constants as rc
import rea_utils as ru

####################################################################################################################
"""CONSTANTS"""

# define which data shall be normalized
method = "MLDS" # MLDS/MLCM

# path of experimental data of Aguilar2020
var_path = rc.p_exp_mldscm  + "results_merged/"     # variegated 
hom_path = rc.p_exp_mldscm  + "results_merged_SR/"  # homogeneous

####################################################################################################################
"""FUNCTIONS"""

"""
CONVERT AN MLDS OR MLCM FILE TO A CSV FILE
call RScript that:
    loads MLDS/MLCM file = experimental data of Aguilar2020
    saves pscale with corresponding confidence intervals in one csv file \
        per observer, background condition (plain/dark/light), \
        background pattern (variegated/homogeneous)
INPUT:
    bg  - background condition
    o   - observer
"""
def convRaw2CSV(bg, o):
    if(method == "MLDS"):
        # filename for variegated/homogeneous MLCM data
        fn = '_'.join([o, "mlds", bgc, rc.fn_ext_mlds])        
        # define command to call rscript
        command = "convMLDS2CSV.r"
        
    elif(method == "MLCM"):
        # filename for variegated/homogeneous MLCM data
        fn = '_'.join([o, "mlcm", rc.fn_ext_mlcm])      
        # define command to call rscript
        command = "convMLCM2CSV.r"
    
    # path to data
    p_var_file = var_path + fn
    p_hom_file = hom_path + fn

    # commands to call subprocess
    cmd_var = ["Rscript", command, p_var_file, o, bgc, rc.var_cond]
    cmd_hom = ["Rscript", command, p_hom_file, o, bgc, rc.hom_cond]
    
    # convert MLDS for variegated data to csv 
    # call program in R via subprocess
    tmp_var = sp.check_output(cmd_var, universal_newlines = True)
    if(tmp_var != "3"):
        raise ValueError('Conversion was not successful')
    
    # convert MLDS for homogeneous data to csv 
    # call program in R via subprocess
    tmp_hom = sp.check_output(cmd_hom, universal_newlines = True)
    if(tmp_hom != "3"):
        raise ValueError('Conversion was not successful')
  
        
"""
NORMALIZE CSV DATA CREATED BY RSCRIPT
normalize pscale and corresponding confidence intervals \
    by last value of pscale -> normalize to 1
INPUT:
    data - data that shall be normalized
RETURN:
    (norm_ps, norm_ustd, norm_lstd) - normalized pscale and confidence intervals
"""
def norm_data(data):
    ps = data["pscale"]
    last_idx = len(ps) - 1    # index of last entry
    norm_factor = ps[last_idx]
    norm_ps = ru.normalize_by_x(ps, norm_factor)
    norm_ustd = ru.normalize_by_x(data["up_std"], norm_factor)
    norm_lstd = ru.normalize_by_x(data["low_std"], norm_factor)
    return(norm_ps, norm_ustd, norm_lstd)


################################################################################################
"""MAIN"""

"""
get experimental data for all observers & background conditions
create one csv file per background condition
"""
for bgc in rc.bg_cond:
    
    # luminance values for specific background condition
    lum = rc.lum_mlds[bgc]
    n_lum = len(lum)
    
    # replicate luminance list for creation of dataframe
    # all observers had the same luminance values within one condition
    rep_lum = [l for i in range(rc.n_obs) for j in range(rc.n_exp_cond) for l in lum]

    # repliacte variegated label for creation of dataframe
    # each luminance value once in each experimental condition
    rep_var = [rc.var_cond] * n_lum
    
    # replicate homogeneous label
    rep_hom = [rc.hom_cond] * n_lum
    
    # iniliaze dictionary
    tmp_dict = {"lum": rep_lum, 
                "pscale": [],
                "up_std": [],
                "low_std": [],
                "obs": [],
                "background": []}
    

    for o in rc.obs:
        # call R script with subprocess to convert MLCM experimental data to CSV file
        # one CSV per observer/condition/var
        convRaw2CSV(bgc, o)
        
        # path to current variegated & homogeneous csv file
        var_file = method + o + bgc + rc.var_cond + ".csv"
        p_var_csv = rc.p_csv_data + var_file
        hom_file = method + o + bgc + rc.hom_cond + ".csv"
        p_hom_csv = rc.p_csv_data + hom_file
        
        # load individual variegated csv data
        var_data = pd.read_csv(p_var_csv, sep = ',')
        # normalize data
        norm_var_ps, norm_var_ust, norm_var_lst = norm_data(var_data)

        # load individual homogeneous csv data        
        hom_data = pd.read_csv(p_hom_csv, sep = ',')
        # normalize data
        norm_hom_ps, norm_hom_ust, norm_hom_lst = norm_data(hom_data)
        
        # replicate observer label for creation of dataframe
        # data for one observer for each lum value and each experimental condition
        rep_obs = [o] * n_lum * rc.n_exp_cond
        tmp_dict["obs"].extend(rep_obs)
        
        # insert values for variegated condition into dictionary
        tmp_dict["background"].extend(rep_var)
        tmp_dict["pscale"].extend(norm_var_ps)
        tmp_dict["up_std"].extend(norm_var_ust)
        tmp_dict["low_std"].extend(norm_var_lst)
        
        # insert values for homogeneous condition into dictionary
        tmp_dict["background"].extend(rep_hom)
        tmp_dict["pscale"].extend(norm_hom_ps)
        tmp_dict["up_std"].extend(norm_hom_ust)
        tmp_dict["low_std"].extend(norm_hom_lst)
        
    # save the data for all observers for one background condition in one csv file 
    # convert dictionary to dataframe
    comb_df = pd.DataFrame(tmp_dict, columns = ["lum", "pscale", "up_std", "low_std", "obs", "background"])
        
    # filename of combined csv file
    comb_csv = method + bgc + ".csv"
    
    # save to csv file
    p_tmp_csv = rc.p_csv_data + comb_csv
    comb_df.to_csv(p_tmp_csv, columns = ["lum", "pscale", "up_std", "low_std", "obs", "background"] , sep = ',', index = False)
        


        
