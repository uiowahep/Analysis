
//	
#ifdef STANDALONE
#include "Muon.h"
#include "Electron.h"
#include "Jet.h"
#include "Vertex.h"
#include "Event.h"
#include "MET.h"
#include "Constants.h"
#include "Streamer.h"
#include "MetaHiggs.h"

//	ROOT headers
#include "TFile.h"
#include "TChain.h"
#include "TString.h"
#include "TMath.h"
#include "TH1D.h"
#include "TLorentzVector.h"
#include "LumiReweightingStandAlone.h"
#include "HistogramSets.h"

#include "boost/program_options.hpp"
#include <signal.h>

#define FILL_JETS(set) \
	set.hDiJetMass->Fill(dijetmass, puweight); \
	set.hDiJetdeta->Fill(TMath::Abs(deta), puweight); \
	set.hDiMuonpt->Fill(p4dimuon.Pt(), puweight); \
	set.hDiMuonMass->Fill(p4dimuon.M(), puweight); \
	set.hDiMuoneta->Fill(p4dimuon.Eta(), puweight); \
	set.hDiMuondphi->Fill(dphi, puweight); \
	set.hMuonpt->Fill(p4m1.Pt(), puweight); \
	set.hMuonpt->Fill(p4m2.Pt(), puweight); \
	set.hMuoneta->Fill(p4m1.Eta(), puweight); \
	set.hMuoneta->Fill(p4m2.Eta(), puweight); \
	set.hMuonphi->Fill(p4m1.Phi(), puweight); \
	set.hMuonphi->Fill(p4m2.Phi(), puweight);

#define FILL_NOJETS(set) \
	set.hDiMuonpt->Fill(p4dimuon.Pt(), puweight); \
	set.hDiMuonMass->Fill(p4dimuon.M(), puweight); \
	set.hDiMuoneta->Fill(p4dimuon.Eta(), puweight); \
	set.hDiMuondphi->Fill(dphi, puweight); \
	set.hMuonpt->Fill(p4m1.Pt(), puweight); \
	set.hMuonpt->Fill(p4m2.Pt(), puweight); \
	set.hMuoneta->Fill(p4m1.Eta(), puweight); \
	set.hMuoneta->Fill(p4m2.Eta(), puweight); \
	set.hMuonphi->Fill(p4m1.Phi(), puweight); \
	set.hMuonphi->Fill(p4m2.Phi(), puweight);

/*
 *	Declare/Define all the service globals
 */
std::string __inputfilename;
std::string __outputfilename;
bool __isMC;
bool __genPUMC;
std::string __puMCfilename;
std::string __puDATAfilename;
bool __continueRunning = true;

/*
 *  Define all the Constants
 */
double _muonMatchedPt = 24.;
double _muonMatchedEta = 2.4;
double _muonPt = 10.;
double _muonEta = 2.4;
double _muonIso = 0.1;
double _leadJetPt = 40.;
double _subleadJetPt = 30.;
double _metPt = 40.;
double _dijetMass_VBFTight = 650;
double _dijetdEta_VBFTight = 3.5;
double _dijetMass_ggFTight = 250.;
double _dimuonPt_ggFTight = 50.;
double _dimuonPt_01JetsTight = 10.;

std::string const NTUPLEMAKER_NAME =  "ntuplemaker_H2DiMuonMaker";

namespace po = boost::program_options;
using namespace analysis::core;
using namespace analysis::dimuon;
using namespace analysis::processing;

TH1D *hEventWeights = NULL;
DimuonSet setNoCats("NoCats");

DimuonSet set1bJets("1bJets");
DimuonSet set1bJets4l("1bJets4l");
DimuonSet set1bJets2Mu2e("1bJets4l2Mu2e");
DimuonSet set1bJets3Mu1e("1bJets4l3Mu1e");
DimuonSet set1bJets4Mu("1bJets4l4Mu");
DimuonSet set1bJets3l("1bJets3l");
DimuonSet set1bJets2l("1bJets2l");

DimuonSet set0bJets("0bJets");
DimuonSet set0bJets4l("0bJets4l");
DimuonSet set0bJets2Mu1e("0bJets4l2Mu1e");
DimuonSet set0bJets3Mu0e("0bJets4l3Mu0e");
DimuonSet set0bJets3Mu1e("0bJets4l3Mu1e");
DimuonSet set0bJets4Mu0e("0bJets4l4Mu0e");
DimuonSet set0bJets2Mu2e("0bJets4l2Mu2e");

