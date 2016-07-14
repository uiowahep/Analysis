#ifndef Analysis__Drivers_HistogramSets_h
#define  Analysis__Drivers_HistogramSets_h

#ifdef STANDALONE

#include "TString.h"
#include "TH1D.h"
#include "TDirectory.h"

namespace analysis
{
	namespace processing
	{
		struct DimuonSet
		{
			DimuonSet(TString const& postfix) 
			{
				_postfix = postfix;
			}

			void init()
			{
				if (_postfix.Data()[0]!='_')
					_postfix = "_"+_postfix;
				gDirectory->mkdir(_postfix);
				gDirectory->cd(_postfix);
				hDiJetMass = new TH1D("DiJetMass", "DiJetMass",
					20, 0, 1000);
				hDiJetdeta = new TH1D("DiJetdeta", "DiJetdeta",
					14, 0, 7);
				hDiMuonpt = new TH1D("DiMuonpt", "DiMuonpt", 
					100, 0, 200);
				hDiMuonMass = new TH1D("DiMuonMass", 
					"DiMuonMass", 110, 50, 160);
				hDiMuoneta = new TH1D("DiMuoneta", "DiMuoneta",
					50, -2.5, 2.5);
				hDiMuondphi = new TH1D("DiMuondphi", 
					"DiMoundphi", 18, -3.6, 3.6);
				hMuonpt = new TH1D("Muonpt", "Muonpt", 
					50, 0, 100);
				hMuoneta = new TH1D("Muoneta", "Muoneta", 
					50, -2.5, 2.5);
				hMuonphi = new TH1D("Muonphi", "Muonphi", 
					36, -3.6, 3.6);
				gDirectory->cd("../");
			}
			~DimuonSet() {}

			TString _postfix;
			TH1D *hDiJetMass;
			TH1D *hDiJetdeta;
			TH1D *hDiMuonpt;
			TH1D *hDiMuonMass;
			TH1D *hDiMuoneta;
			TH1D *hDiMuondphi;
			TH1D *hMuonpt;
			TH1D *hMuoneta;
			TH1D *hMuonphi;
			TH1D *hNpv;
		};
	}
}

#endif

#endif
