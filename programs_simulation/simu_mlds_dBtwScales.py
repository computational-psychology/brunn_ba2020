#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
CALCULATE DISTANCE BETWEEN MLDS SCALES TO ANALYZE DISCRIMINABILITY
COUNT IN HOW MANY RUNS THE DISTANE IS BELOW THE REFERENCE VALUE
Try to estimate whether the scales always differ when they are based on different ground truth functions
one scale based on ground truth with CE and one without CE
"""

################################################################################################
"""IMPORT"""

import simu_constants as sc
import simu_utils as su
import numpy as np
import pandas as pd

################################################################################################
"""CONSTANTS"""

# calculate distance between simulated MLDS scales
method = "MLDS"

# gray background condition
bg = sc.BG_GRAY

# reference value: \
    # avg distance of scales of evenly spaced luminance values
ref_avg = 0.5382159924540952

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
def calc_sum_dist(run):
    #path_ce = sc.p_simu_data + method + "/runs/sim_data_" +ln +'_' + str(run) + "cemlds.csv"
    path_ce = sc.p_simu_mlds_runs + "sim_data_" +ln +'_' + str(run) + "cemlds.csv"
    df_ce = pd.read_csv(path_ce, sep = ",")
    df_ce = df_ce.reset_index(drop = True)
    ps_ce = df_ce["pscale"]
    ps_ce = su.normalize_by_x(ps_ce, ps_ce.iloc[9])
    
    #path_noce = sc.p_simu_data + method + "/runs/sim_data_" +ln +'_' + str(run) + "nocemlds.csv"
    path_noce = sc.p_simu_mlds_runs + "sim_data_" +ln +'_' + str(run) + "nocemlds.csv"
    df_noce = pd.read_csv(path_noce, sep = ",")
    df_noce = df_noce.reset_index(drop = True)
    ps_noce = df_noce["pscale"]
    ps_noce = su.normalize_by_x(ps_noce, ps_noce.iloc[9])
    
    # calculate distance between scales
    d_ps = np.abs(ps_ce - ps_noce)

    # sum up all distance values
    sum_d = np.sum(d_ps)
    
    return(sum_d)
    
################################################################################################
"""MAIN"""

# list to save count below reference value
l_d =[]
    
# initialize dictionary to save distance values for all runs
tmp_dict = {}

# calculate distance of scales for every luminance spacing in sc.spacings
for lum in sc.spacings:    
    # get label of luminance spacing
    ln = su.lum_label(lum)
    colname = ln + "_dist"
    
    # list to save distance per run
    dist = []
    
    # calcualate summed distance for each run
    for i in range(0, sc.N_RUNS):
        # calculate summed distance
        x = calc_sum_dist(i)
        # save value per run
        dist.append(x)
        
    # save values of all runs in dictionary
    tmp_dict[colname] = dist
    
    # calculate average across all runs for this spacing
    avg = np.mean(dist)
    tmp_dict[colname].append(avg)
    
    # count in how many runs the distance was below the reference
    cnt = sum(map(lambda y: y < ref_avg, dist))
    print(cnt, " values are below the avg references for the", ln, " spacing. the avg of ", ln, " is ", avg)
    l_d.append([ln, avg, cnt])

# save distance & average for all runs
# one column per spacing
df_dist = pd.DataFrame(data = tmp_dict, columns = tmp_dict.keys())
df_dist.to_csv((sc.p_simu_data + method + "/simu_mlds_distBtwScales.csv"), sep = ",")

# save count below reference 
df_sum = pd.DataFrame(l_d, columns = ["spacing", "average", "cntBelowReference"])
df_sum.to_csv((sc.p_simu_data + method + "/simu_mlds_cntBelowAvg.csv"), sep = ",")
    
        
        