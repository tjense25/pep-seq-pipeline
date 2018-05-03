#include <string>
#include <vector>
#include "Peptide.h"

#ifndef I_MOTIF_H
#define I_MOTIF_H
class IMotif {
	private:
		std::string motif;
		double motifScore;

	public:
		IMotif(std::string motif, double motifScore);
		std::string getMotif();
		double getMotifScore();
		void setMotifScore(double motifScore);
		std::string str();
		virtual double getAverageToxScore() = 0;
		virtual double getAverageRank() = 0;
		virtual int getTotalCount() = 0;
		virtual int getToxCount() = 0;
		virtual int getNeuCount() = 0;
		virtual int getAntiCount() = 0;
		virtual std::vector<Peptide*> getMatchedPeps() = 0;
};
#endif
