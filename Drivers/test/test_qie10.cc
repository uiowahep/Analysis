#ifdef STANDALONE

#include <iostream>
#include <vector>

#include "TFile.h"
#include "TChain.h"

#include "QIE10Frame.h"

void test_qie10()
{
	TChain *chain = new TChain("maker/Events");
	chain->Add("/Users/vk/software/HiggsAnalysis/files/data/qie10/test.root");
	std::cout << chain->GetEntries() << std::endl;

	analysis::core::QIE10Digis *digis = NULL;
	chain->SetBranchAddress("QIE10Digis", &digis);
	
	for (int i=0; i<chain->GetEntries(); i++)
	{
		chain->GetEntry(i);
		int n = 0;
		std::cout << "#digis=" << digis->size() << std::endl;
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

int main(int argc, char** argv)
{
	test_qie10();
	return 0;
}

#endif
