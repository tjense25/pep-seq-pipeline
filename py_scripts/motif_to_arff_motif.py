#!/usr/bin/pyton
import sys

'''Python script that takes in a list of normal regular expression motifs from
standard input and then converts them to arff motifs by adding commas after
every position in the motif and printing the new arff motif to std output'''

def convertToArffMotif(motif):
	arffMotif = []
	for i,r in enumerate(motif):
		arffMotif.append(r)
		if i != len(motif) - 1:
			arffMotif.append(',')
	return ''.join(arffMotif)

def main():
	for line in sys.stdin:
		if line.startswith("#"): return
		motif, toxicity = line.strip().split(' ')
		print(convertToArffMotif(motif),toxicity)

if __name__ == "__main__":
	main()
