#!/bin/bash

MOTIFS_INPUT=$1
DATA_INPUT=$2
CLASS=$3

#Get the total motif set from the motif output file 
MOTIFS=$(grep "\\s$CLASS" $MOTIFS_INPUT | awk '{print $1}')

for m in $MOTIFS
do
	#add Motif to the tempMotif file in regex format 
	if [ -f "totalmotiftemp.txt" ]
	then
		echo -n "|$m" >> totalmotiftemp.txt
	else
		echo -n "$m" >> totalmotiftemp.txt
	fi
done

#Store the regex for all the motifs in varaible from the text file
MOTIF_SET_REGEX="($(cat totalmotiftemp.txt))"
rm -rf totalmotiftemp.txt

echo "Motif	ToxScore	MotifSet"

#Print out the motif, tox score, and INSIDE for peptides in the motif set
#sed commands changes csv to a tsv, tail gets data all data except first row
sed 's/,/\t/g' $DATA_INPUT | tail -n+2 |awk "\$1 ~ /$MOTIF_SET_REGEX/ {print \$1, \$2, \"INSIDE\";}" | sed 's/ /\t/g'

#Print out the motif, tox score, and OUTSIDE for all peptides outside motif set
sed 's/,/\t/g' $DATA_INPUT | tail -n+2 |awk "\$1 !~ /$MOTIF_SET_REGEX/ {print \$1, \$2, \"OUTSIDE\";}" | sed 's/ /\t/g'

exit 0
