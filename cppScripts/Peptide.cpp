#include <sstream>
#include "Peptide.h"


Peptide::Peptide(std::string sequence, double toxScore, std::string toxClass) :
	sequence{sequence}, toxScore{toxScore} {
		if (toxClass == "toxic") 
			this->toxClass = ToxClass::TOXIC;
		else if (toxClass == "neutral") 
			this->toxClass = ToxClass::NEUTRAL;
		else
			this->toxClass = ToxClass::ANTITOXIC;
}

std::string Peptide::getSequence() {
	return this->sequence;
}

ToxClass Peptide::getToxClass() {
	return this->toxClass;
}

double Peptide::getToxScore() {
	return this->toxScore;
}

std::string Peptide::str() {
	std::ostringstream os;
	os << this->sequence << "," << this->toxScore;
	return os.str();
}
