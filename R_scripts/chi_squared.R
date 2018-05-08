#!/apps/r/3.3.0/bin/Rscript

library(readr)
library(tidyr)
library(dplyr)


args = commandArgs(trailingOnly=TRUE)

#Print error if user did not supply a command argument for file name
if (length(args) == 0) {
	stop("ERROR: Must specify input file as argument", call.=FALSE)
}

in_file <- args[1]

#read infile into a dataframe
motifs <- read_csv(in_file)
#extract just the counts
counts <- select(motifs, ToxicCount, NeutralCount, AntitoxicCount) %>%
 	  mutate( NonToxicCount = NeutralCount + AntitoxicCount) %>%
	  select(ToxicCount, NonToxicCount)

#THe number of chisquared tests we will perform
tests <- nrow(counts)

pvalues <- NULL
significant<- NULL
for (i in 1:tests) {
	p.value <- chisq.test(counts[i, ])$p.value
	signif = FALSE;
	if (p.value < 0.05/tests) { #Bonferroni adjustment of p-values 
		signif = TRUE;
	}
	pvalues <- c(pvalues, p.value)
	significant <- c(significant, signif)
}
motifs$pvalues <-pvalues
motifs$significant<-significant

#calculate how many motifs were significant
sig.motifs <-sum(significant) 
print(paste0(sig.motifs," out of the ",tests," motifs were significant"))

#Write out the additional rows onto the data frame file
write.table(motifs, file=in_file, row.names=FALSE, sep=",", quote=FALSE)
