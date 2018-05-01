#include <fstream>
#include <regex>
#include <sstream>
#include <map>
#include <iostream>
#include <boost/lexical_cast.hpp>
#include "PepLibrary.h"


double PepLibrary::scoreMotif(std::string motif) { 
	std::regex re (motif);

	double total = 0;
	int count = 0;

	for ( const auto &myPair : this->pepToToxicityMap) {
		if (std::regex_match(myPair.first, re) ) {
			total += myPair.second;
			count++;
		}
	}

	return total / count;
}

std::map<std::string, double> PepLibrary::getPepToToxicityMap() {
	return this->pepToToxicityMap;
}

std::string PepLibrary::getPeptides() {
	return this->peptides;
}

PepLibrary::PepLibrary(std::string libFileName) {
	
	std::ifstream inFile;
	inFile.open(libFileName);	
	 
	//Check if InFile exists, if it doesn't stop program
	if(!inFile) {
		std::cerr << "Unable to open library file " << libFileName << std::endl;
		exit(1);
	}

	//Iterate through pepLibrary file and store pepSeqeunce in a string and the map
	std::ostringstream peps;
	std::string line;
	getline(inFile,line);
	while (getline(inFile, line)) {
		std::stringstream linestream(line);
		std::string value;
		double toxScore;
		std::string pepseq;

		getline(linestream,value,',');
		pepseq = value;

		getline(linestream,value,',');
		toxScore = boost::lexical_cast<double>(value);

		this->pepToToxicityMap.emplace(pepseq, toxScore);	
	}

	this->peptides = peps.str();
}
