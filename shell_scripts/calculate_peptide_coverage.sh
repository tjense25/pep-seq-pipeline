#!/bin/bash
set -e

function cleanUp {
	rm -f totalmotiftemp.txt
	echo "ERROR: could not finish calculate_peptide_coverage script"
}
trap cleanUp ERR

#Fucntion to find the  percentage of motifs that are covered by at least one of the motifs in the motif list 
function printPeptideCoverage {
	TOTAL_MOTIF="($(cat totalmotiftemp.txt))"
	COVERED_TOX=$(grep -E "$TOTAL_MOTIF" $DATA_INPUT | grep ",$CLASS"  | wc -l)
	echo "$COUNTER $COVERED_TOX/$TOX_COUNT"

}

if [ $# -lt 4 ] 
then
	echo "ERROR:
	USAGE: ./calcualte_peptide_coverage.sh [MOTIFS_INPUT_FILE] [ORIGINAL_DATA_FILE] [TOXICITY CLASS] [arff: true or false
	"
	exit 1
fi

MOTIFS_INPUT=$1
DATA_INPUT=$2
CLASS=$3
arff=$4

if [ $arff = "true" ]
then
	#Extract motifs from the motifs output file and convert to arff motif format by adding commas after each value
	MOTIFS=$(grep "\\s$CLASS" $MOTIFS_INPUT | awk '{print $1}' | python py_scripts/motif_to_arff_motif.py)
else
	#Extract motifs from first column of motif output file and store into the Motifs varaible
	MOTIFS=$(grep "\\s$CLASS" $MOTIFS_INPUT | awk '{print $1}')
fi

#COUNTER=1
for m in $MOTIFS
do
	#add Motif to the tempMotif file in regex format 
	if [ -f "totalmotiftemp.txt" ]
	then
		echo -n "|(^$m)" >> totalmotiftemp.txt
	else
		echo -n "(^$m)" >> totalmotiftemp.txt
	fi
	#printPeptideCoverage $DATA_INPUT $COUNTER
	#COUNTER=$((COUNTER+1))
done

TOTAL_MOTIF="($(cat totalmotiftemp.txt))"
grep -E "$TOTAL_MOTIF" $DATA_INPUT  > totalmotiftemp.txt

#Total number of motifs that match one of the specified motifs in input file
TOTAL_MOTIF_COUNT=$(cat totalmotiftemp.txt | wc -l)

#OUT OF THE PEPTIDES THAT MATCH ONE OF THE TOTAL MOTIFS
#CALCUALTE HOW MANY ARE TOX/NEUTRAL/ANTITOX
MOTIF_CLASS_COUNT=$(grep ",$CLASS" totalmotiftemp.txt | wc -l)

#Store number of motifs in the original data of the given toxicity class
CLASS_COUNT=$(grep ",$CLASS" $DATA_INPUT | wc -l)

#Pep coverage: the percentage of peptides in the original dataset that match one of the toxic motifs found
PEP_COVERAGE=$(bc -l <<< "$MOTIF_CLASS_COUNT/$CLASS_COUNT")

#Motif accuracy: the percentage of the motifs that match the motifs that are actually toxic
MOTIF_ACCURACY=$(bc -l <<< "$MOTIF_CLASS_COUNT/$TOTAL_MOTIF_COUNT")

echo "# PEP. COVERAGE: $PEP_COVERAGE"
echo "# MOT. ACCURACY: $MOTIF_ACCURACY"

rm -f totalmotiftemp.txt

exit 0