DimuonSet set0bJets2l("0bJets2l");
DimuonSet set2Jets("2Jets");
DimuonSet setVBFTight("VBFTight");
DimuonSet setggFTight("ggFTight");
DimuonSet setggFLoose("ggFLoose");

DimuonSet set01Jets("01Jets");
DimuonSet set01JetsTight("01JetsTight");
DimuonSet set01JetsLoose("01JetsLoose");
DimuonSet set01JetsBB("01JetsBB");
DimuonSet set01JetsBO("01JetsBO");
DimuonSet set01JetsBE("01JetsBE");
DimuonSet set01JetsOO("01JetsOO");
DimuonSet set01JetsOE("01JetsOE");
DimuonSet set01JetsEE("01JetsEE");
DimuonSet set01JetsTightBB("01JetsTightBB");
DimuonSet set01JetsTightBO("01JetsTightBO");
DimuonSet set01JetsTightBE("01JetsTightBE");
DimuonSet set01JetsTightOO("01JetsTightOO");
DimuonSet set01JetsTightOE("01JetsTightOE");
DimuonSet set01JetsTightEE("01JetsTightEE");
DimuonSet set01JetsLooseBB("01JetsLooseBB");
DimuonSet set01JetsLooseBO("01JetsLooseBO");
DimuonSet set01JetsLooseBE("01JetsLooseBE");
DimuonSet set01JetsLooseOO("01JetsLooseOO");
DimuonSet set01JetsLooseOE("01JetsLooseOE");
DimuonSet set01JetsLooseEE("01JetsLooseEE");

bool isBarrel(Muon const& m)
{
	return TMath::Abs(m._eta)<0.8;
}

bool isOverlap(Muon const& m)
{
	return TMath::Abs(m._eta)>=0.8 && TMath::Abs(m._eta)<1.6;
}

bool isEndcap(Muon const& m)
{
	return TMath::Abs(m._eta)>=1.6 && TMath::Abs(m._eta)<2.1;
}

bool passVertex(Vertices* v)
{
	if (v->size()==0)
		return false;
	int n=0;
	for (Vertices::const_iterator it=v->begin();
		it!=v->end() && n<20; ++it)
	{
		if (TMath::Abs(it->_z)<24 &&
			it->_ndf>4)
			return true;
		n++;
	}

	return false;
}

bool passMuon(Muon const& m)
{
	if (m._isGlobal && m._isTracker &&
		m._pt>_muonPt && TMath::Abs(m._eta)<_muonEta &&
		m._isTight && (m._trackIsoSumPt/m._pt)<_muonIso)
		return true;
	return false;
}

bool passMuonHLT(Muon const& m)
{
	if ((m._isHLTMatched[1] || m._isHLTMatched[0]) &&
		m._pt>_muonMatchedPt && TMath::Abs(m._eta)<_muonMatchedEta)
		return true;

	return false;
}

bool passMuons(Muon const& m1, Muon const& m2)
{
	if (m1._charge!=m2._charge &&
		passMuon(m1) && passMuon(m2))
		if (passMuonHLT(m1) || passMuonHLT(m2))
			return true;

	return false;
}

float jetMuondR(float jeta,float jphi, float meta, float mphi)
{
	TLorentzVector p4j,p4m;
	p4j.SetPtEtaPhiM(10, jeta, jphi, 0);
	p4m.SetPtEtaPhiM(10, meta, mphi, 0);
	return p4j.DeltaR(p4m);
}

