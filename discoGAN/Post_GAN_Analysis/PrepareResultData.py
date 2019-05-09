# This program takes the results from MatrixToSequence.py and formats it for other analyses
#
# USAGE: python PrepareResultData.py motifResults.csv filtered418.csv

from sys import argv
import csv
from statistics import mean
import math


def checkMotif(seq, motif):
    for i in range(0, len(seq)):
        if motif != '.':
            if seq[i] != motif[i]:
                return False
    return True


def getMotifCounts(set, motif, c):
    count = 0
    for seq in set:
        if checkMotif(seq, motif):
            count += 1
            if c == "toxic":
                if motif in motifTox:
                    motifTox[motif].append(toxic[seq])
                else:
                    motifTox[motif] = [toxic[seq]]
            else:
                if motif in motifTox:
                    motifTox[motif].append(nonToxic[seq])
                else:
                    motifTox[motif] = [nonToxic[seq]]
    return count


detailsFile = open(argv[2], "r")
motifFile = open(argv[1], 'r')

startIndex = 1
toxic = {}
nonToxic = {}
toxCounts = {}  # {motif:count}
nonToxCounts = {}
motifs = {}
ranks = {}
motifTox = {}
avgTox = {}

motifToxRank = {}
motifDiffRank = {}
motifScoreRank = {}

allToxRank = []
allDiffRank = []
allScoreRank = []

# Write the output file
countsFile = open("rankedMotifs.csv", "w")
countsFile.write("Motif,Transformed Count,Toxic Count,Non-Toxic Count,Avg Toxicitiy")


print("Reading Sequences")
lines = csv.reader(detailsFile)
detailsData = list(lines)
for i in range(startIndex, len(detailsData)):
    if detailsData[2] == "toxic":
        toxic[detailsData[0]] = float(detailsData[1])
    else:
        nonToxic[detailsData[0]] = float(detailsData[1])


print("Reading Motifs")
lines = csv.reader(motifFile)
motifData = list(lines)
for i in range(startIndex, len(motifData)):
    motif = motifData[i][0]
    transformCount = int(motifData[i][1])
    toxCount = getMotifCounts(toxic, motif, "toxic")
    nonToxCount = getMotifCounts(nonToxic, motif, "non")
    toxCounts[motif] = toxCount
    nonToxCounts[motif] = nonToxCount
    motifs[motif] = transformCount


# Ranks motifs based on percentage present in toxic vs difference between toxic and non-toxic occurrences
for motif in motifs:
    toxRank = toxCounts[motif] / len(toxic)
    diffRank = toxRank - (nonToxCounts[motif] / len(nonToxic))
    avgTox = mean(motifTox[motif])
    allToxRank.append(toxRank)
    allDiffRank.append(diffRank)
    allScoreRank.append(avgTox)


maxToxRank = max(allToxRank)
maxDiffRank = max(allDiffRank)
minScoreRank = min(allScoreRank)
adjustment = 0
if (minScoreRank < 0):
    adjustment = -1 * minScoreRank
maxScoreRank = max(allScoreRank) + adjustment

# Normalize all rank values
for motif in motifs:
    toxRank = allToxRank[motif] / maxToxRank
    diffRank = allDiffRank[motif] / maxDiffRank
    avgTox = 1 / ((allScoreRank[motif] + adjustment) / maxScoreRank)
    rank = (toxRank * diffRank * avgTox)**(1.0/3.0)
    ranks[motif] = rank


# Sort ranked motifs and write to file
sortedMotifs = sorted(ranks.items(), key=lambda x: x[1])[::-1]
for motif in sortedMotifs:
    countsFile.write("\n" + motif + "," + str(motifs[motif]) +
                     "," + str(toxCounts[motif]) + "," + str(nonToxCounts[motif]) +
                     "," + str(allScoreRank[motif] / (maxScoreRank - adjustment)))


motifFile.close()
countsFile.close()
detailsFile.close()
