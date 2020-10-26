#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT SIMULATED MATCHING DATA INDIVIDUALLY PER MATCHING BACKGROUND & SPACING
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
mode = "sym"        

################################################################################################
"""MAIN"""

""" 
plot  matching data
"""

for l_target in sc.spacings:
    # get label of target luminance
    tar_label = su.lum_label(l_target)
    for bg_mat in sc.bg_simu:
        bgm = su.bg_label(bg_mat)    
        
        # load matching data, one csv file per spacing
        path = sc.p_simu_data + method + "/" + mode + "/simu_" + method + "_" + mode + "_sig_" + str(sc.SIGMA_MATCH) + "_nruns_" + str(sc.N_RUNS) + "_tlum_" + tar_label + ".csv"
        sim_data = pd.read_csv(path, sep = ',')
        
        # general settings for plotting
        sb.set_style("ticks")
        sb.set_palette(sc.match_palette)
        
        # add title
        plt.title("Simulation of " + mode + " "+ method + " experiment\n Match's background: "+ bgm)
        
        # plot matching data
        sb.lineplot( x = [0,65], y = [0,65], color = "grey", dashes = True)
        sb.lineplot( x = "tar_lum", y = "mat_lum", data = sim_data,  style = "bg_tar", hue = "bg_tar", markers = True, dashes = False, ci = "sd", err_style = "bars")
        
        # re-label y and y axis
        plt.xlabel("target luminance [cd/m²]")
        plt.ylabel("match luminance [cd/m²]")
        
        # save plot as pdf
        plt_name = sc.p_simu_plots + method + "/" + mode + "/simu" + method + "_" + mode + "_bgm_" + bgm + "_sig_" + str(sc.SIGMA_MATCH) + "_nruns_" + str(sc.N_RUNS) + "_tlum_" + tar_label+ ".pdf"
        plt.savefig(plt_name, bbox_inches = 'tight', pad_inches = 0.05)
        plt.close()
            
        
