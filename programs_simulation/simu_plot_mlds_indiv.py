#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT SIMULATED MLDS SCALES FOR EACH SPACING
"""

################################################################################################
"""IMPORT"""

import pandas as pd# for using dataframes
import numpy as np
from matplotlib import pyplot as plt # for plotting
import seaborn as sb # for nicer plotting
import simu_constants as sc 
import simu_utils as su

################################################################################################
"""CONSTANTS"""

# plot perceptual scale (ps) values of simulated MLDS scales and ground truth functions
method = "MLDS"

# gray background condition
bg = sc.BG_GRAY

# luminance values used for gorund truth function
l_whit = np.linspace(sc.MIN_LUM, sc.MAX_LUM, sc.N_WHIT)
################################################################################################
"""MAIN"""

""" 
calculate values for ground truth functions
"""

# ground truth function with CE
f = su.whit_w_ce(l_whit, bg)
ps_whit_ce = su.normalize_to_range(f, (0,1))

# ground truth function without CE
f = su.whit_wo_ce(l_whit, bg)
ps_whit_noce = su.normalize_to_range(f, (0,1))

# create dataframe with ground truth data
tmp_dict = {"lum": l_whit, 
        "psi_w": ps_whit_ce,
        "psi_wo": ps_whit_noce}
whit_df = pd.DataFrame(data = tmp_dict, columns = ["lum_whit", "psi_w", "psi_wo"])

""" 
plot ps values of MLDS scales and ground truth functions
1 plot per spacing
"""
for lum in sc.spacings:    
    # get label of luminance spacing
    ln = su.lum_label(lum)
    
    # load data
    path = sc.p_simu_data + method + "/simu_" + method + "_sig_" + str(sc.SIGMA_MLDS) + "_nruns_" + str(sc.N_RUNS) + "_lum_" + ln + ".csv"
    sim_data = pd.read_csv(path, sep = ',')
    
    # general settings for plots
    sb.set_style("ticks")
    sb.set_palette("colorblind")
    palette = sb.color_palette("colorblind")
    
    # add title
    plt.title("Simulation of MLDS experiment\n Spacing: " + ln)
    
    # add vertical line at background luminance
    plt.axvline(x = bg, color = 'grey', ls = '--')
    
    # plot pscale values for ps values of MLDS scales (markers)
    sb.lineplot( x = "lum", y = "pscale", data = sim_data,  style = "CE", hue = "CE", markers = True, linewidth = 0, dashes = False, ci = "sd", err_style = "bars")
    
    # add ground truth functions as continuous lines
    sb.lineplot(x = l_whit, y = ps_whit_ce, color = palette[0], dashes = True)
    sb.lineplot(x = l_whit, y = ps_whit_noce, color = palette[1], dashes = True)
    
    # relabel x- and y-axis add legend
    plt.xlabel("luminance [cd/m²]")
    plt.ylabel("Perceived lightness")
    # add legend
    plt.legend(loc = 'lower right', frameon = False)
    
    # save plot as pdf
    plt_path = sc.p_simu_plots + method + "/simu_" + method + "_sig_" + str(sc.SIGMA_MLDS) + "_nruns_" + str(sc.N_RUNS) + '_' + ln + "_lum_" + ln + ".pdf"
    plt.savefig(plt_path, bbox_inches = 'tight', pad_inches = 0.05)
    plt.close()
    
