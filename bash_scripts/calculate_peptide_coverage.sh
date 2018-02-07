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


MOTIFS_INPUT=$1
DATA_INPUT=$2
CLASS=$3

arff=true

if [ $arff ]
then
	#Extract motifs from the motifs output file and convert to arff motif format by adding commas after each value
	MOTIFS=$(awk '{print $1,$2}' $MOTIFS_INPUT | python py_scripts/motif_to_arff_motif.py | grep "$CLASS" | awk '{print $1}')
else
	#Extract motifs from first column of motif output file and store into the Motifs varaible
	MOTIFS=$(grep $MOTIFS_INPUT | awk '{print $1}')
fi

#Store number of motifs in the original data of the given toxicity class
CLASS_COUNT=$(grep ",$CLASS" $DATA_INPUT | wc -l)

#COUNTER=1
for m in $MOTIFS
do
	#add Motif to the tempMotif file in regex format 
	if [ -f "totalmotiftemp.txt" ]
	then
		echo -n "$TOTALMOTIFS|(^$m)" >> totalmotiftemp.txt
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

#Pep coverage: the percentage of peptides in the original dataset that match one of the toxic motifs found
PEP_COVERAGE=$(bc -l <<< "$MOTIF_CLASS_COUNT/$CLASS_COUNT")

#Motif accuracy: the percentage of the motifs that match the motifs that are actually toxic
MOTIF_ACCURACY=$(bc -l <<< "$MOTIF_CLASS_COUNT/$TOTAL_MOTIF_COUNT")

echo "PEPTIDE COVERAGE: $PEP_COVERAGE"
echo "MOTIF ACCURACY: $MOTIF_ACCURACY"

rm -f totalmotiftemp.txt
