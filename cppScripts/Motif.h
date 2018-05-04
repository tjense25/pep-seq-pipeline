#include <regex>
#include "IMotif.h"

#ifndef MOTIF_H
#define MOTIF_H
class Motif : public IMotif {
	private:
		std::regex re;
		double averageToxScore;
		double averageRank;
		int totalCount;
		int toxCount;
		int neuCount;
		int antiCount;
		std::vector<Peptide*> matchedPeps;
		bool addPeptide(Peptide* pep);

	public:
		Motif(std::string motif, std::string toxicity, int instances, int missclassified, double motifScore);
		static std::string getHeader();
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
