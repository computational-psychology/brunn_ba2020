#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
SIMULATE AN ASYMMETRIC/SYMMETRIC MATCHING EXPERIMENT
WITH DIFFERENT SPACING OF DATA POINTS
Try to estimate whether the CE is always visible depite coarse spacing
TARGET: based on ground truth function with CE (e.g. presented in front of homogeneous background)
MATCH:  
    asymmetric: based on ground truth function without CE (e.g. embedded in variegated checkerboard)
    symmetric: based on ground truth function with CE (e.g. presented in front of homogeneous background)
ADJUST SIGMA IN SIMU_CONSTANTS
"""

################################################################################################
"""IMPORT"""

import simu_constants as sc
import simu_utils as su
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

################################################################################################
"""CONSTANTS"""

# asymmetric matching experiment
method = "Matching"
mode = "sym" 

# luminance range for finding matching perceived lightness calculated with 
# Whittle's function via "interpolation" btw N_WHIT data points
l_whit = np.linspace(sc.MIN_LUM, sc.MAX_LUM, sc.N_WHIT)

################################################################################################
"""MAIN"""

"""
SIMULATE MATCHING EXPERIMENT
    for every luminance spacing specified in sc.spacings
matching background & target bg are in {light, gray, dark} 
    -> one file per spacing
PROCEDURE:
get perceived lightness for target luminance with CE -> add noise
then percevied lightness for match for noisy target 
then get match luminance based on funtion without CE
"""

# run simulation for every luminance spacing specified in sc.spacings
for l_target in sc.spacings:
    
    # get label of target luminance
    tar_label = su.lum_label(l_target)
    n_lt = len(l_target)
    
    # initialize dictionary to save values of different runs per spacing
    tmp_dict = {"tar_lum": [],
                "mat_lum": [],
                "bg_tar": [],
                "bg_mat": []}
    
    # normally distributed noise: N_RUNS entries btw 0 and SIGMA
    e = np.random.normal(0, sc.SIGMA_MATCH, sc.N_RUNS)

    for bg_mat in sc.bg_simu:
        # get label of match background
        bgm = su.bg_label(bg_mat)    
        # target bg varies, match bg equals bg_mat
        for bg_tar in sc.bg_simu:
            # get label of target background
            bgt = su.bg_label(bg_tar)
            
            # calculate perceived lightness for target luminance with CE
            psi_tar = su.whit_w_ce(l_target, bg_tar)
            psi_tar = su.normalize_to_range(psi_tar, (0,1))
        
            # calculate perceived lightness range for matching luminance without CE
            # calculate for sc.N_WHIT luminance values in l_whit 
            if(mode == "asym"):
                psi_match = su.whit_wo_ce(l_whit, bg_mat)
            elif(mode == "sym"):
                psi_match = su.whit_w_ce(l_whit, bg_mat)
            else:
                raise ValueError("Choose valid mode")
            psi_match = su.normalize_to_range(psi_match, (0,1))
            
            # array for luminance values in different runs
            l_match = np.empty((n_lt, sc.N_RUNS))
        
            """
             get match luminance for each entry of psi_tar
                 - add noise to target luminance
                 - look for the closest value in psi_match 
                 - get the index and then get the coresponding lum value from l_whit
             simulate several times (sc.N_RUNS)
            """
            for j in range(0, sc.N_RUNS):
                for i in range(0, n_lt):
                    # get psi value of target
                    p = psi_tar[i]
                    # add random noise
                    p_err = p + e[j]
                    # get index of closest psi value of matching field
                    idx = su.closest(p_err, psi_match)
                    # get luminance value of match
                    lm = l_whit[idx]
                    # save in array
                    l_match[i, j] = lm
                    
            # replicate elements in lum sc.N_RUNS times for dictionary
            ext_l_target = [ele for ele in l_target for i in range(sc.N_RUNS)]
            tmp_dict["tar_lum"].extend(ext_l_target)
        
            # save matching data of different runs for each target lum value
            ext_l_match = []
            for i in range(n_lt):
                ext_l_match.extend(l_match[i,:])
            tmp_dict["mat_lum"].extend(ext_l_match)        
            
            # replicate and save label of target's background
            ext_t_bg = [bgt] * sc.N_RUNS * n_lt
            tmp_dict["bg_tar"].extend(ext_t_bg)
          
        # replicate and save label of match's background
        ext_m_bg = [bgm] * sc.N_RUNS * n_lt * len(sc.bg_simu)
        tmp_dict["bg_mat"].extend(ext_m_bg)
        
    # convert dictionary to dataframe, one per spacing
    df = pd.DataFrame(tmp_dict, columns = ["tar_lum", "mat_lum", "bg_tar", "bg_mat"])  
    
    # save data in csv file, one file per matching background&spacing
    path = sc.p_simu_data + method + "/" + mode + "/simu_" + method + "_" + mode + "_sig_" + str(sc.SIGMA_MATCH) + "_nruns_" + str(sc.N_RUNS) + "_tlum_" + tar_label+ ".csv"
    df.to_csv(path, columns = ["tar_lum", "mat_lum", "bg_tar", "bg_mat"] , sep = ',', index = False)

# merge data of simulations with different spacings into one big csv file
su.createBigDF(sc.spacings, method, mode)