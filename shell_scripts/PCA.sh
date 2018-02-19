#!/bin/bash

#Shell script to do PCA analysis of raw data:
set -e

INPUT_FILE=$1

if [ $# -lt 1 ] #if number of command line arguments less than 1
then
	echo "ERROR: Please specify input file as argument"
	exit 1
fi

#Store raw data as first command line parameter
RAW_DATA=$1

#take raw data and convert it into a character matrxi
cat $RAW_DATA | python py_scripts/create_pca_matrix.py > temp.csv

#run the character matrix through PCA R script
Rscript --vanilla R_scripts/PCA.R temp.csv

#remove temporary files
rm -f temp.csv Rplots.pdf

exit 0
