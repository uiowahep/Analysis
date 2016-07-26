
#ifdef STANDALONE

#include "TFile.h"
#include "TH1D.h"
#include "TChain.h"
#include "TString.h"
#include "TBufferJSON.h"

#include <iostream>
#include <signal.h>
#include <string>

#include "boost/program_options.hpp"

#include "Event.h"
#include "Streamer.h"

namespace po = boost::program_options;

/*
 *	Global
 */
bool __continueRunning = true;
std::string __inputfile;
std::string __outputfile;
std::string __ntuplemakername = "ntuplemaker_H2DiMuonMaker";

using namespace analysis::core;
using namespace analysis::processing;

/*
 *	Functions 
 */
void sigHandler(int sig)
{
	std::cout << "### Signal: " << sig << " caught. Exiting..." << std::endl;
	__continueRunning = false;
}

void convert()
{
	Streamer s(__inputfile, __ntuplemakername+"/Events");
	s.chainup();

	Event *event=NULL;
	s._chain->SetBranchAddress("Event", &event);
	uint32_t numEntries = s._chain->GetEntries();
	ofstream out(__outputfile);
	out << "[";
	for (uint32_t i=0; i<numEntries && __continueRunning; i++)
	{
		if (i%1000==0)
			std::cout << "### Processing Event " << i << std::endl;
		s._chain->GetEntry(i);
//		h->FillRandom("gaus", 10000);
//		TString json = TBufferJSON::ConvertToJSON(h);
		TString json = TBufferJSON::ConvertToJSON(event, TClass::GetClass("analysis::core::Event"));
		out << json.Data() << ","<< std::endl; 
//		std::cout << json.Data() << std::endl;
	}
	out << "]";

	return;
}

int main(int argc, char** argv)
{
	signal(SIGABRT, &sigHandler);
	signal(SIGTERM, &sigHandler);
	signal(SIGINT, &sigHandler);

	po::options_description desc("Allowed Program Options");
	desc.add_options()
		("help", "produce help messgaes")
		("input", po::value<std::string>(), "a file specifying all the ROOT files to process")
		("output", po::value<std::string>(), "a filename specifying the output file")
	;
	po::variables_map vm;
	po::store(po::parse_command_line(argc, argv, desc), vm);
	po::notify(vm);
	if (vm.count("help") || argc<2)
	{
		std::cout << desc << std::endl;
		return 1;
	}

	__inputfile = vm["input"].as<std::string>();
	__outputfile = vm["output"].as<std::string>();

	convert();

	return 0;
}

#endif
