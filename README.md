# Pep-seq Pipeline
<h2> Automated pipeline to run all pep-seq code on simulated and raw data<h2>

***

<h2> Pipeline Components </h2>

The pep-seq pipeline puts together the 7 essential steps of finding a toxic
motifs in a peptide library into a single program. It relies heavily on the 
code and data found in our original pep-seq repo as well as the code we wrote
for the MotifFinder algorithm, but with a bash script and added stats tests which 
combines all the parts together and a more organized design. 

There are 7 essential steps to our pipeline:

1.	Filter original protein library to try to reduce noise in the data
2. 	Format the filtered protein library into an atribute relation file format to
	be used for further steps of the pipeline.
3.	Run the arff file through a Random Forest machine learning classifier
	using weka code
4.	Take the resulting the output of the Random Forest model and pipe it
	into our MotifFinder from a decision forest java code. Which will ouput
	a list of possible motifs which are most likely to be
	toxic/antitoxic/etc.
5.	Use the probable motifs found to cluster the data into groups peptides
	groups that match those motifs
6. 	Use motif finding algorithms to find a consensus motif for each of the 
	clusters
7.	Run statistical test on these consensus motifs  to test if expression of 
	that motif causes a statistically significant difference in antimicrobial 
	activity of the peptide

***

<h3>1. FILTER: </h3>

Filter uses a python script to convert the original peptide library data into
a new format that contains a nomializtion of the toxicity class. Its purpose is
two-fold

1. 	Get rid of data that has too much noise. The two main ways that we filter
	are by first checking to see if the toxicity score differs
	significantly between the two replicates. And second by tossing out
	replicates that contained too few data points in their sample. Peptides
	were also filtered out if the contianed one of the 8 underrepresented
	amino acid residues.
2.	Classify each of the peptide sequences as either toxic, antitoxic, or
	neutral. We calculated a toxicity score by adding up the replicates in
	the reference sample and dividing by sum of the replicates in the
	induced sample. We then found the std. deviation and all peptides
	greater than one std deviation were classified toxic, all those less
	than one std. deviation classified antitoxic, and those in between were
	classified as neutral.

<h3>2. FORMAT:  </h3>

After the data has been filtered and classified. We convert the new filtered
input data into the correct file format to be ran through a machine learning
classifier. Weka requires that data be in an attribute relation file format
(arff). And Step two of the pipeline runs the data through a python script to
format this data correctly.

An optional step before formatting is to balance the data set. Based on how we
defined toxic, antitoxic, and neutral classes, the nuetral peptides were
significantly overrepresented. This can cause high bias in the machine learning
classifiers (in the worst case, the learner classifies all peptides as
neutral).To prevent this we can balance the data which will overrepresent data
from the two minority classes and take a smaller random sample out of the
neutral data. Use -b on the command line to run this balance script

<h3>3. CLASSIFY: </h3>

After the data has been formatted into an arff file. It is put into a Random
Forest machine learning classifier so we can try to learn the patterns present
in the data. To do this we use the Random Forest classifier in Weka
(weka.classifiers.trees.RandomForest). We chose to use 500 iterations, a
bagging size of 50%, random choice if there is a tie, and to allow for
unclassified instances because these gave us the highest true positive and
lowest false positive scores for our training set. The complete weka command we
used is below:

```bash
java -cp dependency_jars/weka.jar weka.classifiers.trees.RandomForest -U -B -P 50 -I 500 -print -no-cv  -t $INPUT_FILE 
```

If the data is already in arff format, you can skip to this step by including 
the command line parameter --arff. It is also possible to run a normal decision
tree instead of a random Forest by including the parameter --j48 which will run
a j48 classifier instead of a random Forest. We recommend using random Forest because
it helps prevent overfitting of the training set. But with extremely large datasets
a j48 classifier will run much faster and be much more manageable.

<h3>4. FIND PARTIAL MOTIFS: </h3>

To find partial motifs we take the output of the Random Forest (or j48)
classifier and traverse the tree to recreate the motifs the learner used to
correctly classify the peptides. We use the MotifFinderDecisionTree java
program that we created to do this. Full documentation on this program can be
found at this link: <a href="https://github.com/tjense25/MotifFinderDecisionTree"> https://github.com/tjense25/MotifFinderDecisionTree </a> 

The general idea is that the program will traverse through all 500 decision
trees and store at each node a growing motif based on how the tree was split
and pruned. Once it gets to a leaf node we have found a partial or local motif
which it will store into a data structure with information about how many
peptides were classified at that leaf and how many were classified incorrectly.
It uses this classified/misclassified counts to score the motif then order all
the motifs and print out the toxic motifs with the highest scores. These
represent the motifs which are most likely to be the most toxic in the proetin
library

<h3>5. CLUSTER: </h3>

The clustering phase of the pipeline takes the results from the motif finder
and does meta analysis on the motifs as well as clustering the original data
based on those motifs. The motifs are treated as regular expressions and all
peptides that match that regex will clustered together based on that motif, and
this list of clustered data will be used to find consensus motifs later in the
pipeline.

The metaanalysis performed at this step calculates the peptide coverage and
motif accuracy of the motifs the motif finder found and also calcualtes chi
squared test of independence on the counts of motifs to see if they
statistically significantly fall into one of the classifications. This allows
us to say that a motif is statistically toxic or antitoxic, etc. 

Peptide coverage is a percent from 0 to 1, and represents what percentage of
the peptides have at least one motif matching to them in the classified motif
set. The closer the value is to one, the better the motifs are at capturing the
data. Motif accuracy is what percentage of peptides matched by the classified
motifs are actually of a matching class. There is usually a tradeoff between
peptide coverage and motif accuracy, for instance the trivial regex '........'
which would literally match everything would have a 1.0 peptide coverage, but
since it matches everything it would have terrible motif accuracy- close to
'.33'. On the other side a highly specialized toxic motif '.F.FY.RF' may have
motif accuracy score of 1.0: every single motif that matches this regex is
toxic. However, it will only have a peptide coverage score of 0.03: meaning
only 3% of all toxic motifs are matched by this pattern.

We want a set of toxic motifs that maximizes both of these scores, so a set of
motifs which will match ALL peptides (have good peptide coverage), and not
match any antitoxic or neutral peptides (have good motif accuracy).

<h3>6. FIND CONSENSUS MOTIFS: </h3>

<h3>7. TEST SIGNIFICANCE: </h3>

***

<h2> USAGE: </h2>

To run the pep-seq pipeline execute the run.sh script while in the pep-seq-pipeline main directory:

```bash
./run.sh [input_file_name] [-options]
```

<h3>OPTIONS:</h3>

	<b>--arff</b>: data already in arff format, don not convert data
	<b>--anti:</b> also find antitoxic motifs <br>
	<b>--neutral:</b> also find neutral motifs <br>
	<b>--help:</b> print usage <br>
	<b>-b:</b> balance the data before running machine learning classifier <br>
	<b>-k [number_of_motifs]:</b> specify the number of motifs to find <br>
	<b>-o [out_dir]:</b> specify directy in results/ to save output files <br>

***

<h2> OUTPUT: </h2>

The pep-seq pipeline either prints ouput directly to the screen or saves output files in a
directory in the result folder if the -o option is specific as a command parameter.
 
