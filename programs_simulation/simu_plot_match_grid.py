#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT SIMULATED MATCHING DATA IN ONE GRID

"""
################################################################################################

"""IMPORT"""

import pandas as pd # for using dataframes
from matplotlib import pyplot as plt # for plotting
import seaborn as sb # for nicer plotting
import simu_constants as sc 
import simu_utils as su

################################################################################################
"""CONSTANTS"""

# symmetric matching experiment
method = "Matching"
mode = "asym"

n_col = len(sc.bg_simu)

################################################################################################
"""MAIN"""

""" 
plot "symmetric" matching data in plotgrid
"""

# load "big" csv file
p_sim_data = sc.p_simu_data + method + "/" + mode + "/simu_" + method + "_" + mode + "_sig_" + str(sc.SIGMA_MATCH) + "_nruns_" + str(sc.N_RUNS) + ".csv"
df = pd.read_csv(p_sim_data, sep = ',')
        
# general settings for plotting
sb.set_style("ticks")
sb.set_palette(sc.match_palette)

g = sb.FacetGrid(df, col = "match_bg", row = "spacing", margin_titles = True)
axes = g.fig.axes

 # add vertical line at background luminances for each facet
for ax in axes:
    ax.axvline(x = sc.BG_DARK, color = 'grey', ls = ':', label = "dark bg")
    ax.axvline(x = sc.BG_GRAY, color = 'grey', ls = '-.', label = "gray bg")
    ax.axvline(x = sc.BG_LIGHT, color = 'grey', ls = '--', label = "light bg")

# add title     
g.fig.suptitle("Simulation of " + mode + " "+ method + " experiment")#+ ", target-bg: "+ bgt) #+ mod_title)

# plot macthing data
g.map(sb.lineplot, "tar_lum", "mat_lum", data = df,  style = "target_bg", hue = "target_bg", markers = True, dashes = False, ci = "sd", err_style = "bars")

# relabel axes y and y axis
g.set_axis_labels("target luminance [cd/m²]", "match luminance [cd/m²]")

# add legend
g.add_legend()    

# save plot as pdf
plt_name = sc.p_simu_plots + method + "/" + mode + "/grid/simu" + method + "_" + mode + "_sig_" + str(sc.SIGMA_MATCH) + "_nruns_" + str(sc.N_RUNS) + ".pdf"
plt.savefig(plt_name, bbox_inches = 'tight', pad_inches = 0.05)
plt.close()
            
        
