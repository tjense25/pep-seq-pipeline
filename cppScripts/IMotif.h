#include <string>
#include <vector>
#include "Peptide.h"
#include "ToxClass.h"

#ifndef I_MOTIF_H
#define I_MOTIF_H
class IMotif {
	private:
		std::string motif;
		ToxClass toxClass;
		int instances;
		int missclassified;
		double motifScore;

	public:
		IMotif(std::string motif, std::string toxicity, int instances, int missclassified, double motifScore);
		std::string getMotif();
		double getMotifScore();
		ToxClass getToxClass();
		int getNumInstances();
		int getNumMissclassified();
		void setMotifScore(double motifScore);
		virtual std::string str();
		virtual double getAverageToxScore() = 0;
		virtual double getAverageRank() = 0;
		virtual int getTotalCount() = 0;
		virtual int getToxCount() = 0;
		virtual int getNeuCount() = 0;
		virtual int getAntiCount() = 0;
		virtual std::vector<Peptide*> getMatchedPeps() = 0;
};
#endif
