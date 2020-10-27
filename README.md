# brunn_ba2020

This GitHub folder contains the programs, data, and plots used in my bachelor thesis "The Crispening Effect: An Artifact of a Method or a Feature of the Visual System" (June 2020 to October 2020).

All programs were written and tested in Python version 3.7.6 or R version 3.2.3.
For the python programs the modules pandas, numpy, pyplot (matplotlib), itertools, subprocess and pyreadr are used.

The programs used for the simulation and the reanalysis can be found in the folders programs_simulations and programs_reanalysis, respectively.
The folder "data" contains the experimental data used for this bachelor thesis and generated during the simulations and reanaysis.
The folder "plots" contains all plots generated in the simulation and reanalysis.
It is possible to generate all data and plots again with the provided programs.
Only the experimental data of Aguilar and Maertens 202o is needed as a preliminary for the reanalysis. These data can be found in data/exp_aguilar2020.

In the following, I explain the structure of each folder.

#######################################################################################

1) data/ contains all data.
	1.1) exp_aguilar2020/ contains the experimental data provided by Guillermo Aguilar. 
		This folder has two subfolders: Matching and mlds_cm which contain the data of the asymmetric matching experiment and the MLDS/MLCM experiment, respectively. 
		Those subfolders are again divided into one folder for the data obtained with a variegated checkerboard and the other one for the data obtained with a homogeneous background. 
		The extension for the folder containing the data for the homogeneous background is "SR".
		For the Matching data, the subfolders are called results or resultsSR and contain .txt files with the data.
		For the MLDS and MLCM data, the subfolders are called results_merged and results_merged_SR. These folders contain .MLDS and .MLCM files that have to be loaded and processed in R. The convMLDSCM2CSV.py program takes care of that.
	1.2) reanalysis/ contains all data needed for or generated in the reanalysis.
		The lut.csv file enables the conversion of luminance values between 0 and 1 to a luminance range between 0 and 255. This is needed for converting the match's luminance in convMatching2CSV.py.
		The folder "csv_data" contains csv_files with the MLDS pscales and confidence intervals for each observer and viewing conditions and additionally, holds other files generated during the reanalysis.
	1.3) simulation/ contains all data generated in the simulations. The folder is subdivided into two folders, one for the matching simulation and one for the MLDS simulation.
		1.3.1) Matching/ this folder is also subdivided into an "asym" and "sym" folder. 
			The asym folder contains the data which was generated in the simulation with the target based on ground truth with CE and the match was based on ground truth without CE. 
			In contrast, the sym folder contains the data which was generated in the simulation where both target and match were based on ground truth with CE.
			Both folders contain individual files for each spacing, indicated by ...tlum_"spacing".csv where is in [centbg, coarse, coarseX, even].
			The simulaion was repeated for different magnitudes of noise indicated with ...sig_0.0X... where X is in [2, 4, 8].
			Additionally, a big csv file (...sig_0.0X...nruns_100.csv) exists for each noise level that joins the matching data of all spacings in one file. 
			These combined files are used in the plotting routines.
			
		1.3.2) MLDS/ this folder contains the data generated in the MDLS simulation.
			It contains combined files with the normalized pscale values for 100 runs for each spacing (simu_MLDS_sig_0.1_nruns_100_lum_"spacing".csv).
			Additionally, files of the evaluation of the simulation are saved here.
			simu_MLDSslope.csv contains the slope values of the average perceptual scale values of each spacing.
			simu_d2truth..  contains the distance of each average perceptual scale value to the corresponding ground truth value.
			simu_sumd2truth_... has the summed distance over all average values from simu_d2truth... per spacing and per CE condition. sum_ce and sum_noce indicate the scales with and without CE, respectively.
			simu_mlds_distBtwScales.csv has one column per spacing. Each column contains the summed distance between the scales for each run.Hence, each column has 100 entries. Additionally, the last row is added which specifies the average summed distance for the respective spacing.
			simu_mlds_cntBelowAvg.csv contains the average distance for each spacing. Additionally, cntBelowReference specifies in how many runs the distance was below the reference defined in simu_constants.py
			"runs/" the subfolder "runs contains the individual csv files for each simulation run. Once with the different luminance values of the triads and the corresponding response variables. The other files, specified with the extensino "mlds.csv" contain the simulated perceptual scales and the corresponding confidence intervals for each run.

