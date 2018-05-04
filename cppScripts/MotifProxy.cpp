#include "MotifProxy.h"

MotifProxy::MotifProxy(std::string motif, std::string toxicity, int instances, int missclassified, double motifScore) :
	IMotif::IMotif(motif, toxicity, instances, missclassified, motifScore), 
	subject{NULL} {}

MotifProxy::~MotifProxy() {
	delete subject;
	subject = NULL;
}

void MotifProxy::loadMotif() {
	IMotif* obj = this;
	std::string toxicity;
	switch(getToxClass()) {
		case ToxClass::TOXIC: toxicity="toxic"; break;
		case ToxClass::NEUTRAL: toxicity="neutral"; break;
		case ToxClass::ANTITOXIC: toxicity="anti-toxic"; break;
	}
	subject = new Motif(getMotif(), toxicity, getNumInstances(), getNumMissclassified(), getMotifScore());
}
	
double MotifProxy::getAverageToxScore() {
	if (! subject) loadMotif();
	return subject->getAverageToxScore();
}

double MotifProxy::getAverageRank() {
	if (! subject) loadMotif();
	return subject->getAverageRank();
}

int MotifProxy::getTotalCount() {
	if (! subject) loadMotif();
	return subject->getTotalCount();
}

int MotifProxy::getToxCount() {
	if (! subject) loadMotif();
	return subject->getToxCount();
}
	
int MotifProxy::getNeuCount() {
	if (! subject) loadMotif();
	return subject->getNeuCount();
}

int MotifProxy::getAntiCount() {
	if (! subject) loadMotif();
	return subject->getAntiCount();
}

std::vector<Peptide*> MotifProxy::getMatchedPeps() {
	if (! subject) loadMotif();
	return subject->getMatchedPeps();
}

std::string MotifProxy::str() {
	if (! subject) loadMotif();
	return subject->str();
}
