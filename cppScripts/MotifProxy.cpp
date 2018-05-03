#include "MotifProxy.h"

MotifProxy::MotifProxy(std::string motif, double motifScore) :
	IMotif::IMotif(motif, motifScore), subject{NULL} 
		{}

MotifProxy::~MotifProxy() {
	delete subject;
	subject = NULL;
}

void MotifProxy::loadMotif() {
	subject = new Motif(IMotif::getMotif(), IMotif::getMotifScore());
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
