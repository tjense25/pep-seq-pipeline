#! usr/bin/env python
import sys

def classifyT_I(T_I):
	if T_I < 0.4:
		return 'toxic'
	elif T_I < 0.8:
		return 'mild-toxic'
	elif T_I < 1.2:
		return 'neutral'
	elif T_I < 1.6:
		return 'mild-anti-toxic'
	else:
		return 'anti-toxic'

def isGoodSeq(pepseq):
	for res in 'AWPMTQEK':
		if res in pepseq:
			return False

	return True

if len(sys.argv) >= 2:
	filter_threshold = 50
	if len(sys.argv) == 3:
		filter_threshold = int(sys.argv[2])
	InFile = open(sys.argv[1], 'rU')
	outFileName = sys.argv[1].strip('.csv') + ('_formatted%d.csv' % filter_threshold)
	OutFile = open(outFileName, 'w')
	OutFile.write('pep-seq\tT_I\tToxicity\n')
	linenumber = 0
	for line in InFile:
		if(linenumber == 0):
			linenumber += 1
			continue;
		else:
			columns = line.strip('\n').split(',')
			pepseq = (columns[1])[1:]
			ref_count = int(columns[4]) + int(columns[5]) + 1
			induced_count = int(columns[6]) + int(columns[7]) + 1
			T_I = float(induced_count)/ref_count
			perc_diff = float(induced_count - ref_count)/ref_count
			if ref_count >= filter_threshold and isGoodSeq(pepseq) and perc_diff < 5:
				OutFile.write(pepseq + ',')
				OutFile.write('%f,' % (perc_diff))
				OutFile.write(classifyT_I(T_I) + '\n')
				
	InFile.close()
	OutFile.close()
