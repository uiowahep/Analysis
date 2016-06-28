
//	
#ifndef STANDALONE
#include "Analysis/Core/interface/Muon.h"
#else 
#include "Muon.h"
#endif

#include "Streamer.h"
#include "Constants.h"

//	ROOT headers
#include "TFile.h"
#include "TChain.h"
#include "TString.h"

void synchronize(std::string const& inputname)
{
	using namespace analysis::core;
	using namespace analysis::processing;
	Streamer streamer(inputname, NTUPLEMAKER_NAME+"/Events");
	streamer.chainup();

	return;
}

int main(int argc, char** argv)
{
	if (argc<2 || argc>2)
	{
		std::cout << "Usage:" << std::endl
			<< "./synchronize <input file name>" << std::endl;
		return 1;
	}

	synchronize(argv[1]);
	return 0;
}
