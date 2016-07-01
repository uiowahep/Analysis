#ifdef STANDALONE

#include <iostream>
#include <vector>

#include "TFile.h"
#include "TChain.h"
#include "TH2D.h"

#include "Streamer.h"
#include "QIE10Frame.h"
#include "HFFrame.h"

// NEEDS UPDATING
double adc2fC_QIE10[256]={
  // - - - - - - - range 0 - - - - - - - -
  //subrange0 
  1.58, 4.73, 7.88, 11.0, 14.2, 17.3, 20.5, 23.6, 
  26.8, 29.9, 33.1, 36.2, 39.4, 42.5, 45.7, 48.8,
  //subrange1
  53.6, 60.1, 66.6, 73.0, 79.5, 86.0, 92.5, 98.9,
  105, 112, 118, 125, 131, 138, 144, 151,
  //subrange2
  157, 164, 170, 177, 186, 199, 212, 225,
  238, 251, 264, 277, 289, 302, 315, 328,
  //subrange3
  341, 354, 367, 380, 393, 406, 418, 431,
  444, 464, 490, 516, 542, 568, 594, 620,

  // - - - - - - - range 1 - - - - - - - -
  //subrange0
  569, 594, 619, 645, 670, 695, 720, 745,
  771, 796, 821, 846, 871, 897, 922, 947,
  //subrange1
  960, 1010, 1060, 1120, 1170, 1220, 1270, 1320,
  1370, 1430, 1480, 1530, 1580, 1630, 1690, 1740,
  //subrange2
  1790, 1840, 1890, 1940,  2020, 2120, 2230, 2330,
  2430, 2540, 2640, 2740, 2850, 2950, 3050, 3150,
  //subrange3
  3260, 3360, 3460, 3570, 3670, 3770, 3880, 3980,
  4080, 4240, 4450, 4650, 4860, 5070, 5280, 5490,
  
  // - - - - - - - range 2 - - - - - - - - 
  //subrange0
  5080, 5280, 5480, 5680, 5880, 6080, 6280, 6480,
  6680, 6890, 7090, 7290, 7490, 7690, 7890, 8090,
  //subrange1
  8400, 8810, 9220, 9630, 10000, 10400, 10900, 11300,
  11700, 12100, 12500, 12900, 13300, 13700, 14100, 14500,
  //subrange2
  15000, 15400, 15800, 16200, 16800, 17600, 18400, 19300,
  20100, 20900, 21700, 22500, 23400, 24200, 25000, 25800,
  //subrange3
  26600, 27500, 28300, 29100, 29900, 30700, 31600, 32400,
  33200, 34400, 36100, 37700, 39400, 41000, 42700, 44300,

  // - - - - - - - range 3 - - - - - - - - -
  //subrange0
  41100, 42700, 44300, 45900, 47600, 49200, 50800, 52500,
  54100, 55700, 57400, 59000, 60600, 62200, 63900, 65500,
  //subrange1
  68000, 71300, 74700, 78000, 81400, 84700, 88000, 91400,
  94700, 98100, 101000, 105000, 108000, 111000, 115000, 118000,
  //subrange2
  121000, 125000, 128000, 131000, 137000, 145000, 152000, 160000,
  168000, 176000, 183000, 191000, 199000, 206000, 214000, 222000,
  //subrange3
  230000, 237000, 245000, 253000, 261000, 268000, 276000, 284000,
  291000, 302000, 316000, 329000, 343000, 356000, 370000, 384000

};

void analyze(std::string const& inputname);

int main(int argc, char** argv)
{
	analyze(argv[1]);
		
	return 0;
}

