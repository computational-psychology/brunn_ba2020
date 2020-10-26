#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2020
@author: Carolin Brunn
"""

"""
PLOT SLOPE OF SIMULATED MLDS SCALES
one facetgrid for all spacings
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

# plto slope for MLDS data
method = "MLDS" 

# specify how many columns the grid shall have
# recommended: 2-3
n_col = 2

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
df = pd.read_csv(path, sep = ',')

# initialize grid
g = sb.FacetGrid(df, col = "spacing", col_wrap = n_col, margin_titles = True)
axes = g.fig.axes

# add title
g.fig.suptitle("Slope of simulated MLDS scales")

# plot slope against luminance
g.map(sb.lineplot, "lum", "slope",  data = df, style = "CE", hue = "CE", markers = True, dashes = False)

# add vertical line at background luminance for each facet
for ax in axes:
    ax.axvline(x = bg, color = 'grey', ls = '--', label = "bg luminance")
    
# add legend
g.add_legend()

# relabel x- and y-axis
g.set_axis_labels("luminance [cd/m²]", "Slope of perc. lightness")  

plt_path = sc.p_simu_plots + method + "/simu_" + method + "slope.pdf"
plt.savefig(plt_path, bbox_inches = 'tight', pad_inches = 0.05)
plt.close()
    
