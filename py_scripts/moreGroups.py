
import numpy as np

import matplotlib.pyplot as pit
import os
import matplotlib.pyplot as plt

import sys
import pickle
import csv
import numpy as np
import tensorflow as tf
# # # read in the data
numResidues = 8
numQualities = 25


print("started")


# def myround(x, prec=2, base=0.5):
#     return round(base * round(float(x)/base),prec)


# grab command-line  arguments
# args = str(sys.argv)
# if (len(sys.argv) > 2) or (len(sys.argv) < 2):
#     print("error in command-line argumetns")
canonPath = "C:\\Users\\BCBrown\\Desktop\\ClementLab\\all_data_filtered.csv"
nonCanonPath = "C:\\Users\\BCBrown\\Desktop\\ClementLab\\lblarge.filteredHphobCharge.csv"
def readData(inputPath):
    inputData = []
    with open(inputPath) as inputFile:
        for line in inputFile:
            # Split the line and grab the data I want to keep
            line = line.split(",")
            sequence = line[0]
            score = line[-2] # bin the scores
            toxicity = line[-1]
            inputData.append([sequence, float(score), toxicity])
    return inputData

nonCanonData = readData(nonCanonPath)
canonData = readData(canonPath)

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
                else :
                    attributes = np.append(attributes, float(value))
                i = i + 1
            # grab the first character
           # make a list in the rest of the
            referenceDict[aminoAcid] = attributes
    return referenceDict

referenceDict = getRefDict()

# before changing the sequences into a matrix, separate them into categories

ncTestingToxic = []
ncTestingAntitoxic = []
ncTestingNeutral = []

ncToxScore = []
ncAntiScore = []
ncNeutScore = []

neg80 = []
neg58 = []
neg45 = []
neg35 = []
neg275 = []
neg19 = []
neg01 = []
pos01 = []
pos17 = []
pos1and5 = []
for peptide in canonData:
    try:
        if peptide[1] <= -0.80:
            neg80.append(peptide)
        elif peptide[1] <= -0.58:
            neg58.append(peptide)
        elif peptide[1] <= -0.45:
            neg45.append(peptide)
        elif peptide[1] <= -0.35:
            neg35.append(peptide)
        elif peptide[1] <= -0.275:
           neg275.append(peptide)
        elif peptide[1] <= -0.19:
            neg19.append(peptide)
        elif peptide[1] <= -0.1:
            neg01.append(peptide)
        elif peptide[1] <= 0.01:
            pos01.append(peptide)
        elif peptide[1] <= 0.17:
            pos17.append(peptide)
        elif peptide[1] <= 1.5:
            pos1and5.append(peptide)
        else:
            print(peptide)
    except:
        print(type(peptide[1]))


# print(len(neg80))
# print(len(neg58))
# print(len(neg45))
# print(len(neg35))
# print(len(neg275))
# print(len(neg19))
# print(len(neg01))
# print(len(pos01))
# print(len(pos17))
# print(len(pos1and5))






