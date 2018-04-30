#include<string>
#include<map>

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
		double scoreMotif(std::string motif);
};
#endif
