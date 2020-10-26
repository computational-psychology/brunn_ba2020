#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT SIMULATED MLDS SCALES FOR EACH RUN WITH BOOTSTRAP INTERVALS
might serve as an additional indicator for the discriminability but mostly the conf. intervals overlap
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

method = "MLDS"

# gray background condition
bg = sc.BG_GRAY

####################################################################################################################
""" FUNCTIONS """

"""
NORMALIZE MLDS DATA
normalize pscale values and confidence intervals
"""
def normalize_df_mlds(df):
    fac = df.loc[9,"pscale"]
    n_ps = df["pscale"] / fac
    n_low = df["low_boot"] / fac
    n_high = df["high_boot"] / fac
    n_df = pd.DataFrame(data = list(zip(n_ps, n_low, n_high)), columns = ["pscale", "low", "high"])
    return(n_df)

################################################################################################

"""MAIN"""

# settings for plotting
sb.set_style("ticks")
sb.set_palette("colorblind")
palette = sb.color_palette("colorblind")

# plot MLDS scales with confidence intervals for eaach spacing
# one plot per spacing & run
for lum in sc.spacings:    
    # get label of luminance spacing
    ln = su.lum_label(lum)
      
    # plots for each run
    for j in range(0, sc.N_RUNS):
        # load data once with and once without ce
        for CRISP in [True, False]:
            ce = "ce" if CRISP else "noce"
            path = sc.p_simu_mlds_runs + "/sim_data_" +ln +'_' + str(j) + ce + "mlds.csv"
            
            if(CRISP):
                df_ce = pd.read_csv(path, sep = ',')
                df_ce = normalize_df_mlds(df_ce)
            else:
                df_noce = pd.read_csv(path, sep = ',')
                df_noce = normalize_df_mlds(df_noce)
            
            
        # add vertical line at background luminance
        plt.axvline(x = bg, color = 'grey', ls = '--')
        # add title depending on run and spacing
        plt.title("Simulation of MLDS experiment\n Run: " + str(j) + ln)
        
        # plot pscale values with markers
        plt.plot(lum, df_ce["pscale"], color = palette[0], label = "with CE", marker = 'x', linewidth = 0)
        plt.plot(lum, df_noce["pscale"], color = palette[1], label = "without CE", marker = 'o', linewidth = 0)
        
        # plot confidence intervals
        plt.vlines(lum, ymin = df_ce["low"], ymax = df_ce["high"], color = palette[0])
        plt.vlines(lum, ymin = df_noce["low"], ymax = df_noce["high"], color = palette[1])
        
        # save plot, one per run & spacing
        plt_path = sc.p_simu_plots + method + "/runwboot/simu_" + method + '_' + ln + "_boot_run_" + str(j) + "_sig_" + str(sc.SIGMA_MLDS) + ".pdf"
        plt.savefig(plt_path, bbox_inches = 'tight', pad_inches = 0.05)
        plt.close()
    


