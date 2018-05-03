#include <sstream>
#include "IMotif.h"

IMotif::IMotif(std::string motif, double motifScore) :
	motif{motif}, motifScore{motifScore} {}

std::string IMotif::getMotif() {
	return this->motif;
}

double IMotif::getMotifScore() {
	return this->motifScore;
}

void IMotif::setMotifScore(double motifScore) {
	this->motifScore = motifScore;
}

std::string IMotif::str() {
	std::ostringstream os;
	os << this->motif << "\t" << this->motifScore << std::endl;
	return os.str();
}