//  provide the vector of muons and the positions of muons currently being stufied
void categorize(Electrons *electrons, Muons *muons, int im1, int im2, 
    Jets* jets, Muon const& mu1, Muon const&  mu2, 
	MET const& met, Event const& event, float puweight=1.)
{
	TLorentzVector p4m1, p4m2;
	p4m1.SetPtEtaPhiM(mu1._pt, mu1._eta, 
		mu1._phi, PDG_MASS_Mu);
	p4m2.SetPtEtaPhiM(mu2._pt, mu2._eta, 
		mu2._phi, PDG_MASS_Mu);
	TLorentzVector p4dimuon = p4m1 + p4m2;

	//	Fill the No Categorization Set
	double dphi = p4m1.DeltaPhi(p4m2);
	setNoCats.hDiMuonpt->Fill(p4dimuon.Pt(), puweight);
	setNoCats.hDiMuonMass->Fill(p4dimuon.M(), puweight);
	setNoCats.hDiMuoneta->Fill(p4dimuon.Eta(), puweight);
	setNoCats.hDiMuondphi->Fill(dphi, puweight);
	setNoCats.hMuonpt->Fill(p4m1.Pt(), puweight);
	setNoCats.hMuonpt->Fill(p4m2.Pt(), puweight);
	setNoCats.hMuoneta->Fill(p4m1.Eta(), puweight);
	setNoCats.hMuoneta->Fill(p4m2.Eta(), puweight);
	setNoCats.hMuonphi->Fill(p4m1.Phi(), puweight);
	setNoCats.hMuonphi->Fill(p4m2.Phi(), puweight);
	
	if (!(p4dimuon.M()>110 && p4dimuon.M()<160 &&
		mu1._isPF && mu2._isPF))
		return;

	std::vector<TLorentzVector> p4jets;
    std::vector<TLorentzVector> p4bjets;
	for (Jets::const_iterator it=jets->begin(); it!=jets->end(); ++it)
	{
        //  jets for VBF/ggF
		if (it->_pt>30 && TMath::Abs(it->_eta)<4.7)
		{
			if (!(jetMuondR(it->_eta, it->_phi, mu1._eta, mu1._phi)<0.3) && 
				!(jetMuondR(it->_eta, it->_phi, mu2._eta, mu2._phi)<0.3))
			{
				TLorentzVector p4;
				p4.SetPtEtaPhiM(it->_pt, it->_eta, it->_phi, it->_mass);
				p4jets.push_back(p4);
			}
		}

        //  bjets
        if (it->_pt>30 && TMath::Abs(it->_eta)<2.4 &&
            it->_btag[0]>=0.8)
        {
			TLorentzVector p4;
			p4.SetPtEtaPhiM(it->_pt, it->_eta, it->_phi, it->_mass);
			p4bjets.push_back(p4);
        }
	}

    if (p4bjets.size()>=1)
    {
        FILL_NOJETS(set1bJets);
        if ((muons->size()+electrons->size())==4)
        {
            FILL_NOJETS(set1bJets4l);
            if (muons->size()==2 && electrons->size()==2)
            {
                FILL_NOJETS(set1bJets2Mu2e);
            }
            else if (muons->size()==3 && electrons->size()==1)
            {
                FILL_NOJETS(set1bJets3Mu1e);
            }
            else // 1 possibility only - 4 mu
            {
                FILL_NOJETS(set1bJets4Mu);
            }
        }
        else if ((muons->size()+electrons->size())==3)
        {
            FILL_NOJETS(set1bJets3l);
        }
        else // we already have 2 muons -> that means electrons->size()==0 already
        {
            FILL_NOJETS(set1bJets2l);
        }
    }
    else // 0bjets
    {
        FILL_NOJETS(set0bJets);
        if ((muons->size()-2+electrons->size()>0)) // > 0 leptons
        {
            FILL_NOJETS(set0bJets4l);
            if (muons->size()==2 && electrons->size()==1)
            {
                FILL_NOJETS(set0bJets2Mu1e);
            }
            else if (muons->size()==3 && electrons->size()==0)
            {
                FILL_NOJETS(set0bJets3Mu0e);
            }
            else if (muons->size()==3 && electrons->size()==1)
            {
                FILL_NOJETS(set0bJets3Mu1e);
            }
            else if (muons->size()==4 && electrons->size()==0)
            {
                FILL_NOJETS(set0bJets4Mu0e);
            }
            else // this is only possibility in any case
            {
                FILL_NOJETS(set0bJets2Mu2e);
            }
        }
        else
        {
            //
            //  Original Categories - 2jets and 01jets
            //
	bool isPreSelected = false;
	if (p4jets.size()>=2)
	{
		TLorentzVector p4lead = p4jets[0]; 
		TLorentzVector p4sub = p4jets[1];
		TLorentzVector dijet = p4lead + p4sub;

		float deta = p4lead.Eta() - p4sub.Eta();
		float dijetmass = dijet.M();
			
		if (p4lead.Pt()>_leadJetPt && p4sub.Pt()>_subleadJetPt &&
			met._pt<_metPt)
		{
			isPreSelected = true;

			set2Jets.hDiJetMass->Fill(dijetmass, puweight);
			set2Jets.hDiJetdeta->Fill(TMath::Abs(deta), puweight);
			set2Jets.hDiMuonpt->Fill(p4dimuon.Pt(), puweight);
			set2Jets.hDiMuonMass->Fill(p4dimuon.M(), puweight);
			set2Jets.hDiMuoneta->Fill(p4dimuon.Eta(), puweight);
			set2Jets.hDiMuondphi->Fill(dphi, puweight);
			set2Jets.hMuonpt->Fill(p4m1.Pt(), puweight);
			set2Jets.hMuonpt->Fill(p4m2.Pt(), puweight);
			set2Jets.hMuoneta->Fill(p4m1.Eta(), puweight);
			set2Jets.hMuoneta->Fill(p4m2.Eta(), puweight);
			set2Jets.hMuonphi->Fill(p4m1.Phi(), puweight);
			set2Jets.hMuonphi->Fill(p4m2.Phi(), puweight);

			//	categorize
			if (dijetmass>_dijetMass_VBFTight && TMath::Abs(deta)>_dijetdEta_VBFTight)
			{
				//	VBF Tight
				setVBFTight.hDiJetMass->Fill(dijetmass, puweight);
				setVBFTight.hDiJetdeta->Fill(TMath::Abs(deta), puweight);
				setVBFTight.hDiMuonpt->Fill(p4dimuon.Pt(), puweight);
				setVBFTight.hDiMuonMass->Fill(p4dimuon.M(), puweight);
				setVBFTight.hDiMuoneta->Fill(p4dimuon.Eta(), puweight);
				setVBFTight.hDiMuondphi->Fill(dphi, puweight);
				setVBFTight.hMuonpt->Fill(p4m1.Pt(), puweight);
				setVBFTight.hMuonpt->Fill(p4m2.Pt(), puweight);
				setVBFTight.hMuoneta->Fill(p4m1.Eta(), puweight);
				setVBFTight.hMuoneta->Fill(p4m2.Eta(), puweight);
				setVBFTight.hMuonphi->Fill(p4m1.Phi(), puweight);
				setVBFTight.hMuonphi->Fill(p4m2.Phi(), puweight);
				return;
			}
			if (dijetmass>_dijetMass_ggFTight && p4dimuon.Pt()>_dimuonPt_ggFTight)
			{
				//	ggF Tight
				setggFTight.hDiJetMass->Fill(dijetmass, puweight);
				setggFTight.hDiJetdeta->Fill(TMath::Abs(deta), puweight);
				setggFTight.hDiMuonpt->Fill(p4dimuon.Pt(), puweight);
				setggFTight.hDiMuonMass->Fill(p4dimuon.M(), puweight);
				setggFTight.hDiMuoneta->Fill(p4dimuon.Eta(), puweight);
				setggFTight.hDiMuondphi->Fill(dphi, puweight);
				setggFTight.hMuonpt->Fill(p4m1.Pt(), puweight);
				setggFTight.hMuonpt->Fill(p4m2.Pt(), puweight);
				setggFTight.hMuoneta->Fill(p4m1.Eta(), puweight);
				setggFTight.hMuoneta->Fill(p4m2.Eta(), puweight);
				setggFTight.hMuonphi->Fill(p4m1.Phi(), puweight);
				setggFTight.hMuonphi->Fill(p4m2.Phi(), puweight);
				return;}
			else
			{	//	ggF Loose
				setggFLoose.hDiJetMass->Fill(dijetmass, puweight);
				setggFLoose.hDiJetdeta->Fill(TMath::Abs(deta), puweight);
				setggFLoose.hDiMuonpt->Fill(p4dimuon.Pt(), puweight);
				setggFLoose.hDiMuonMass->Fill(p4dimuon.M(), puweight);
				setggFLoose.hDiMuoneta->Fill(p4dimuon.Eta(), puweight);
				setggFLoose.hDiMuondphi->Fill(dphi, puweight);
				setggFLoose.hMuonpt->Fill(p4m1.Pt(), puweight);
				setggFLoose.hMuonpt->Fill(p4m2.Pt(), puweight);
				setggFLoose.hMuoneta->Fill(p4m1.Eta(), puweight);
				setggFLoose.hMuoneta->Fill(p4m2.Eta(), puweight);
				setggFLoose.hMuonphi->Fill(p4m1.Phi(), puweight);
				setggFLoose.hMuonphi->Fill(p4m2.Phi(), puweight);
				return;
			}
		}
	}
	if (!isPreSelected)
	{
		set01Jets.hDiMuonpt->Fill(p4dimuon.Pt(), puweight);
		set01Jets.hDiMuonMass->Fill(p4dimuon.M(), puweight);
		set01Jets.hDiMuoneta->Fill(p4dimuon.Eta(), puweight);
		set01Jets.hDiMuondphi->Fill(dphi, puweight);
		set01Jets.hMuonpt->Fill(p4m1.Pt(), puweight);
		set01Jets.hMuonpt->Fill(p4m2.Pt(), puweight);
		set01Jets.hMuoneta->Fill(p4m1.Eta(), puweight);
		set01Jets.hMuoneta->Fill(p4m2.Eta(), puweight);
		set01Jets.hMuonphi->Fill(p4m1.Phi(), puweight);
		set01Jets.hMuonphi->Fill(p4m2.Phi(), puweight);
		if (isBarrel(mu1) && isBarrel(mu2))
		{
			//	BB
			FILL_NOJETS(set01JetsBB);
		}
		else if ((isBarrel(mu1) && isOverlap(mu2)) ||
			(isBarrel(mu2) && isOverlap(mu1)))
		{
			//	BO
			FILL_NOJETS(set01JetsBO);
		}
		else if ((isBarrel(mu1) & isEndcap(mu2)) || 
			(isBarrel(mu2) && isEndcap(mu1)))
		{
			//	BE
			FILL_NOJETS(set01JetsBE);
		}
		else if (isOverlap(mu1) && isOverlap(mu2))
		{
			//	OO
			FILL_NOJETS(set01JetsOO);
		}
		else if ((isOverlap(mu1) && isEndcap(mu2)) ||
			(isOverlap(mu2) && isEndcap(mu1)))
		{
			//	OE
			FILL_NOJETS(set01JetsOE);
		}
		else if (isEndcap(mu1) && isEndcap(mu2))
		{
			//	EE
			FILL_NOJETS(set01JetsEE);
		}

		//	separate loose vs tight
		if (p4dimuon.Pt()>=_dimuonPt_01JetsTight)
		{
			//	01Jet Tight
			set01JetsTight.hDiMuonpt->Fill(p4dimuon.Pt(), puweight);
			set01JetsTight.hDiMuonMass->Fill(p4dimuon.M(), puweight);
			set01JetsTight.hDiMuoneta->Fill(p4dimuon.Eta(), puweight);
			set01JetsTight.hDiMuondphi->Fill(dphi, puweight);
			set01JetsTight.hMuonpt->Fill(p4m1.Pt(), puweight);
			set01JetsTight.hMuonpt->Fill(p4m2.Pt(), puweight);
			set01JetsTight.hMuoneta->Fill(p4m1.Eta(), puweight);
			set01JetsTight.hMuoneta->Fill(p4m2.Eta(), puweight);
			set01JetsTight.hMuonphi->Fill(p4m1.Phi(), puweight);
			set01JetsTight.hMuonphi->Fill(p4m2.Phi(), puweight);
			if (isBarrel(mu1) && isBarrel(mu2))
			{
				//	BB
				FILL_NOJETS(set01JetsTightBB);
			}
			else if ((isBarrel(mu1) && isOverlap(mu2)) ||
				(isBarrel(mu2) && isOverlap(mu1)))
			{
				//	BO
				FILL_NOJETS(set01JetsTightBO);
			}
			else if ((isBarrel(mu1) & isEndcap(mu2)) || 
				(isBarrel(mu2) && isEndcap(mu1)))
			{
				//	BE
				FILL_NOJETS(set01JetsTightBE);
			}
			else if (isOverlap(mu1) && isOverlap(mu2))
			{
				//	OO
				FILL_NOJETS(set01JetsTightOO);
			}
			else if ((isOverlap(mu1) && isEndcap(mu2)) ||
				(isOverlap(mu2) && isEndcap(mu1)))
			{
				//	OE
				FILL_NOJETS(set01JetsTightOE);
			}
			else if (isEndcap(mu1) && isEndcap(mu2))
			{
				//	EE
				FILL_NOJETS(set01JetsTightEE);
			}
			return;
		}
		else
		{
			//	01Jet Loose
			set01JetsLoose.hDiMuonpt->Fill(p4dimuon.Pt(), puweight);
			set01JetsLoose.hDiMuonMass->Fill(p4dimuon.M(), puweight);
			set01JetsLoose.hDiMuoneta->Fill(p4dimuon.Eta(), puweight);
			set01JetsLoose.hDiMuondphi->Fill(dphi, puweight);
			set01JetsLoose.hMuonpt->Fill(p4m1.Pt(), puweight);
			set01JetsLoose.hMuonpt->Fill(p4m2.Pt(), puweight);
			set01JetsLoose.hMuoneta->Fill(p4m1.Eta(), puweight);
			set01JetsLoose.hMuoneta->Fill(p4m2.Eta(), puweight);
			set01JetsLoose.hMuonphi->Fill(p4m1.Phi(), puweight);
			set01JetsLoose.hMuonphi->Fill(p4m2.Phi(), puweight);
			if (isBarrel(mu1) && isBarrel(mu2))
			{
				//	BB
				FILL_NOJETS(set01JetsLooseBB);
			}
			else if ((isBarrel(mu1) && isOverlap(mu2)) ||
				(isBarrel(mu2) && isOverlap(mu1)))
			{
				//	BO
				FILL_NOJETS(set01JetsLooseBO);
			}
			else if ((isBarrel(mu1) & isEndcap(mu2)) || 
				(isBarrel(mu2) && isEndcap(mu1)))
			{
				//	BE
				FILL_NOJETS(set01JetsLooseBE);
			}
			else if (isOverlap(mu1) && isOverlap(mu2))
			{
				//	OO
				FILL_NOJETS(set01JetsLooseOO);
			}
			else if ((isOverlap(mu1) && isEndcap(mu2)) ||
				(isOverlap(mu2) && isEndcap(mu1)))
			{
				//	OE
				FILL_NOJETS(set01JetsLooseOE);
			}
			else if (isEndcap(mu1) && isEndcap(mu2))
			{
				//	EE
				FILL_NOJETS(set01JetsLooseEE);
			}
			return;
		}
	}
    }   // no indentation!!! this is for veto on leptons for 0b-jet categories
    }   // no indentaion!!! this is closing for 0b-jet categorization
	
	return;
}

