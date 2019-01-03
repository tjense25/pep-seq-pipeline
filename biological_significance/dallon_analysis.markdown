
# Analysis of Dallon's Data
## Introduction:

The data here are based on Figure 23 on page 53 of Emma Dallon's masters thesis.

In the experiment described by this figure, different "vectors" (small loops of DNA) containing different short peptides were inserted into E. coli strands, whose growth was then measured. Peptides/vectors which caused a decrease in growth rate were labeled as toxic. The majority of toxic peptides had a high positive charge and were hydrophobic (see Figure 22 on page 50). Peptides with these qualities are known as "canonical".

The experiment examined over 100,000 different peptides. However, only a few were examined in detail. The data here represent some of those peptides that were looked at most in detail.

## data and methods:

I scraped [this data](../biological_significance/dallons_peptides.csv) from Figure 23 of Emma Dallon's master's thesis. Bellow are some annotations for the data:

A3 was a non-toxic peptide.

B1-B6 were the 6 most toxic peptides. They followed the trend of high positive charge and hydrophobicity.

C1 was a "canonical" peptide, meaning it followed the trend of high positve charge and hydrophobicity (see page 52).

C2-C5 were "non-canonical" peptides.

*I added numbers to the letters (i.e. C**1**) left to right, top to bottom*

I then used the [motifFinder.py](../biological_significance/motifFinder.py) script to identify which motifs matched these peptides. Output from that step can be found in [dallon_intersect_our_motifs.csv](dallon_intersect_our_motifs.csv). The sequence motifs are not particularly pertinent to what I did next--rather, I was itnerested in the number of motifs that matched each peptide. 

I summarized the number of motifs that matched each peptide bellow:

| Sequence Name | Number of Motif Matches |
| ---- | ---- |
| A3:NonToxic   | 2                       |
| B1            | 3                       |
| B2            | 6                       |
| B3            | 3                       |
| B4            | 4                       |
| B5            | 4                       |
| B6            | 2                       |
| C1            | 8                       |
| C2            | 0                       |
| C3            | 1                       |
| C4            | 3                       |
| C5            | 0                       |
| total         | 34                      |

Note the number of motifs that matched canonical toxic peptides (B1-C1) was greater, on average, by **3.286** than non-canonical toxic peptides (C2-C5).

I wanted to quantify the probability of such an outcome occuring according to chance. Given the irregularity of the data, espeically the possible lack of statistical normality and the small sample size, a perumutation test seemed like the best option. The code to perform this test can be found [ADD LINK]().

![alt text](https://github.com/tjense25/pep-seq-pipeline/blob/master/biological_significance/PermutationTestDallonData.png "Permutation Test Null Distribution")

## Conclusions:

It makes a lot of sense that the motifs tend ot match "canonical" peptides--the twenty most toxic peptides are canonical. Furthermore, the majority of toxic peptides were canonical. *If we could get ahold of a list of non-canonical toxic peptides, and train on that, perhaps we would get a more interesting result.*


