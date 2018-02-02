#! usr/bin/env python
import sys

residues = 'RHKDESTNQCGPAVILFMYW'
if len(sys.argv) == 2 and sys.argv[1].endswith('.csv'):
	InFile = open(sys.argv[1], 'rU')
	outFileName = sys.argv[1].strip('.csv') + '.arff'
	OutFile = open(outFileName, 'w')
	OutFile.write('@relation pep-seq\n')
	res_nominal = '{R,H,D,S,N,C,G,V,I,L,F,Y}'
	for i in range(1, 9):
		OutFile.write('@attribute pos%d %s\n' % (i, res_nominal))
	OutFile.write('@attribute toxicity  {toxic, neutral, anti-toxic}\n')
	OutFile.write('@data\n')
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
				OutFile.write(r + ',')
			OutFile.write('%s\n' % toxicity)
	InFile.close();
	OutFile.close();
else:
	print("ERROR")
