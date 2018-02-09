#!/apps/r/3.3.0/bin/Rscript

args = commandArgs(trailingOnly=TRUE)

#Print error if user did not supply a command argument for file name
if (length(args) == 0) {
	stop("ERROR: Must specify input file as argument", call.=FALSE)
}

in_file <- args[1]

#read infile into a dataframe
motifcounts <- read.csv(file=in_file, header=TRUE, stringsAsFactors=FALSE)
#extract just the counts
counts <- motifcounts[,c("toxic", "neutral","anti.tox")]

#THe number of chisquared tests we will perform
tests <- nrow(counts)

pvalues <- NULL
significant<- NULL
for (i in 1:tests) {
	p.value <- chisq.test(counts[i, ])$p.value
	pvalues <- c(pvalues, p.value)
	if (p.value > 0.05/tests) { #applying Bonferroni correction for multiple testing
		stat.signif = FALSE
	} else {
		stat.signif = TRUE
	}
	significant <- c(significant, stat.signif)
}

motifcounts$pvalues <-pvalues
motifcounts$significant<-significant

#calculate how many motifs were significant
sig.motifs <-sum(significant) 
print(paste0(sig.motifs," out of the ",tests," motifs were significant"))

#Write out the additional rows onto the data frame file
write.table(motifcounts, file=in_file, row.names=FALSE, sep=",", quote=FALSE)
