#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
SIMULATE DATA OF AN MLDS EXPERIMENT WITH DIFFERENT SPACING OF DATA POINTS
Try to estimate whether perceptual scales w/ or w/o CE are always distinghuishable
estimate one scale based once on ground truth function with CE and once without CE
"""

####################################################################################################################
""" IMPORT """

import simu_constants as sc
import simu_utils as su
import itertools
import numpy as np
import pandas as pd
import subprocess as sp
import pyreadr as pr

####################################################################################################################
""" CONSTANTS """

method = "MLDS"

# specify background condition
bg = sc.BG_GRAY

####################################################################################################################
""" FUNCTIONS """

"""
CALCULATE MLDS DECISION VARIABLE
1. calculate psi for corresponding luminance values with or without CE
2. compute decision variable: 
        if x1 & x2 ar emore similar: resp = 0
        else if x2 & x3 are more similar: resp = 0
INPUT:
        lt  - list of luminance trials
        pf  - function that shall be used for psi calculation with/without CE
        e   - random normally distributed noise
        bg  - background luminance
RETURN:
        rsp - list with luminance trials and corresponding responses
"""
def calc_resp(lt, pf, e, bg):
    # calculate normalization factor to normalize psi values to NORM_RANGE
    nf = calc_norm_factor(bg)
    rsp = []
    for i in range(0, len(lt)):
        l = lt[i]
        
        # calculate psi value for correspondig l
        psi = pf(np.asarray(l), bg)
        
        # normalize psi value
        p = nf[0]*psi + nf[1]
        
        # compute decision variable to decide which of the two pairs is more similar
        d = (p[2] - p[1]) - (p[1] - p[0])
        # add noise
        d_err = d + e[i]
        if d_err < 0 :
            r = 0
        else:
            r = 1
        # save resp and corresponding trial
        rsp.append((r, l[0], l[1], l[2]))
    return rsp

"""
CALCULATE THE NORM_FACTOR by which the psi values have to be normalized 
in order to be in NORM_RANGE and comparable
INPUT:
    bg - background luminance
RETURN:
    norm_factor - list with factors a and b to normalize values
"""
def calc_norm_factor(bg):
    # psi value of max lum
    p_max = psif(np.array(sc.MAX_LUM), bg)
    # psi value of min lum
    p_min = psif(np.array(sc.MIN_LUM), bg)
    
    # normalize to a desired range using a linear transformation
    a = (sc.NORM_RANGE[1] - sc.NORM_RANGE[0]) / (p_max - p_min) 
    b = sc.NORM_RANGE[1] - a * p_max
    norm_factor = [a, b]
    return norm_factor

    
####################################################################################################################
""" MAIN """

"""
SIMULATE MLDS EXPERIMENT FOR DIFFERENT LUMINANCE SPACINGS
"""

# simulate for every luminance spacing specified in simu_constants
for lum in sc.spacings: 
    
    # create all possible combinations/trials for l1, l2, l3
    lum_trials = [x for x in itertools.combinations(lum, 3)]
    lum_trials = lum_trials *10
    n_lt = len(lum_trials)  # number of trials
    
    # get label of luminance spacing
    ln = su.lum_label(lum)
    
    # initialize dictionary
    ps_dict = {"lum": [],
                "pscale": [],
                "CE": []}

    # simulate once with and once without CE
    for CRISP in [True, False]:
        ce = "ce" if CRISP else "noce"
        ce_label = "yes" if CRISP else "no"
        
        # list to save response values of differnt runs
        l_ps_runs = np.empty((sc.N_LUM_MLDS, sc.N_RUNS))
        
        # simulate responses for sc.N_RUNS runs
        for run in range(0, sc.N_RUNS):
            print(run)
            # normally distributed noise: len(lum_trials) entries btw 0 and SIGMA
            e = np.random.normal(0, sc.SIGMA_MLDS, len(lum_trials))
            
            # specify whether to use an internal function with or without crispening for the simulation
            if(CRISP):
                psif = su.whit_w_ce
            else:
                psif = su.whit_wo_ce
            
            # calculate psi for lum_trials and simulate decision responses based on these psi values
            resp = calc_resp(lum_trials, psif, e, bg)
            df_resp = pd.DataFrame(resp, columns = ['resp', 'S1', 'S2', 'S3' ])
            
            # save this file and pass it to R-function MLDS
            path = sc.p_simu_mlds_runs + "/sim_data_" +ln +'_' + str(run) + ce
            df_resp.to_csv((path + ".csv"), index = False)
            
            """ 
            call R functions with subprocess from here:
                estimate the scale using MLDS
                max value is fixed to 1/noise
                min vlaue is fixed to 0
            """
            cmd = ["Rscript", "simu_mlds_boot.r", path]
            test = sp.check_output(cmd, universal_newlines = True)
            # random control number 3 is returned by R script
            if(test == "3"):                
                path = sc.p_simu_mlds_runs + "/sim_data_" +ln +'_' + str(run) + ce + "mlds.csv"
                df = pd.read_csv(path, sep = ',')
            else:
                raise ValueError('mlds pscale could not be calculated')
              
            # normalize pscale
            nx = df["pscale"][len(df["pscale"])-1]
            df["pscale"] = su.normalize_by_x(df["pscale"], nx)
            
            # save pscale for each run
            l_ps_runs[:,run] = df['pscale']
        
        # save data for further processing/plotting
        # replicate luminance label sc.N_RUNS times
        ext_lum = [ele for ele in lum for i in range(sc.N_RUNS)]
        ps_dict["lum"].extend(ext_lum)
        
        # save pscale of different runs for each lum value
        l_ps = []
        for i in range(sc.N_LUM_MLDS):
            l_ps.extend(l_ps_runs[i,:])
        ps_dict["pscale"].extend(l_ps)   
        
        # replicate CE label
        ext_cond = [ce_label] * sc.N_RUNS * len(lum)
        ps_dict["CE"].extend(ext_cond)
    
    # create dataframe and save as csv
    df_pscale = pd.DataFrame(ps_dict, columns = ["lum", "pscale", "CE"]) 
    df_path = sc.p_simu_data + method + "/simu_" + method + "_sig_" + str(sc.SIGMA_MLDS) + "_nruns_" + str(sc.N_RUNS) + "_lum_" + ln + ".csv"
    df_pscale.to_csv(df_path , sep = ',', index = False)
            
            