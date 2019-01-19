# This program filters out peptides with high hydrophobicity and charge and creates a csv file with the rest of the peptides
#
# USAGE: python filterHydrophobCharge.py raw_data.csv outFile.csv chargeCutoff hphobCutoff

from sys import argv
import csv
import math


def getToxIndex(refSum,iSum):
    return math.log10((iSum + 1)/(refSum + 1))

def getToxClass(toxIndex):
    if toxIndex < -0.3:
        return "toxic"
    if toxIndex > 0.2:
        return "anti-toxic"
    return "neutral"


outputFile = open(argv[2], "w")
infoFile = open(argv[1], 'r')
lines = csv.reader(infoFile)
dataset = list(lines)
startIndex = 1
chargeCut = int(argv[3])
hphobCut = int(argv[4])


# Write the header in the output file
outputFile.write("Filtered out peptides with charge >= " + str(chargeCut) + " or hydrophobicity >= " + str(hphobCut))
outputFile.write("\n#**start of data**:\n")
outputFile.write("\nPEPSEQ,HPHOB,CHARGE,REF1,REF2,IP1,IP2,REF_SUM,IP_SUM,T_I,TOXICITY")


print("Writing peptides")
for i in range(startIndex, len(dataset)):
    pep = dataset[i][1]
    #if pep not in peptides:
    #    continue
    hphob = int(dataset[i][2])
    charge = int(dataset[i][3])
    if hphob >= hphobCut or charge >= chargeCut:
        continue
    r1 = int(dataset[i][4])
    r2 = int(dataset[i][5])
    i1 = int(dataset[i][6])
    i2 = int(dataset[i][7])
    toxIndex = getToxIndex(r1 + r2, i1 + i2)
    toxClass = getToxClass(toxIndex)
    outputFile.write("\n" + pep + "," + str(hphob) + "," + str(charge) + "," + str(r1) + "," + str(r2) + "," + str(i1)
                     + "," + str(i2) + "," + str(r1 + r2) + "," + str(i1 + i2) + "," + str(toxIndex) + "," + toxClass)


outputFile.close()
infoFile.close()
