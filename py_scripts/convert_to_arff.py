#! usr/bin/env python
import sys

def main():
	if len(sys.argv) == 2:
		InFile = open(sys.argv[1], 'rU')
		sys.stdout.write('@relation pep-seq\n')
		residues = 'RHKDESTNQCGPAVILFMYW'
		res_nominal = '{R,H,D,S,N,C,G,V,I,L,F,Y}'
		for i in range(1, 9):
			sys.stdout.write('@attribute pos%d %s\n' % (i, res_nominal))
		sys.stdout.write('@attribute toxicity  {toxic, neutral, anti-toxic}\n')
		sys.stdout.write('@data\n')
		linenumber = 0
		for line in InFile:
			if(linenumber == 0):
				linenumber += 1
				continue
			else:
				columns = line.strip('\n').split(',')
				pepseq = columns[0];
				toxicity = columns[8];
				for r in pepseq:
					if r not in residues:
						r = "?"
					sys.stdout.write(r + ',')
				sys.stdout.write('%s\n' % toxicity)
		InFile.close();
	else:
		print("ERROR: INPUT DATA FILE NOT GIVEN")

if __name__ == "__main__":
	main()
