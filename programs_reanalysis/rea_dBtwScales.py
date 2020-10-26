#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
CALCULATE DISTANCE BETWEEN MLDS SCALES OF AGUILAR2020
Try to estimate whether the scales always differ when they are based on different ground truth functions
one scale based on ground truth with CE and one without CE
"""

################################################################################################
"""IMPORT"""

import rea_constants as rc
import rea_utils as ru
import numpy as np
import pandas as pd

################################################################################################
"""CONSTANTS"""

# specify whether the distance shall be calculated for scales obained with MLDS or MLCM
method = "MLDS" # "MLDS"/"MLCM"

################################################################################################
"""FUNCTIONS"""

"""
CALCULATE SUMMED DISTANCE OF TWO SCALES IN PARTICULAR RUN
load saved simulation data for experiment based on ground truth with/without CE
calculate distance between each two data points
sum up distance
INPUT:
    run     - particular run to calculate distance
RETURN:
    sum_d   - summed distance between scales of run
"""
def calc_sum_dist(df):
    
    # split dataframe into two dataframes for variegated 
    df_o_var = df.loc[df_o["background"] == "variegated"]
    df_o_hom = df.loc[df_o["background"] == "homogeneous"]
    df_o_var = df_o_var.reset_index(drop = True)
    df_o_hom = df_o_hom.reset_index(drop = True)
    ps_var = df_o_var["pscale"]
    ps_hom = df_o_hom["pscale"]
    
    # calculate distance between scales
    d_ps = np.abs(ps_var - ps_hom)

    # sum up all distance values
    sum_d = np.sum(d_ps)
    
    return(sum_d)
    
################################################################################################
"""MAIN"""

# initialize dictionary to save distance values for all runs
tmp_dict = {"background":[], 
            "O1_dist": [],
            "O2/MM_dist": [],
            "O3/GA_dist": [],
            "O4/MK_dist": [],
            "O5_dist": [],
            "O6_dist": [],
            "O7_dist": [],
            "O8_dist": []
            }

# create one plot grid per background condition
for bgc in rc.bg_cond:
    tmp_dict["background"].append(bgc)
    
    # load csv file 
    csv_file = rc.p_csv_data + method + bgc + ".csv"
    df = pd.read_csv(csv_file, sep = ",")
    
    # calculate distance of scales for every luminance spacing in sc.spacings
    for o in rc.obs:
        # observer label used in the paper
        ol = rc.obs_label_map.loc[o, "label"]
        colname = ol + "_dist"
        
        # extract information for particular observer
        df_o = df.loc[df["obs"] == o]
        df_o = df_o.reset_index(drop = True)
    
        # calculate summed distance
        x = calc_sum_dist(df_o)
                  
        # save values of all runs in dictionary
        tmp_dict[colname].append(x)
        
# save summed distance for each backgroundconditin per observer
# one column per spacing
df_dist = pd.DataFrame(data = tmp_dict, columns = tmp_dict.keys())
df_dist.to_csv((rc.p_csv_data + method + "_distBtwScales.csv"), sep = ",")


        
        