#! usr/bin/env python
import sys

'''Python script to convert pep-seq data into arff format to be used in machine
learning algorithms. Reads a csv file in from std input and prints to stdout
the same file but in atribute relation format. The arff has 9 total attributes:
one for amino acid residue for each position of the peptide and one for the toxicity 
classification (toxic, antitoxic, or neutral).'''
def main():
	sys.stdout.write('@relation pep-seq\n') 
	residues = 'RHKDESTNQCGPAVILFMYW' #Not all residues present because some missing from our original dataset
	res_nominal = '{R,H,D,S,N,C,G,V,I,L,F,Y}'

	#Write out each of the positions and residues as an attribute
	for i in range(1, 9):
		sys.stdout.write('@attribute pos%d %s\n' % (i, res_nominal))

	#Write to stdout the toxicity class attribute
	sys.stdout.write('@attribute toxicity  {toxic, neutral, anti-toxic}\n')
	sys.stdout.write('@data\n')
	for line in sys.stdin:
		columns = line.strip('\n').split(',')
		pep_sequence = columns[0];
		toxicity = columns[8];
		#for each position in pep sequence output the Residue seperated by commas
		for r in pep_sequence:
			if r not in residues:
				r = "?"
			sys.stdout.write(r + ',')
		sys.stdout.write('%s\n' % toxicity)

if __name__ == "__main__":
	main()