float sampleinfo(std::string const& inputname)
{
	Streamer s(inputname, NTUPLEMAKER_NAME+"/Meta");
	s.chainup();

	using namespace analysis::dimuon;
	MetaHiggs *meta=NULL;
	s._chain->SetBranchAddress("Meta", &meta);

	long long int numEvents = 0;
	long long int numEventsWeighted = 0;
	for (int i=0; i<s._chain->GetEntries(); i++)
	{
		s._chain->GetEntry(i);
		numEvents+=meta->_nEventsProcessed;
		numEventsWeighted+=meta->_sumEventWeights;
	}
	std::cout 
		<< "#events processed total = " << numEvents << std::endl
		<< "#events weighted total = " << numEventsWeighted << std::endl;

	return numEventsWeighted;
}

void generatePUMC()
{
    std::cout << "### Generate PU MC file...." << std::endl;
	TFile *pufile = new TFile(__puMCfilename.c_str(), "recreate");
	TH1D *h = new TH1D("pileup", "pileup", 50, 0, 50);

	Streamer s(__inputfilename, NTUPLEMAKER_NAME+"/Events");
	s.chainup();

	EventAuxiliary *aux=NULL;
	s._chain->SetBranchAddress("EventAuxiliary", &aux);
	int numEvents = s._chain->GetEntries();
	for (uint32_t i=0; i<numEvents; i++)
	{
		s._chain->GetEntry(i);
		h->Fill(aux->_nPU, aux->_genWeight);
	}

	pufile->Write();
	pufile->Close();
}

