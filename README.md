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

<h4>1. FILTER: </h4>

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

<h4>2. FORMAT:  </h4>

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

<h4>3. CLASSIFY: </h4>

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

<h4>4. FIND PARTIAL MOTIFS: </h4>

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

<h4>5. CLUSTER: </h4>

<h4>6. FIND CONSENSUS MOTIFS: </h4>

<h5>7. TEST SIGNIFICANCE: </h5>




 
