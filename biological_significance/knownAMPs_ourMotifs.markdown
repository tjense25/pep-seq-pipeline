# Known AMPs_ourMotifs

This document is a write up of the most important discoveries from the knownAMP_intersect_our_motifs.csv document.

## Most important Peptides/motifs:

### 1) Temporin-SHF : FFFLSRIF

**Number of matching motifs:** 5

**Mode of action:** Temporin-SHF targets the membranes of bacteria. It likely acts as a detergent, preferentially disrupting bacterial membranes likely by the ["carpet method"](https://www.researchgate.net/figure/A-model-of-a-carpet-like-mechanism-for-membrane-disruption-In-this-model-the-peptides_fig2_23981203).

**canonical:** The peptide is **highly canonical**; it has a net charge of +2, and, at 50% phenylalanine, has a high level of hydrophobicity.

**eye candy:** Figure 9 contains a nice 3-dimentional model of the conformation the peptide takes when interacting with a micel (a dissintigrated portion of a bacterial membrane).


![alt text](https://github.com/tjense25/pep-seq-pipeline/blob/master/biological_significance/dallon_analysis_number_2.png "")

**biological proof**: A variety of assays demonstate the antimicrobial nature of the peptide.

http://www.jbc.org/content/285/22/16880.full.pdf

--------
### 2)	pleurostrin : VRPYLVAF

**Number of matching motifs:** 3

**Mode of action:** The mode of action isn't explicitely given in the study. However, the authors report results from an assay in which ribosomal activity was reduced in response to pleurostrin. This finding is consistent with [other antifungal peptides](https://www.degruyter.com/view/j/bchm.2003.384.issue-5/bc.2003.090/bc.2003.090.xml), which also decrease the speed of ribosomal activity. This may indicate that pleurostrin interacts with ribosomes to decrease cell proliferation.

**canonical:** *no data given in the study*.

**eye candy:** Figure 4 shows side-by-side the effect of pleurostrin on strains of fungi that cause harm to crops. 

**biological proof**  One assay was used to determine antifungal activity, while a second assay was used to determine the peptides effect on ribosomal efficiency. This peptide is a little interesting because it is an *antifungal* peptide isolated *from a fungus!*

https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0196978105001816

--------

### 3) Cr‐ACP1 : WKLFDDGV

**Number of matching motifs:** 2

**Mode of action:** Seems to target DNA (based on *in vitro* binding studies)
 > The Trp2 residue was positioned between two hydrophilic branches and inserted into two nucleotide bases that assist in a “hydrophilic hug.” Coleman and Oakley [1980] observed that this might be an important factor in the recognition of single‐stranded nucleic acids by single‐strand binding proteins. The insertion of an aromatic amino acid side chain into an apurinic site might form the basis for the selective recognition of such sites in apurinic DNA [Behmoaras et al., 1981b]. As observed with the peptide isolated here, **the presence of hydrophobic residues surrounding cationic residues is observed in 80% of peptides with anticancer activity.** deposited on APD2 [Behmoaras et al., 1981a].

**canonical:** No (I think)

**eye candy:** Figure 4 is probably the best figure this analysis found.

**biological proof** Chemical modificiation (acetylation) weakened the anticancer and antimicrobial activity. Molecular modeling was used to demonstrate how the peptide could bind to DNA.

**fun fact:** This peptide comes from a plant in the Cycad Family, which means it is related to those plants that look like a cross between pineapples and palm trees that you see in depictions of dinosaur landscapes. 

https://onlinelibrary-wiley-com.erl.lib.byu.edu/doi/full/10.1002/jcb.23343 http://www.camp.bicnirrh.res.in/seqDisp.php?id=CAMPSQ2471

## General summary:

#### The mystery of bradykinins

Many of the peptides were *bradykinins*. This is a bit puzzling at first, since bradykinins are a class of inflamatory mediators that, in humans, bind to the B1 and B2 receptors to trigger various inflamatory responses--nothing to do with antimicrobial activity. The fourth intance of "bradykinin" in [this article](http://www.jbc.org/content/280/41/34832.full) was the closest thing I could find in terms of evidence in the literature that bradkykinins have antimicrobial activity.


#### Bacteroicins


## Additional Papers:

#### Mandal SM, Dey S, Mandal M, Sarkar S, Maria‐Neto S, Franco OL. 2009. Identification and structural insights of three novel antimicrobial peptides isolated from green coconut water. Peptides 30: 633–637.

[This paper](https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0196978108004968) identified 3 new antimicrobial peptides of length 8, 11, and 9. The peptides are non-canonical in nature. The paper has great molecular models of the peptides.

> The total net charge of Cn-AMP1 is +1, exhibiting a hydrophobic ratio of 44% and a boman index of 1.32 kcal/mol. **These properties, associated to the ability to form a helix**, as observed by helix wheel predictor (data not shown) and molecular modeling (Fig. 3) explain why this peptide was able to cause deleterious effects in bacteria. Moreover, **antibacterial activity of cationic peptides can also be modulated through modification in peptide's hydrophobicity or net charge** [14], [32]. Moreover, Cn-AMP2 and 3 showed acidic properties (Table 2) but similar hydrophobic rate suggesting that **cationic charges found in Cn-AMP1 is the main cause for higher antibacterial activity when compared to Cn-AMP2 and 3**. Ionic interaction probably is the initial attraction between AMPs and target cell, which occur through an electrostatic bonding between cationic peptide and negatively charged components present on the **outer bacterial envelope**, such as phosphate groups from lipopolysaccharides of Gram-negative bacteria or lipoteichoic acids exposed on Gram-positive bacteria surfaces. In the case of Gram-negative bacteria, **this peptide may also insert into the outer membrane structure in a process driven by hydrophobic interactions** and possibly involving refolding of the peptides into a membrane-associated structure [13]. However, the **antibacterial activity caused by acidic peptides such as Cn-AMP2 and 3 was a surprisingly data, since no basic exposed residue was observed. This result indicates that basic residues are truly important for bactericidal activity, since Cn-AMP1 showed a clear higher activity. Nevertheless these residues seems to be not essential, being the antimicrobial activity of Cn-AMP2 and 3 more related to hydrophobic amino acid residues as described above.**

[this database](https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0196978108004968) reports that only 9.2% of the toxic peptides they have on file have a net negative charge. Systein, glycine, serine, and alanine are the 4 most abundant amino acids in this database.

additional 8-mers I found

| sequence | canonical? | source
| ------ | ------- | -------
| YCSYTMEA | no | https://www-sciencedirect-com.erl.lib.byu.edu/science/article/pii/S0196978108004968


