#!/usr/bin/python
import sys
import random
import re

'''Symulated data 7 adds a lot of noise to the data while keeping the complexity of the motifs as sim6. 
   Instead of having specific motifs for the neutral data, they are now generated completely randomly following
   no motif. The idea being that there are specific motifs that cause a peptide to either be toxic or antitoxic,
   but nothing in particular that causes it to have no effect. If the machine can successfully find the motifs for 
   toxic or antitoxic, it can simply call everything that doesn't match one of those motifs neutral. Also we added
   additional noise in that not all motifs are represented with exactly 10 peptides. The expression depth for each of 
   the motifs now ranges randomly from 5 to 20 proteins per motifs in the training data set.'''

#Function creates a set of motifs by randomly selecting
#4 out of 8 positions to put a random residue in
#motifs describes as strings where * can be any residue
def createMotifs(num_to_create, residues):
	motifs = set()
	while len(motifs) < num_to_create:
		motif = []
		blank = random.sample(range(8), 4)
		for i in range(8):
			if i in blank:
				motif.append('*')
			else:
				motif.append(random.choice(residues))
		motifs.add(''.join(motif))
	return motifs

#Generates a randomly created peptide that matches a given motif
def getPepsMatchingMotif(num_to_create, motif, residues):
	#store values in a set to make sure there is no duplication
	peps = set()
	while len(peps) < num_to_create:
		pep = []
		for res in motif:
			if res == '*': # (if res is not in the given motif choose random residue to put there)
				pep.append(random.choice(residues))
			else:
				pep.append(res)
		#convert peptide list into a string and add it to set
		peps.add(''.join(pep))
	return peps
			

def main():

	#Training Data file-- will contain 5 to 20 data points per motif
	OutFile = open('arff_files/simulated_data/simulated_data_7.arff', 'w')
	#Test data file will contain 2 peps per motif
	TEST  = open('arff_files/simulated_data/TEST7.arff', 'w')

	toxic = set()
	neutral = set()
	antitoxic = set()
	
	residues = ['R','H','D','S','N','C','G','V','I','L','F','Y'] #Some residues not inluded because they're not present in original dataset

	#Create a list of 200  motifs (first 100 will be toxic, the last 100 will be antitoxic)
	motifs = createMotifs(200, residues)
	for i,motif in enumerate(motifs):
		numToCreate = random.randint(5, 20)
		if i < 100:
			#get 10 peptides that match motif and add them to set
			# '|' is union operator in python sets
			toxic = toxic | getPepsMatchingMotif(numToCreate, motif, residues)
			toxicity = "toxic"
		else:
			antitoxic = antitoxic | getPepsMatchingMotif(numToCreate, motif, residues)
			toxicity = "anti-toxic"
		OutFile.write('%% %s: %s\n' % (motif, toxicity))
	
	# get 2000 randomly generated neutral motifs that don't match any specific motif
	neutral = getPepsMatchingMotif(2000, '********', residues)

	OutFile.write('@relation pep-seq\n')
	TEST.write('@relation pep-seq\n')
	
	#output attribute information for the arff file.
	#for each position in the peptide, print out the residues as their possible nominal values
	for i in range(1,9):
		OutFile.write('@attribute pos%d {' % i)
		TEST.write('@attribute pos%d {' % i)
		for r in residues:
			if r == 'R':
				OutFile.write('R')
				TEST.write('R')
				continue
			OutFile.write(',%s' % r)
			TEST.write(',%s' % r)
		OutFile.write('}\n')
		TEST.write('}\n')

	OutFile.write('@attribute toxicity {anti-toxic, neutral, toxic}\n')
	TEST.write('@attribute toxicity {anti-toxic, neutral, toxic}\n')
	OutFile.write('@data\n')
	TEST.write('@data\n')
	

	#Print out all the peptides in the toxicity sets to the arff file with their corresponding label
	for tox_pep in toxic:
		for i in range(8):
			OutFile.write('%s,' % tox_pep[i])
		OutFile.write('toxic\n')
	for neu_pep in neutral:
		for i in range(8):
			OutFile.write('%s,' % neu_pep[i])
		OutFile.write('neutral\n')
	for antitox_pep in  antitoxic:
		for i in range(8):
			OutFile.write('%s,' % antitox_pep[i])
		OutFile.write('anti-toxic\n')
	OutFile.close()

	#Now create TEST file with one match for each of the motifs
	for i,motif in enumerate(motifs):
		if i < 100:
			#For each motif: get 2 peptides that match it then print them out in arff format witht their label
			for pep in getPepsMatchingMotif(2, motif, residues):
				for r in range(8):
					TEST.write('%s,' % pep[r])
				TEST.write('toxic\n')
		else:
			for pep in getPepsMatchingMotif(2, motif, residues):
				for r in range(8):
					TEST.write('%s,' % pep[r])
				TEST.write('anti-toxic\n')

	#Generate 300 random neutral peptides that don't match any specific motif (adds a lot of noise to the data)
	testNeutrals = getPepsMatchingMotif(300, '********', residues)
	for neu in testNeutrals:
		for r in range(8):
			TEST.write('%s,' % neu[r])
		TEST.write('neutral\n')
				
if __name__ == '__main__':
	main()
