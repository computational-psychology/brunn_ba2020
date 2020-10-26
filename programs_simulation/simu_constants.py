#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
CONSTANTS WHICH ARE USED IN PROGRAMS SIMULATING MATCHING, MLDS AND MLCM EXPERIMENT
WITH DIFFERENT SPACING OF DATA POINTS
"""

####################################################################################################################
"""IMPORT"""

import numpy as np

##########################################################
""" PATHS """

# path to data
p_simu_data = "../data/simulation/"

# path to data of single runs in MLDS
p_simu_mlds_runs = "../data/simulation/MLDS/runs/"

# path to save plots
p_simu_plots = "../plots/simulation/"

##########################################################
""" SIMULATION PARAMETERS """

# number of different runs
# minimize effect of noise
# average over results of diff. runs
N_RUNS = 100

# number of different luminance values for targets in matching experiment
N_TARG_MATCH = 40    

# number of different luminance values in MLDS/MLCM
N_LUM_MLDS = 10
N_LUM_MLCM = 10

# specify sigma
SIGMA_MATCH = 0.08
SIGMA_MLDS = 0.1
SIGMA_MLCM = 0.1

# specify to which range values shall be normalized
NORM_RANGE = (0, 1)

# number of points used for creating linspace array 
# for creating values with Whittle's function by interpolating
N_WHIT = 100000

##########################################################
""" BACKGROUND/LUMINANCE """

# luminance of gray background
BG_GRAY = 20.56
# luminance of dark background
BG_DARK = 5
# luminance of light background
BG_LIGHT = 50
bg_simu = [BG_GRAY, BG_DARK, BG_LIGHT]

# minimal luminance value
MIN_LUM = 0    

# maximal luminance value
MAX_LUM = 65   

# different 10 luminance values -> diff. spacing for MLDS and MLCM
lum0 = np.array((0, 7.2, 14.4, 21.6, 28.8, 36.1, 43.3, 50.5, 57.7, 65)) # even
lum1 = np.array((1, 5 , 18, 19, 20, 21, 22, 25, 40, 65))                # cent bg
lum2 = np.array((0, 5, 10, 35, 40, 45, 50, 55, 60, 65))                 # coarse
lum3 = np.array((1, 5 , 10, 15, 25, 34, 40, 46, 55, 65))                # coarse1
lum4 = np.array((1, 5 , 10, 30, 40, 45, 50, 55, 60, 65))                # coarse2
lum5 = np.array((0, 5, 10, 15, 20, 35, 45, 50, 55, 65))                 # coarse3

# list of spacings for simulation
spacings = [lum0, lum1, lum2, lum3, lum4, lum5]

##########################################################
""" PLOTS """
match_palette = ["#fb6a4a", "#252525", "#74a9cf"]

### COLORS ###
# mittelblau: "#74a9cf"
# dunkleres blau: #2b8cbe
# blau3: #3182bd
# lila: #5e3c99
# orange: #e66101
# orange 2: #fe9929
# red: #e34a33
# red2. #de2d26
# red3: #fb6a4a
# sehr dunkelgrau: #252525