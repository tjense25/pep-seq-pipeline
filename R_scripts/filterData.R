#!/apps/r/3.3.0/bin/Rscript

#install necesary libraries
library(ggplot2)
library(ggthemes)
library(readr)
library(dplyr)
library(stringr)
library(magrittr)


#Input is a vector of toxicity scores, and outputs a vector of Toxicity classes
#base off the toxicity cut off:
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

#Read in pepseq data as a dataframe
in_file <- args[1]
pepSeq <- read_csv(in_file)

pepSeq <- select(pepSeq, PEPSEQ, REF1, REF2, IND1, IND2) %>% #select PepSeq columns and ref and ind counts
	    mutate(PEPSEQ=str_sub(PEPSEQ,2,-1), 	#remove first G from pepseq
	           REFSUM =REF1 + REF2,			#create new column for referred sum and induced sum
		   INDSUM = IND1 + IND2) %>%
	    mutate(TOXSCORE = log10((INDSUM + 1)/(REFSUM + 1))) %>% #calculate toxScore
	    mutate(CLASS = classify(TOXSCORE)) %>%      #create new column for toxClass factor from toxicity score
	    filter(REFSUM + INDSUM > 250) %>%		#filter to contain only large bacteria samples
	    select(PEPSEQ,TOXSCORE,CLASS)	

#output new data frame to a file as a csv
write.csv(pepSeq, file="raw_data/filtered.csv", row.names=FALSE, quote=FALSE)

#plot distrubtion of tox scores in the filtered data as histogram
ggplot(pepSeq, aes(TOXSCORE, fill=CLASS)) +
	geom_histogram(bins=50) +
	ggtitle("Distribution of Toxicity Scores in Filtered Data") +
	xlab("Toxicity Score") +
	ylab("Count") +
	labs(fill = "Toxicity Class") + 
	theme(plot.title = element_text(hjust = 0.5)) + 
	theme_economist()

ggsave("raw_data/rawDataHistogram.pdf")

#plot distriubtion of tox scores as a box plot
ggplot(pepSeq, aes(CLASS, TOXSCORE, fill=CLASS)) +
	geom_boxplot() +
	ggtitle("Distribution of Toxicity Scores in Filtered Data") +
	xlab("Toxicity Class") +
	ylab("Toxicity Score") +
	labs(fill = "Toxicity Class") + 
	theme(plot.title = element_text(hjust = 0.5)) + 
	theme_economist()

ggsave("raw_data/rawDataBoxPlot.pdf")
