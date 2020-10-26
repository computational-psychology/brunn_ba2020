#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT DATA OF AGUILAR & MAERTENS 2020 INDIVIDUALLY PER OBSERVER
one plot per observer per condition
plot data for variegated condition and homogeneous condition in one plot
variegated: expected to not show CE
homogeneous: expected to show CE
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
method = "MLDS" # "MLDS"/"MLCM"/"Matching"

####################################################################################################################
"""MAIN"""

""" plot data for each observer individually"""

# general settings for plots
sb.set_style("ticks")
sb.set_palette("colorblind")
palette = sb.color_palette("colorblind")

# plot experimental data for all observers separately
for bgc in rc.bg_cond:
    # luminance value of background
    bg = rc.bg_lum[bgc]
    
    # load csv file for bgc background condition
    csv_file = method + bgc + ".csv"
    df = pd.read_csv((rc.p_csv_data + csv_file), sep = ',')
    
    # plot individual data for each observer
    for o in rc.obs:
        # extract observer-specific data
        df_obs = df.loc[df["obs"] == o]
        
        # observer label used in the Aguilar2020
        ol = rc.obs_label_map.loc[o, "label"]
        
        # add title depending on background condition
        if(bgc == "plain"):
            plt.title(method + " experiment data\n" + ol + ", transparency: none")
        else:
            plt.title(method + " experiment data\n" + ol + ", transparency: "+ bgc)
        
        # add vertical line at background luminance
        plt.axvline(x = bg, color = 'grey', ls = '--', label = "bg luminance")
        
        # plot data for the respective method    
        if(method == "Matching"):
            # plot matching data
            sb.lineplot( x = "tar_lum", y = "mat_lum", style = "background", hue = "background",  data = df_obs,  markers = True, dashes = False, ci = "sd", err_style = "bars")
            # re-label y and y axis
            plt.xlabel("target luminance [cd/m²]")
            plt.ylabel("match luminance [cd/m²]")
            
        elif((method == "MLDS") or (method == "MLCM")):
            # plot MLDS data
            sb.lineplot( x = "lum", y = "pscale", style = "background", hue = "background",  data = df_obs,  markers = True, dashes = False)

            # add vertical lines for standard deviation
            df_o_var = df_obs.loc[df_obs["background"] == rc.var_cond]
            df_o_hom = df_obs.loc[df_obs["background"] == rc.hom_cond]
            plt.vlines(df_o_var["lum"], ymin = df_o_var["low_std"], ymax = df_o_var["up_std"], color = palette[0])
            plt.vlines(df_o_hom["lum"], ymin = df_o_hom["low_std"], ymax = df_o_hom["up_std"], color = palette[1])
            
            # re-label y and y axis
            plt.xlabel("luminance [cd/m²]")
            plt.ylabel("perceived lightness")
        else:
            raise ValueError ("Choose valid experimental method")
            
        # define location of legend
        plt.legend(loc = "upper left", frameon = False)
        
        # save plot as pdf
        # one plot per observer per condition
        plt_name = rc.p_rea_data_plots + method + '/' + method + '_'+ o + '_' + bgc + ".pdf"
        plt.savefig(plt_name, bbox_inches = 'tight', pad_inches = 0.05)
        plt.close()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        