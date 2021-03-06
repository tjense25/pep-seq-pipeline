#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <boost/lexical_cast.hpp>
#include "PepLibrary.h"
#include "MotifSet.h"
#include "MotifProxy.h"

MotifSet::MotifSet(std::string motifFileName) :
	motifSetAccuracy{0}, peptideCoverage{0}, toxCount{0} {
		this->outside = PepLibrary::getInstance()->getPeptides();
		initTotalTox();
		std::vector<IMotif*> motifs = loadMotifs(motifFileName);
		createMotifSet(motifs);
}

MotifSet::~MotifSet() {
	for ( auto motif : this->insideMotifs) {
		delete motif;
		motif = NULL;
	}
	this->insideMotifs.clear();
}

std::vector<IMotif*> MotifSet::loadMotifs(std::string motifFileName) {
	std::ifstream inFile;
	inFile.open(motifFileName);

	if(!inFile) {
		std::cerr << "ERROR: Invalid motif file " << motifFileName << std::endl;
		exit(1);
	}

	std::vector<IMotif*> motifs;
	std::string motifSeq;
	std::string toxicity;
	std::string value;
	int instances;
	int missclassified;
	double motifScore;
	getline(inFile, value); //read in header
	while (inFile >> value) {

		//check to see if we've reached the end of the motif list, break if we have
		if (value.length() >= 1 && value[0] == '#') continue;
		motifSeq = value;

		//skip over the next two columns as we only need the actual motif
		inFile >> toxicity;

		//getnumber of RF instances
		inFile >> value;
		instances = boost::lexical_cast<int>(value);

		//get NUmber of missclassified
		inFile >> value;
		missclassified = boost::lexical_cast<int>(value);

		//store MotifScore
		inFile >> value;
		motifScore = boost::lexical_cast<double>(value);

		motifs.push_back(new MotifProxy(motifSeq, toxicity, instances, missclassified, motifScore));
	}

	inFile.close();
	return motifs;
}

void MotifSet::initTotalTox() {
	int total = 0;
	for ( const auto &pep : this->outside) {
		if (pep->getToxClass() == ToxClass::TOXIC) total++;
	}
	this->totalTox = total;
}

double MotifSet::getMotifSetAccuracy() {
	return this->motifSetAccuracy;
}

double MotifSet::getPeptideCoverage() {
	return this->peptideCoverage;
}

double MotifSet::calculateF1(double x, double y) {
	if (x == 0 || y == 0) {
		return 0;
	}
	return 2*(x * y) / (x + y);
}

double MotifSet::getF1() {
	return calculateF1(this->motifSetAccuracy,
			   this->peptideCoverage);
}

std::vector<IMotif*> MotifSet::getMotifs() {
	return this->insideMotifs;
}

bool MotifSet::addMotif(IMotif* motif) {
	std::regex re (motif->getMotif());
	int tempToxCount = this->toxCount;
	std::vector<Peptide*> matchedPeps;
	for ( auto pep : this->outside ) {
		if (std::regex_match(pep->getSequence(), re)) {
			matchedPeps.push_back(pep);
			if (pep->getToxClass() == ToxClass::TOXIC) tempToxCount++;
		}
	}

	double tempMSA = double(tempToxCount) / (this->inside.size() + matchedPeps.size());
	double tempPC = double(tempToxCount) / (totalTox);
	if ( getF1() > calculateF1(tempMSA, tempPC)) return false;

	this->toxCount = tempToxCount;
	this->motifSetAccuracy = tempMSA;
	this->peptideCoverage = tempPC;

	for ( auto pep : matchedPeps) {
		this->inside.push_back(pep);
		this->outside.erase(std::find(outside.begin(), outside.end(), pep));
	}

	this->insideMotifs.push_back(motif);

	return true;
	
}

void MotifSet::createMotifSet(std::vector<IMotif*> motifs) {
	int poorMotifCount = 0;
	for ( auto motif : motifs) {
		if ( ++poorMotifCount > 5 || !addMotif(motif)) {
			//we've hit 5 bad motifs in a row	
			//Make greedy decision to stop searching as motifSet probs not getting better
			delete motif;
			motif = NULL;
		} else {
			poorMotifCount = 0;
		}

	}
	//Get maximum average rank
	double maxRank = (*std::max_element(insideMotifs.begin(), insideMotifs.end(), 
			[](IMotif* lhs, IMotif* rhs) {
				return lhs->getAverageRank() > rhs->getAverageRank();
			}))->getAverageRank();

	for ( auto motif : insideMotifs) {
		double oldScore = motif->getMotifScore();	
		motif->setMotifScore( oldScore*motif->getAverageRank() / maxRank);
	}

	//Sort motifs by the Updated MotifScore
	std::sort(insideMotifs.begin(), insideMotifs.end(), 
			[](IMotif* lhs, IMotif* rhs) {
				return lhs->getMotifScore() > rhs->getMotifScore();
			});
	
}

int MotifSet::getNumMotifs() {
	return this->insideMotifs.size();
}

std::string MotifSet::str() {
	std::ostringstream os;
	os << Motif::getHeader() << std::endl;
	for ( auto motif : insideMotifs) {
		os << motif->str() << std::endl;
	}	
	return os.str();
}

std::string MotifSet::results() {
	std::ostringstream os;
	os << "Motif Set Results:" << std::endl << std::endl;
	os << "Selected " << insideMotifs.size() << " Motifs:" << std::endl;
	os << "Motif Set Accuracy: " << this->motifSetAccuracy << std::endl;
	os << "Peptide Coverage: " << this->peptideCoverage << std::endl;
	os << "F1: " << this->getF1() << std::endl;
	return os.str();
}

void MotifSet::savePepsToFile(std::string pepFileName) {
	std::ofstream pepFile;
	pepFile.open(pepFileName);

	pepFile << "PepSeq,ToxScore,MotifSet" << std::endl;

	for (auto pep : inside) {
		pepFile << pep->str() << ",INSIDE" << std::endl;
	}

	for (auto pep : outside) {
		pepFile << pep->str() << ",OUTSIDE" << std::endl;
	}
		
	pepFile.close();
}

