#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT SLOPE OF EXPERIMENTAL DATA OF AGUILAR & MAERTENS 2020 INDIVIDUALLY PER OBSERVER
plot  slope of variegated condition and homogeneous condition in one plot
"""

####################################################################################################################

"""IMPORT"""
import pandas as pd
from matplotlib import pyplot as plt # for plotting
import seaborn as sb # for nicer plotting
import rea_constants as rc
import rea_utils as ru

####################################################################################################################
"""CONSTANTS"""

# specify whether MLDS or MLCM or Matching slope shall be plotted
method = "MLDS" # "MLDS"/"MLCM"/"Matching"

####################################################################################################################
"""MAIN"""

""" plot slope for each observer individually"""

# general settings for plots
sb.set_style("ticks")
sb.set_palette("colorblind")
palette = sb.color_palette("colorblind")

# plot experimental data for all observers separately
for bgc in rc.bg_cond:
    # luminance value of background
    bg = rc.bg_lum[bgc]
    
    # load csv file for bgc background condition
    p_csv_file = rc.p_csv_data + method + bgc + "_slope.csv"
    df = pd.read_csv(p_csv_file, sep = ',')
    
    # plot individual data for each observer
    for o in rc.obs:
        # extract observer-specific data from dataframe
        df_obs = df.loc[df["obs"] == o]
        
        # observer label as in Aguilar2020
        ol = rc.obs_label_map.loc[o, "label"]
        # add title to figure
        plt.title("Slope of " + method + " data\n" + ol + ", condition: "+ bgc)
        
        # add vertical line at background luminance
        plt.axvline(x = bg, color = 'grey', ls = '--', label = "bg luminance")

        # plot slope 
        sb.lineplot( x = "lum", y = "slope", style = "background", hue = "background",  data = df_obs,  markers = True, dashes = False)
        
        # re-label x- and y-axis
        plt.xlabel("luminance [cd/m²]")
        if(method == "Matching"):
            plt.ylabel("slope of match luminance")  
        elif((method == "MLDS") or (method == "MLCM")):
            plt.ylabel("slope of perc. lightness")
            
        # define location of legend
        plt.legend(loc = "upper right", frameon = False)
        
        # save plot as pdf, one plot per observer/background condition
        plt_name = rc.p_rea_slope_plots + method + '/' + method + '_' + o + '_' + bgc + "_slope.pdf"
        plt.savefig(plt_name, bbox_inches = 'tight', pad_inches = 0.05)
        plt.close()
        
        
        