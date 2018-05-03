#include <string>
#include <vector>
#include "MotifSet.h"
#include "Peptide.h"
#include "Motif.h"

#ifndef PEP_LIBRARY_H
#define PEP_LIBRARY_H
class PepLibrary
{
	private:
		std::vector<Peptide*> peptides;

		static PepLibrary* SINGLETON;
		PepLibrary(); 
		~PepLibrary();
		PepLibrary(PepLibrary const&);
		PepLibrary& operator=(PepLibrary const&);

		
	public:
		static PepLibrary* getInstance();
		static void destroyInstance();
		void loadPepLibrary(std::string libFileName);
		std::vector<Peptide*> getPeptides();
		MotifSet createMotifSet(std::string motifFileName);
};
#endif
