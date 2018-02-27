#!/usr/bin/python
import sys
import random
import re
from gen_sim_data import getRandomToxScore

def main():
	OutFile = open('simulated_data/simulated_data_1.csv', 'w')
	residues = ['R','H','D','S','N','C','G','V','I','L','F','Y']

	toxic = set()
	neutral = set()
	antitoxic = set()

	#generate random data that matches the motif C**VY**F and call these peptides toxic
	for i in range(1000):
		toxic_peptide = []
		toxic_peptide.append('C')
		toxic_peptide.extend(random.sample(residues, 2))
		toxic_peptide.append('V')
		toxic_peptide.append('Y')
		toxic_peptide.extend(random.sample(residues, 2))
		toxic_peptide.append('F')
		toxic.add(''.join(toxic_peptide))

	#generates random data that matches the simulated antitoxic motif HVV***G*
	for i in range(1000):
		antitoxic_peptide = []
		antitoxic_peptide.append('H')
		antitoxic_peptide.append('V')
		antitoxic_peptide.append('V')
		antitoxic_peptide.extend(random.sample(residues, 3))
		antitoxic_peptide.append('G')
		antitoxic_peptide.append(random.choice(residues))
		antitoxic.add(''.join(antitoxic_peptide))

	#generate random peptides that do not match either motif, call them neutral
	for i in range(1000):
		neutral_peptide = []
		neutral_peptide.extend(random.sample(residues, 8))
		neutral_peptide = ''.join(neutral_peptide)
		if re.search(r'C\w\wVY\w\wF', neutral_peptide):
			continue
		elif re.search(r'HVV\w\w\wG\w', neutral_peptide):
			continue
		else:
			neutral.add(neutral_peptide)

	for tox_pep in toxic:
		OutFile.write('%s,' % tox_pep)
		OutFile.write('%f,' % getRandomToxScore("toxic"))
		OutFile.write('toxic\n')
	for neu_pep in neutral:
		OutFile.write('%s,' % neu_pep)
		OutFile.write('%f,' % getRandomToxScore("neutral"))
		OutFile.write('neutral\n')
	for antitox_pep in  antitoxic:
		OutFile.write('%s,' % antitox_pep)
		OutFile.write('%f,' % getRandomToxScore("anti-toxic"))
		OutFile.write('anti-toxic\n')
	OutFile.close()

	
if __name__ == '__main__':
	main()
