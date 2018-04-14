from imblearn.over_sampling import SMOTE
from sys import argv
import csv
from collections import Counter
import random
import time
#from imblearn.datasets import fetch_datasets
#from sklearn.datasets import make_classification

start = time.time()

# Reads csv file, creates two datasets: one containing proteins and class, the other containing tox scores, with y being class for corresponding tox score
def readFile(oldFile, writer):
    csvfile = open(oldFile, 'r')
    lines = csv.reader(csvfile)
    dataset = list(lines)
    writer.writerows(dataset)
    proteinData = []
    toxData = []
    y = []
    startIndex = 0
    if dataset[0][0] == 'PEPSEQ':
        startIndex = 1
    for i in range(startIndex, len(dataset)):
        # Separate each row in original dataset into 2 datasets
        toxScore = [float(dataset[i][1])]
        proteinData.append([dataset[i][0], dataset[i][2]])
        toxData.append(toxScore)
        # Append target value to y, 0 if toxic, 1 if neutral, 2 if anti-toxic
        if dataset[i][2] == 'toxic':
            y.append(0)
        elif dataset[i][2] == 'neutral':
            y.append(1)
        else:
            y.append(2)
    csvfile.close()
    return proteinData, toxData, y, writer

# Generates blosum matrix as a dictionary
# Returns blosum matrix and list of amino acids in order of the matrix
def makeBlosum():
    matrix = {}
    xAxis = []
    # Read matrix from txt file
    with open('blosum62.txt', 'r') as myFile:
        for line in myFile:
            line = line.rstrip('\n')
            lineList = line.split()
            # Skips commented lines
            if lineList[0] != '#' and lineList[0] != '*':
                # Reads x-axis label
                if len(matrix) == 0:
                    xAxis = lineList
                    xAxis.remove('*')
                    for aminoAcid in lineList:
                        matrix[aminoAcid] = {}
                else:
                    # Reads y-axis label and adds matrix values to the dictionary, excludes asterisk
                    aminoAcid = lineList[0]
                    for i in range(1, len(lineList) - 1):
                        key = xAxis[i - 1]
                        # convert weight to int, add 5 so there are no negative values
                        matrix[key][aminoAcid] = int(lineList[i]) + 5
    return matrix, xAxis

# Applies smote on tox scores
# returns resampled tox scores (x) and resampled y values
def smote(x, y):
    sm = SMOTE(ratio='minority')
    xResampled, yResampled = SMOTE().fit_sample(x, y)
    return xResampled, yResampled


# returns a list of all weights from blosum62 for the desired amino acid against all other amino acids
def getWeightList(blosum, aminoAcid):
    weightList = []
    for a in aminoAcidList:
        weightList.append(blosum[aminoAcid][a])
    return weightList


# Finds the smallest number of mutations between the sequence and the other sequences in the dataSet
# Finds the indices for the locations of mutations between current sequence and others in the dataset
def getMinMutationAndLocations(currentClassSamples, curSeq):
    locations = []
    minMutation = 8
    for protein in currentClassSamples:
        diffs = 0
        for i in range(len(protein[0])):
            if protein[0][i] != curSeq[i]:
                locations.append(i)
                diffs += 1
        if diffs != 0 and diffs < minMutation:
            minMutation = diffs
    return locations, minMutation


# Generates synthetic sequence based on most similar sequences in the data, with mutations based on blosum62 matrix
def generateSequence(currentClassSamples, seq, blosum, aminoAcidList):
    possibleLocations, minMutation = getMinMutationAndLocations(currentClassSamples, seq)
    #print(possibleLocations)
    mutationIndex = random.sample(possibleLocations, minMutation)
    #originalAminoAcids = []
    #for i in  mutationIndex:
    #    originalAminoAcids.append(seq[i])
    newSeq = []
    for i in range(len(seq)):
        if i in mutationIndex:
            weightList = getWeightList(blosum, seq[i])
            newSeq.append(random.choices(aminoAcidList, weightList, k=1)[0])
        else:
            newSeq.append(seq[i])
    return ''.join(newSeq)

# POWB = Protein Oversampling With Blosum62
# Generates synthetic sequences for a given class, number of sequences to be generated depends on multiplier, plus any remainder (base samples chosen randomly)
# Returns list of newly generated sequences
def powb(currentClassSamples, className, multiplier, remainder, blosum, aminoAcidList):
    newSeqs = []
    # For each sample in protein data in the current class, it creates a new synthetic sequence, and does this i=multiplier times
    for seq in currentClassSamples:
        i = 0
        while i != multiplier:
            newSeqs.append(generateSequence(currentClassSamples, seq[0], blosum, aminoAcidList))
            i += 1
    # For additional synthetic samples required, randomly choose a sequence from the original data as a base
    for k in range(remainder):
        seq = random.sample(currentClassSamples, 1)[0]
        newSeqs.append(generateSequence(currentClassSamples, seq[0], blosum, aminoAcidList))
    return newSeqs


# Looks at tox scores generated from SMOTE, determines how many proteins to generate and calls POWB
# Returns new Protein dataset, where each item is a list in the form [sequence, class]
def addSyntheticProteins(proteinData, counterOriginal, counterResampled, blosum, aminoAcidList):
    classCode = {0: 'toxic', 1: 'neutral', 2: 'anti-toxic'}
    newData = proteinData[:]
    for i in range(3):
        diff = counterResampled[i] - counterOriginal[i]
        if diff < 0:
            print("\nUndersampling happened?")
            print("original for " + classCode[i] + ": " + str(counterOriginal[i]))
            print("resampled for " + classCode[i] + ": " + str(counterResampled[i]))
            System.exit(0)
        if diff != 0:
            multiplier = int(diff / counterOriginal[i])
            remainder = diff % counterResampled[i]
            currentClassSamples = []
            for sequence in proteinData:
                if sequence[1] == classCode[i]:
                    currentClassSamples.append(sequence)
            seqs = powb(currentClassSamples, classCode[i], multiplier, remainder, blosum, aminoAcidList)
            for protein in seqs:
                newData.append([protein, classCode[i]])
    return newData

# Writes the data from the new protein data and toxicity data into a combined csv file
def writeCSV(writer, newProteins, xResampled, yResampled, originalSize):
    classCode = {0: 'toxic', 1: 'neutral', 2: 'anti-toxic'}
    for i in range(originalSize, len(yResampled)):
        writer.writerow([newProteins[i][0], str(xResampled[i][0]), classCode[yResampled[i]]])


# Command Line Argument: spsoAndSmote.py originalFilename.csv newFilename.csv
newData = open(argv[2], 'w', newline='')
writer = csv.writer(newData)
proteinData, toxData, y, writer = readFile(argv[1], writer)
counterOriginal = Counter(y)
blosum, aminoAcidList = makeBlosum()
xResampled, yResampled = smote(toxData, y)
counterResampled = Counter(yResampled)
newProteins = addSyntheticProteins(proteinData, counterOriginal, counterResampled, blosum, aminoAcidList)
writeCSV(writer, newProteins, xResampled, yResampled, len(y))
newData.close()

end = time.time()
print("Total runtime is " + str(end - start) + " seconds")
