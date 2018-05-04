//Lazy Loading proxy for the MotifClass,
//Instantiating a motif object requires iterating over the entire pepLibrary,
//so we only want to instantiate the motifs that are actually in the motifSet
#include "IMotif.h"
#include "Motif.h"

#ifndef MOTIF_PROXY_H
#define MOTIF_PROXY_H
class MotifProxy : public IMotif {
	private:
		Motif* subject;
		void loadMotif();

	public:
		MotifProxy(std::string motif, std::string toxicity, int instances, int missclassified, double motifScore);
		~MotifProxy();
		std::string str();
		double getAverageToxScore();
		double getAverageRank();
		int getTotalCount();
		int getToxCount();
		int getNeuCount();
		int getAntiCount();
		std::vector<Peptide*> getMatchedPeps();
};
#endif

