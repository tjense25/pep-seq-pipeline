#!/apps/r/3.3.0/bin/Rscript

#install necesary libraries
library(ggplot2)
library(ggthemes)
library(readr)
library(dplyr)
library(stringr)
library(magrittr)


classify <- function(x) {
	TOX_THRESHOLD <- -0.3 #value corresponding to there being a two times less peps in induced compared to ref
	ANTITOX_THRESHOLD <- 0.2 #value corresponding to there being two times as many peps in induced compared to ref

	sapply(x, function(x) {
		x <- as.double(x)
		class <- NULL
		if (x < TOX_THRESHOLD) {
			class <- "toxic"
		} else if (x > ANTITOX_THRESHOLD){
			class <- "anti-toxic"
		}
		else {
			class <- "neutral"
		}
		return(class)})
}
		

#get input data from command line and read it into a data frame

args = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
	stop("ERROR: Must specify input file as argument", call.=FALSE)
}

in_file <- args[1]
pepSeq <- read_csv(in_file)

pepSeq <- select(pepSeq, PEPSEQ, REF1, REF2, IND1, IND2) %>%
	    mutate(PEPSEQ=str_sub(PEPSEQ,2,-1),
	           REFSUM =REF1 + REF2, 
		   INDSUM = IND1 + IND2) %>%
	    mutate(TOXSCORE = log10((INDSUM + 1)/(REFSUM + 1))) %>%
	    mutate(CLASS = classify(TOXSCORE)) %>%
	    filter(REFSUM + INDSUM > 250) %>%
	    select(PEPSEQ,TOXSCORE,CLASS)

write.csv(pepSeq, file="raw_data/filtered.csv", row.names=FALSE, quote=FALSE)

ggplot(pepSeq, aes(TOXSCORE, fill=CLASS)) +
	geom_histogram(bins=50) +
	ggtitle("Distribution of Toxicity Scores in Filtered Data") +
	xlab("Toxicity Score") +
	ylab("Count") +
	labs(fill = "Toxicity Class") + 
	theme(plot.title = element_text(hjust = 0.5)) + 
	theme_economist()

ggsave("raw_data/rawDataHistogram.pdf")

ggplot(pepSeq, aes(CLASS, TOXSCORE, fill=CLASS)) +
	geom_boxplot() +
	ggtitle("Distribution of Toxicity Scores in Filtered Data") +
	xlab("Toxicity Class") +
	ylab("Toxicity Score") +
	labs(fill = "Toxicity Class") + 
	theme(plot.title = element_text(hjust = 0.5)) + 
	theme_economist()

ggsave("raw_data/rawDataBoxPlot.pdf")
