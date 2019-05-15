# This program takes the Results.csv and converts the toxic sequences to a FASTA file

# USAGE: python MakeFasta.py Results.csv

from sys import argv
import csv
import time


start_time = time.time()
detailsFile = open(argv[1], "r")
fasta = open("GANFasta.fa", "w")

startIndex = 1


print("Reading Sequences")
lines = csv.reader(detailsFile)
detailsData = list(lines)
for i in range(startIndex, len(detailsData)):
    fasta.write(">seq" + str(i) + "\n")
    fasta.write(detailsData[i][1])

fasta.close()
detailsFile.close()

print("Finished in " + str(time.time() - start_time) + " seconds")
