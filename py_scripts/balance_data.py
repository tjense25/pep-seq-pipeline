#!/user/bin/ python
import sys
import random


'''Balancing peptide classes by replicating all of the motifs in the toxic and
antitoxic classes while taking a smaller random sample of the overrepresented
neutral data. This transformation allows all the classes to have the same order
of magnitude, so random forest learning models should not be biased to the
overrepresented calss'''

def main():
	REP_NUM = 3 #Number of times to repeat anti and toxic peps
	NEU_NUM	= 32000 #Number of neutral motifs to keep
	linenumber = 0
	neutral_lines = []
	for line in sys.stdin:
		#ignore the first line (only contains column names)
		if(linenumber == 0):
			linenumber += 1
			continue
		else:
			columns = line.strip('\n').split(',')
			toxicity = columns[8];
			if toxicity == 'neutral':
				neutral_lines.append(line)
			else:
				#Repeat antitoxic and toxic lines
				for i in range(REP_NUM):
					sys.stdout.write(line)
				
	#Take random sample out of the Neutral motifs and print them
	for i in random.sample(range(0, len(neutral_lines)), NEU_NUM):
		sys.stdout.write(neutral_lines[i])

if __name__ == "__main__":
	main()
