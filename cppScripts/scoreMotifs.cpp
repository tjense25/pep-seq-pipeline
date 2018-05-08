#include <iostream>
#include "PepLibrary.h"


int main(int argc, char** argv) {

	if (argc < 2) {
		std::cerr << "ERROR: Please specify path to input library and path to motifs list." << std::endl;
		exit(1);
	}

	PepLibrary* peptides = PepLibrary::getInstance();
	peptides->loadPepLibrary(argv[1]);
	MotifSet ms = peptides->createMotifSet(argv[2]);
	std::cout << ms.str() << std::endl;
	std::cerr << ms.results() << std::endl;
	ms.savePepsToFile("clusteredPeps.csv");
}
