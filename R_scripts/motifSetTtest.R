#!/apps/r/3.3.0/bin/Rscript

#install necesary libraries to read in and plot data
library(ggplot2)
library(ggthemes)
library(readr)
library(dplyr)
library(magrittr)

#read in command line arguments
args = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
	stop("ERROR: Must specify input file as argument", call.=FALSE)
}

#Read in motifSetData as a dataframe
in_file <- args[1]
peps <- read_tsv(in_file)

head(peps)

#store dataframe of thsoe peps that are inside the motifSet
insideMS <- peps %>% filter(MotifSet == "INSIDE") %>% select(-MotifSet)

#store dataframe of peps that are outside of the motifSet
outsideMS <- peps %>% filter(MotifSet == "OUTSIDE") %>% select(-MotifSet)

#conduct T test on difference of average tox score between peps
#in and outside motifset
t.test(insideMS$ToxScore, outsideMS$ToxScore)


#plot the distribution of toxScores seperated by MotifSet group
ggplot(peps, aes(MotifSet,ToxScore)) +
	 geom_boxplot() + 
	 ggtitle("Relative Distribution of Peptides in Motif Set") +
	 xlab("Motif Set") +
	 ylab("Toxicity Score") +
	 labs(colour = "Toxicity Class") + 
	 theme_economist()

ggsave("MotifSetBoxPlot.jpg")
