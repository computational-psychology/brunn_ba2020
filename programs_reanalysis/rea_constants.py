#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
CONSTANTS WHICH ARE USED IN PROGRAMS REANALYZING EXPERIMENTAL DATA OF AGUILAR & MAERTENS 2020
RE-PLOT DATA AND ANALYZE SLOPE OF THE DATA
"""
####################################################################################################################
"""IMPORT"""

import pandas as pd

##########################################################
""" PATHS """

# location of experimental data
# mlds/mlcm data
p_exp_mldscm = "../data/exp_aguilar2020/mlds_cm/"
# matching data
p_exp_match = "../data/exp_aguilar2020/Matching/"

# path to save RDS data
p_rds_data = "../data/reanalysis/rds_data/"

# path to save csv data
p_csv_data = "../data/reanalysis/csv_data/"

# folder where to save plots
p_rea_plots = "../plots/reanalysis/"
p_rea_data_plots = p_rea_plots + "data/"
p_rea_slope_plots = p_rea_plots + "slope/"

# filename extension for MLDS data
fn_ext_mlds = "indexed.fr.glm.MLDS"
fn_ext_mlcm = "indexed.fr.glm.MLCM"


# lookup table to convert match lum [0, 1] to "normal lum range
p_lut = "../data/reanalysis/lut.csv"
lut = pd.read_csv(p_lut, sep = ' ')

##########################################################
""" EXPERIMENTAL CONDITONS """

# number of experimental conditions: variegated/homogeneous
n_exp_cond = 2 
# extensions for varigeated and homogeneous condition
var_cond = "variegated"
hom_cond = "homogeneous"
  
##########################################################
""" OBSERVERS """  

# list with observer "names"
obs = ['sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'test']
# define order of observers in plots:
    # obs 1-8: obs_order = ["sub6", "sub1" ,"test", "sub2", "sub7", "sub4", "sub3", "sub5"] #observer 1 to 8
    # obs ordered based on strength of CE, decreasing:
obs_order = ["sub4", "sub6", "sub2", "sub1", "sub7", "sub3", "test", "sub5"] 

# amount of observers
n_obs = len(obs)

# mapping between observer filenames and labels used in the paper
obs_label_map = pd.DataFrame( data = {"obs": ['sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'test'],
                                     "label": ["O2/MM", "O4/MK", "O7", "O6", "O8", "O1", "O5", "O3/GA"]})
obs_label_map = obs_label_map.set_index("obs", drop = True)

##########################################################
""" BACKGROUND/LUMINANCE """

# list with different experimental contexts
bg_cond = ['plain', 'dark', 'light']

# dictionary for different background luminances in different experimental contexts (MLDS & MATCHING)
bg_lum = {"dark": [80.91], "plain": [173.74], "light": [132.3]}

# dataframe with luminance values used in MLDS in different experimental contexts
lum_mlds = pd.DataFrame( data = {"plain": [25, 40, 60, 89, 120, 155, 199, 242, 281, 312], 
                            "light": [73, 79, 87, 99, 111, 125, 144, 159, 176, 188],
                            "dark": [22, 28, 36, 48, 60, 74, 92, 108, 125, 137]})

# dataframe to map between reflectance and luminance values in MATCHING (for target match)
lr_map = pd.DataFrame(data = {'r':[0.06, 0.11, 0.19, 0.31, 0.46, 0.63, 0.82, 1.05, 1.29, 1.50, 1.67, 1.95, 2.22],
    'plain': [15, 25, 40, 60, 89, 120, 155, 199, 242, 281, 312, 365, 415],
    'dark': [18, 22, 28, 36, 48, 60, 74, 92, 108, 125, 137, 157, 177],
    'light': [69, 73, 79, 87, 99, 111, 125, 144, 159, 176, 188, 209, 229]})
lr_map = lr_map.set_index("r", drop = True)
