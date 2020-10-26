### CONSTANTS ###

# path to save csv data
p_csv_data <<- "../data/reanalysis/csv_data/"

#############################################################################################
### FUNCTIONS ###

# load an MLCM file from given path
# save pscale and confidence intervals in a CSV file 
conv2CSV <- function(p, o, c, v) {
  # load MLCM object from path p
  load(p)
  
  # get pscale depending on background condition
  ps <- switch(c, "plain" = bg.full$pscale[ , 1], "dark" = bg.full$pscale[ , 2], "light" = bg.full$pscale[ , 3])

  # get confidence intervals depending on background condition
  up.std <- switch(c, "plain" = bg.high[ , 1], "dark" = bg.high[ , 2], "light" = bg.high[ , 3])
  low.std <- switch(c, "plain" = bg.low[ , 1], "dark" = bg.low[ , 2], "light" = bg.low[ , 3])
  
  # define filename
  fn <- paste(p_csv_data, "MLCM", o, c, v, ".csv", sep = "")

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


