#include <sstream>
#include "IMotif.h"

IMotif::IMotif(std::string motif, std::string toxicity, int instances, int missclassified, double motifScore) :
	motif{motif}, motifScore{motifScore}, instances{instances},
	missclassified{missclassified} {
		if (toxicity == "toxic")
			this->toxClass = ToxClass::TOXIC;
		else if (toxicity == "nuetral")
			this->toxClass = ToxClass::NEUTRAL;
		else
			this->toxClass = ToxClass::ANTITOXIC;
	}

std::string IMotif::getMotif() {
	return this->motif;
}

ToxClass IMotif::getToxClass() {
	return this->toxClass;
}

int IMotif::getNumInstances() {
	return this->instances;
}

int IMotif::getNumMissclassified() {
	return this->missclassified;
}

double IMotif::getMotifScore() {
	return this->motifScore;
}

void IMotif::setMotifScore(double motifScore) {
	this->motifScore = motifScore;
}

std::string IMotif::str() {
	std::ostringstream os;
	os << this->motif << "," 
	   << this->instances << "," 
	   << this->missclassified << ","
	   << this->motifScore << "," << std::endl;
	return os.str();
}

