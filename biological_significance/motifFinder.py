#!/user/bin/env python3
import csv
import sys
import re
from datetime import datetime

# motifFilder.py 
# Biran Brown, Fall 2018

# motifFinder.py takes an input file with a list of peptide motifs,
# along with another input file of peptide sequences,
# and outputs a file that contains the peptides sequences that 
# matched the motifs of the first file

# example input:
# python motifFinder.py motifs.csv sequences.csv output.csv

# Example Files:

# motifs.csv:
# MotifSeq,NumRFInstances,NumMissclassified,TotalPeptideCount,ToxicCount,NeutralCount,AntitoxicCount,AverageToxScore,AverageRank,MotifScore
# ...F...Y,4367,1,563,490,65,8,-0.551437,66987.4,2183.5
# .Y.....Y,1608,0,627,549,70,8,-0.529763,66267.1,1608
 
# sequences.csv:

# Peptide,Database
# PFKLSLHL,APD
# FFHLHFHY,APD
# FFFLSRIF,APD
# ISVCITVC,APD
# KIIFLIAI,APD
# RLGDGCTR,APD
# VAVLVLGA,APD

# output.csv:
# (the user gives a name to the new file, which will look like this:)

# sequence, motif, database


# read in input file
args = str(sys.argv)
if (len(sys.argv) > 4) or (len(sys.argv) < 4):
	print("error in command-line arguments")
motifCSV = sys.argv[1]
knownCSV = sys.argv[2]
outputFileName = sys.argv[3]

# open outputFile
outputFile = open(outputFileName, "w+")

ourMotifs = []
# read in motifCSV
with open(motifCSV) as motifFile:
	lineReader = csv.reader(motifFile)
 	i = 0	
	for row in lineReader:
		if len(row) > 0 and i > 0:
			ourMotifs.append(row[0])
		i = i + 1
		
#read in konwnCSV
knownMotifs = {}
with open(knownCSV) as knownFile:
	lineReader = csv.reader(knownFile)
	i = 0
	for row in lineReader:
		if len(row) > 0 and i > 0:
			knownMotifs[row[0]] = row[1]
		i = i + 1

# perform the comparison ************************8

# output the header in the output file
outputFile.write("File was produced at " + str(datetime.now()) + " using motifFinder.py\n")
outputFile.write("command used: python motifFinder.py " + motifCSV + " " + knownCSV + " " + outputFileName)
outputFile.write("\n#**start of data**:")
outputFile.write("\nPeptide,Motif,Database\n")

# for each element in knownMotifs
for knownMotif in knownMotifs:
	# for each element in ourMotifs
	for ourMotif in ourMotifs:
		# perform a letter by letter comparison
		accept = True
		iterator = 0
		while iterator < len(knownMotif):
			# ignore if ourMotif == '.'
			if ourMotif[iterator] != '.':
				# reject if the two strings do not match at that posiiton
				if knownMotif[iterator] != ourMotif[iterator]:
					accept = False
			iterator = iterator + 1
		if accept:
			outputRow = knownMotif + "," + ourMotif + "," + knownMotifs[knownMotif] + "\n"			
			# write to output File
			outputFile.write(outputRow)			
			
	
outputFile.close()


