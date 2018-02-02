
#! usr/bin/env python
import sys
import random


#Balancing peptide calsses by duplicating all of the antitoxic and 
#toxic peptides while throwing a randomly selected half of the neutral data
#Doubling the antitoxic and toxic and halving the neutral makes all the classes have the
#same order of magnitude, so machine learning models should not classify all as neutral.
residues = 'RHKDESTNQCGPAVILFMYW'
if len(sys.argv) == 2 and sys.argv[1].endswith('.csv'):
	InFile = open(sys.argv[1], 'rU')
	outFileName = sys.argv[1].strip('.csv') + '.new_balance.csv'
	OutFile = open(outFileName, 'w')
	linenumber = 0
	neutral_lines = []
	for line in InFile:
		if(linenumber == 0):
			linenumber += 1
			continue
		else:
			columns = line.strip('\n').split(',')
			toxicity = columns[8];
			if toxicity == 'neutral':
				neutral_lines.append(line)
			else:
				OutFile.write(line)
				OutFile.write(line)
	for i in random.sample(range(0, len(neutral_lines)), 4*5458):
		OutFile.write(neutral_lines[i])
	InFile.close();
	OutFile.close();
else:
	print("ERROR")
