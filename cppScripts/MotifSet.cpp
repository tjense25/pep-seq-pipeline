#include <regex>
#include <sstream>
#include "MotifSet.h"

MotifSet::MotifSet(std::map<std::string, double> peptides, std::vector<std::string> motifs) :
	outside{peptides}, motifSetAccuracy{0}, peptideCoverage{0}, toxCount{0} {
		initTotalTox();
		createMotifSet(motifs);
	}

void MotifSet::initTotalTox() {
	int total;
	for ( const auto &pep : this->outside) {
		if (pep.second < -0.3) total++;
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
	return 2*(x + y) / (x*y);
}

double MotifSet::getF1() {
	return calculateF1(this->motifSetAccuracy,
			   this->peptideCoverage);
}

std::vector<std::string> MotifSet::getMotifs() {
	return this->insideMotifs;
}

bool MotifSet::addMotif(std::string motif) {
	std::regex re (motif);
	int tempToxCount = this->toxCount;
	std::map<std::string, double> matchedPeps;
	for ( const auto &pep : this->outside ) {
		if (std::regex_match(pep.first, re)) {
			matchedPeps.emplace(pep.first, pep.second);
			if (pep.second < -0.3) tempToxCount++;
		}
	}

	double tempMSA = double(tempToxCount) / (this->inside.size() + matchedPeps.size());
	double tempPC = double(tempToxCount) / (totalTox);
	if ( getF1() > calculateF1(tempMSA, tempPC)) return false;

	this->toxCount = tempToxCount;
	this->motifSetAccuracy = tempMSA;
	this->peptideCoverage = tempPC;

	for ( const auto &pep : matchedPeps) {
		this->inside.emplace(pep.first, pep.second);
		this->outside.erase(pep.first);
	}

	return true;
	
}

void MotifSet::createMotifSet(std::vector<std::string> motifs) {
	int poorMotifCount = 0;
	for ( auto motif : motifs) {
		if (!addMotif(motif) && ++poorMotifCount > 5) {
			break; 
			//we've hit 5 bad motifs in a row	
			//Make greedy decision to stop searching as motifSet probs not getting better
		} else {
			poorMotifCount = 0;
		}

	}
}