void analyze(std::string const& inputname)
{
	TFile *out = new TFile("analyzeqie10.root", "recreate");
	TH1D *hADC1Distribution = new TH1D("ADC1Distribution", "ADC1Distribution",
		256, 0, 256);
	TH1D *hADC2Distribution = new TH1D("ADC2Distribution", "ADC2Distribution",
		256, 0, 256);
	TH1D *hfC1Distribution = new TH1D("fC1Distribution", "fC1Distribution",
		200, 0, 1000);
	TH1D *hfC2Distribution = new TH1D("fC2Distribution", "fC2Distribution",
		200, 0, 1000);
	TH1D *hfC1_PED = new TH1D("fC1_PED", "fC1_PED", 40, 0, 200);
	TH1D *hfC2_PED = new TH1D("fC2_PED", "fC2_PED", 40, 0, 200);
	TH1D *hfC1_new = new TH1D("fC1_new", "fC1_new", 40, 0, 200);
	TH1D *hfC2_new = new TH1D("fC2_new", "fC2_new", 40, 0, 200);
	TH1D *hRatio_PED = new TH1D("Ratio_PED", "Ratio_PED", 200, 0, 2);
	TH1D *hRatio_new = new TH1D("Ratio_new", "Ratio_new", 200, 0, 2);
	TH2D *hCorrelation = new TH2D("Correlation", "Correlation",
		40, 0, 200, 40, 0, 200);
	TH1D *hfC1_fC2zs = new TH1D("fC1_fC2zs", "fC1_fC2zs",
		40, 0, 200);
	TH1D *hfC2_fC1zs = new TH1D("fC2_fC1zs", "fC2_fC1zs",
		40, 0, 200);

	using namespace analysis::core;
	using namespace analysis::processing;
	Streamer s(inputname, "maker/Events");
	s.chainup();

	QIE10Digis *qie10s = NULL;
	s._chain->SetBranchAddress("QIE10Digis", &qie10s);

	for (int i=0; i<s._chain->GetEntries(); i++)
	{
		s._chain->GetEntry(i);
		if (i%1000==0)
			std::cout << "### Event " << i << std::endl;

		QIE10Frame df1, df2;
		for (QIE10Digis::const_iterator it=qie10s->begin();
			it!=qie10s->end(); ++it)
		{
			if (it->_iphi==39 && it->_depth==2)
			{
				if (it->_ieta==34)
				{
					for (int k=0; k<4; k++)
					{
						df1._adc[k]=it->_adc[k];
						df1._ltdc[k]=it->_ltdc[k];
					}
				}
				else if (it->_ieta==30)
				{
					for (int k=0; k<4; k++)
					{
						df2._adc[k]=it->_adc[k];
						df2._ltdc[k]=it->_adc[k];
					}
				}
			}
		}

		double fC1 = adc2fC_QIE10[df1._adc[2]];
		double fC2 = adc2fC_QIE10[df2._adc[2]];
		double fC1_ped = fC1-adc2fC_QIE10[5];
		double fC2_ped = fC2-adc2fC_QIE10[4];
		hADC1Distribution->Fill(df1._adc[2]);
		hADC2Distribution->Fill(df2._adc[2]);
		hfC1Distribution->Fill(fC1);
		hfC2Distribution->Fill(fC2);
		hfC1_PED->Fill(fC1_ped);
		hfC2_PED->Fill(fC2_ped);
		hCorrelation->Fill(fC1_ped, fC2_ped);
		if (fC1_ped>30 && fC2_ped>30)
			hRatio_PED->Fill(fC2_ped/fC1_ped);
		double scale = 0.9726;
		double fC2_new = fC2_ped/scale;
		double fC1_new = fC1_ped;
		hfC1_new->Fill(fC1_new);
		hfC2_new->Fill(fC2_new);

		if (fC1_new<30 && fC2_new>10)
			hfC2_fC1zs->Fill(fC2_new);
		if (fC2_new<30 && fC1_new>10)
			hfC1_fC2zs->Fill(fC1_new);

	}	

	hfC2_fC1zs->Scale(1./hfC2_fC1zs->Integral());
	hfC1_fC2zs->Scale(1./hfC1_fC2zs->Integral());

	out->Write();
	out->Close();
}

#endif
