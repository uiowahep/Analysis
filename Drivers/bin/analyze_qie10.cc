#ifdef STANDALONE

#include <iostream>
#include <fstream>
#include <vector>

#include "TCanvas.h"
#include "TFile.h"
#include "TChain.h"
#include "TH2D.h"
#include "TString.h"
#include "TPaveStats.h"
#include "TF1.h"
#include "TLegend.h"
#include "TStyle.h"

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
	TH1D *hfC1_PED = new TH1D("fC1_PED", "fC1_PED", 50, -50, 200);
	TH1D *hfC2_PED = new TH1D("fC2_PED", "fC2_PED", 50, -50, 200);
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
	TH1D *hTDC1_PMT = new TH1D("TDC1_PMT", "TDC1_PMT",
		64, 0, 64);
	TH1D *hTDC2_PMT = new TH1D("TDC2_PMT", "TDC2_PMT",
		64, 0, 64);
	TH1D *hTDC1_ALL = new TH1D("TDC1_ALL", "TDC1_ALL",
		64, 0, 64);
	TH1D *hTDC2_ALL = new TH1D("TDC2_ALL", "TDC2_ALL",
		64, 0, 64);
	TH2D *hTDCvsfC_1 = new TH2D("TDCvsfC1", "TDCvsfC1",
		50, -50, 200, 64, 0, 64);
	TH2D *hTDCvsfC_2 = new TH2D("TDCvsfC2", "TDCvsfC2",
		50, -50, 200, 64,0,64);
	TH2D *hTDCvsfC_1_CUT = new TH2D("TDCvsfC1_CUT", "TDCvsfC1_CUT",
		50, -50, 200, 64, 0, 64);
	TH2D *hTDCvsfC_2_CUT = new TH2D("TDCvsfC2_CUT", "TDCvsfC2_CUT",
		50, -50, 200, 64,0,64);
	TH1D *hTDC1 = new TH1D("TDC1", "TDC1", 64, 0, 64);
	TH1D *hTDC2 = new TH1D("TDC2", "TDC2", 64, 0, 64);
	TH2D *hfC2vsfC1_1 = new TH2D("fC2vsfC1_1", "fC2vsfC1_1",
		40, 0, 200, 40, 0, 200);
	TH2D *hfC2vsfC1_2 = new TH2D("fC2vsfC1_2", "fC2vsfC1_2",
		40, 0, 200, 40, 0, 200);
	TH1D *hM1 = new TH1D("M1", "M1", 200, 0, 100);
	TH1D *hM2 = new TH1D("M2", "M2", 200, 0, 1);
	TH1D *hM3 = new TH1D("M3", "M3", 200, 0, 1);
	TH1D *hM4 = new TH1D("M4", "M4", 200, 0, 1);

	TH1D *hSum = new TH1D("Sum", "Sum", 40, 0, 400);
	TH1D *hSumM1 = new TH1D("SumM1", "SumM1", 40, 0, 400);
	TH1D *hSumM2 = new TH1D("SumM2", "SumM2", 40, 0, 400);
	TH1D *hSumM3 = new TH1D("SumM3", "SumM3", 40, 0, 400);
	TH1D *hSumM4 = new TH1D("SumM4", "SumM4", 40, 0, 400);

	int numl18 = 0;
	int numl18andg18 = 0;
	int mclass[4] = {0,0,0,0};
	int mclass1[4] = {0,0,0,0};
	int mclass2[4] = {0,0,0,0};

	using namespace analysis::core;
	using namespace analysis::processing;
	Streamer s(inputname, "maker/Events");
	s.chainup();
	ofstream out_txt("events_qie10.txt");
	out_txt << "fC1    fC2    tdc1    tdc2    m1    m2    m3    m4"
		<< std::endl;

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
						df2._ltdc[k]=it->_ltdc[k];
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

		double tdc1 = df1._ltdc[2];
		double tdc2 = df2._ltdc[2];
		hTDC1->Fill(df1._ltdc[2]);
		hTDC2->Fill(df2._ltdc[2]);
		if (fC1_new>45)
			hTDC1_ALL->Fill(df1._ltdc[2]);
		if (fC2_new>45)
			hTDC2_ALL->Fill(df2._ltdc[2]);
		hTDCvsfC_1->Fill(fC1_new, df1._ltdc[2]);
		hTDCvsfC_2->Fill(fC2_new, df2._ltdc[2]);
		if (fC1_new<45 && fC2_new>100)
		{
			hTDCvsfC_2_CUT->Fill(fC2_new, df2._ltdc[2]);
			hfC2_fC1zs->Fill(fC2_new);
			hTDC2_PMT->Fill(df2._ltdc[2]);
			if (tdc2<18)
				numl18++;
			if (tdc2<18 && tdc1>18)
				numl18andg18++;
		}
		if (fC2_new<45 && fC1_new>100)
		{
			hTDCvsfC_1_CUT->Fill(fC1_new, df1._ltdc[2]);
			hfC1_fC2zs->Fill(fC1_new);
			hTDC1_PMT->Fill(df1._ltdc[2]);
			if (tdc1<18)
				numl18++;
			if (tdc1<18 && tdc2>18)
				numl18andg18++;
		}

		if (tdc1<18 && tdc2>18)
			hfC2vsfC1_1->Fill(fC1_new, fC2_new);
		if (tdc2<18 && tdc1>18)
			hfC2vsfC1_2->Fill(fC1_new, fC2_new);


		if (fC1_new>10 && fC2_new>10)
		{
			double s1 = max(fC1_new, fC2_new);
			double s2 = min(fC1_new, fC2_new);

			double m1 = s1/s2;
			double mean = (s1+s2)/2.;
			double m2 = sqrt((s1-mean)*(s1-mean)+(s2-mean)*(s2-mean))/(s1+s2);
			double m3 = (s1-mean)/(s1+s2);
			double m4 = (s1-s2)/(s1+s2);

			hM1->Fill(m1);
			hM2->Fill(m2);
			hM3->Fill(m3);
			hM4->Fill(m4);
			hSum->Fill(s1+s2);

			if ((s1+s2)>=200)
			{
				out_txt  << fC1 << "  " << fC2 << "  " << tdc1 << "  " << tdc2
					<< "  " << m1 << "  " << m2 << "  " << m3 << "  " << m4
					<< std::endl;
			}

			if (m1>3)
			{
				hSumM1->Fill(2*s2);
				mclass[0]++;
				if (tdc1<18 && tdc2>18)
					mclass2[0]++;
				if (tdc2<18 && tdc1>18)
					mclass2[0]++;
				if (tdc1<18 || tdc2<18)
					mclass1[0]++;
			}
			else
				hSumM1->Fill(s1+s2);
			if (m2>0.3)
			{
				hSumM2->Fill(2*s2);
				mclass[1]++;
				if (tdc1<18 && tdc2>18)
					mclass2[1]++;
				if (tdc2<18 && tdc1>18)
					mclass2[1]++;
				if (tdc1<18 || tdc2<18)
					mclass1[1]++;
			}
			else
				hSumM2->Fill(s1+s2);
			if (m3>0.25)
			{
				hSumM3->Fill(2*s2);
				mclass[2]++;
				if (tdc1<18 && tdc2>18)
					mclass2[2]++;
				if (tdc2<18 && tdc1>18)
					mclass2[2]++;
				if (tdc1<18 || tdc2<18)
					mclass1[2]++;
			}
			else
				hSumM3->Fill(s1+s2);
			if (m4>0.4)
			{
				hSumM4->Fill(2*s2);
				mclass[3]++;
				if (tdc1<18 && tdc2>18)
					mclass2[3]++;
				if (tdc2<18 && tdc1>18)
					mclass2[3]++;
				if (tdc1<18 || tdc2<18)
					mclass1[3]++;
			}
			else
				hSumM4->Fill(s1+s2);


		}
	}	

	hfC2_fC1zs->Scale(1./hfC2_fC1zs->Integral());
	hfC1_fC2zs->Scale(1./hfC1_fC2zs->Integral());
	hTDC1_ALL->Scale(1./hTDC1_ALL->Integral());
	hTDC2_ALL->Scale(1./hTDC2_ALL->Integral());
	hTDC1_PMT->Scale(1./hTDC1_PMT->Integral());
	hTDC2_PMT->Scale(1./hTDC2_PMT->Integral());

	//	dir for pics
	TString dir="/Users/vk/software/Analysis/docs/qie10/pics/results/";

	//	plot with styles
	TCanvas *c1 = new TCanvas("c1", "c1", 600, 400);
	c1->cd();
	hfC1_PED->GetXaxis()->SetTitle("fC (PED subtracted)");
	hfC2_PED->GetXaxis()->SetTitle("fC (PED subtracted)");
	hfC1_PED->GetYaxis()->SetTitle("#Events");
	hfC2_PED->GetYaxis()->SetTitle("#Events");
	hfC1_PED->SetLineColor(kRed);
	hfC2_PED->SetLineColor(kBlack);
	hfC1_PED->Draw();
	gPad->Update();
	TPaveStats* stats1 = (TPaveStats*)hfC1_PED->FindObject("stats");
	hfC2_PED->Draw("sames");
	gPad->Update();
	TPaveStats* stats2 = (TPaveStats*)hfC2_PED->FindObject("stats");
	stats1->SetTextColor(kRed);
	stats2->SetTextColor(kBlack);
	stats2->SetX1NDC(stats1->GetX1NDC()); stats2->SetX2NDC(stats1->GetX2NDC());
	stats2->SetY1NDC(-stats1->GetY2NDC()+2*stats1->GetY1NDC()); stats2->SetY2NDC(stats1->GetY1NDC());
	gPad->Modified();
	c1->SetLogy();
	c1->SaveAs(dir+"fC1_and_fC2_spectra_overlaid.pdf");

	TCanvas *c2 = new TCanvas("c2", "c2", 600, 400);
	c2->cd();
	hRatio_PED->GetXaxis()->SetTitle("fC1 / fC2");
	hRatio_PED->GetYaxis()->SetTitle("#Events");
	hRatio_PED->SetLineColor(kBlack);
	hRatio_PED->Rebin(20);
	TF1 *fitRatio_PED = new TF1("mygauss", "gaus", 0, 2);
	fitRatio_PED->SetLineColor(kRed);
	hRatio_PED->Draw();
	hRatio_PED->Fit("mygauss", "R", "sames");
	gStyle->SetOptFit(1111);
	gPad->Update();
	c2->SaveAs(dir+"fC1_over_fC2_ratio.pdf");

	TCanvas *c3 = new TCanvas("c3", "c3", 600, 400);
	c3->cd();
	c3->SetLogz();
	hTDCvsfC_1->GetXaxis()->SetTitle("fC");
	hTDCvsfC_1->GetYaxis()->SetTitle("TDC");
	hTDCvsfC_2->GetXaxis()->SetTitle("fC");
	hTDCvsfC_2->GetYaxis()->SetTitle("TDC");
	hTDCvsfC_1->Draw("colz");
	c3->SaveAs(dir+"TDCvsfC1.pdf");
	hTDCvsfC_2->Draw("colz");
	c3->SaveAs(dir+"TDCvsfC2.pdf");

	TCanvas *c4 = new TCanvas("c4", "c4", 600, 400);
	c4->cd();
	c4->SetLogy();
	hTDC1_ALL->GetXaxis()->SetTitle("TDC");
	hTDC1_ALL->GetYaxis()->SetTitle("#Events");
	hTDC1_PMT->GetXaxis()->SetTitle("TDC");
	hTDC1_PMT->GetYaxis()->SetTitle("#Events");
	hTDC2_ALL->GetXaxis()->SetTitle("TDC");
	hTDC2_ALL->GetYaxis()->SetTitle("#Events");
	hTDC2_PMT->GetXaxis()->SetTitle("TDC");
	hTDC2_PMT->GetYaxis()->SetTitle("#Events");
	hTDC1_ALL->SetLineColor(kBlack);
	hTDC1_PMT->SetLineColor(kRed);
	hTDC1_ALL->Draw();
	gPad->Update();
	stats1 = (TPaveStats*)hTDC1_ALL->FindObject("stats");
	hTDC1_PMT->Draw("sames");
	gPad->Update();
	stats2 = (TPaveStats*)hTDC1_PMT->FindObject("stats");
	stats1->SetTextColor(kBlack);
	stats2->SetTextColor(kRed);
