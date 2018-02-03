#!/bin/bash

#Check to see if there is at least one command line argument
if [ $# -lt 1 ]
then
	echo "ERROR: You must specify input file as command line argument"
	echo "$USAGE"
	exit 1
fi

INPUT_FILE=$1
shift

#Check if Input file is a valid file
if [ ! -f $INPUT_FILE ]
then
	echo "Input file $1 is not valid"
	echo "$USAGE"
	exit 1
fi

#Initialize parameter values
K=30

#Iterate through command line arguments and store data into variables
while [ $# -gt 0 ]
do
	ARG="$1"
	case "$ARG" in
		--arff) #data already in arff format
			arff=true
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
		-o) #Save output of the model to a new direcrtory in results
			output=true
			OUTDIR=$2
			shift
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
if [ $balance ] && [ ! $arff ]
then
	>&2 echo "Balancing Input Data . . . "
	cat $INPUT_FILE | python py_scripts/balance_data.py &> balancedtemp.csv
	INPUT_FILE=balancedtemp.csv
fi

#If passed in input file is not already an arff file, convert it to arff format
if [ ! $arff ]
then
	>&2 echo "Converting Input Data to Arff Format . . ."
	cat $INPUT_FILE | python py_scripts/convert_to_arff.py &> arfftemp.arff
	INPUT_FILE=arfftemp.arff
	#rm -f balancedtemp.csv
fi

#Run Weka's random forest classifiers on the arff file and store the tree output into temp.txt
>&2 echo "Running Random Forest Classification Algorithm on Data . . . "
java -cp dependency_jars/weka.jar weka.classifiers.trees.RandomForest -U -B -P 50 -I 500 -no-cv -print -t $INPUT_FILE &> foresttemp.txt
rm -f arfftemp.arff

#Take the output of weka's Random Forest classifier and put it into our MotifFounder Algorithm
>&2 echo "Finding Motifs From Random Forest . . . "
java -jar dependency_jars/MotifFinder.jar foresttemp.txt $K &> motifs.txt
rm -f foresttemp.txt

#If output is true, save the output file to the specifies directory in results. If it does not exist, create such a directory
#If output not specified print out the motifs data to standard output
if [ $output ]
then
	>&2 echo "Saving Output to results/$OUTDIR . . . "
	mkdir results/$OUTDIR 2> /dev/null
	mv motifs.txt results/$OUTDIR
else
	cat motifs.txt
	rm -f motifs.txt
fi

echo "Pep-seq pipeline executed successfully!"
exit 0
