#!/apps/r/3.3.0/bin/Rscript

#install necesary libraryies
library(ggplot2)
library(ggthemes)
library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(magrittr)

#Code to run Principal component analysis on data, view the multi dimensional
#data in less dimensions

args = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
	stop("ERROR: Must specify input file as argument", call.=FALSE)
}

in_file <- args[1]
pepSeq <- read_csv(in_file)

pepPosTitle <- paste0("pos",1:8)
pepPosTitle

pepSeq <- select(pepSeq, PEPSEQ, CLASS) %>%
	mutate(PEPSEQ = str_split(PEPSEQ, pattern="")) %>%
	mutate(PEPSEQ = paste(PEPSEQ, collapse=",")) %>%
	separate(PEPSEQ, pepPosTitle, sep=",")

RESIDUES <- c('A','C','D','E','F','G','H','I','K','L',
		'M','N','P','Q','R','S','T','V','W','Y')
