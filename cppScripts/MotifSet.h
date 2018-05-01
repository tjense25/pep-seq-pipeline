#include <string>
#include <vector>
#include <map>

#ifndef MOTIF_SET_H
#define MOTIF_SET_H
class MotifSet
{
	private:
		std::map<std::string, double> outside;
		std::map<std::string, double> inside;
		std::vector<std::string> insideMotifs;
		double motifSetAccuracy;
		double peptideCoverage;
		int toxCount;
		int totalTox;
		void createMotifSet(std::vector<std::string> motifs);
		bool addMotif(std::string motif);
		void initTotalTox();
		double calculateF1(double x, double y);
	public:
		MotifSet(std::map<std::string, double> peptides, std::vector<std::string> motifs);
		double getMotifSetAccuracy();
		double getPeptideCoverage();
		double getF1();
		std::vector<std::string> getMotifs();
};
#endif

