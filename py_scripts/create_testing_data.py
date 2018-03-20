#!/usr/bin/python
import sys
import random
import re
from gen_sim_data import getRandomToxScore, createMotifs, getPepsMatchingMotif


def main(k):

	OutFile = open('testing_data/test%d.csv' % k, 'w')

	toxic = set()
	neutral = set()
	antitoxic = set()
	
	residues = ['A','E','K','M','P','Q','T','W','R','H','D','S','N','C','G','V','I','L','F','Y'] #Now containing all residues

	numToxicMotifs = k
	numToxicPeps = 2000
	numToCreate = numToxicPeps // numToxicMotifs

	motifs = createMotifs(2*numToxicMotifs, residues)
	for i,motif in enumerate(motifs):
		if i < numToxicMotifs:
			# '|' is union operator in python sets
			toxic = toxic | getPepsMatchingMotif(numToCreate, motif, residues)
			toxicity = "toxic"
		else:
			antitoxic = antitoxic | getPepsMatchingMotif(numToCreate, motif, residues)
			toxicity = "anti-toxic"
		OutFile.write('%% %s: %s\n' % (motif, toxicity))
	
	# get 2000 randomly generated neutral motifs that don't match any specific motif
	neutral = getPepsMatchingMotif(numToxicPeps, '********', residues)

	OutFile.write('PEPSEQ,TOXSCORE,CLASS')
	

	

	#Print out all the peptides in the toxicity sets to the arff file with their corresponding label
	for tox_pep in toxic:
		OutFile.write("%s,%f,%s\n" % (tox_pep, getRandomToxScore("toxic"), "toxic"))
	for neu_pep in neutral:
		OutFile.write("%s,%f,%s\n" % (neu_pep, getRandomToxScore("neutral"), "neutral"))
	for antitox_pep in  antitoxic:
		OutFile.write("%s,%f,%s\n" % (antitox_pep, getRandomToxScore("anti-toxic"), "anti-toxic"))
		
	OutFile.close()


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("ERROR: please specify number of toxic motifs to create")
		sys.exit(0)
	k = int(sys.argv[1])
	main(k)
