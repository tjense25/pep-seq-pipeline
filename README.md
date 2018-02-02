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

<h2> INPUT: </h2>




 