# ## turn the sequence into a 3-dimentional np array
#     # make a new array at each level.
#     # append that new aray to the right dimentions of the higher array
def makeMatrix(data):
    print(data[0])
    preImageHolder = np.ndarray(shape = (0,0), dtype = float)
    i = 0
    for item in data:
        newImage = np.ndarray(shape = (0,), dtype = float)
        j = 0
        while j < len(item[0]):
        # for letter in item[0]:
            newImage = np.append(newImage, referenceDict[item[0][j]], axis = 0)
            j = j + 1
        i = i + 1
        print("I: " + str(i))
        preImageHolder = np.append(preImageHolder, newImage)
    print("reshapeing")
    preImageHolder = np.reshape(preImageHolder, (i, numResidues, numQualities))
    pickleOut = open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\preImageHolder.pickle", "wb")
    pickle.dump(preImageHolder, pickleOut)
    pickleOut.close()

    preImageHolder = pickle.load(open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\preImageHolder.pickle", "rb"))
    i = len(preImageHolder)
    # rotate the images 90 degrees
    imageHolder = np.ndarray(shape = (0,), dtype = float)
    for k in range(i):
        imageHolder = np.append(imageHolder, np.rot90(preImageHolder[k], 1))
        print(k)
    print("FINAL RESHAPING")
    imageHolder = np.reshape(imageHolder, (i, numQualities, numResidues))
    print("final reshaping complete")
    return imageHolder

# print("ABOUT TO MAKE MATRIX")
# pre_X = makeMatrix(canonData)
# print("matrix complete")
# pickleOut = open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\X_big.pickle", "wb")
# pickle.dump(pre_X, pickleOut)
# pickleOut.close()

def getLabels(data):
    labels = np.ndarray(shape = (0,))
    i = 0
    newLabel = 0
    while i < len(data):
        # grab the the matrix of length currentLength
        if data[i][1] <= -0.8:
            newLabel = 1
        elif data[i][1] <= -0.58:
            newLabel = 2
        elif data[i][1] <= -0.45:
            newLabel = 3
        elif data[i][1] <= -0.38:
            newLabel = 4
        elif data[i][1] <= -0.275:
            newLabel = 5
        elif data[i][1] <= -0.19:
            newLabel = 6
        elif data[i][1] <= -0.01:
            newLabel = 7
        elif data[i][1] <= 0.01:
            newLabel = 8
        elif data[i][1] <= -1.7:
            newLabel = 9
        labels = np.append(labels, newLabel)
        i = i + 1
    return labels

# Y = getLabels(canonData)
# #
# pickleOut = open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\Y_big.pickle", "wb")
# pickle.dump(Y, pickleOut)
# pickleOut.close()

X = pickle.load(open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\X_big.pickle", "rb"))
Y = pickle.load(open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\Y_big.pickle", "rb"))
# *******************************************************************************************************

# introduce some error into the toxic peptides. Try something more complex than ust bluring them.
# use the blossom network.


# ***************


# model.add(tf.keras.layers.Dense(num, activation = tf.nn.relu))
# # model.add(tf.keras.layers.Dense(50, activation = tf.nn.relu))
# # model.add(tf.keras.layers.Dense(, activation = tf.nn.relu))
# # model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # model.add(tf.keras.layers.Dense(200, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(300, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(200, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # # add another layer
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
#
# # model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # add a second one
# # model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # add another layer
# model.add(tf.keras.layers.Dense(10, activation = tf.nn.relu))
# add another layer
# model.add(tf.keras.layers.Dense(50, activation = tf.nn.relu))
# # add another layer
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # # add another layer
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(50, activation = tf.nn.relu))

# add an output layer
# model.add(tf.keras.layers.Dense(10, activation = tf.nn.softmax)) # cannot be deterministic

# ****************************

# make the model:
model = tf.keras.models.Sequential()

num = numQualities*numResidues




# I need some sort of layer before I flatten
model.add(tf.keras.layers.Dense(num, activation = tf.nn.relu))
# add the input layer (and flatten the image)
model.add(tf.keras.layers.Flatten())
# add a dense layer (number of neurons, activation function)


model.add(tf.keras.layers.Dense(num, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(50, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(200, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(num, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(num, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(num/2, activation = tf.nn.relu))
# # add another layer
model.add(tf.keras.layers.Dense(num/3, activation = tf.nn.relu))

# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# add a second one
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# add another layer
model.add(tf.keras.layers.Dense(num/4, activation = tf.nn.relu))

model.add(tf.keras.layers.Dense(num/5, activation = tf.nn.relu))




#
#
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # add a second one
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # add another layer
# model.add(tf.keras.layers.Dense(9, activation = tf.nn.relu))
# # add another layer
# model.add(tf.keras.layers.Dense(50, activation = tf.nn.relu))
# # add another layer
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # # add another layer
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(50, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(9, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(50, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(200, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(300, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(200, activation = tf.nn.relu))
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# # # add another layer
# model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
# add an output layer
model.add(tf.keras.layers.Dense(10, activation = tf.nn.softmax)) # cannot be deterministic

# compile the model (could use stochastic gradient decent for optimizer,
model.compile(optimizer = 'adam',
              loss = 'sparse_categorical_crossentropy', # could be binary for cats/dogs
              metrics = ['accuracy'])

# train! # FIXME: Pick an x that is the randomized toxic/neutral stuff. Pick a y that is the labels for the x's.

# xIn = open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\X.pickle", "rb")
# justX = pickle.load(xIn)
# yIn = open("C:\\Users\\BCBrown\\Desktop\\ClementLab\\Y.pickle", "rb")
# justY = pickle.load(yIn)
#
# print(justX.shape)
# print(len(justY))

history = model.fit(X[1000:], Y[1000:], epochs=15, batch_size=100)

# test!

val_loss, val_acc = model.evaluate(X[0:999], Y[0:999])

model.save_weights("C:\\Users\\BCBrown\\Desktop\\ClementLab\\deltaManyEpocs.h5")

print(val_loss, val_acc)

print(history.history.keys())
print(history.history)
# plt.plot(history.history['acc'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train'], loc='upper left')
# plt.show()


# maybe check out flow networks?





