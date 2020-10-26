library(snow)
workers <- c("localhost", "localhost", "localhost", "localhost")
master <- "localhost"

calculateCI = TRUE # if true, calculated CI using bootstrap. it takes some time

library('MLDS')
source("pboot.mlds.R")

################################################################################################

### FUNCIONS ###

# get all unique luminance values of the file
uniqueEntries <- function(df){
  l1 <- unique(df["S1"])
  l2 <- unique(df["S2"])  
  l3 <- unique(df["S3"])
  l <- c(l1, l2, l3)
  ul <- unique(unlist(l))
  return(ul)
}

analyzemlds <- function(fn, mlds.file) {
  # calculate bootstraps
  obs.bt <- pboot.mlds(mlds.file, nsim=1000, workers = workers, master=master)
  
  n <- nrow(obs.bt$boot.samp)
  samples <- apply(obs.bt$boot.samp, 2, function(x) x/x[n])
  
  # calculate upper and lower limit
  obs.low <- c("0"=0, apply(samples, 1, quantile, probs = 0.025))
  obs.high <- c("0"=0, apply(samples, 1, quantile, probs = 0.975))
  
  # save pscale and confidence interval limits into csv file
  ps <- mlds.file$pscale
  df <- data.frame(pscale = ps, high_boot = obs.high[0:10], low_boot = obs.low[0:10])
  write.csv(df, file=paste(fn, 'mlds.csv', sep = ""))
}

################################################################################################

### MAIN ###

args <- commandArgs(trailingOnly = TRUE)
path <- args[1]

# load data points of simulated data from disk
dat <- read.table(paste(path, ".csv", sep = ''), header = TRUE, sep = ",")

n_rows <- nrow(dat["resp"])

# get all unique luminance values of the file
uni_lum <- uniqueEntries(dat)
n_ent <- length(uni_lum)

# convert all entries in the file to integers
# assign integer values depending on luminance values
for(i in (1:n_rows)){
  for(j in 2:4){
    for(k in 1:n_ent) {
      if(dat[i,j] == uni_lum[k]){
        dat[i,j] <- k
        break
      }
    }
  }
}

# MLDS on the preprocessed data
dat.mlbs <- as.mlbs.df(dat)
dat.mlds <- mlds(dat.mlbs)
analyzemlds(path, dat.mlds)

cat(3)