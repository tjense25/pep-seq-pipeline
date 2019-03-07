import tensorflow as tf
import numpy as np
import numpy as np
import matplotlib.pyplot as pit
import os
import matplotlib.pyplot as plt
import csv
import sys
# # # read in the data
numResidues = 8
numQualities = 25

def myround(x, prec=2, base=0.5):
    return round(base * round(float(x)/base),prec)

# grab command-line  arguments
args = str(sys.argv)
if (len(sys.argv) > 2) or (len(sys.argv) < 2):
    print("error in command-line argumetns")
inputPath = sys.argv[1]

def readData(inputPath):
    inputData = []
    with open(inputPath) as inputFile:
        for line in inputFile:
            # Split the line and grab the data I want to keep
            line = line.split(",")
            sequence = line[0]
            score = myround(line[-2]) # bin the scores
            toxicity = line[-1]
            inputData.append([sequence, score, toxicity])
    return inputData

inputData = readData(inputPath)

def getRefDict():
    referenceDict = {}
    aminoAcidMatrix = "C:\\Users\\BCBrown\\Desktop\\ClementLab\\aaMatrix.csv"
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

referenceDict = getRefDict()

# before changing the sequences into a matrix, separate them into categories

testingToxic = []
trainingToxic = []
testingNeutral = []
trainingNeutral = []
testingAntitoxic = []
trainingAntitoxic = []
t = 0
n = 0
a = 0
for peptide in inputData:
    # if t == 114:
    #     print("here")
    # if t == 1151:
    #     print("here too")
    if peptide[2] == "toxic\n":
        if t <= 115:
            testingToxic.append(peptide)
        elif t < 1152:
           trainingToxic.append(peptide)
        t = t + 1
    elif peptide[2] == "neutral\n":
        if n <= 115:
            testingNeutral.append(peptide)
        elif n < 1152:
            trainingNeutral.append(peptide)
        n = n + 1
    elif peptide[2] == "anti-toxic\n":
        if a <= 115:
            testingAntitoxic.append(peptide)
        elif a < 1152:
            trainingAntitoxic.append(peptide)
        a = a + 1



def makeMatrix(data):
    # print(data[0])
    preImageHolder = np.ndarray(shape = (0,0), dtype = float)
    i = 0
    for item in data:
        newImage = np.ndarray(shape = (0,), dtype = float)
        j = 1
        while j < len(item[0]):
        # for letter in item[0]:
            newImage = np.append(newImage, referenceDict[item[0][j]], axis = 0)
            j = j + 1
        i = i + 1
        preImageHolder = np.append(preImageHolder, newImage)
    preImageHolder = np.reshape(preImageHolder, (i, numResidues, numQualities))
    # rotate the images 90 degrees
    imageHolder = np.ndarray(shape = (0,), dtype = float)
    for k in range(i):
        imageHolder = np.append(imageHolder, np.rot90(preImageHolder[k], 1))

    imageHolder = np.reshape(imageHolder, (i, numQualities, numResidues))
    return imageHolder

testToxic = makeMatrix(testingToxic)
testNeutral = makeMatrix(testingNeutral)
testAntitoxic = makeMatrix(testingAntitoxic)
trainToxic = makeMatrix(trainingToxic)
trainNeutral = makeMatrix(trainingNeutral)
trainAnti = makeMatrix(trainingAntitoxic)


def concatenateData(data, labels):
    newData = np.ndarray(shape = (0,0,0), dtype = float)
    newLabels = np.ndarray(shape = (0,))

    total = 0
    i = 0
    while i < len(data): # for each input image set
        k = 0
        while k < len(data[i]): # append all the data
            newData = np.append(newData, data[i][k])
            newLabels = np.append(newLabels, labels[i])
            k = k + 1
        total = total + k
        i = i + 1
    newData = np.reshape(newData, (total,numQualities,numResidues))
    # print(type(newLabels))
    return [newData, newLabels]


