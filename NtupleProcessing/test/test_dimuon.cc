
#include "config.h"
#ifndef STANDALONE
#include "Analysis/Core/interface/Muon.h"
#else 
#include "Muon.h"
#endif

#include "TFile.h"
#include "TChain.h"
#include "TString.h"

void test_dimuon()
{
	
	TString filename = "/Users/vk/software/HiggsAnalysis/files/data/ntuplemaking_singleMuon_Run2016B_PromptReco_v2_MINIAOD.root";
	TChain *chain = new TChain("ntuplemaker_H2DiMuonMaker/Events");
	chain->Add(filename);
	std::cout << "Total #Entries: "<< chain->GetEntries() << std::endl;

	using namespace analysis::core;
	analysis::core::Muons *muons1=NULL;
	chain->SetBranchAddress("Muons1", &muons1);
	for (int i=0; i<chain->GetEntries(); i++)
	{
		chain->GetEntry(i);
		std::cout << "#Muons1: " << muons1->size() << std::endl;
//		for (Muons::const_iterator it=muons1->begin(); it!=muon1->end(); ++it)
//		{
//			std::cout <<
//		}
	}
	return;
}

int main(int argc, char** argv)
{
	test_dimuon();
	return 0;
}
