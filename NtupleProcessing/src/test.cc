#include <iostream>
#include <vector>

#include "TFile.h"
#include "TChain.h"

#include "/Users/vk/software/HCALDQM/Analysis/Core/interface/QIE10Frame.h"

void test()
{
	TChain *chain = new TChain("maker/QIE10Maker/Events");
	chain->Add("/Users/vk/software/HCALDQM/Analysis/data/ntuples/test.root");
	std::cout << chain->GetEntries() << std::endl;

	analysis::core::QIE10Digis *digis = NULL;
	chain->SetBranchAddress("QIE10Digis", &digis);
	
	for (int i=0; i<chain->GetEntries(); i++)
	{
		chain->GetEntry(i);
		int n = 0;
		for (uint32_t j=0; j<digis->size(); j++)
			n++;
		std::cout << n << std::endl;
	}

	std::cout << "Finished!" << std::endl;
}

