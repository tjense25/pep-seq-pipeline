#include "Motif.h"
#include "PepLibrary.h"

Motif::Motif(std::string motif, std::string toxicity, int instances, int missclassified, double motifScore) : 
	IMotif::IMotif(motif, toxicity, instances, missclassified, motifScore),
	 re(motif), averageToxScore{0}, averageRank{0}, totalCount{0},
	toxCount{0}, neuCount{0}, antiCount{0} {

	std::vector<Peptide*> peps = PepLibrary::getInstance()->getPeptides();
	for ( int i = 0; i < peps.size(); i++) {
		if (addPeptide(peps[i])) {
			averageRank = (totalCount*averageRank + i) / (totalCount + 1);
			totalCount++;
		}
	}
		
}


bool Motif::addPeptide(Peptide* pep) {
	if (!std::regex_match(pep->getSequence(), re)) return false;

	matchedPeps.push_back(pep);
	switch(pep->getToxClass()) {
		case ToxClass::TOXIC: toxCount++; break;
		case ToxClass::NEUTRAL: neuCount++; break;
		case ToxClass::ANTITOXIC: antiCount++; break;
	}
	averageToxScore = (totalCount*averageToxScore + pep->getToxScore()) / (totalCount + 1);

	return true;
}

double Motif::getAverageToxScore() {
	return this->averageToxScore;
}

double Motif::getAverageRank() {
	return this->averageRank;
}

int Motif::getTotalCount() {
	return this->totalCount;
}

int Motif::getToxCount() {
	return this->toxCount;
}

int Motif::getNeuCount() {
	return this->neuCount;
}

int Motif::getAntiCount() {
	return this->antiCount;
}

std::vector<Peptide*> Motif::getMatchedPeps() {
	return this->matchedPeps;
}

std::string Motif::str() {
	ostringstream os (IMotif::str());
	os << this->toxCount << ","
	   << this->neuCount << ","
	   << this->antiCount << ","
	   << this->totalCount << ","
	   << this->averageToxScore << ","
	   << this->averageRank << ","
	   << this->motifScore << std::endl;
	return os.str();
}
