#!/apps/r/3.3.0/bin/Rscript

#install necesary libraryies
library(ggplot2)
library(ggthemes)
library(readr)
library(dplyr)

#Code to run Principal component analysis on data, view the multi dimensional
#data in less dimensions

args = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
	stop("ERROR: Must specify input file as argument", call.=FALSE)
}

in_file <- args[1]
pepSeqData <- read_csv(in_file)

#remove the toxicity column of matrix and store result as matrix 
characterMatrix <- as.matrix(select(pepSeqData, -toxClass))

#get principal components from the matrix and store it in an object
pepSeqPC <- prcomp(characterMatrix)

#extract actual principal components and plot the first two PCs
PCs <- as.data.frame(pepSeqPC$x)

ggplot(PCs, aes(x=PC1, y=PC2, colour=pepSeqData$toxClass)) +
	geom_point() +
	labs(colour = "Toxicity Class") + 
	ggtitle("Principal Component Analysis Plot") +
	theme(plot.title = element_text(hjust = 0.5)) + 
	theme_economist()

ggsave("results/PCA/pcaPlot.pdf")

#find out how much variance is explained by the first 10 principal components
#and make a graphic to describe this

percentVE <- 100 * pepSeqPC$sdev^2 / sum(pepSeqPC$sdev^2)

percentVEdf <- data.frame(PC=1:10, PercentExplained=percentVE[1:10])

ggplot(percentVEdf, aes(PC, PercentExplained, fill=PC)) +
	geom_bar(stat="identity") +
	xlab("Principal Component") +
	ylab("% Variance explained") +
	theme(legend.position="none") +
	theme_economist()

ggsave("results/PCA/varainceExplainedPCA.pdf")
