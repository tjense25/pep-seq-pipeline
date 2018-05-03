#include <fstream>
#include <iostream>
#include <algorithm>
#include <boost/lexical_cast.hpp>
#include "PepLibrary.h"
#include "MotifSet.h"

PepLibrary* PepLibrary::SINGLETON = NULL;

PepLibrary::PepLibrary() {}

PepLibrary::~PepLibrary() {
	for ( auto pep : peptides) {
		delete pep;
		pep = NULL;
	}
	peptides.clear();
}

PepLibrary::PepLibrary(PepLibrary const& that) {}

PepLibrary& PepLibrary::operator=(PepLibrary const& that) {}

PepLibrary* PepLibrary::getInstance() {
	if (! SINGLETON) {
		SINGLETON = new PepLibrary();
	}
	return SINGLETON;
}

void PepLibrary::destroyInstance() {
	delete SINGLETON;
	SINGLETON = NULL;
}

std::vector<Peptide*> PepLibrary::getPeptides() {
	return this->peptides;
}

MotifSet PepLibrary::createMotifSet(std::string motifFileName) {
	MotifSet motifSet(motifFileName);
	return motifSet;
}

void PepLibrary::loadPepLibrary(std::string libFileName) {
	
	std::ifstream inFile;
	inFile.open(libFileName);	
	 
	//Check if InFile exists, if it doesn't stop program
	if(!inFile) {
		std::cerr << "Unable to open library file " << libFileName << std::endl;
		exit(1);
	}

	//Iterate through pepLibrary file and store pepSeqeunce in a string and the map
	std::string line = "";
	while (line == "" || line[0] == '%') {
		getline(inFile,line); //skip over comments at head of file
	}
	getline(inFile,line); //read in header
	while (getline(inFile, line)) {
		std::stringstream linestream(line);
		std::string sequence;
		std::string value;
		double toxScore;
		std::string toxClass;

		getline(linestream,sequence,',');

		getline(linestream,value,',');
		toxScore = boost::lexical_cast<double>(value);

		getline(linestream,toxClass,',');

		this->peptides.push_back(new Peptide(sequence, toxScore, toxClass));
	}

	std::sort(peptides.begin(), peptides.end(), 
			[](Peptide* a, Peptide* b) -> bool {
				return a->getSequence() != b->getSequence() ? a->getToxScore() > b->getToxScore() : a->getSequence() < b->getSequence();
			});

}
