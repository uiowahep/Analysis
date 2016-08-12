/*
 * TestLimitResultPlot.C
 *
 *  Created on: Feb 17, 2015
 *      Author: avanhoef
 */

#include <iostream>
#include <string>
#include <vector>

#include "TMultiGraph.h"
#include "TGraphAsymmErrors.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TH1.h"
#include "TH1F.h"
#include "TAxis.h"
#include "TLatex.h"
#include "TLine.h"
#include "TLegend.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TStyle.h"
#include "TROOT.h"

using namespace std;

TLegend* CreateLegend(int nEntries)
{
	double top = 0.87;
	double left = 0.62;
	TLegend* legend = new TLegend(left, top - nEntries * 0.04, left + 0.23, top);

	legend->SetBorderSize(0);
	legend->SetFillColor(0);
	legend->SetFillStyle(0);
	legend->SetTextFont(42);
	legend->SetTextSize(0.03);

	return legend;
}

void TestLimitResultPlot()
{
	gStyle->SetOptStat(0);

	double Xmin = 0;
	double Xmax = 5;

	vector<string> titles;
	titles.push_back("VBF");
	titles.push_back("ggFTight");
	titles.push_back("ggFLoose");
	titles.push_back("2Jets");

	vector<string> expLimitString;
	expLimitString.push_back("18.4375% (exp.)");
	expLimitString.push_back("31.125% (exp.)");
	expLimitString.push_back("30.375% (exp.)");
	expLimitString.push_back("19.0625% (exp.)");

	vector<double> expectedLimits;
	expectedLimits.push_back(1.52);
	expectedLimits.push_back(1.60);
	expectedLimits.push_back(1.62);
	expectedLimits.push_back(0.88);

	vector<double> expectedLimits1SigmaUp;
	expectedLimits1SigmaUp.push_back(0.65);
	expectedLimits1SigmaUp.push_back(0.72);
	expectedLimits1SigmaUp.push_back(0.99);
	expectedLimits1SigmaUp.push_back(0.37);

	vector<double> expectedLimits1SigmaDown;
	expectedLimits1SigmaDown.push_back(0.44);
	expectedLimits1SigmaDown.push_back(0.47);
	expectedLimits1SigmaDown.push_back(0.56);
	expectedLimits1SigmaDown.push_back(0.26);

	vector<double> expectedLimits2SigmaUp;
	expectedLimits2SigmaUp.push_back(1.5);
	expectedLimits2SigmaUp.push_back(1.67);
	expectedLimits2SigmaUp.push_back(2.49);
	expectedLimits2SigmaUp.push_back(0.86);

	vector<double> expectedLimits2SigmaDown;
	expectedLimits2SigmaDown.push_back(2.0);
	expectedLimits2SigmaDown.push_back(0.76);
	expectedLimits2SigmaDown.push_back(0.86);
	expectedLimits2SigmaDown.push_back(0.42);

	const Int_t n = expectedLimits.size();
	Double_t x[n];
	Double_t e1xl[n];
	Double_t e1xh[n];

	Double_t e2xl[n];
	Double_t e2xh[n];

	Double_t y[n];
	Double_t eyl[n];
	Double_t eyh[n];

	Double_t zero[n];

	for (unsigned int i = 0; i < n; i++)
	{
		x[i] = expectedLimits[i];
		e1xl[i] = expectedLimits1SigmaDown[i];
		e1xh[i] = expectedLimits1SigmaUp[i];

		e2xl[i] = expectedLimits2SigmaDown[i];
		e2xh[i] = expectedLimits2SigmaUp[i];

		y[i] = n - i - 0.5;
		eyl[i] = 0.2;
		eyh[i] = 0.2;

		zero[i] = 0.;
	}

	TGraphAsymmErrors* gr2Sigma = new TGraphAsymmErrors(n, x, y, e2xl, e2xh, eyl,
			eyh);
	gr2Sigma->SetFillColor(kYellow);

	TGraphAsymmErrors* gr1Sigma = new TGraphAsymmErrors(n, x, y, e1xl, e1xh, eyl,
			eyh);
	gr1Sigma->SetFillColor(kGreen);

	TGraphAsymmErrors* gr = new TGraphAsymmErrors(n, x, y, zero, zero, zero,
			zero);
	gr->SetMarkerColor(kBlack);
	gr->SetMarkerSize(1.3);
	gr->SetMarkerStyle(5);

	TCanvas* plot = new TCanvas("c2", "", 0, 10, 610, 800);

	TMultiGraph* mg = new TMultiGraph();
	mg->Add(gr2Sigma);
	mg->Add(gr1Sigma);
	mg->Add(gr);
	mg->Draw("AP2");

	mg->GetXaxis()->SetTitle("95% CL Limit on B(h #rightarrow e#tau), %");
	mg->GetXaxis()->SetTitleOffset(0.8);
	mg->GetXaxis()->SetTitleSize(0.055);
	mg->GetXaxis()->CenterTitle(true);
	mg->GetXaxis()->SetLabelSize(0.045);
	mg->GetXaxis()->SetLimits(Xmin, Xmax);

	mg->GetYaxis()->SetRangeUser(0, n);
	mg->SetMaximum(n);
	mg->GetYaxis()->SetNdivisions(n * 100);

	TLatex latex;
	latex.SetTextSize(0.035);

	TLatex latex2;
	latex2.SetTextSize(0.018);
	for (unsigned int i = 0; i < n; i++)
	{
		string title = titles.at(i);
		string expLimit = expLimitString.at(i);

		double titleIndex = -0.62;
		double expLimitIndex = -0.6;

		if (Xmax == 10)
		{
			titleIndex = -1.25;
			expLimitIndex = -1.2;
		}

		latex.DrawLatex(titleIndex, n - i - 0.45, title.data());
		latex2.DrawLatex(expLimitIndex, n - i - 0.7, expLimit.data());
	}

	TLegend* legend = CreateLegend(3);
	legend->AddEntry(gr, "Expected", "p");
	legend->AddEntry(gr1Sigma, "Expected #pm 1 #sigma", "f");
	legend->AddEntry(gr2Sigma, "Expected #pm 2 #sigma", "f");
	legend->Draw("same");

	TLine* line = new TLine();
	line->SetLineColor(kBlack);
	line->DrawLine(Xmin, 1, Xmax, 1);

	plot->SaveAs("test.pdf");

}

