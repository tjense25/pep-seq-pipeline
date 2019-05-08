# This program compares motifs found by the GAN and RF
#
# USAGE: python GANvsRF.py GANMotifs.csv RFMotifs.csv

from sys import argv
import csv
import math


# Open files
outFile = open("commonMotifs.csv", "w")
outFile.write("Motif,GAN Rank,RF Rank")
ganFile = open(argv[1], 'r')
rfFile = open(argv[2], "r")

startIndex = 1
ganMotifs = {}
rfMotifs = {}

print("Reading GAN Motifs")
lines = csv.reader(ganFile)
ganData = list(lines)
for i in range(startIndex, len(ganData)):
    motif = ganData[i][0]
    ganMotifs[motif] = i


print("Reading RF Motifs")
lines = csv.reader(rfFile)
rfData = list(lines)
for i in range(startIndex, len(rfData)):
    motif = rfData[i][0]
    rfMotifs[motif] = i


print("Comparing Motifs")
for ganMotif in ganMotifs:
    if ganMotif in rfMotifs:
        outFile.write("\n" + ganMotif + "," + str(ganMotifs[ganMotif]) + "," + str(rfMotifs[ganMotif]))


outFile.close()
ganFile.close()
rfFile.close()