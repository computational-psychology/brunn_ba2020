#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
FUNCTIONS WHICH ARE USED IN PROGRAMS SIMULATING MATCHING AND MLDS EXPERIMENT
WITH DIFFERENT SPACING OF DATA POINTS
Try to estimate whether perceptual scales w/ or w/o CE are always distinghuishable
"""

####################################################################################################################
"""IMPORT"""

import numpy as np 
import pandas as pd
import simu_constants as sc

####################################################################################################################
"""FUNCTIONS"""

"""
IMPLEMENT FORMULA WITH CE DEVELOPED BY WHITTLE, 1992
calculate brightness values for corresponding luminance values with CE
INPUT:
        l - list of luminance values
        bg - background luminance
RETURN:
        B - list of corresponding brightness values according to Whittle 1992
"""
def whit_w_ce(l, bg):
    ''' 
    calculate brightness for experiment with CE
    '''
    # constants described in Whittle 1992
    a_dec = -7.07
    a_inc = 8.22
    b = 6.58
    k = 0.055
    Ld = 0.39
    Lb = bg

    # separated calculations for decrements and increments as described in the text pp. 1502-1503
    dec = l[l<=Lb]
    inc = l[l>Lb]

    dL_inc = np.abs(inc - Lb)
    dL_dec = np.abs(dec - Lb)
    
    # 'Whittle contrast', different for decrements and increments
    W_inc = dL_inc / (Lb+Ld)
    W_dec = ((1.0 - k ) * dL_dec)/(dec + Ld + k*dL_dec)

    # Brightness
    B_inc = a_inc*np.log(1+b*W_inc)
    B_dec = a_dec*np.log(1+b*W_dec)
    
    # concatenating: list of brightness values corresponding to l
    B = np.concatenate((B_dec, B_inc)) 
    
    return B

##########################################################

"""
IMPLEMENT FORMULA WITHOUT CE DEVELOPED BY WHITTLE, 1992
corresponds to the best fitting power law, \
    a, b, n where determined with function fitting on Whittle's digitzed data
calculate brightness values for corresponding luminance values without CE
INPUT:
        l   - list of luminance values
        bg  - background luminance
RETURN:
        B   - list of corresponding brightness values according to Whittle 1992
"""

def whit_wo_ce(l, bg):
    a = -1.93136537
    b = 4.1591527
    n = 0.45353061

    B = a + b*(l**n)
    return B
    
##########################################################

""" 
NORMALIZE ARRAY TO A SPECIFIED RANGE
using a linear transformation a*x + b
INPUT:
    x_arr       - array of values that shall be normalized
    endrange    - specifIED range to which data shall be normalized
RETURN:
    norm_arr  - array with normalized values
"""
def normalize_to_range(x_arr, endrange = (0,1)):
    # calculate factors to normalize data
    a = (endrange[1] - endrange[0]) / (max(x_arr) - min(x_arr)) 
    b = endrange[1] - a*max(x_arr)
    # normalize x_arr
    norm_arr = a * x_arr + b
    return norm_arr

##########################################################

""" 
NORMALIZE ARRAY BY CERTAIN FACTOR
INPUT:
    arr - array of values that shall be normalized
    x   - normalization factor
RETURN:
    norm_arr - array with normalized values
"""
def normalize_by_x(arr, x):
    norm_arr = arr/x
    return norm_arr

##########################################################

"""
GET INDEX OF ENTRY IN AN ARRAY WHOSE VALUE IS CLOSEST TO K
np.argmin() returns the indices of minimum elements
INPUT:
    k   - value that will be compared to elements of the list/array
    lst - list/array to search
RETURN:
    i - index of entry in list which is closest to k
"""
def closest(k, lst):
    # calculate absolute differences between array entries and k 
    lst_diff = np.abs(lst - k)
    i = lst_diff.argmin()
    return i

##########################################################

"""
DEFINE LABEL OF LUMINANCE SPACING
INPUT:
    l - luminance spacing
