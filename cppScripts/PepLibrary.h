#include <string>
#include <map>
#include "MotifSet.h"

#ifndef PEP_LIBRARY_H
#define PEP_LIBRARY_H
class PepLibrary
{
	private:
		std::string peptides;
		std::map<std::string, double> pepToToxicityMap;
	public:
		PepLibrary(std::string libFileName);
		std::string getPeptides();
		std::map<std::string, double> getPepToToxicityMap();
		double scoreMotif(std::string motif);
		MotifSet createMotifSet(std::vector<std::string> motifs);
};
#endif
