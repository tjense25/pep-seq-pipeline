#!/bin/bash
set -e

function cleanUp {
	rm -f cluster_temp.txt
	echo "Failed to run motif_count shell script"
}
trap cleanUp ERR

MOTIFS_INPUT=$1
DATA_INPUT=$2
arff=$3

if [ $arff = true ]
then
	MOTIFS=$(awk '{print $1,$2}' $MOTIFS_INPUT | python py_scripts/motif_to_arff_motif.py | awk '{print $1}')
else
	MOTIFS=$(awk '{print $1}' $MOTIFS_INPUT)
fi

echo "motif,toxic,neutral,anti-tox"

for m in $MOTIFS
do
	grep "^$m" $DATA_INPUT > cluster_temp.txt
	TOX_COUNT=$(grep ',tox' cluster_temp.txt | wc -l)
	NEU_COUNT=$(grep ',neu' cluster_temp.txt | wc -l)
	ANTI_COUNT=$(grep ',anti' cluster_temp.txt | wc -l)
	motif=$(sed 's/,//g' <<< $m)
	echo "$motif,$TOX_COUNT,$NEU_COUNT,$ANTI_COUNT"
done

rm -f cluster_temp.txt

exit 0