#######################################################################################
	
2) plots/ contains all plots
	2.1) reanalysis/ contains all plots generated in the reanalysis.
	
		2.1.1) data/ contains three subfolders, one for each method -- MLCM, MLDS, and Matching. In these plots the perceptual scales are plotted against luminance. Each of the subfolders contains individual plots for each observer per background condition -- plain (= no transparency), dark, and light.
			Additionally, the folders have one subfolder: "grid/". This folder contains plotsgrids with all observers per background condition.
			The "grid/" folders in MLDS and MLCM also contain a grid with only two exemplary observers (described in the thesis) per background condition.
			
		2.1.2) slope/ contains three subfolders, one for each method -- MLCM, MLDS, and Matching. In these plots the slope of the perceptual scales is plotted against luminance. The rest of the strucure is described as above for 2.1.1) data/.
		
	2.2) simulation/ contains all plots generated in the simulation.
	
		2.2.1) MLDS/ contains plots for the simulated perceptual scales and the corresponding slopes for each spacing. The extension ..._slope.pdf indicates the slope plots. The files simu_MLDS_sig_0.1_... are the plots with the simulated perceptual scales per spacing.
			The subfolder "runwboot/" contains plots with the perceptual scales and confidence intervals for each run of the MLDS simulation.
			
		2.2.2) Matching/ contains two subfolders: asym and sym for the asymmetric and symmetric matching experiment, respectively.
			Both subfolders have individual plots per each differing match background indicated by ..._bgm_"XYZ" with "XYZ" in [dark, gray, light] and per spacing.
			Additionally, they have the subfolder "grid/" which contains grids with several plots. In "asym/grid/" the files. ..lum_012.pdf are the plots for the even, centbg, and coarse spacing analyzed in the simulation part of the thesis. The simuMatching_..._nruns_100.pdf files show plotgrids with plots for all spacings and different macth backgrounds. The "sig_0.0X" indicates which noise level was used. In "sym/grid/" the file with the extension _even.pdf" contains the plot shown in the thesis - "symmetric" matching and shows the plots for different match backgrounds for the even spacing.

#######################################################################################

In the following, "Prerequisites" indicate which programs have to be run beforehand in the case that any data has been deleted. If all data is available the programs can be run without any prerequisites.

