# USAGE: python matrixMaker.py aaMatrix.csv canon.csv nonCanon.csv nonToxic.csv outputToxic.json ouputNonToxic.json

# A is non-toxic and B is toxic

import numpy as np
import csv
import random
import math
import os
from PIL import Image


def getRefDict():
    referenceDict = {}
    aminoAcidMatrix = "C:\\Users\\krist\\PycharmProjects\\PepSeq\\DiscoGAN\\aaMatrix.csv"
    with open(aminoAcidMatrix) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            # make new list
            aminoAcid = ""

            attributes = np.ndarray(shape = (0,), dtype = float)
            i = 0
            for value in row:
                if i == 0:
                    aminoAcid = value # save which amino acid this is for
                else:
                    attributes = np.append(attributes, float(value))
                i = i + 1
            referenceDict[aminoAcid] = attributes
    return referenceDict


def getAA(val, index, referenceDict):
    bestDiff = math.inf
    possible = []
    for key in referenceDict:
        diff = math.fabs(val - referenceDict[key][-1 - index])
        if diff < bestDiff:
            possible = [key]
            bestDiff = diff
        elif diff == bestDiff:
            possible.append(key)

    return random.sample(possible,1)[0]


def findConsensusString(allPeps):
    sequence = ""
    for i in range(0, len(allPeps[0])):
        allAA = []
        for pep in allPeps:
            allAA.append(pep[i])
        sequence += max(set(allAA), key=allAA.count)
    return sequence


def matrixToSequence(matrix):
    referenceDict = getRefDict()
    referenceDict.pop('_', None)
    possible = []

    p = 0

    for property in matrix:
        print(property[0])

    exit(0)
    for property in matrix:
        pep = ""
        for val in property:
            pep += getAA((val / 255), p, referenceDict)
        possible.append(pep)
        p += 1
    return findConsensusString(possible)


def findMotif(seq1, seq2):
    if len(seq1) == 9 and seq1[0] == "G":
        seq1 = seq1[1:]
    if len(seq2) == 9 and seq2[0] == "G":
        seq2 = seq2[1:
               ]
    motif = ""
    for i in range(0, len(seq1)):
        if seq1[i] == seq2[i]:
            motif += "."
        else:
            motif += seq2[i]
    return motif


def findBestMotifs(changes, file):
    maxChanges = 9
    sortedMotifs = sorted(changes.items(), key=lambda x: x[1])[::-1]

    for motif in sortedMotifs:
        if 8 - motif[0].count(".") > maxChanges:
            continue
        file.write("\n" + motif[0] + "," + str(motif[1]))


def getPrefix(filename):
    prefix = ""
    for c in filename:
        if c != ".":
            prefix += c
        else:
            return prefix


def main():
    changes = {}
    dPath = "test_1_results\\0.0"
    directory = os.fsencode(dPath)
    batchNum = 0
    outFile = open("test_1_results\\Batch_" + str(batchNum) + "_Results.csv", "w")
    outFile.write("Original Sequence,New Sequence,Toxic Motifs,Non-Toxic Motifs")
    outFileDetailed = open("test_1_results\\Batch_" + str(batchNum) + "_Detailed.csv", "w")
    outFileDetailed.write("A,AB,ABA,B,BA,BAB,ABA Changes,BAB Changes")


    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".A.npy"):
            prefix = getPrefix(filename)

            print("Reading sample " + prefix)

            imageA = np.load(dPath + "\\" + filename)
            imageAB = np.load(dPath + "\\" + prefix + ".AB.npy")
            imageABA = np.load(dPath + "\\" + prefix + ".ABA.npy")
            imageB = np.load(dPath + "\\" + prefix + ".B.npy")
            imageBA = np.load(dPath + "\\" + prefix + ".BA.npy")
            imageBAB = np.load(dPath + "\\" + prefix + ".BAB.npy")

            seqA = matrixToSequence(imageA)
            seqAB = matrixToSequence(imageAB)
            seqABA = matrixToSequence(imageABA)
            seqB = matrixToSequence(imageB)
            seqBA = matrixToSequence(imageBA)
            seqBAB = matrixToSequence(imageBAB)

            motifAB = findMotif(seqA, seqAB)
            motifBA = findMotif(seqB, seqBA)
            motifABA = findMotif(seqA, seqABA)
            motifBAB = findMotif(seqB, seqBAB)

            if motifAB in changes:
                changes[motifAB] += 1
            else:
                changes[motifAB] = 1

            outFile.write("\n" + seqA + "," + seqAB + "," + motifAB + "," + motifBA)
            outFileDetailed.write("\n" + seqA + "," + seqAB + "," + seqABA + "," +
                                  seqB + "," + seqBA + "," + seqBAB + "," +
                                  str(8 - motifABA.count(".")) + "," + str(8 - motifBAB.count(".")))
        else:
            continue

    outFileMotif = open("test_1_results\\Batch_" + str(batchNum) + "_Motifs.csv", "w")
    outFileMotif.write("Motif,Num Occurrences")
    findBestMotifs(changes, outFileMotif)

    outFile.close()
    outFileDetailed.close()
    outFileMotif.close()


main()

