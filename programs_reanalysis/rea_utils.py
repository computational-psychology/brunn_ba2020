#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
FUNCTIONS WHICH ARE USED IN PROGRAMS REANALYSING MATCHING AND MLDS DATA OF AGUILAR & MAERTENS 2020
RE-PLOT DATA AND ANALYZE SLOPE OF THE DATA
"""

####################################################################################################################
"""IMPORT"""

import numpy as np
import pandas as pd
import rea_constants as rc

####################################################################################################################
"""FUNCTIONS"""

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

##########################################################

"""
AVERAGE DATA OF MULTIPLE Y VALUES FOR ONE X VALUE
used e.g. for matching data before calculating the slope
get unique values for target luminance
calculate average of all y values for the unique x values
INPUT:
    df - dataframe with column with x values and column with multiple y values for one x
    xl - label of column with x values
    yl - label of column with y values
RETURN:
    x_uni - vector with unique values of x
    y_avg - vector with average values of y per x
"""
def avg_data(df, xl, yl):
    x_uni = np.sort(df[xl].unique())
    y_avg = []
    for i in x_uni:
        # extract all values for one particular x
        tmp = df.loc[df[xl] == i]
        # average over values
        tmp_y = np.mean(tmp[yl])
        y_avg.append(tmp_y)
    return(x_uni, y_avg)
        

####################################################################################################################
### FUNCTIONS USED ONLY FOR MATCHING ###

"""
LUMINANCE CONVERSION BASED ON LUT.CSV
convert the luminance valueS in range [0:1] to 'normal' luminance based on lut.csv 
INPUT: 
    ml  - list of luminance values in [0, 1] (e.g. match luminance)
RETURN:
    lum - list of luminance values in [0, 255]
"""
def conv_lut(ml):
    l = rc.lut.loc[:, ["IntensityIn", "Luminance"]]
    # initialize list to save luminance values
    lum = []
    # assign a lum value from lut to each entry of ml
    for i in range(0, len(ml)):
        tmp = ml.iloc[i]
        x = closest(tmp, l.loc[:, "IntensityIn"])   # get index of closest value in lut table 
        m = float(rc.lut.loc[x, "Luminance"])       # take the closest value in the lut as luminance value
        lum.append(m)
    return(lum)

##########################################################

"""
MAP REFLECTANCE VALUES TO LUMINANCE VALUES
map the unique r values to corresponding luminance values
INPUT:
    r_list  - list with unique reflectance values
    c       - background condition (plain, light, dark)
RETURN:
    lum     - list of luminance values (one per reflectance value)
"""
def map_rl(r_list, c):
    # list to save luminance values
    lum = []
    
    # assign a luminance value to each reflectance value
    for r in r_list:
        l = rc.lr_map.loc[r, c]
        lum.append(l)
    return lum


    
    