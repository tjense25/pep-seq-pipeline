# This program takes the results from MatrixToSequence.py and formats it for other analyses
#
# USAGE: python PrepareResultData.py motifResults.csv detailsResults.csv

from sys import argv
import csv
import math


def checkMotif(seq, motif):
    for i in range(0, len(seq)):
        if motif != '.':
            if seq[i] != motif[i]:
                return False
    return True


def getMotifCounts(set, motif):
    count = 0
    for seq in set:
        if checkMotif(seq, motif):
            count += 1
    return count


# TODO: Should I use details or original pepseq file as reference?
detailsFile = open(argv[2], "r")
motifFile = open(argv[1], 'r')

startIndex = 1
toxic = []
nonToxic = []
toxCounts = {}  # {motif:count}
nonToxCounts = {}
motifs = {}
ranks = {}

# Write the output file
countsFile = open("rankedMotifs.csv", "w")
countsFile.write("Motif,Transformed Count,Toxic Count,Non-Toxic Count")


print("Reading Sequences")
lines = csv.reader(detailsFile)
detailsData = list(lines)
for i in range(startIndex, len(detailsData)):
    #toxic.append(detailsData[1])  # AB
    toxic.append(detailsData[3])  # B
    #nonToxic.append(detailsData[4])  # BA
    nonToxic.append(detailsData[0])  # A


print("Reading Motifs")
lines = csv.reader(motifFile)
motifData = list(lines)
for i in range(startIndex, len(motifData)):
    motif = motifData[i][0]
    transformCount = int(motifData[i][1])
    toxCount = getMotifCounts(toxic, motif)
    nonToxCount = getMotifCounts(nonToxic, motif)
    toxCounts[motif] = toxCount
    nonToxCounts[motif] = nonToxCount
    motifs[motif] = transformCount


# Ranks motifs based on percentage present in toxic vs difference between toxic and non-toxic occurrences
for motif in motifs:
    toxRank = toxCounts[motif] / len(toxic)
    diffRank = toxRank - (nonToxCounts[motif] / len(nonToxic))
    rank = toxRank + diffRank / 2
    ranks[motif] = rank


# Sort ranked motifs and write to file
sortedMotifs = sorted(ranks.items(), key=lambda x: x[1])[::-1]
for motif in sortedMotifs:
    countsFile.write("\n" + motif + "," + str(motifs[motif]) + "," + str(toxCounts[motif]) + "," + str(nonToxCounts[motif]))



motifFile.close()
countsFile.close()
detailsFile.close()
#statsFile.close()