# # inputs:
# # data: a list containing 3-dimensional matrices
# # labels: a list containing the labels of those 3-dimensional matrices
def getXandY(data, labels):
    if (len(data) != len(labels)):
        return("ERROR, input lists must be of equal length")


    # print(data)
    length = len(data)
    #
    # # generate a list, 0-totalLength, and randomize it
    indexes = np.arange(length)
    np.random.shuffle(indexes)
    # print(indexes)


    shuffledData = np.ndarray(shape = (0,0,0), dtype = float)
    shuffledLabels = np.ndarray(shape = (0,))
    i = 0
    while i < length:
        # grab the the matrix of length currentLength
        shuffledData = np.append(shuffledData, data[indexes[i]])
        shuffledLabels = np.append(shuffledLabels, labels[indexes[i]])
        i = i + 1
    shuffledData = np.reshape(shuffledData, (length, numQualities, numResidues))
    return[shuffledData,shuffledLabels]
#
trainingData = concatenateData([testAntitoxic, testToxic, testNeutral], [0,1,2])
x_train,y_train = getXandY(trainingData[0], trainingData[1])



testingData = concatenateData([trainAnti, trainToxic, trainNeutral], [0,1,2])
x_test,y_test = getXandY(testingData[0], testingData[1])

print(testToxic.shape)
print(testNeutral.shape)
print(testAntitoxic.shape)
print(trainToxic.shape)
print(trainNeutral.shape)
print(trainAnti.shape)

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

# *******************************************************************************************************

# introduce some error into the toxic peptides. Try something more complex than ust bluring them.
# use the blossom network.


import pickle

# x_test_file = open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\ImageArrays\\x_test.npy", "rb")
# y_test_file = open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\ImageArrays\\y_test.npy", "rb")
# x_train_file = open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\ImageArrays\\x_train.npy", "rb")
# y_train_file = open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\ImageArrays\\y_train.npy", "rb")

# x_test = np.fromfile("C:\\Users\\BCBrown\\Desktop\\ClementLab\\ImageArrays\\x_test")
# y_test = np.fromfile("C:\\Users\\BCBrown\\Desktop\\ClementLab\\ImageArrays\\y_test")
# x_train = np.fromfile("C:\\Users\\BCBrown\\Desktop\\ClementLab\\ImageArrays\\x_train")
# y_train = np.fromfile("C:\\Users\\BCBrown\\Desktop\\ClementLab\\ImageArrays\\y_train")

# x_test = pickle.load(x_test_file)
# y_test = pickle.load(x_test_file)
# x_train = pickle.load(x_train_file)
# y_train = pickle.load(x_train_file)

# y_test = np.reshape(y_test,)

# make the model:
model = tf.keras.models.Sequential()
C:\Users\BCBrown\PycharmProjects\chemSig\matrixMaker.py
num = numQualities*numResidues
# I need some sort of layer before I flatten
model.add(tf.keras.layers.Dense(num, activation = tf.nn.relu))
# add the input layer (and flatten the image)
model.add(tf.keras.layers.Flatten())
# add a dense layer (number of neurons, activation function)
model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# add a second one
model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# add another layer
model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# add another layer
model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# add another layer
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # add another layer
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # add another layer
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# add an output layer
model.add(tf.keras.layers.Dense(3, activation = tf.nn.softmax)) # cannot be deterministic

# compile the model (could use stochastic gradient decent for optimizer,
model.compile(optimizer = 'adam',
              loss = 'sparse_categorical_crossentropy', # could be binary for cats/dogs
              metrics = ['accuracy'])

# train! # FIXME: Pick an x that is the randomized toxic/neutral stuff. Pick a y that is the labels for the x's.
print(type(y_train))

model.fit(x_test, y_test, epochs=5)

# test!
val_loss, val_acc = model.evaluate(x_train, y_train)
print(val_loss, val_acc)

# model.save_weights("model1")

import pickle
x_train_pickle = open("x_train.pickle", "wb")
pickle.dump(x_train, x_train_pickle)

y_train_pickle = open("y_train.pickle", "wb")
pickle.dump(y_train, y_train_pickle)

y_test_pickle = open("y_test.pickle", "wb")
pickle.dump(y_test, y_test_pickle)

x_test_pickle = open("x_test.pickle", "wb")
pickle.dump(x_test, x_test_pickle)
