#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT SLOPE OF SIMULATED MLDS SCALES
individually for each spacing
"""

################################################################################################

"""IMPORT"""

import pandas as pd
from matplotlib import pyplot as plt # for plotting
import seaborn as sb # for nicer plotting
import simu_constants as sc
import simu_utils as su


################################################################################################
"""CONSTANTS"""

# plot slope for MLDS data
method = "MLDS" 

# specify background condition
bg = sc.BG_GRAY

################################################################################################
"""MAIN"""

""" plot slope in one grid for all spacings """

# general settings for plots
sb.set_style("ticks")
sb.set_palette("colorblind")
palette = sb.color_palette("colorblind")

path = sc.p_simu_data + method + "/simu_" + method + "slope.csv"
df_all = pd.read_csv(path, sep = ',')

""" 
plot slope of MLDS scales
1 plot per spacing
"""
for lum in sc.spacings:  
    # get label of luminance spacing
    ln = su.lum_label(lum)
    
    df = df_all.loc[df_all["spacing"] == ln]
    
    # add title
    plt.suptitle("Slope of simulated MLDS scales")
    
    # plot slope against luminance
    sb.lineplot( "lum", "slope",  data = df, style = "CE", hue = "CE", markers = True, dashes = False)
    
    # add vertical line at background luminance for each facet
    plt.axvline(x = bg, color = 'grey', ls = '--', label = "bg luminance")
        
    # relabel x- and y-axis
    plt.xlabel("luminance [cd/m²]")
    plt.ylabel("Slope of perc. lightness")  
    
    plt_path = sc.p_simu_plots + method + "/simu_" + method + ln + "_slope.pdf"
    plt.savefig(plt_path, bbox_inches = 'tight', pad_inches = 0.05)
    plt.close()
    
