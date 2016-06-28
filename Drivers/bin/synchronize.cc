
//	
#ifdef STANDALONE
#include "Muon.h"
#include "Jet.h"
#include "Vertex.h"
#include "Event.h"
#include "MET.h"
#include "Constants.h"
#include "Streamer.h"

//	ROOT headers
#include "TFile.h"
#include "TChain.h"
#include "TString.h"
#include "TMath.h"
#include "TLorentzVector.h"

std::string const NTUPLEMAKER_NAME =  "ntuplemaker_H2DiMuonMaker";

#define VBFTight 0
#define ggFTight 1
#define VBFLoose 2
#define JET01Tight 3
#define JET01Loose 4
#define NCATEGORIES 5

std::vector<std::pair<int, long long int> >  categories[NCATEGORIES];

using namespace analysis::core;
using namespace analysis::processing;

bool passVertex(Vertices* v)
{
	if (v->size()==0)
		return false;
	for (Vertices::const_iterator it=v->begin();
		it!=v->end(); ++it)
		if (TMath::Abs(it->_z)<24 &&
			it->_ndf>4)
			return true;

	return false;
}

bool passMuon(Muon const& m)
{
	if (m._isGlobal && m._isTracker &&
		m._pt>10 && TMath::Abs(m._eta)<2.4 &&
		m._isTight && m._trackIsoSumPt/m._pt<0.1)
		return true;
	return false;
}

bool passMuonHLT(Muon const& m)
{
	if ((m._isHLTMatched[1] || m._isHLTMatched[0]) &&
		m._pt>20 && TMath::Abs(m._pt)<2.4)
		return true;

	return false;
}

bool passMuons(Muons* m1, Muons* m2)
{
	if (m1->size()!=m2->size())
	{
		std::cout << "### Muon vector sizes mismatch!!!" << std::endl;
		return false;
	}
	for (uint32_t i=0; i<m1->size(); i++)
	{
		if (m1->at(i)._charge!=m2->at(i)._charge &&
			passMuon(m1->at(i)) && passMuon(m2->at(i)))
			return true;
		if (passMuonHLT(m1->at(i)) || passMuonHLT(m2->at(i)))
			return true;
	}

	return false;
}

void categorizeJets(Jets* jets, Muons* mus1, Muons* mus2, MET const& met,
	Event const& event)
{
	int run = event._run;
	long long e = event._event;
	std::pair<int, long long int> runevent(run, e);

	for (uint32_t i=0; i<mus1->size(); i++)
	{
		TLorentzVector p4m1, p4m2;
		p4m1.SetPtEtaPhiM(mus1->at(i)._pt, mus1->at(i)._eta, 
			mus1->at(i)._phi, PDG_MASS_Mu);
		p4m2.SetPtEtaPhiM(mus1->at(i)._pt, mus2->at(i)._eta, 
			mus2->at(i)._phi, PDG_MASS_Mu);
		TLorentzVector p4dimuon = p4m1 + p4m2;
		if (!(p4dimuon.M()>100 && p4dimuon.M()<110 &&
			mus1->at(i)._isPF && mus2->at(i)._isPF))
			continue;

		bool isPreSelected = false;
		if (jets->size()==2)
		{
			TLorentzVector p4lead; TLorentzVector p4sub;
			p4lead.SetPtEtaPhiM(jets->at(0)._pt, jets->at(0)._eta,
				jets->at(0)._phi, jets->at(0)._mass);
			p4sub.SetPtEtaPhiM(jets->at(1)._pt, jets->at(1)._eta,
				jets->at(1)._phi, jets->at(1)._mass);
			TLorentzVector dijet = p4lead + p4sub;
	
			float deta = p4lead.Eta() - p4sub.Eta();
			float dijetmass = dijet.M();
	
			if (p4lead.Pt()>40 && p4sub.Pt()>30 &&
				met._pt<40)
			{
				isPreSelected = true;
				if (dijetmass>650 && TMath::Abs(deta)>3.5)
				{categories[VBFTight].push_back(runevent);continue;}
				if (dijetmass>250 && p4dimuon.Pt()>50)
				{categories[ggFTight].push_back(runevent);continue;}
				else
				{categories[VBFLoose].push_back(runevent);continue;}
			}
		}
		if (!isPreSelected)
		{
			if (p4dimuon.Pt()>=10)
			{categories[JET01Tight].push_back(runevent);continue;}
			else
			{categories[JET01Loose].push_back(runevent);continue;}
		}
	}
	return;
}

void synchronize(std::string const& inputname)
{
	Streamer streamer(inputname, NTUPLEMAKER_NAME+"/Events");
	streamer.chainup();

	Muons *muons1;
	Muons *muons2;
	Jets *jets;
	Vertices *vertices;
	Event *event;
	MET *met;
	streamer._chain->SetBranchAddress("Muons1", &muons1);
	streamer._chain->SetBranchAddress("Muons2", &muons2);
	streamer._chain->SetBranchAddress("Jets", &jets);
	streamer._chain->SetBranchAddress("Vertices", &vertices);
	streamer._chain->SetBranchAddress("Event", &event);
	streamer._chain->SetBranchAddress("MET", &met);

	for (uint32_t i=0; i<streamer._chain->GetEntries(); i++)
	{
		streamer._chain->GetEntry(i);
		if (i%1000==0)
			std::cout << "### Event " << i << std::endl;

		//
		//	Selections
		//
		if (!passVertex(vertices))
			continue;
		if (!passMuons(muons1, muons2))
			continue;
		categorizeJets(jets, muons1, muons2, *met, *event);
	}

	for (uint32_t i=0; i<NCATEGORIES; i++)
		std::cout << "CATEGORY: " << i << "  #EVENTS: " 
			<< categories[i].size() << std::endl;

	return;
}

int main(int argc, char** argv)
{
	if (argc<2 || argc>2)
	{
		std::cout << "Usage:" << std::endl
			<< "./synchronize <input file name>" << std::endl;
		return 1;
	}

	synchronize(argv[1]);
	return 0;
}

#endif
