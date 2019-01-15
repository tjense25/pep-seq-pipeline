# Known AMPs_ourMotifs

This document is a write up of the most important discoveries from the knownAMP_intersect_our_motifs.csv document.

## Most important Peptides/motifs:

### 1) Temporin-SHF : FFFLSRIF

**Number of matching motifs:** 5

**Mode of action:** Temporin-SHF targets the membranes of bacteria. It likely acts as a detergent, preferentially disrupting bacterial membranes likely by the ["carpet method"](https://www.researchgate.net/figure/A-model-of-a-carpet-like-mechanism-for-membrane-disruption-In-this-model-the-peptides_fig2_23981203).

**canonical:** The peptide is **highly canonical**; it has a net charge of +2, and, at 50% phenylalanine, has a high level of hydrophobicity.

**eye candy:** Figure 9 contains a nice 3-dimentional model of the conformation the peptide takes when interacting with a micel (a small bubble of surfactant). Information on the surfactant (DPC) used in this study can be found [here](https://pubs.acs.org/doi/10.1021/acs.langmuir.5b02077) and [here](https://en.wikipedia.org/wiki/Phosphocholine)


![alt text](https://github.com/tjense25/pep-seq-pipeline/blob/master/biological_significance/temporin-SHf.jpg "TEMPORIN-sHf model based on NMR spectroscopy")

**biological proof**: A variety of assays demonstate the antimicrobial nature of the peptide.

http://www.jbc.org/content/285/22/16880.full.pdf

--------
### 2)	pleurostrin : VRPYLVAF

**Number of matching motifs:** 3

**Mode of action:** The mode of action isn't explicitely given in the study. However, the authors report results from an assay in which ribosomal activity was reduced in response to pleurostrin. This finding is consistent with [other antifungal peptides](https://www.degruyter.com/view/j/bchm.2003.384.issue-5/bc.2003.090/bc.2003.090.xml), which also decrease the speed of ribosomal activity. This may indicate that pleurostrin interacts with ribosomes to decrease cell proliferation.

**canonical:** *no data given in the study*.

**eye candy:** Figure 4 shows side-by-side the effect of pleurostrin on strains of fungi that cause harm to crops.

![alt text](https://github.com/tjense25/pep-seq-pipeline/blob/master/biological_significance/pleurostrin_on_p_piricola.jpg "Pleurostrin fungisidal assay on the fungus *P. piricola*")

**biological proof**  One assay was used to determine antifungal activity, while a second assay was used to determine the peptides effect on ribosomal efficiency. This peptide is a little interesting because it is an *antifungal* peptide isolated *from a fungus!*

https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0196978105001816



--------

### 3) Cr‐ACP1 : WKLFDDGV

**Number of matching motifs:** 2

**Mode of action:** Seems to target DNA (based on *in vitro* binding studies)
 > The Trp2 residue was positioned between two hydrophilic branches and inserted into two nucleotide bases that assist in a “hydrophilic hug.” Coleman and Oakley [1980] observed that this might be an important factor in the recognition of single‐stranded nucleic acids by single‐strand binding proteins. The insertion of an aromatic amino acid side chain into an apurinic site might form the basis for the selective recognition of such sites in apurinic DNA [Behmoaras et al., 1981b]. As observed with the peptide isolated here, **the presence of hydrophobic residues surrounding cationic residues is observed in 80% of peptides with anticancer activity.** deposited on APD2 [Behmoaras et al., 1981a].

**canonical:** No (charge of -1 at normal pH, *hydrophobic*, with a hydropathy score of -1.4)

**eye candy:** Figure 4 is probably the best figure this analysis found.

![alt text](https://github.com/tjense25/pep-seq-pipeline/blob/master/biological_significance/Cr‐ACP1.jpg "Molecular Dynamics (MD) simulation of Cr-ACP1 binding to DNA.")

**biological proof** Chemical modificiation (acetylation) weakened the anticancer and antimicrobial activity. Molecular modeling was used to demonstrate how the peptide could bind to DNA.

**fun fact:** This peptide comes from a plant in the Cycad Family, which means it is related to those plants that look like a cross between pineapples and palm trees that you see in depictions of dinosaur landscapes. 

https://onlinelibrary-wiley-com.erl.lib.byu.edu/doi/full/10.1002/jcb.23343 http://www.camp.bicnirrh.res.in/seqDisp.php?id=CAMPSQ2471

### 4) Cn-AMP3 : YCSYTMEA

*This peptide is not found in the "known_AMP.csv" or "known_AMP_intersect_our_motifs.csv" documents. Rather, I (happily) found this peptide while searching through the literature. I found the number of matching motifs using the same process as above, running motifFinder.py against this peptide and the list of motifs from the first round of the pep-seq pipeline.*

**Number of matching motifs:** 1 (Y..Y....)

**Mode of action:** probably through membrane interactions. However, the mechanism may be novel. Most membrane-interacting bacteriocides are basic, while this peptide was acidic. To quote the paper:

>  Despite of most antimicrobial peptides found in plants have been characterized as cationic [19], few organisms have shown the presence of acidic bactericidal peptides with included chilli peppers [7], snakes [31] and several others.

**canonical:** Yes and no. The peptide has a charge of -1, which is unusual. But it also has hydrophobic regions. A similar, related compound (Cn-AMP1) had a positive charge and hydrophobic regions and had much stronger antimicrobial activity. The authors think that the combination of hydrophobic regions and basicity/positive are what cause the three peptides discussed in the paper to be antimicrobial.

**biological proof:** Bacteriocidal activity was tested against four strains of infectious bacteria. MIC represented the concentration at which the peptide's presence inhibited bacterial growth. below is the data from a figure that summarized the effectiveness of each peptide. The Cn-AMP1 and Cn-AMP2 were both more effective, though Cn-AMP3 was the only 8-mer.

Pathogenic bacteria	| Cn-AMP1 MIC (μg ml−1)	| Cn-AMP2 MIC (μg ml−1)	| **Cn-AMP3 MIC (μg ml−1)**
----- | ----- | ----- | -----
E. coli	| 82	| 170	| **302**
B. subtilis	| 76	| 150	| **257**
P. aeruginosa	| 79	| 169	| **259**
S. aureus	| 80	| 170	| **274**

Again, to quote the paper:

> This result indicates that basic residues are truly important for bactericidal activity, since Cn-AMP1 showed a clear higher activity. Nevertheless these residues seems to be not essential, being the antimicrobial activity of Cn-AMP2 and 3 more related to hydrophobic amino acid residues as described above.**

**Eye candy:** ![alt text](https://github.com/tjense25/pep-seq-pipeline/blob/master/biological_significance/Cn-AMP3.jpg "Molecular Dynamics (MD) simulation of Cn-AMP3 (bottom one)")

**Fun fact:** the peptide was derived from *Cocos nucifera*, aka green coconot water!

Here is some of this data in table form:

| sequence | canonical? | number of matching motifs | name | source 
| ------ | ------- | ----- | ----- | -------
| YCSYTMEA | sort of | 1 | Cn-AMP3 | https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0196978108004968

Mandal SM, Dey S, Mandal M, Sarkar S, Maria‐Neto S, Franco OL. 2009. Identification and structural insights of three novel antimicrobial peptides isolated from green coconut water. Peptides 30: 633–637.

https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0196978108004968

## General Notes:

#### The mystery of bradykinins

Many of the peptides were *bradykinins*. This is a bit puzzling at first, since bradykinins are a class of inflamatory mediators that, in humans, bind to the B1 and B2 receptors to trigger various inflamatory responses--nothing to do with antimicrobial activity. The fourth intance of "bradykinin" in [this article](http://www.jbc.org/content/280/41/34832.full) was the closest thing I could find in terms of evidence in the literature that bradkykinins have antimicrobial activity.

#### Bacteroicins

Several of the compounds were *bacteroicins*. Bacterioicins are compounds produced *by bacteria* that are active against other types of bacteria.

#### Charge/hydrophobicity and toxicity

[this database](https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0196978108004968) reports that only 9.2% of the toxic peptides they have on file have a net negative charge. Systein, glycine, serine, and alanine are the 4 most abundant amino acids in this database.

[the paper](https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0196978108004968) from which Cn-AMP3 came speculated about the importance of having high charge and hydrophobicity for a peptide to interact with bacterial membranes.

