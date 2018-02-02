#!/bin/bash

INPUT_FILE=$1
shift

#Check if Input file is a valid file
if [ ! -f $INPUT_FILE ]
then
	echo "Input file $1 is not valid"
	echo "$USAGE"
	exit 1
fi

#Iterate through command line arguments and store data into variables
while [ $# -gt 0 ]
do
	ARG="$1"
	case "$ARG" in
		--arff) #data already in arff format
			arff=true
			;;
		-T)  #Specifies test file to run in the machine learning algorithm
			test_file=true
			TEST=$2
			shift
			;;
		-k) #Specify number of motifs to test (default is 30)
			K=$2
			shift
			;;
		--anti) #Also find antitoxic motifs
			anti=true
			;;
		--neutral) #Also find neutral motifs
			neutral=true
			;;
		-b) #Balance the data before running random forest classifier
			balance=true
			;;
		*) #Default branch, print argument not valid and usage then exit
			echo "Not a valid argument: $1"
			echo "$USAGE"
			exit 1
			;;
	esac
	shift
done

#IF balance parameter was passed in, run python balance script on the input data
if [ balance && ! arff ]
then
	python py_scripts/balance_data.py $INPUT_FILE &> temp.txt
	INPUT_FILE=temp.txt
fi

#If passed in input file is not already an arff file, convert it to arff format
if [ ! arff ]
then
	python py_scripts/convert_to_arff.py $INPUT_FILE &> temp.txt
	INPUT_FILE=temp.txt
fi

exit 0
