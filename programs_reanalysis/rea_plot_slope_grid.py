#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT SLOPE OF EXPERIMENTAL DATA OF AGUILAR & MAERTENS 2020
one facetgrid per backgorund condition
"""

################################################################################################

"""IMPORT"""

import pandas as pd
from matplotlib import pyplot as plt # for plotting
import seaborn as sb # for nicer plotting
import rea_constants as rc
import rea_utils as ru


################################################################################################
"""CONSTANTS"""

# specify whether MLDS or MLCM or Matching slope shall be plotted
method = "Matching" # "MLDS"/"MLCM"/"Matching"

# specify how many columns the grid shall have
# recommended: 2-4
n_col = 3

################################################################################################
"""MAIN"""

""" plot slope in one grid per bg condition (plain, light, dark) """

# general settings for plots
sb.set_style("ticks")
sb.set_palette("colorblind")
palette = sb.color_palette("colorblind")

# create one plot grid per background condition
for bgc in rc.bg_cond:
    # luminance value of background
    bg = rc.bg_lum[bgc]
    
    # get observer label like in Aguilar2020
    ol_list = []
    for o in rc.obs_order:
        ol = rc.obs_label_map.loc[o, "label"]
        ol_list.append(ol)
    
    # load csv file for bgc background condition
    p_csv_file = rc.p_csv_data + method + bgc + "_slope.csv"
    df = pd.read_csv(p_csv_file, sep = ',')
    
    # initialize grid
    g = sb.FacetGrid(df, col = "obs", col_wrap = n_col, col_order = rc.obs_order, margin_titles = True)
    axes = g.fig.axes
    
    # add title depending on background condition
    if(bgc == "plain"):
        g.fig.suptitle("Slope of " + method + " data\n" + "transparency: none")
    else:
        g.fig.suptitle("Slope of " + method + " data\n" +"transparency: "+ bgc)
       
    # plot slope against luminance
    g.map(sb.lineplot, "lum", "slope", style = "background", hue = "background",  data = df,  markers = True, dashes = False)
    
    # add vertical line at background luminance for each facet
    for i in range(0, len(rc.obs)):
        axes[i].axvline(x = bg, color = 'grey', ls = '--', label = "bg luminance")
        # set observer name as in Aguilar2020 
        axes[i].set_title(ol_list[i])

    # add legend
    if(n_col%2 != 0):
        # add legend in the empty facet at the lower right
        axes[(rc.n_obs-1)].legend(bbox_to_anchor = (1.9, 0.2), loc = "lower right", frameon = False)
    else:
        g.add_legend()
    
    # re-label x- and y-axis
    if(method == "Matching"):
        g.set_axis_labels("luminance [cd/m²]", "Slope of match luminance")  
    elif((method == "MLDS") or (method == "MLCM")):
        g.set_axis_labels("luminance [cd/m²]", "Slope of perc. lightness")  
    
    # save plot as pdf, one pdf per background condition
    plt_name = rc.p_rea_slope_plots + method + '/grid/' + method + '_' + bgc + ".pdf"
    plt.savefig(plt_name, bbox_inches = 'tight', pad_inches = 0.05)
    plt.close()
     

        
        
        