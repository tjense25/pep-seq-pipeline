#include "IMotif.h"
#include "Peptide.h"

#ifndef MOTIF_SET_H
#define MOTIF_SET_H
class MotifSet
{
	private:
		std::vector<Peptide*> outside;
		std::vector<Peptide*> inside;
		std::vector<IMotif*> insideMotifs;
		double motifSetAccuracy;
		double peptideCoverage;
		int toxCount;
		int totalTox;
		void createMotifSet(std::vector<IMotif*> motifs);
		bool addMotif(IMotif* motif);
		void initTotalTox();
		std::vector<IMotif*> loadMotifs(std::string motifFileName);
		double calculateF1(double x, double y);
	public:
		MotifSet(std::string motifFileName);
		~MotifSet();
		double getMotifSetAccuracy();
		double getPeptideCoverage();
		double getF1();
		int getNumMotifs();
		std::vector<IMotif*> getMotifs();
		std::string str();
};
#endif