void process()
{
	//	out ...
	TFile *outroot = new TFile(__outputfilename.c_str(), "recreate");
    hEventWeights = new TH1D("eventWeights", "eventWeights", 1, 0, 1);
	setNoCats.init();
	set2Jets.init();
	set01Jets.init();
	setVBFTight.init();
	setggFTight.init();
	setggFLoose.init();
	set01JetsTight.init();
	set01JetsLoose.init();
	set01JetsBB.init();
	set01JetsBO.init();
	set01JetsBE.init();
	set01JetsOO.init();
	set01JetsOE.init();
	set01JetsEE.init();
	set01JetsTightBB.init();
	set01JetsTightBO.init();
	set01JetsTightBE.init();
	set01JetsTightOO.init();
	set01JetsTightOE.init();
	set01JetsTightEE.init();
	set01JetsLooseBB.init();
	set01JetsLooseBO.init();
	set01JetsLooseBE.init();
	set01JetsLooseOO.init();
	set01JetsLooseOE.init();
	set01JetsLooseEE.init();

    set1bJets.init();
    set1bJets4l.init();
    set1bJets2Mu2e.init();
    set1bJets3Mu1e.init();
    set1bJets4Mu.init();
    set1bJets3l.init();
    set1bJets2l.init();
    set0bJets.init();
    set0bJets4l.init();
    set0bJets2Mu1e.init();
    set0bJets3Mu0e.init();
    set0bJets3Mu1e.init();
    set0bJets4Mu0e.init();
    set0bJets2Mu2e.init();
    set0bJets2l.init();

	//	get the total events, etc...
	long long int numEventsWeighted = sampleinfo(__inputfilename);
    hEventWeights->Fill(0.5, numEventsWeighted);

	//	generate the MC Pileup histogram
	if (__genPUMC && __isMC)
		generatePUMC();

	Streamer streamer(__inputfilename, NTUPLEMAKER_NAME+"/Events");
	streamer.chainup();

    Muons *muons=NULL;
    Electrons *electrons=NULL;
	Jets *jets=NULL;
	Vertices *vertices=NULL;
	Event *event=NULL;
	EventAuxiliary *aux=NULL;
	MET *met=NULL;
	streamer._chain->SetBranchAddress("Muons", &muons);
	streamer._chain->SetBranchAddress("Electrons", &electrons);
	streamer._chain->SetBranchAddress("Jets", &jets);
	streamer._chain->SetBranchAddress("Vertices", &vertices);
	streamer._chain->SetBranchAddress("Event", &event);
	streamer._chain->SetBranchAddress("EventAuxiliary", &aux);
	streamer._chain->SetBranchAddress("MET", &met);

	//	init the PU reweighter
	reweight::LumiReWeighting *weighter = NULL;
	if (__isMC)
	{
		std::cout << "mcPU=" << __puMCfilename << "  dataPU="
			<< __puDATAfilename << std::endl;
		TString mc_pileupfile = __puMCfilename.c_str();
		TString data_pileupfile = __puDATAfilename.c_str();
		weighter = new reweight::LumiReWeighting(mc_pileupfile.Data(), 
            data_pileupfile.Data(), "pileup", "pileup");
	}

	//	Main Loop
	uint32_t numEntries = streamer._chain->GetEntries();
	for (uint32_t i=0; i<numEntries && __continueRunning; i++)
	{
		streamer._chain->GetEntry(i);
		if (i%1000==0)
			std::cout << "### Event " << i << " / " << numEntries
				<< std::endl;

		float puweight = __isMC ? weighter->weight(aux->_nPU)*aux->_genWeight :
			1.;

		//
		//	Selections
		//
		if (!passVertex(vertices))
			continue;
		if (!(aux->_hasHLTFired[0] || aux->_hasHLTFired[1]))
			continue;

        //  prepare the pairs of muons
        int im1 = 0;
        for (analysis::core::Muons::const_iterator it=muons->begin();
            it!=muons->end(); ++it)
        {
            int im2 = im1+1;
            for (analysis::core::Muons::const_iterator jt=(it+1);
                jt!=muons->end(); ++jt)
            {
                //  determine if we have 2 muons that we need
                if (passMuons(*it, *jt))
                    //  up to 2 other leptons - we already know that we have 2 muons!
                    if ((muons->size()+electrons->size())<=4)
			            categorize(electrons, muons, im1, im2, 
                            jets, *it, *jt, *met, *event, puweight);
                im2++;
		    }
            im1++;
        }
	}

	outroot->Write();
	outroot->Close();

	return;
}