3) programs_simulation/ contains all programs used for the simulation.
	3.1) simu_constants.py defines all constants and paths that are needed for the simulation. The noise level, the number of runs and the number of targets etc can be changed here. It also defines the different spacings used in the simulation.
	3.2) simu_utils.py defines functions that were needed several times in different simulation scenarios.
	
	3.3) pboot.mlds.R was provided by Guillermo Aguilar and enables the parallelized bootstrap calculation. It is called by simu_mlds_boot.R.
	
	3.4) simu_mlds_boot.R calculates MLDS scales and the corresponding confidence intervals (via bootstrap) based on response variables generated in simu_mdls.py. The program is called from there via subprocess.
	
	3.5) simu_mlds.py simulate MLDS experiment. Calls simu_mlds_boot.R via subprocess. simulates experiment once with internal function with and the other time without CE. The data is saved in individual csv files for each run and the normalized perceptual scales of all runs are saved in one big csv file for all spacings together.
	
	3.6) simu_matching.py simulates a matching expeirment. The variable "mode" can be changed to "sym" or "asym" in order to simulate a symmetric or asymmetric experiment, respectively. "symmetric" means that target and match are simulated based on ground truth functions with CE. "asymmetric" means that the target is simulated with CE and the match without CE. The data is saved in one csv file per spacing and additionally a big csv file containing all data is generated in the end.
	
	3.7) simu_mlds_d2Truth.py calculates the distance of the perceptual scale values to the corresponding ground truth value.
		prerequisite: simu_mlds.py
	
	3.8) simu_mlds_dBtwScales.py calculates the distance of the perceptual scale values between the scales with and without CE.
		prerequisite: simu_mlds.py
		
	3.9) simu_calc_slope.py calculate slope of MLDS scale. The program should be easily adaptable for the matchng data.
		prerequisite: simu_mlds.py
		
	3.10) simu_plot_match_grid/indiv.py plot the simulated matching data in a grid or individually, respectively. The "mode" (asym/sym) should be specified at the beginning of the program.
		prerequisite: simu_matching.py
	
	3.11) simu_plot_mldsboot_runwise.py plot the MLDS scales for each run with the corresponding confidence intervals.
		prerequisite: simu_mlds.py
	
	3.12) simu_plot_mlds_indiv.py plot the average (over n runs) perceptual scales for each spacing.
		prerequisite: simu_mlds.py
		
	3.13) simu_plot_slope_grid/indiv.py plot the slope of the MLDS scales in a grid or individually for each spacing, respectively.
		prerequisite: simu_mlds.py, simu_calc_slope.py

#######################################################################################

"Prerequisites" indicate which programs have to be run beforehand in the case that any data has been deleted. If all data is available the programs can be run without any prerequisites.

4) programs_reanalysis/
	4.1) rea_constants.py defines all constants and paths that are needed in the reanalysis. The order of the observers in the plots can be changed here. Additionally, some observers/background conditions etc can be excluded in the processing by excluding them in this file.
	
	4.2) rea_utils.py defines functions that were needed several times in the reanalyis.
	
	4.3) convMLDS2CSV.R and convMLCM2CSV.R load an R MLDS or MLCM file and convert it to a csv file (one per observer and background condition). They are called by convMLDSCM2CSV.py via subprocess. 
	
	4.4) convMLDSCM2CSV.py converts the original expeirmental data, an MLDS or MLCM file, to a csv file with the above-mentioined R Scripts (via subprocess). Additionally, it creates one big csv file with the data of all observers, one file per background condition. The method (MLDS/MLCM) whose data shall be converted has to be specified above.
	
	4.5) convMatching2CSV.py converts the original expeirmental data, a .txt file, to a csv file. During this conversion it converts all luminance value to be in the range between 0 and 255. In the end, one csv file per background condition is created.
	
	4.6) rea_calc_slope.py calculates the slope for the data of the different methods. Specify at the beginning of the program (CONSTANTS) for which method the slope shall be calculated.
		prerequisite: the conversion of the data of the respective method.
		
	4.7) rea_dBtwScales.py calculate the distance between the MDLS or MLCM scales at the perceptual scale values. Specify at the beginning of the program (CONSTANTS) for which method (MLDS/MLCM) the distance shall be calculated.
		prerequisite: the conversion of the MLDS/MLCM data
		
	4.8) rea_plot_data_indiv/grid.py plot the data in a grid or individually for each spacing, respectively. Specify at the beginning of the program (CONSTANTS) for which method (MLDS/MLCM/Matching) the data shall be plotted. For the grid, the number of columns can be changed as well.
		prerequisite: the conversion of the data of the respective method
	
	4.9) rea_plot_slope_indiv/grid.py plot the slope of the data in a grid or individually for each spacing, respectively. Specify at the beginning of the program (CONSTANTS) for which method (MLDS/MLCM/Matching) the slope shall be plotted. For the grid, the number of columns can be changed as well.
		prerequisite: the conversion of the data of the respective method + rea_calc_slope.py
	
	

			
	
