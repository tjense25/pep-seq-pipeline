#!/apps/r/3.3.0/bin/Rscript

#install necesary libraries to read in and plot data
library(ggplot2)
library(ggthemes)
library(readr)
library(dplyr)
library(magrittr)

args = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
	stop("ERROR: Must specify input file as argument", call.=FALSE)
}

in_file <- args[1]

peps <- read_csv(in_file)

head(peps)

#store dataframe of thsoe peps that are inside the motifSet
insideMS <- peps %>% filter(MotifSet == "INSIDE") %>% select(-MotifSet)

#store dataframe of peps that are outside of the motifSet
outsideMS <- peps %>% filter(MotifSet == "OUTSIDE") %>% select(-MotifSet)

t.test(insideMS$ToxScore, outsideMS$ToxScore)

ggplot(peps, aes(MotifSet,ToxScore)) +
	 geom_boxplot() + 
	 theme_economist()

ggsave("MotifSetBoxPlot.jpg")
