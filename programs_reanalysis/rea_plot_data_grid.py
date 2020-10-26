#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT EXPERIMENTAL DATA OF AGUILAR & MAERTENS 2020 IN GRID
ONE GRID PER BACKGROUND CONDITION (FOR ALL OBSERVERS)
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

# specify whether MLDS or MLCM or Matching data shall be plotted
method = "Matching" # "MLDS"/"MLCM"/"Matching"

# specify how many columns the grid shall have
# recommended: 2-4
n_col = 3

####################################################################################################################
"""MAIN"""

""" plot data in one grid per bg condition (plain, light, dark) """

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
    csv_file = method + bgc + ".csv"
    df = pd.read_csv((rc.p_csv_data + csv_file), sep = ',')

    # initialize grid
    g = sb.FacetGrid(df, col = "obs", col_order = rc.obs_order, col_wrap = n_col, margin_titles = True)
    axes = g.fig.axes
    
    # add title depending on background condition
    if(bgc == "plain"):
        g.fig.suptitle(method + " experiment data\n" + "transparency: none")
    else:
        g.fig.suptitle(method + " experiment data\n" + "transparency: "+ bgc)
    
    # plot data for the respective method    
    if(method == "Matching"):
        # plot matching data with standard deviation
        g.map(sb.lineplot, "tar_lum", "mat_lum", style = "background", hue = "background",  data = df,  markers = True, dashes = False, ci = "sd", err_style = "bars")
        # re-label y and y axis
        g.set_axis_labels("target luminance [cd/m²]", "match luminance [cd/m²]")
        
    elif((method == "MLDS") or (method == "MLCM")):
        # plot MLDS/MLCM data
        g.map(sb.lineplot, "lum", "pscale", style = "background", hue = "background",  data = df,  markers = True, dashes = False)

        # add standard deviation for each facet
        i = 0
        for o in rc.obs_order:
            df_obs = df.loc[df["obs"] == o]
            df_o_var = df_obs.loc[df_obs["background"] == rc.var_cond]
            df_o_hom = df_obs.loc[df_obs["background"] == rc.hom_cond]
            axes[i].vlines(df_o_var["lum"], ymin = df_o_var["low_std"], ymax = df_o_var["up_std"], color = palette[0])
            axes[i].vlines(df_o_hom["lum"], ymin = df_o_hom["low_std"], ymax = df_o_hom["up_std"], color = palette[1])
            i += 1
            
        # relabel axes y and y axis
        g.set_axis_labels("luminance [cd/m²]", "perceived lightness")
        
    else:
        raise ValueError ("Choose valid experimental method")
    
    # add vertical line at background luminance for each facet
    for i in range(0, len(rc.obs)):
        axes[i].axvline(x = bg, color = 'grey', ls = '--', label = "bg luminance")
        # set title as in paper 
        axes[i].set_title(ol_list[i])

    # add legend
    if(n_col%2 != 0):
        # add legend in the empty facet at the lower right
        axes[(rc.n_obs-1)].legend(bbox_to_anchor = (1.9, 0.2), loc = "lower right", frameon = False)
    else:
        g.add_legend()
    
    # save plot as pdf
    plt_name = rc.p_rea_data_plots + method + '/grid/' + method + '_' + bgc + ".pdf"
    plt.savefig(plt_name, bbox_inches = 'tight', pad_inches = 0.05)
    plt.close()
    









