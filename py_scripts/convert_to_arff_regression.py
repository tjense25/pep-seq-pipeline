#! usr/bin/env python
import sys 

def main():
	sys.stdout.write('@relation pep-seq\n') 
	residues = 'RHKDESTNQCGPAVILFMYW' #Not all residues present because some missing from our original dataset
	res_nominal = '{R,H,D,S,N,C,G,V,I,L,F,Y}' #used for raw_data
	#res_nominal = '{A,C,D,E,F,G,H,I,K,L,M,N,P,Q,R,S,T,V,W,Y}' #to be used for simulated data that has all residues 

	#Write out each of the positions and residues as an attribute
	for i in range(1, 9):
		sys.stdout.write('@attribute pos%d %s\n' % (i, res_nominal))

	#Write to stdout the toxicity class attribute
	sys.stdout.write('@attribute toxicity NUMERIC\n')
	sys.stdout.write('@data\n')
	for line in sys.stdin:
		columns = line.strip('\n').split(',')
		pep_sequence = columns[0];
		toxicity = columns[1];
		#for each position in pep sequence output the Residue seperated by commas
		for r in pep_sequence:
			if r not in residues:
				r = "?"
			sys.stdout.write(r + ',')
		sys.stdout.write('%s\n' % toxicity)
		
if __name__ == "__main__":
	main()
