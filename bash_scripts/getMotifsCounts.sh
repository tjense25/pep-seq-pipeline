#!/bin/bash

MOTIFS=$(awk '{print $1,$2}' $1 | python py_scripts/motif_to_arff_motif.py)

for m in $MOTIFS
do
	echo "$m"
done