//	stats1->SetX1NDC(stats1->GetX1NDC()); stats2->SetX2NDC(stats1->GetX2NDC());
	stats2->SetX1NDC(stats1->GetX1NDC()); stats2->SetX2NDC(stats1->GetX2NDC());
	stats2->SetY1NDC(-stats1->GetY2NDC()+2*stats1->GetY1NDC()); stats2->SetY2NDC(stats1->GetY1NDC());
	gPad->Modified();
	c4->SaveAs(dir+"TDC_distribution_overlaidwithPMT_A1.pdf");

	TCanvas *c5 = new TCanvas("c5", "c5", 600, 400);
	c5->cd();
	c5->SetLogy();
	hTDC2_ALL->SetLineColor(kBlack);
	hTDC2_PMT->SetLineColor(kRed);
	hTDC2_ALL->Draw();
	gPad->Update();
	stats1 = (TPaveStats*)hTDC2_ALL->FindObject("stats");
	hTDC2_PMT->Draw("sames");
	gPad->Update();
	stats2 = (TPaveStats*)hTDC2_PMT->FindObject("stats");
	stats1->SetTextColor(kBlack);
	stats2->SetTextColor(kRed);
//	stats1->SetX1NDC(stats1->GetX1NDC()); stats2->SetX2NDC(stats1->GetX2NDC());
	stats2->SetX1NDC(stats1->GetX1NDC()); stats2->SetX2NDC(stats1->GetX2NDC());
	stats2->SetY1NDC(-stats1->GetY2NDC()+2*stats1->GetY1NDC()); stats2->SetY2NDC(stats1->GetY1NDC());
	gPad->Modified();
	c5->SaveAs(dir+"TDC_distribution_overlaidwithPMT_A2.pdf");

	TCanvas *c6 = new TCanvas("c6", "c6", 600, 400);
	c6->cd();
	c6->SetLogz();
	hfC2vsfC1_1->GetXaxis()->SetTitle("fC1");
	hfC2vsfC1_1->GetYaxis()->SetTitle("fC2");
	hfC2vsfC1_2->GetXaxis()->SetTitle("fC1");
	hfC2vsfC1_2->GetYaxis()->SetTitle("fC2");
	hfC2vsfC1_1->Draw("colz");
	c6->SaveAs(dir+"fC2vsfC1_1.pdf");
	hfC2vsfC1_2->Draw("colz");
	c6->SaveAs(dir+"fC2vsfC1_2.pdf");

	TCanvas *c7 = new TCanvas("c7", "c7", 600, 400);
	c7->cd();
	c7->SetLogy();
	hM1->GetXaxis()->SetTitle("M1");
	hM2->GetXaxis()->SetTitle("M2");
	hM3->GetXaxis()->SetTitle("M3");
	hM4->GetXaxis()->SetTitle("M4");
	hM1->GetYaxis()->SetTitle("#Events");
	hM2->GetYaxis()->SetTitle("#Events");
	hM3->GetYaxis()->SetTitle("#Events");
	hM4->GetYaxis()->SetTitle("#Events");
	hM1->Draw();
	c7->SaveAs(dir+"M1.pdf");
	hM2->Draw();
	c7->SaveAs(dir+"M2.pdf");
	hM3->Draw();
	c7->SaveAs(dir+"M3.pdf");
	hM4->Draw();
	c7->SaveAs(dir+"M4.pdf");

	hSum->GetXaxis()->SetTitle("S1+S2");
	hSumM1->GetXaxis()->SetTitle("Signal");
	hSumM2->GetXaxis()->SetTitle("Signal");
	hSumM3->GetXaxis()->SetTitle("Signal");
	hSumM4->GetXaxis()->SetTitle("Signal");
	hSum->GetYaxis()->SetTitle("#Events");
	hSumM1->GetYaxis()->SetTitle("#Events");
	hSumM2->GetYaxis()->SetTitle("#Events");
	hSumM3->GetYaxis()->SetTitle("#Events");
	hSumM4->GetYaxis()->SetTitle("#Events");

	hSumM1->SetStats(0);
	hSumM2->SetStats(0);
	hSumM3->SetStats(0);
	hSumM4->SetStats(0);

	hSum->SetLineColor(kBlack);
	hSumM1->SetLineColor(kRed);
	hSumM2->SetLineColor(kGreen);
	hSumM3->SetLineColor(kBlue);
	hSumM4->SetLineColor(kOrange);
	hSum->Draw();
	hSumM1->Draw("same");
	hSumM2->Draw("same");
	hSumM3->Draw("same");
	hSumM4->Draw("same");
	TLegend *leg = new TLegend(0.79, 0.3, 0.99, 0.5);
	leg->SetHeader("Methods");
	leg->SetTextSize(0.03);
	leg->AddEntry(hSum, "S1+S2");
	leg->AddEntry(hSumM1, "M1");
	leg->AddEntry(hSumM2, "M2");
	leg->AddEntry(hSumM3, "M3");
	leg->AddEntry(hSumM4, "M4");
	leg->Draw();
	c7->SaveAs(dir+"Sums.pdf");

	out->Write();
	out->Close();

	std::cout << "#events with tdc<18 = " << numl18 << std::endl;
	std::cout << "#events with tdc<18 && tdc>18 for the other anode - "
		<< numl18andg18 << std::endl;
	for (int i=0; i<4; i++)
		std::cout << mclass[i] << "  ";
	std::cout << std::endl;
	for (int i=0; i<4; i++)	
		std::cout << mclass2[i] << "  ";
	std::cout << std::endl;
	for (int i=0; i<4; i++)	
		std::cout << mclass1[i] << "  ";
	std::cout << std::endl;
}

#endif