void sigHandler(int sig)
{
	cout << "### Signal: " << sig << " caughter. Exiting..." << endl;
	__continueRunning = false;
}

void printCuts()
{
    std::cout << "Cuts:" << std::endl
        << "_muonMatchedPt = " << _muonMatchedPt << std::endl
        << "_muonMatchedEta = " << _muonMatchedEta << std::endl
        << "_muonPt = " << _muonPt << std::endl
        << "_muonEta = " << _muonEta << std::endl
        << "_muonIso = " << _muonIso << std::endl
        << "_leadJetPt = " << _leadJetPt << std::endl
        << "_subleadJetPt = " << _subleadJetPt << std::endl
        << "_metPt = " << _metPt << std::endl
        << "_dijetMass_VBFTight = " << _dijetMass_VBFTight << std::endl
        << "_dijetdEta_VBFTight = " << _dijetdEta_VBFTight << std::endl
        << "_dijetMass_ggFTight = " << _dijetMass_ggFTight << std::endl
        << "_dimuonPt_ggFTight = " << _dimuonPt_ggFTight << std::endl
        << "_dimuonPt_01JetsTight = " << _dimuonPt_01JetsTight << std::endl;
}

int main(int argc, char** argv)
{
	/*
	 *	Register signals
	 */
	signal(SIGABRT, &sigHandler);
	signal(SIGTERM, &sigHandler);
	signal(SIGINT, &sigHandler);

	std::string none;
	bool genPUMC = false;

	/*
	 *	Pare Options
	 */
	po::options_description desc("Allowed Program Options");
	desc.add_options()
		("help", "produce help messages")
		("input", po::value<std::string>(), "a file specifying all the ROOT files to process")
		("isMC", po::value<bool>(), "type of data: DATA vs MC")
		("output", po::value<std::string>(), "output file name")
		("genPUMC", po::value<bool>(&genPUMC)->default_value(false), "true if should generate the MC PU file")
		("puMC", po::value<std::string>(&none)->default_value("None"), "MC PU Reweight file")
		("puDATA", po::value<std::string>(&none)->default_value("None"), "DATA PU Reweight file")
        ("muonMatchedPt", po::value<double>(&_muonMatchedPt)->default_value(_muonMatchedPt), "Muon Matched Pt Cut")
        ("muonMatchedEta", po::value<double>(&_muonMatchedEta)->default_value(_muonMatchedEta), "Muon Matched Eta Cut")
        ("muonPt", po::value<double>(&_muonPt)->default_value(_muonPt), "Muon Pt Cut")
        ("muonEta", po::value<double>(&_muonEta)->default_value(_muonEta), "Muon Eta Cut")
        ("muonIso", po::value<double>(&_muonIso)->default_value(_muonIso), "Muon Isolation Cut")
        ("leadJetPt", po::value<double>(&_leadJetPt)->default_value(_leadJetPt), "Lead Jet Pt Cut")
        ("subleadJetPt", po::value<double>(&_subleadJetPt)->default_value(_subleadJetPt), "SubLeading Jet Pt Cut")
        ("metPt", po::value<double>(&_metPt)->default_value(_metPt), "MET Pt Cut")
        ("dijetMass_VBFTight", po::value<double>(&_dijetMass_VBFTight)->default_value(_dijetMass_VBFTight), "DiJet Mass VBFTight-Category Cut")
        ("dijetdEta_VBFTight", po::value<double>(&_dijetdEta_VBFTight)->default_value(_dijetdEta_VBFTight), "DiJet deta VBFTight-Category Cut")
        ("dijetMass_ggFTight", po::value<double>(&_dijetMass_ggFTight)->default_value(_dijetMass_ggFTight), "DiJet Mass ggFTight-Category Cut")
        ("dimuonPt_ggFTight", po::value<double>(&_dimuonPt_ggFTight)->default_value(_dimuonPt_ggFTight), "DiMuon Pt ggFTight-Category Cut")
        ("dimuonPt_01JetsTight", po::value<double>(&_dimuonPt_01JetsTight)->default_value(_dimuonPt_01JetsTight), "DiMuon Pt 01JetsTight-Category Cut")
	;

	po::variables_map vm;
	po::store(po::parse_command_line(argc, argv, desc), vm);
	po::notify(vm);

	if (vm.count("help") || argc<2)
	{
		std::cout << desc << std::endl;
		return 1;
	}

	//	Assign globals
	__inputfilename = vm["input"].as<std::string>();
	__isMC = vm["isMC"].as<bool>();
	__outputfilename = vm["output"].as<std::string>();
	__genPUMC = vm["genPUMC"].as<bool>();
	__puMCfilename = vm["puMC"].as<std::string>();
	__puDATAfilename = vm["puDATA"].as<std::string>();
    _muonMatchedPt = vm["muonMatchedPt"].as<double>();
    _muonMatchedEta = vm["muonMatchedEta"].as<double>();
    _muonPt = vm["muonPt"].as<double>();
    _muonEta = vm["muonEta"].as<double>();
    _muonIso = vm["muonIso"].as<double>();
    _leadJetPt = vm["leadJetPt"].as<double>();
    _subleadJetPt = vm["subleadJetPt"].as<double>();
    _metPt = vm["metPt"].as<double>();
    _dijetMass_VBFTight = vm["dijetMass_VBFTight"].as<double>();
    _dijetdEta_VBFTight = vm["dijetdEta_VBFTight"].as<double>();
    _dijetMass_ggFTight = vm["dijetMass_ggFTight"].as<double>();
    _dimuonPt_ggFTight = vm["dimuonPt_ggFTight"].as<double>();
    _dimuonPt_01JetsTight = vm["dimuonPt_01JetsTight"].as<double>();
    printCuts();

	//	start processing
	process();
	return 0;
}

#endif
