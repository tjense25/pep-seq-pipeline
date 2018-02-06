#!/bin/bash
set -e

MOTIFS_INPUT=$1
DATA_INPUT=$2
arff=$3

function printPeptideCoverage {
	TOTAL_MOTIF="($(cat totalmotiftemp.txt))"
	grep -E "$TOTAL_MOTIF" $DATA_INPUT > 

}

if [ $arff ]
then
	MOTIFS=$(awk '{print $1,$2}' $MOTIFS_INPUT | python py_scripts/motif_to_arff_motif.py | awk '{print $1}')
else
	MOTIFS=$(awk '{print $1}' $MOTIFS_INPUT)
fi

COUNTER=1
for m in $MOTIFS
do
	if [ -f "totalmotiftemp.txt" ]
	then
		echo -n "$TOTALMOTIFS|(^$m)" >> totalmotiftemp.txt
	else
		echo -n "(^$m)" >> totalmotiftemp.txt
	fi
	printPeptideCoverage $DATA_INPUT $COUNTER
	$((COUNTER++))
	
done
