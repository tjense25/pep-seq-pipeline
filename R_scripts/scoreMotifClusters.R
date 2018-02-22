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

peps <- select(peps, TOXSCORE, Motif)

head(peps)

peps$Motif <- as.factor(peps$Motif)


motifs = NULL
averageToxScore = NULL
for (motif in levels(peps$Motif))
{
	motifs <- c(motifs, motif)
	cluster <- filter(peps, Motif==motif)
	averageToxScore <- c(averageToxScore,mean(cluster$TOXSCORE))

}

motifScores <- tibble(Motif=motifs, ToxScore=averageToxScore) %>%
		arrange(ToxScore)

print(motifScores)

