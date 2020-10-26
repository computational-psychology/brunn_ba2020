#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
CALCULATE DISTANCE BETWEEN MLDS SCALES AND CORRESPONDING GROUND TRUTH SCALES
calculate distance between a simulated MLDS scale and the ground truth function it was based on (w/ or w/o CE)
no interpolation -> calculation only between perceptual scale values and ground truth values at the respective point
sum up all distance values for one spacing and CE condition (2 sums per spacing)
save data in 2 csv files:
    1: all distance values between the scale values and ground truth for each spacing
    2: summed distance ( w/ & w/o CE ) for each spacing
"""

################################################################################################
"""IMPORT"""

import pandas as pd
import numpy as np
import simu_constants as sc 
import simu_utils as su
from matplotlib import pyplot as plt

################################################################################################
"""CONSTANTS"""

# calculate distance of simulated MLDS scales to ground truth functions
method = "MLDS"

# gray background condition
bg = sc.BG_GRAY

# dictionaries to save distance results
dist_dict = {"spacing":[],
            "lum": [],
            "dist": [],
            "CE": []}
sum_dict = {"spacing": [],
           "sum_ce": [],
           "sum_noce": []}

################################################################################################
"""MAIN"""

""" 
calculate values for ground truth functions
"""
l_whit = np.linspace(sc.MIN_LUM, sc.MAX_LUM, sc.N_WHIT)

# ground truth function with CE
f = su.whit_w_ce(l_whit, bg)
ps_whit_ce = su.normalize_to_range(f, (0,1))

# ground truth function without CE
f = su.whit_wo_ce(l_whit, bg)
ps_whit_noce = su.normalize_to_range(f, (0,1))
    
"""
calculate distance to ground truth for every luminance spacing in sc.spacings
"""
for lum in sc.spacings:    
    # get label of luminance spacing
    ln = su.lum_label(lum)

    # load data for particular spacing
    path = sc.p_simu_data + method + "/simu_" + method + "_sig_" + str(sc.SIGMA_MLDS) + "_nruns_" + str(sc.N_RUNS) + "_lum_" + ln + ".csv"
    sim_data = pd.read_csv(path, sep = ',')
    
    # get uniue luminance values in the simulated data \
        # should be close to luminance values of spacing
    uni_lum = np.unique(sim_data["lum"])
    
    # initialize lists to save calculated distance per value
    d_ce = []
    d_noce = []
    for i in uni_lum:
        # extract psi values for particular luminance value
        df = sim_data.loc[sim_data["lum"] == i]
        #df = df.reset_index(drop = True)
        
        # split dataframe: 1 for values based on function with CE and 1 without
        df_ce = df.loc[df["CE"] == "yes"]
        df_ce = df_ce.reset_index(drop = True)
        df_noce = df.loc[df["CE"] == "no"]
        df_noce = df_noce.reset_index(drop = True)
        
        # calculate average psi value for particular lum value (w/ & w/o CE)
        ps_ce = np.mean(df_ce["pscale"])
        ps_noce = np.mean(df_noce["pscale"])

        # get index of luminance value in l_whit closest to i
        idx = su.closest(i, l_whit)
        
        # calculate distance between ps value of simulated scale and ground truth function
        x = np.abs(ps_ce - ps_whit_ce[idx])
        y = np.abs(ps_noce - ps_whit_noce[idx])
        d_ce.append(x)
        d_noce.append(y)
    
    # calculate summed distance for all lum values in the particular spacing
    sum_ce = np.sum(d_ce)
    sum_noce = np.sum(d_noce)
    
    # replicate data to save in one labeled dataframe
    dist = []
    dist.extend(d_ce)
    dist.extend(d_noce)
    ce = ["yes"]*10 + ["no"]*10
    rep_ln = [ln] * len(lum) * 2
    rep_lum = list(lum) * 2
    
    # save all distance values of the particular spacing in one dictionary
    dist_dict["spacing"].extend(rep_ln)
    dist_dict["lum"].extend(rep_lum)
    dist_dict["dist"].extend(dist)
    dist_dict["CE"].extend(ce)

    # saved summed distance in second dictionary
    sum_dict["spacing"].append(ln)
    sum_dict["sum_ce"].append(sum_ce)
    sum_dict["sum_noce"].append(sum_noce)

"""
convert dictionaries to dataframes
save df as csv file
one file with data for all different spacings
"""
df_dist = pd.DataFrame(data = dist_dict, columns = ["spacing", "lum", "dist", "CE"])
p_df_dist = sc.p_simu_data + method + "/simu_d2truth_" + method + "_sig_" + str(sc.SIGMA_MLDS) + "_nruns_" + str(sc.N_RUNS) + ".csv" #+ '_' + ln + '_' + ".csv"
df_dist.to_csv(p_df_dist , sep = ',', index = False)

df_sum = pd.DataFrame(data = sum_dict, columns = ["spacing", "sum_ce", "sum_noce"])
p_df_sum = sc.p_simu_data + method + "/simu_sumd2truth_" + method + "_sig_" + str(sc.SIGMA_MLDS) + "_nruns_" + str(sc.N_RUNS) + ".csv"#+ '_' + ln + '_' + ".csv"
df_sum.to_csv(p_df_sum, sep = ',')