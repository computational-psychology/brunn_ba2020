#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
CALCULATE SLOPE OF SIMULATED MLDS SCALES
calculate slope between each two data points
x data points result in x-1 slope values
"""

####################################################################################################################
"""IMPORT"""

import numpy as np
import pandas as pd
import simu_constants as sc
import simu_utils as su

####################################################################################################################
"""CONSTANTS"""

# specify for which method the slope shall be calculated
method = "MLDS" # "MLDS"/"MLCM"/"Matching"

if(method == "MLDS"):
    x_label = "lum"
    y_label = "pscale"
else:
    raise ValueError ("Choose valid experimental method")

####################################################################################################################
""" FUNCTIONS """

"""
AVERAGE OVER ALL PSCALE VALUES FOR ONE LUM VALUE
get all pscale values for one luminance value
-> average
"""
def get_ps_per_lum(df, l):
    ps = []
    for i in l:
        tmp_ps = df.loc[df["lum"] == i]
        tmp_ps.reset_index(drop = True)
        x = np.mean(tmp_ps["pscale"])
        ps.append(x)
    return(ps)  
        
####################################################################################################################
"""MAIN"""

# initialize temporary dictionary for slope data
tmp_dict = {"lum": [],
            "slope": [], 
            "CE": [],
            "spacing": []}
    
""" calculate slope for each spacing"""
for lum in sc.spacings: 
    # label for particular spacing
    ln = su.lum_label(lum)
    path = sc.p_simu_data + method + "/simu_" + method + "_sig_" + str(sc.SIGMA_MLDS) + "_nruns_" + str(sc.N_RUNS) + "_lum_" + ln + ".csv"
  
    df = pd.read_csv(path, sep = ',')
    df_ce = df[df["CE"] == "yes"]
    df_noce = df[df["CE"] == "no"]
    
    # extract luminance values of spacing
    x_lum = np.unique(df[x_label])
    
    y_ps_ce = get_ps_per_lum(df_ce, x_lum)
    y_ps_noce = get_ps_per_lum(df_noce, x_lum)
    
    sl_lum = su.cal_sl_lum(x_lum)
    slope_ce = su.calc_slope(x_lum, y_ps_ce)
    slope_noce = su.calc_slope(x_lum, y_ps_noce)
            
    # replicate label of spacing for dataframe
    space_label = [ln]*len(sl_lum)*2
    
    # insert data in dictionary
    tmp_dict["lum"].extend(np.tile(sl_lum, 2))
    tmp_dict["slope"].extend(slope_ce)
    tmp_dict["CE"].extend(["yes"]*len(slope_ce))
    tmp_dict["slope"].extend(slope_noce)
    tmp_dict["CE"].extend(["no"]*len(slope_noce))
    tmp_dict["spacing"].extend(space_label)
    
# convert dictionary to dataframe
sl_df = pd.DataFrame(tmp_dict, columns = ["lum", "slope", "CE", "spacing"])
# save as csv file 
sl_path = sc.p_simu_data + method + "/simu_" + method + "slope.csv"
sl_df.to_csv(sl_path, sep = ',', index = False)