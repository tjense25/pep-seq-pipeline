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
ggplot(peps, aes(x=MotifSet,y=ToxScore)) +
	 geom_boxplot() + 
	 annotate("rect", xmin=-Inf, xmax=Inf, ymin=-Inf, ymax=-.3, alpha=0.2, fill="#619CFF") + 
	 annotate("rect", xmin=-Inf, xmax=Inf, ymin=-.3, ymax=.2, alpha=0.2, fill="#00BA38") +
	 annotate("rect", xmin=-Inf, xmax=Inf, ymin=.2, ymax=Inf, alpha=0.2, fill="#F8766D") +
	 ggtitle("Pep-Seq Pipeline Output for Simulated Data") +
	 xlab("Motif Set") +
	 ylab("Toxicity Score") +
	 theme_bw() +
	 theme(text = element_text(size=20),
	       plot.title = element_text(hjust = 0.5),
	       panel.border = element_blank(),
	       panel.grid.major = element_blank(),
	       axis.line = element_line(colour = "black")) + 

ggsave("MotifSetBoxPlot.jpg")
