#!/apps/r/3.3.0/bin/Rscript

args = commandArgs(trailingOnly=TRUE)

if (length(args) == 0) {
	stop("ERROR: Must specify input file as argument", call.=FALSE)
}

in_file <- args[1]

motifcounts <- read.csv(file=in_file, header=TRUE)
counts <- motifcounts[,- 1]
print(counts)
