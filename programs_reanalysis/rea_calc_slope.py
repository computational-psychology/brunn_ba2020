#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
CALCULATE SLOPE FOR ALL OBSERVERS AND SAVE IN CSV FILE PER BACKGROUND CONDITION
calculate slope between each two data points
x data points result in x-1 slope values
"""

####################################################################################################################
"""IMPORT"""

import numpy as np
import pandas as pd
import rea_constants as rc
import rea_utils as ru

####################################################################################################################
"""CONSTANTS"""

# specify for which method the slope shall be calculated
method = "Matching" # "MLDS"/"MLCM"/"Matching"

# specify names to extract columns from dataframe depending on method
if(method == "Matching"):    
    x_label = "tar_lum"
    y_label = "mat_lum"
elif((method == "MLDS") or (method == "MLCM")):
    x_label = "lum"
    y_label = "pscale"
else:
    raise ValueError ("Choose valid experimental method")

####################################################################################################################
"""MAIN"""

""" calculate slope for each background condition"""
for bgc in rc.bg_cond:
    
    # load csv file for bgc background condition
    csv_file = method + bgc + ".csv"
    #p_tmp_csv = rc.p_csv_data + csv_file
    df = pd.read_csv((rc.p_csv_data + csv_file), sep = ',')

    # initialize temporary dictionary for slope data
    tmp_dict = {"lum": [],
                "slope": [], 
                "obs": [], 
                "background": []}
    
    # calculate slope for each observer
    for o in rc.obs:
        # extract observer-specific data
        df_obs = df.loc[df["obs"] == o]
        df_o_var = df_obs.loc[df_obs["background"] == rc.var_cond] # variegated 
        df_o_hom = df_obs.loc[df_obs["background"] == rc.hom_cond] # homogeneous

        # get average matching value for target luminance \
        # multiple matching luminance values per target luminance value
        if(method == "Matching"):
            x_var, y_var = ru.avg_data(df_o_var, x_label, y_label)
            x_hom, y_hom = ru.avg_data(df_o_hom, x_label, y_label)
        # MLDS data has only one pscale value per luminance value
        elif((method == "MLDS") or (method == "MLCM")):   
            x_var = df_o_var[x_label]
            y_var = df_o_var[y_label]
            x_hom = df_o_hom[x_label]
            y_hom = df_o_hom[y_label]
        
        # calculate slope luminance values: slope is calculated btw each two x values (luminance)
        var_lum = ru.cal_sl_lum(x_var)
        hom_lum = ru.cal_sl_lum(x_hom)
        
        # calculate slope
        var_slope = ru.calc_slope(x_var, y_var)
        hom_slope = ru.calc_slope(x_hom, y_hom)

        # repliacte variegated/homogeneous label for creation of dataframe
        # each slope value once in each experimental condition
        rep_var = [rc.var_cond] * len(var_slope)
        rep_hom = [rc.hom_cond] * len(hom_slope)
        
        n_entries = len(var_slope) + len(hom_slope)
        
        # replicate observer label
        # data for one observer for each lum value and each experimental condition
        rep_obs = [o] * n_entries
        tmp_dict["obs"].extend(rep_obs)
        
        # insert values for variegated condition
        tmp_dict["background"].extend(rep_var)
        tmp_dict["lum"].extend(var_lum)
        tmp_dict["slope"].extend(var_slope)
        
        # insert values for homogeneous condition
        tmp_dict["background"].extend(rep_hom)
        tmp_dict["lum"].extend(hom_lum)
        tmp_dict["slope"].extend(hom_slope) 

    # convert dictionary to dataframe
    sl_df = pd.DataFrame(tmp_dict, columns = ["lum", "slope", "obs", "background"])

    # save to csv file
    # one csv file per background condition
    p_slope_csv = rc.p_csv_data + method + bgc + "_slope.csv"
    sl_df.to_csv(p_slope_csv, columns = ["lum", "slope", "obs", "background"] , sep = ',', index = False)
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    