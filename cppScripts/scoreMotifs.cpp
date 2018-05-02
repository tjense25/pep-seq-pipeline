#include <utility>
#include <fstream>
#include <sstream>
#include <map>
#include <iostream>
#include <vector>
#include <algorithm>
#include "PepLibrary.h"

std::vector<std::string> loadMotifs(std::string motifFileName) {
	std::ifstream inFile;
	inFile.open(motifFileName);

	if(!inFile) {
		std::cerr << "ERROR: Invalid motif file " << motifFileName << std::endl;
		exit(1);
	}

	std::vector<std::string> motifs;
	std::string motif;
	getline(inFile, motif);
	while (inFile >> motif) {

		//check to see if we've reached the end of the motif list, break if we have
		if (motif.length() >= 1 && motif[0] == '#') break;

		motifs.push_back(motif);

		//skip over the next three columns as we only need the actual motif
		for (int i = 0; i < 3; i++) {
			inFile >> motif;
		}
	}

	return motifs;
}

int main(int argc, char** argv) {

	if (argc < 2) {
		std::cerr << "ERROR: Please specify path to input library and path to motifs list." << std::endl;
	}

	PepLibrary peptides(argv[1]);
	std::vector<std::string> motifs = loadMotifs(argv[2]);
	MotifSet ms = peptides.createMotifSet(motifs);
	std::cout << "Selected " << ms.getNumMotifs() << " motifs:" << std::endl;
	motifs = ms.getMotifs();
	std::vector<std::pair<double, std::string>> scoredMotifs;
	for ( auto motif : motifs) {
		scoredMotifs.push_back(std::pair<double, std::string>(peptides.scoreMotif(motif),motif));
	}	

	std::sort(scoredMotifs.begin(), scoredMotifs.end());

	for (const auto &myPair : scoredMotifs) {
		std::cout << myPair.second << "\t" << myPair.first << std::endl;
	}

	std::cout << "Motif Set Accuracy: " << ms.getMotifSetAccuracy() << std::endl;
	std::cout << "Peptide Coverage: " << ms.getPeptideCoverage() << std::endl;
	std::cout << "F1: " << ms.getF1() << std::endl;
	return 0;
}
