#!/usr/bin/python
import sys
import random
import re

'''sim9 is similar to the other simulated data, but does not create an arff.
  isntead it creates a csv similar to what we would receive after filtering the
  raw data. To do this, in addition to assigning the random motifs a class of
  toxic, it also assigns it a randomly selected number in that toxicity range.
  The toxicity range is defined in the filter file. Less than -.3 is toxic,
  less than .3 is neutral and greater than .3 is toxic. It also samples from a
  gaussian distribution, centered at -.1 and with a similar spread to the
  filtered data. Therefore, this simulated data almost exactly resembles what
  we find in raw data'''

def getClassForScore(toxScore):
	if toxScore == None:
		return None
	elif toxScore < -.3:
		return "toxic"
	elif toxScore < .2:
		return "neutral"
	else:
		return "anti-toxic"


def getRandomToxScore(toxClass):
	mu = -0.2380324 #calculated from the mean of the filtered raw data
	sigma = 0.3607984 #calculated from the standard deviation of filtered raw data
	toxScore = None
	while(getClassForScore(toxScore) != toxClass):
		toxScore = random.gauss(mu, sigma)
	return toxScore

	

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
	OutFile = open('simulated_data/simulated_data_10.csv', 'w')
	#Test data file will contain 2 peps per motif
	#TEST  = open('simulated_data/TEST8.arff', 'w')

	toxic = set()
	neutral = set()
	antitoxic = set()
	
	residues = ['A','E','K','M','P','Q','T','W','R','H','D','S','N','C','G','V','I','L','F','Y'] #Now containing all residues

	#Create a list of 200  motifs (first 100 will be toxic, the last 100 will be antitoxic)
	motifs = createMotifs(50, residues)
	for i,motif in enumerate(motifs):
		numToCreate = 40 #random.randint(5, 20)
		if i < 40:
			#get 10 peptides that match motif and add them to set
			# '|' is union operator in python sets
			toxic = toxic | getPepsMatchingMotif(numToCreate, motif, residues)
			toxicity = "toxic"
		else:
			antitoxic = antitoxic | getPepsMatchingMotif(numToCreate, motif, residues)
			toxicity = "anti-toxic"
		#OutFile.write('%% %s: %s\n' % (motif, toxicity))
	
	# get 2000 randomly generated neutral motifs that don't match any specific motif
	neutral = getPepsMatchingMotif(1600, '********', residues)

	OutFile.write('PEPSEQ,TOXSCORE,CLASS')
	#TEST.write('PEPSEQ,TOXSCORE,CLASS')
	
	#output attribute information for the arff file.
	#for each position in the peptide, print out the residues as their possible nominal values
	#for i in range(1,9):
	#	OutFile.write('@attribute pos%d {' % i)
	#	TEST.write('@attribute pos%d {' % i)
	#	for r in residues:
	#		if r == 'A':
	#			OutFile.write('A')
	#			TEST.write('A')
	#			continue
	#		OutFile.write(',%s' % r)
	#		TEST.write(',%s' % r)
	#	OutFile.write('}\n')
	#	TEST.write('}\n')

	#OutFile.write('@attribute toxicity {anti-toxic, neutral, toxic}\n')
	#TEST.write('@attribute toxicity {anti-toxic, neutral, toxic}\n')
	#OutFile.write('@data\n')
	#TEST.write('@data\n')
	

	#Print out all the peptides in the toxicity sets to the arff file with their corresponding label
	for tox_pep in toxic:
		OutFile.write("%s,%f,%s\n" % (tox_pep, getRandomToxScore("toxic"), "toxic"))
	for neu_pep in neutral:
		OutFile.write("%s,%f,%s\n" % (neu_pep, getRandomToxScore("neutral"), "neutral"))
	for antitox_pep in  antitoxic:
		OutFile.write("%s,%f,%s\n" % (antitox_pep, getRandomToxScore("anti-toxic"), "anti-toxic"))
		
	OutFile.close()

	##Now create TEST file with one match for each of the motifs
	#for i,motif in enumerate(motifs):
	#	if i < 100:
	#		#For each motif: get 2 peptides that match it then print them out in arff format witht their label
	#		for pep in getPepsMatchingMotif(2, motif, residues):
	#			for r in range(8):
	#				TEST.write('%s,' % pep[r])
	#			TEST.write('toxic\n')
	#	else:
	#		for pep in getPepsMatchingMotif(2, motif, residues):
	#			for r in range(8):
	#				TEST.write('%s,' % pep[r])
	#			TEST.write('anti-toxic\n')

	##Generate 300 random neutral peptides that don't match any specific motif (adds a lot of noise to the data)
	#testNeutrals = getPepsMatchingMotif(300, '********', residues)
	#for neu in testNeutrals:
	#	for r in range(8):
	#		TEST.write('%s,' % neu[r])
	#	TEST.write('neutral\n')
				
if __name__ == '__main__':
	main()
