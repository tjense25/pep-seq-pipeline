#!/bin/bash
set -e

MOTIFS_INPUT=$1
DATA_INPUT=$2
arff=$3

if [ $arff ]
then
	MOTIFS=$(awk '{print $1,$2}' $MOTIFS_INPUT | python py_scripts/motif_to_arff_motif.py | awk '{print $1}')
else
	MOTIFS=$(awk '{print $1}' $MOTIFS_INPUT)
fi

rm -f motifcluster.txt

for m in $MOTIFS
do
	echo "MOTIF: $m" >> motifcluster.txt
	grep "^$m" $DATA_INPUT >> motifcluster.txt
	echo "" >> motifcluster.txt
done
