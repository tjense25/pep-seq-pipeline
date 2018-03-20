#!/bin/bash

#SBATCH --time=02:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=1G   # memory per CPU core
#SBATCH -J "PepseqPipeline"   # job name

# Compatibility variables for PBS. Delete if not needed.
export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`
export PBS_JOBID=$SLURM_JOB_ID
export PBS_O_WORKDIR="$SLURM_SUBMIT_DIR"
export PBS_QUEUE=batch

# Set the max number of threads to use for programs using OpenMP. Should be <=
# ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
module load r/3/3
module load jdk/1.8.0-121


# exit if any of the commands fail
set -e

#Set clean up function to be called if error occurs and program exits
#Removes all the temp files created in the bash script
function cleanUp {
	rm -rf temp/
	rm -f Rplots.pdf
	echo "ERROR: pep-seq pipeline script failed"
}
trap cleanUp ERR

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

#make temp directory to store temporary files
mkdir temp

#IF balance parameter was passed in, run python balance script on the input data
if [ $balance = true ] && [  ! $arff = true ]
then
	>&2 echo "Balancing Input Data . . . "
	cat $INPUT_FILE | python py_scripts/balance_data.py &> temp/balancedtemp.csv
	INPUT_FILE=temp/balancedtemp.csv
fi

#If passed in input file is not already an arff file, convert it to arff format
if [ ! $arff = true ]
then
	>&2 echo "Converting Input Data to Arff Format . . ."
	cat $INPUT_FILE | python py_scripts/convert_to_arff.py &> temp/arfftemp.arff
	INPUT_FILE=temp/arfftemp.arff
	rm -f temp/balancedtemp.csv
fi

#Run Weka's random forest classifiers on the arff file and store the tree output into temp.txt
>&2 echo "Running Random Forest Classification Algorithm on Data . . . "

#module load jdk/1.8.0-121 #(Uncomment this line if java not updated)

java -cp dependency_jars/weka.jar weka.classifiers.trees.RandomForest -U -B -P 50 -I 500 -no-cv -print -t $INPUT_FILE &> temp/foresttemp.txt
rm -f temp/arfftemp.arff

MOTIF_FILE=temp/motifs.txt
#Take the output of weka's Random Forest classifier and put it into our MotifFounder Algorithm
>&2 echo "Finding Motifs From Random Forest . . . "
if [ $anti = true ] && [ $neutral = true ]
then
	java -jar dependency_jars/MotifFinder.jar temp/foresttemp.txt -k $K &> temp/motifs.txt
elif [ $anti = true ]
then
	java -jar dependency_jars/MotifFinder.jar temp/foresttemp.txt -k $K -noneu &> temp/motifs.txt
elif [ $neutral = true ]
then
	java -jar dependency_jars/MotifFinder.jar temp/foresttemp.txt -k $K -noanti &> temp/motifs.txt
else
	java -jar dependency_jars/MotifFinder.jar temp/foresttemp.txt -k $K -noneu -noanti &> temp/motifs.txt
fi
rm -f temp/foresttemp.txt

#Calculate motif coverage and motif accuracy of the selected motifs and print
#these values out in the motif file that was created
>&2 echo "Calculating Motif Coverage of Selected Motifs . . ."

echo "##############################" >> temp/motifs.txt
echo "####TOXIC:" >> temp/motifs.txt
shell_scripts/calculate_peptide_coverage.sh temp/motifs.txt $RAW_FILE "tox" $arff>> temp/motifs.txt

if [ $neutral = true ]
then
	echo "####NEUTRAL:" >> temp/motifs.txt
	shell_scripts/calculate_peptide_coverage.sh temp/motifs.txt $RAW_FILE "neu" $arff >> temp/motifs.txt
fi 

if [ $anti = true ] 
then
	echo "####ANTITOXIC:" >> temp/motifs.txt
	shell_scripts/calculate_peptide_coverage.sh temp/motifs.txt $RAW_FILE "anti"  $arff >> temp/motifs.txt
fi
echo "##############################" >> temp/motifs.txt

#Calculate the counts of the motifs that were created that match what motifs
#and calcualte which motifs are statistically significant
>&2 echo "Calcualting motif counts and running chi-squared test of independece . . ."

#module load r/3/3 #(Include if R module not loaded)

shell_scripts/cluster_peps.sh temp/motifs.txt $RAW_FILE $arff > temp/motif_counts.csv
Rscript --vanilla R_scripts/chi_squared.R temp/motif_counts.csv &> /dev/null

>&2 echo "clustering motifs based on ToxSet . . . "
#Run motifSet T test for peps inside and outside of the motif set
shell_scripts/group_tox_scores.sh temp/motifs.txt $RAW_FILE "tox" > temp/motifSetPeps.tsv
Rscript --vanilla R_scripts/motifSetTtest.R temp/motifSetPeps.tsv &> /dev/null
rm -f temp/motifSetPeps.tsv
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
	mv temp/motifs.txt results/$OUTDIR
	mv temp/motif_counts.csv results/$OUTDIR
	mv MotifSetBoxPlot.jpg results/$OUTDIR
else
	cat temp/motifs.txt
	echo
	cat temp/motif_counts.csv
fi

rm -rf temp/
echo "Pep-seq pipeline executed successfully!"
exit 0
