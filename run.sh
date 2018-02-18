#!/bin/bash
# exit if any of the commands fail
#set -e

#Set clean up function to be called if error occurs and program exits
#Removes all the temp files created in the bash script
function cleanUp {
	rm -f balancedtemp.csv
	rm -f arfftemp.arff
	rm -f foresttemp.txt
	rm -f motifs.txt
	rm -f motif_counts.csv
	echo "ERROR: pep-seq pipeline script failed"
}
#trap cleanUp ERR

#Set usage 
USAGE="
USAGE:
./run.sh [input_file_name] [-options]

OPTIONS:
	--arff: data already in arff format, don't convert data
	--anti: also find antitoxic motifs
	--neutral: also find neutral motifs
	--help: print usage
	-b: balance the data before running machine learning classifier
	-k [number_of_motifs]: specify the number of motifs to find
	-o [out_dir]: specify directory in results/ in which to save the output files
"

#Check to see if there is at least one command line argument
if [ $# -lt 1 ]
then
	echo "ERROR: You must specify input file as command line argument"
	echo "$USAGE"
	exit 1
fi

RAW_FILE=$1
INPUT_FILE=$RAW_FILE
shift

#Check if Input file is a valid file
if [ ! -f $INPUT_FILE ]
then
	echo "ERROR: Input file $1 is not valid"
	echo "$USAGE"
	exit 1
fi

#Initialize parameter values
K=30
arff=false
anti=false
neutral=false
balance=false
output=false

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
		--help) #Print Usage message
			echo "Help Requested."
			echo "$USAGE"
			exit 1
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
if [ $balance = true ] && [  ! $arff = true ]
then
	>&2 echo "Balancing Input Data . . . "
	cat $INPUT_FILE | python py_scripts/balance_data.py &> balancedtemp.csv
	INPUT_FILE=balancedtemp.csv
fi

#If passed in input file is not already an arff file, convert it to arff format
if [ ! $arff = true ]
then
	>&2 echo "Converting Input Data to Arff Format . . ."
	cat $INPUT_FILE | python py_scripts/convert_to_arff.py &> arfftemp.arff
	INPUT_FILE=arfftemp.arff
	rm -f balancedtemp.csv
fi

#Run Weka's random forest classifiers on the arff file and store the tree output into temp.txt
>&2 echo "Running Random Forest Classification Algorithm on Data . . . "

#module load jdk/1.8.0-121 #(Uncomment this line if java not updated)

java -cp dependency_jars/weka.jar weka.classifiers.trees.RandomForest -U -B -P 50 -I 500 -no-cv -print -t $INPUT_FILE &> foresttemp.txt
rm -f arfftemp.arff

MOTIF_FILE=motifs.txt
#Take the output of weka's Random Forest classifier and put it into our MotifFounder Algorithm
>&2 echo "Finding Motifs From Random Forest . . . "
if [ $anti = true ] && [ $neutral = true ]
then
	java -jar dependency_jars/MotifFinder.jar foresttemp.txt -k $K &> motifs.txt
elif [ $anti = true ]
then
	java -jar dependency_jars/MotifFinder.jar foresttemp.txt -k $K -noneu &> motifs.txt
elif [ $neutral = true ]
then
	java -jar dependency_jars/MotifFinder.jar foresttemp.txt -k $K -noanti &> motifs.txt
else
	java -jar dependency_jars/MotifFinder.jar foresttemp.txt -k $K -noneu -noanti &> motifs.txt
fi
rm -f foresttemp.txt

#Calculate motif coverage and motif accuracy of the selected motifs and print
#these values out in the motif file that was created
>&2 echo "Calculating Motif Coverage of Selected Motifs . . ."

echo "##############################" >> motifs.txt
echo "####TOXIC:" >> motifs.txt
shell_scripts/calculate_peptide_coverage.sh motifs.txt $RAW_FILE "tox" $arff>> motifs.txt

if [ $neutral = true ]
then
	echo "####NEUTRAL:" >> motifs.txt
	shell_scripts/calculate_peptide_coverage.sh motifs.txt $RAW_FILE "neu" $arff >> motifs.txt
fi 

if [ $anti = true ] 
then
	echo "####ANTITOXIC:" >> motifs.txt
	shell_scripts/calculate_peptide_coverage.sh motifs.txt $RAW_FILE "anti"  $arff >> motifs.txt
fi
echo "##############################" >> motifs.txt

#Calculate the counts of the motifs that were created that match what motifs
#and calcualte which motifs are statistically significant
>&2 echo "Calcualting motif counts and running chi-squared test of independece . . ."

#module load r/3/3 #(Include if R module not loaded)

shell_scripts/cluster_peps.sh motifs.txt $RAW_FILE $arff > motif_counts.csv
Rscript --vanilla R_scripts/chi_squared.R motif_counts.csv

#Run motifSet T test for peps inside and outside of the motif set
shell_scripts/group_tox_scores.sh motifs.txt $RAW_FILE $arff > motifSetPeps.tsv
Rscript --vanilla R_scripts/motifSetTtest.R motifSetPeps.tsv
rm -f motifSetPeps.tsv
rm -f Rplots.pdf

#If output is true, save the output file to the specifies directory in results. If it does not exist, create such a directory
#If output not specified print out the motifs data to standard output
if [ $output = true ]
then
	>&2 echo "Saving Output to results/$OUTDIR . . . "
	if [ ! -d "results/$OUTDIR" ]
	then
		mkdir results/$OUTDIR
	fi
	mv motifs.txt results/$OUTDIR
	mv motif_counts.csv results/$OUTDIR
	mv MotifSetBoxPlot.jpg results/$OUTDIR
else
	cat motifs.txt
	echo
	cat motif_counts.csv
	rm -f motifs.txt
	rm -f motif_counts.csv
fi

echo "Pep-seq pipeline executed successfully!"
exit 0
