#!/usr/bin/python

import sys

'''Python script to convert a comma seperated value represented the pepseq and
conver it to a character matrix that has 160 columns: one for every position
for the peptide and for each residue. So the first column represents is pos1
an A, then is pos1=C, and so on. Output is stored as a csv to be read into R
and run a principal component analysis.'''

#Function to print header of the new matrix:
#pos1=R,pos1=H,pos1=D . . . pos8=F,pos8=Y,toxClass
def printHeader():
	residues='RHDSNCGVILFY' #not all residues present raw_data set, only have 12
	for i in range(1,9):
		for r in residues:
			sys.stdout.write("pos%d=%s," % (i, r))
	sys.stdout.write("%s\n" % "toxClass")
	

def main():
	residues='RHDSNCGVILFY' #not all residues present raw_data set, only have 12
	printHeader();
	sys.stdin.readline(); #read in and skip over header line in input
	for line in sys.stdin:
		columns = line.strip('\n').split(',')
		pepSeq = columns[0];
		toxClass = columns[2];
		#iterate over all 8 positions of the peptide
		for i in range(8):
			#then iterate over all amino acids in residues string
			for r in residues:
				if pepSeq[i] == r:
					#write out a 1, if res at position in
					#peptide matches the res
					sys.stdout.write("1,")
				else:
					#output 0 if it doesn't match
					sys.stdout.write("0,")
		sys.stdout.write("%s\n" % toxClass)

if __name__ == "__main__":
	main()
