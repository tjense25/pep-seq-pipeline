cmake_minimum_required(VERSION 3.6)
project(ScoreMotifs CXX)

add_executable(scoreMotifs scoreMotifs.cpp Peptide.cpp IMotif.cpp Motif.cpp
	MotifProxy.cpp MotifSet.cpp PepLibrary.cpp)

set_target_properties(scoreMotifs PROPERTIES
	CXX_STANDARD 14
	CXX_EXTENSIONS FALSE
	CXX_STANDARD_REQUIRED TRUE
)
