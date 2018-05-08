#include <string>
#include "ToxClass.h"

#ifndef PEPTIDE_H
#define PEPTIDE_H
class Peptide {
	private:
		std::string sequence;
		double toxScore;
		ToxClass toxClass;
	public:
		Peptide(std::string sequence, double toxScore, std::string toxClass);
		std::string getSequence();
		ToxClass getToxClass();
		double getToxScore();
		std::string str();
};
#endif
