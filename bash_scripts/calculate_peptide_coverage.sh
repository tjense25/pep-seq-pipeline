#!/bin/bash
set -e

MOTIFS_INPUT=$1
DATA_INPUT=$2
arff=$3

#Fucntion to find the  percentage of motifs that are covered by at least one of the motifs in the motif list 
function printPeptideCoverage {
	TOTAL_MOTIF="($(cat totalmotiftemp.txt))"
	COVERED_TOX=$(grep -E "$TOTAL_MOTIF" $1 | grep ',tox' | wc -l)
	echo "$2 $COVERED_TOX/$TOX_COUNT"

}

if [ $arff ]
then
	#Extract motifs from the motifs output file and convert to arff motif format by adding commas after each value
	MOTIFS=$(awk '{print $1,$2}' $MOTIFS_INPUT | python py_scripts/motif_to_arff_motif.py | awk '{print $1}')
else
	#Extract motifs from first column of motif output file and store into the Motifs varaible
	MOTIFS=$(awk '{print $1}' $MOTIFS_INPUT)
fi

#Store number of motifs that are toxic in original data as an env variable
export TOX_COUNT=$(grep ',tox' $DATA_INPUT | wc -l)
#Store number of motifs that are neutral in the original data as an env variable
export NEU_COUNT=$(grep ',neu' $DATA_INPUT | wc -l)
#Store number of motifs that are anti-toxic  in the original data as an env variable
export ANTI_COUNT=$(grep ',anti' $DATA_INPUT | wc -l)

COUNTER=1
for m in $MOTIFS
do
	#add Motif to the tempMotif file in regex format 
	if [ -f "totalmotiftemp.txt" ]
	then
		echo -n "$TOTALMOTIFS|(^$m)" >> totalmotiftemp.txt
	else
		echo -n "(^$m)" >> totalmotiftemp.txt
	fi
	printPeptideCoverage $DATA_INPUT $COUNTER
	COUNTER=$((COUNTER+1))
done

rm -f totalmotiftemp.txt
