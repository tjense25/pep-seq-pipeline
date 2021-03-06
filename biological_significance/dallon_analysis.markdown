
# Analysis of Dallon's Data
## Introduction:

This file presents my (Brian's) analysis of several of the figures in Emma Dallon's master's thesis.

In the experiment described by these figures, different "vectors" (small loops of DNA) containing different short peptides were inserted into E. coli strands, whose growth was then measured. Peptides/vectors which caused a decrease in growth rate were labeled as toxic. The majority of toxic peptides had a high positive charge and were hydrophobic (see Figure 22 on page 50). Peptides with these qualities are known as "canonical".

## data and methods:

The experiment examined over 100,000 different peptides. However, only a few were examined in detail, and data regarding that analysis was presented in figure 23 on page 50. I scraped [this data](../biological_significance/dallons_in_depth_peptides.csv) from that figure. Bellow are some annotations for the data:

A3 was a non-toxic peptide.

B1-B6 were the 6 most toxic peptides. They followed the trend of high positive charge and hydrophobicity.

C1 was a "canonical" peptide, meaning it followed the trend of high positve charge and hydrophobicity (see page 52).

C2-C5 were "non-canonical" peptides.

*I added numbers to the letters (i.e. C**1**) left to right, top to bottom*

I then used the [motifFinder.py](../biological_significance/motifFinder.py) script on the data I obtained from figure 23 to identify which motifs matched the peptides represented there. Output from that step can be found in [dallon_intersect_our_motifs.csv](dallon_intersect_our_motifs.csv). The actual motifs are not particularly pertinent to what I did next--rather, I was interested in the number of motifs that matched each peptide. 

I summarized the number of motifs that matched each peptide bellow:

| Sequence Name | Number of Motif Matches |
| ---- | ---- |
| A3:NonToxic   | 2                       |
| B1            | 3                       |
| B2            | 6                       |
| B3            | 3                       |
| B4            | 4                       |
| B5            | 5                       |
| B6            | 2                       |
| C1            | 8                       |
| C2            | 0                       |
| C3            | 1                       |
| C4            | 3                       |
| C5            | 0                       |
| total         | 34                      |

Note the number of motifs that matched canonical toxic peptides (B1-C1) was greater, on average, by **3.286** than non-canonical toxic peptides (C2-C5).

I wanted to quantify the probability of such an outcome occuring according to chance. Given the irregularity of the data, espeically the possible lack of statistical normality and the small sample size, a perumutation test seemed like the best option. The code to perform this test can be found [here](../biological_significance/permutationTest.R).

The test reported an empirical **p-value of 0.03247**, sufficient evidence to **reject the null hypothesis that the two populations have an equal likelihood of matching a motif**. This may indicate that the pipeline tends to find motifs that give canonical attributes (positive charge and hydrophobicity) to the peptide.

Bellow you will find a graphical representation of how that empirical p-value was obtained. The permutation test generated a pseudo-distribution for the null hypothesis by changing the assignment of what was considered canonical and non-canonical. This process was repeated 100,000 times to produce the distribution bellow. Bars in red represent the percent of differences that were as-or-more extreme than the actual difference observed in the data.

![alt text](https://github.com/tjense25/pep-seq-pipeline/blob/master/biological_significance/dallon_analysis_round_1.png "First Permutation Test Null Distribution")

The sample size for this experiment was relatively small, so I decided to repeat it again, expanding the canonical peptides used from the 6 most toxic peptides, to the 44 most toxic peptides. The [sequences of these peptides](../biological_significance/most_toxic.csv) were obtained from table 6 on page 49 of Emma's thesis.

Most of the 44 most toxic peptides were non canonical. However, one (#18) was clearly non-canonical, and in the analysis was grouped as such. Peptide #33 had high hydrophobicity, but a negative charge, making it neither clearly canonical or non-canonical, so it was excluded from the analysis.

I used the [motifFinder.py](../biological_significance/motifFinder.py) script on , which produced [the following output file](../biological_significance/most_toxic_intersect_our_motifs.csv). I then summarized that data bellow:

| Sequence Name | Number of Motif Matches |
| ---- | ---- |
| 1             | 3                       |
| 2             | 6                       |
| 3             | 3                       |
| 4             | 4                       |
| 5             | 5                       |
| 6             | 2                       |
| 7             | 3                       |
| 8             | 6                       |
| 9             | 6                       |
| 10            | 7                       |
| 11            | 3                       |
| 12            | 1                       |
| 13            | 5                       |
| 14            | 2                       |
| 15            | 6                       |
| 16            | 6                       |
| 17            | 0                       |
| 18 *nonCanonical*  | 0                       |
| 19            | 2                       |
| 20            | 8                       |
| 21            | 7                       |
| 22            | 2                       |
| 23            | 3                       |
| 24            | 8                       |
| 25            | 1                       |
| 26            | 3                       |
| 27            | 6                       |
| 28            | 8                       |
| 29            | 7                       |
| 30            | 5                       |
| 31            | 9                       |
| 32            | 3                       |
| 33 *negative charge* | 3                |
| 34            | 11                      |
| 35            | 0                       |
| 36            | 1                       |
| 37            | 4                       |
| 38            | 0                       |
| 39            | 0                       |
| 40            | 2                       |
| 41            | 0                       |
| 42            | 2                       |
| 43            | 7                       |
| 44            | 7                       |
| total         | 174                     |

Note that the mean number of matches in the canonical peptides from this table was **3.342857 higher** than the mean number of matches in the non canonical peptides (number 18 from this table, and C2-C5 from the table above).

I ran a [modified version of the same R script](../biological_significance/permutationTest2.R) I used before, incorperating this new data. 

The test reported an empirical **p-value of 0.0144**, which was again sufficient evidence to **reject the null hypothesis that the two populations have an equal likelihood of matching a motif**.

As before, I generated a figure to demonstrate how the p-value was obtained:

![alt text](https://github.com/tjense25/pep-seq-pipeline/blob/master/biological_significance/dallon_analysis_number_2.png "Second Permutation Test Null Distribution")

A larger sample size of non canonical toxic peptides would be preferable, but **the data seem to indicate that the motifs found by the pipeline tend to be associated with canonical properties in the matching peptide.**

## Conclusions:

It makes sense that the motifs tend ot match "canonical" peptides, as the majority of toxic peptides (which were used to train the random forest) were canonical. *If we could obtain a list of non-canonical toxic peptides to train on, perhaps we would get a more inteesting result.*

While these data suggest that the current implementation of PepSeq tends to *favor* canonical motifs, PepSeq does not do so exclusively. There were motifs that matched the non-canonical peptides. *It would be extremely interesting to filter out the motifs that add charge and hydrophobicity to the peptide in order to identify putative non-canonical motifs.* The tests outlined here could be repeated in order to validate that the filtered motifs tend to match non-canonical peptides. 


