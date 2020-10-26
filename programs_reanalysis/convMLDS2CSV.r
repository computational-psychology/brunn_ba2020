### CONSTANTS ###

# path to save csv data
p_csv_data <<- "../data/reanalysis/csv_data/"

#############################################################################################
### FUNCTIONS ###

# load an MLDS file from given path
# save pscale and confidence intervals in a CSV file 
conv2CSV <- function(p, o, c, v) {
  # load MLCM object from path p
  load(p)
  
  # get pscale
  ps <- obs.mlds$pscale
  
  # get confidence intervals
  up.std <- obs.high[1:10]
  low.std <- obs.low[1:10]

  # define filename
  fn <- paste(p_csv_data, "MLDS", o, c, v, ".csv", sep = "")
  
  # create dataframe and save as csv
  df <- data.frame(pscale = ps, up_std = up.std, low_std = low.std)
  write.csv(df, file=paste(fn,  sep = ""))
}

#############################################################################################
### MAIN ###

args <- commandArgs(trailingOnly = TRUE)
path <- args[1] # path
obs <- args[2]  # observer
cond <- args[3] # background condition
var <- args[4]  # variegated/homogeneous
conv2CSV(path, obs, cond, var)
cat(3)


