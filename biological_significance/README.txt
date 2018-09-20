Hypothesis: the toxic peptides interact with essential proteins in E. coli

What do we have to work with?
  - Toxic Peptides
      - There were 47175 toxic peptides.
      - Some motifs generated from these peptides had no demonstratable toxicity in and of themselves
        - The nature of toxicity in motifs is more nuanced than our algorithm for finding them so far
        - OR, the experiment was not representitive of the toxic nature of the motifs.
  - Proteins in E. coli
      - There are 4.5-5,000 genes in E. coli
      - Thee are 9,115 resolved proteins and 2,205 ligands on the Protein Data Base for E. coli (there is some redundancy)
        - http://www.rcsb.org/pdb/results/results.do?tabtoshow=Current&qrid=B0FE5209 
      - Good news is, most of the protome of E. coli is resolved!
      - Bad news is, I'm not sure if those 'resolved' protein structures are entirely accurate. Conformation may chane in different conditions.
      
 Conclusion:
   - Testing every toxic peptide against every protein is probably impossible right now
      - plus, there is nothing elegant about doing that. We want to explain WHY certain GROUPS are toxic.
      - We may want to choose a subset of the toxic peptides to work with
  - We could generate a sub-set of 'interesting' toxic peptides
      - For example, we may want to look at all the peptides with a particular motif (not neccesarily a 'toxic' one, either).
          - we could then find all the peptides with that motif that are toxic, and put them in group "A"
          - we could then find all the peptides with that motif that are NOT toxic, and put them in group "B"
          - We could then try to characterise the 3-dimentional strucutre of the peptides in A and compare them to B
              - We could use that comparison to determine toxic SHAPES rather than MOTIFS
   - Once we have toxic SHAPES, we could take a group of toxic peptides with the same shape/motif, and try it against the E. coli proteome
      - We need to determine how much we can get done with autodoc
      
It would be nice if:
  - We could find a list of the most important genes in E. coli and test those proteins first
  - We could run a few more biology experiments to validate our bioinformatical data
      - The only problem is that Emma Dallon moved schools and they are phasing out that project!
  
What is our goal?
  - we have a few options:
      - determine toxic motifs
      - determine toxic shapes
      - determine the mechanism of toxicity
      - determine the potential impact on humans

I wonder. . . 
  - If we can find the causitive protein, it would be really cool if we could find a homologue of the protein in H. sapiens to determine its toxicity on humans.