RETURN:
    ln - label of spacing
"""
def lum_label(l):
    if(np.all(l == sc.lum0)):
        ln = "even"
    elif(np.all(l == sc.lum1)):
        ln = "centbg"
    elif(np.all(l == sc.lum2)):
        ln = "coarse"
    elif(np.all(l == sc.lum3)):
        ln = "coarse1"
    elif(np.all(l == sc.lum4)):
        ln = "coarse2"
    elif(np.all(l == sc.lum5)):
        ln = "coarse3"
    else:
        raise ValueError('Choose a valid luminance spacing')
    return ln


##########################################################

"""
DEFINE LABEL OF BACKGROUND LUMINANCE
INPUT:
    bg - background luminance
RETURN:
    bgn - label of bg
"""
def bg_label(bg):
    if(bg == sc.BG_GRAY):
        bgn = "gray"
    elif(bg == sc.BG_DARK):
        bgn = "dark"
    elif(bg == sc.BG_LIGHT):
        bgn = "light"
    else:
        raise ValueError('Choose a valid background condition')
    return bgn

##########################################################

"""
MERGE ALL FILES OF SIMULATED MATCHING EXPERIMENT INTO ONE FILE PER MODE & SIGMA
INPUT:
    spacings    - luminance spacings, specified in simu_constants
    method      - always matching
    mode        - asymmetric/symmetric
DEPENDS ON: sigma - specified in constants
"""
def createBigDF(spacings, method, mode):
    tmp_dict = {"tar_lum":[],
                "mat_lum":[],
                "target_bg":[],
                "match_bg":[],
                "spacing":[]}
    # for all spacings specified in spacings
    for l in spacings:
        ln = lum_label(l)
        path = sc.p_simu_data + method + "/" + mode + "/simu_" + method + "_" + mode + "_sig_" + str(sc.SIGMA_MATCH) + "_nruns_" + str(sc.N_RUNS) + "_tlum_" + ln + ".csv"
        sim_data = pd.read_csv(path, sep = ',')
        tmp_dict["tar_lum"].extend(sim_data["tar_lum"])
        tmp_dict["mat_lum"].extend(sim_data["mat_lum"])
        tmp_dict["target_bg"].extend(sim_data["bg_tar"])
        tmp_dict["match_bg"].extend(sim_data["bg_mat"])
        
        # replicate label of spacing for dataframe
        space_label = [ln]*len(sim_data["tar_lum"])
        tmp_dict["spacing"].extend(space_label)
        
    # convert dictionary to dataframe, one per spacing
    df = pd.DataFrame(tmp_dict, columns = ["tar_lum", "mat_lum", "target_bg", "match_bg", "spacing"]) 
    # save data in csv file, one file per matching background&spacing
    path = sc.p_simu_data + method + "/" + mode + "/simu_" + method + "_" + mode + "_sig_" + str(sc.SIGMA_MATCH) + "_nruns_" + str(sc.N_RUNS) + ".csv"
    df.to_csv(path, columns = ["tar_lum", "mat_lum", "target_bg", "match_bg", "spacing"] , sep = ',', index = False)
    
##########################################################

"""
CALCULATE SLOPE BETWEEN TWO DATA ARRAYS
difference(y)/difference(x)
INPUT:
    x, y - two lists/arrays between which the slope will be calculated
RETURN:
    s - calculated slope
"""
def calc_slope(x, y):
    d_x = np.diff(x)
    d_y = np.diff(y)
    s = d_y / d_x
    return s

##########################################################

"""
CALCULATE LUMINANCE VALUES AT WHICH THE SLOPE WILL BE CALCULATED
between each two data luminance values
INPUT:
    l - list of data luminance values
RETURN:
    sl - list of luminance values between each two data luminance values
"""
def cal_sl_lum(l):
    dl = np.diff(l)
    dl2 = dl/2
    sl = l[0:9] + dl2
    return sl