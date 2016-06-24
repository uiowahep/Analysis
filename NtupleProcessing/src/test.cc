#include <iostream>
#include <vector>

#include "TFile.h"
#include "TChain.h"

#include "Analysis/Core/interface/QIE10Frame.h"

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
		{
			for (int k=0; k<10; k++)
				std::cout << digis->at(j)._adc[k] << "  ";
			std::cout << std::endl;
			n++;
		}
		std::cout << std::endl;
		std::cout << n << std::endl;
	}

	std::cout << "Finished!" << std::endl;
}

