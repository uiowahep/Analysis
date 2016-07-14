
//	
#ifdef STANDALONE
#include "Muon.h"
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

/*
 *	Declare/Define all the globals
 */
std::string __inputfilename;
std::string __outputfilename;
bool __isMC;
std::string __puMCfilename;
std::string __puDATAfilename;
bool __continueRunning = true;

std::string const NTUPLEMAKER_NAME =  "ntuplemaker_H2DiMuonMaker";

namespace po = boost::program_options;
using namespace analysis::core;
using namespace analysis::dimuon;
using namespace analysis::processing;

DimuonSet setNoCats("_NoCats");
DimuonSet set2Jets("_2Jets");
DimuonSet set01Jets("_01Jets");

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
		m._pt>10 && TMath::Abs(m._eta)<2.4 &&
		m._isTight && (m._trackIsoSumPt/m._pt)<0.1)
		return true;
	return false;
}

bool passMuonHLT(Muon const& m)
{
	if ((m._isHLTMatched[1] || m._isHLTMatched[0]) &&
		m._pt>20 && TMath::Abs(m._eta)<2.4)
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

void categorize(Jets* jets, Muon const& mu1, Muon const&  mu2, 
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
	setNoCats.hDiMuonpt->Fill(p4dimuon.Pt());
	setNoCats.hDiMuonMass->Fill(p4dimuon.M());
	setNoCats.hDiMuoneta->Fill(p4dimuon.Eta());
	setNoCats.hDiMuondphi->Fill(dphi);
	setNoCats.hMuonpt->Fill(p4m1.Pt());
	setNoCats.hMuonpt->Fill(p4m2.Pt());
	setNoCats.hMuoneta->Fill(p4m1.Eta());
	setNoCats.hMuoneta->Fill(p4m2.Eta());
	setNoCats.hMuonphi->Fill(p4m1.Phi());
	setNoCats.hMuonphi->Fill(p4m2.Phi());
	
	if (!(p4dimuon.M()>110 && p4dimuon.M()<160 &&
		mu1._isPF && mu2._isPF))
		return;

	std::vector<TLorentzVector> p4jets;
	for (Jets::const_iterator it=jets->begin(); it!=jets->end(); ++it)
	{
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
	}
	if (p4jets.size()>2)
		return;

	bool isPreSelected = false;
	if (p4jets.size()==2)
	{
		TLorentzVector p4lead = p4jets[0]; 
		TLorentzVector p4sub = p4jets[1];
		TLorentzVector dijet = p4lead + p4sub;

		float deta = p4lead.Eta() - p4sub.Eta();
		float dijetmass = dijet.M();
			
		if (p4lead.Pt()>40 && p4sub.Pt()>30 &&
			met._pt<40)
		{
			isPreSelected = true;

			set2Jets.hDiJetMass->Fill(dijetmass);
			set2Jets.hDiJetdeta->Fill(TMath::Abs(deta));
			set2Jets.hDiMuonpt->Fill(p4dimuon.Pt());
			set2Jets.hDiMuonMass->Fill(p4dimuon.M());
			set2Jets.hDiMuoneta->Fill(p4dimuon.Eta());
			set2Jets.hDiMuondphi->Fill(dphi);
			set2Jets.hMuonpt->Fill(p4m1.Pt());
			set2Jets.hMuonpt->Fill(p4m2.Pt());
			set2Jets.hMuoneta->Fill(p4m1.Eta());
			set2Jets.hMuoneta->Fill(p4m2.Eta());
			set2Jets.hMuonphi->Fill(p4m1.Phi());
			set2Jets.hMuonphi->Fill(p4m2.Phi());

			//	categorize
			if (dijetmass>650 && TMath::Abs(deta)>3.5)
			{
				return;
			}
			if (dijetmass>250 && p4dimuon.Pt()>50)
			{
				return;}
			else
			{
				return;}
		}
	}
	if (!isPreSelected)
	{
		set01Jets.hDiMuonpt->Fill(p4dimuon.Pt());
		set01Jets.hDiMuonMass->Fill(p4dimuon.M());
		set01Jets.hDiMuoneta->Fill(p4dimuon.Eta());
		set01Jets.hDiMuondphi->Fill(dphi);
		set01Jets.hMuonpt->Fill(p4m1.Pt());
		set01Jets.hMuonpt->Fill(p4m2.Pt());
		set01Jets.hMuoneta->Fill(p4m1.Eta());
		set01Jets.hMuoneta->Fill(p4m2.Eta());
		set01Jets.hMuonphi->Fill(p4m1.Phi());
		set01Jets.hMuonphi->Fill(p4m2.Phi());
		if (p4dimuon.Pt()>=10)
		{
			return;
		}
		else
		{
			return;
		}
	}
	
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

void process()
{
	long long int numEventsWeighted = sampleinfo(__inputfilename);

	//	out ...
	TFile *outroot = new TFile(__outputfilename.c_str(), "recreate");
	setNoCats.init();
	set2Jets.init();
	set01Jets.init();

	Streamer streamer(__inputfilename, NTUPLEMAKER_NAME+"/Events");
	streamer.chainup();

	Muons *muons1=NULL;
	Muons *muons2=NULL;
	Jets *jets=NULL;
	Vertices *vertices=NULL;
	Event *event=NULL;
	EventAuxiliary *aux=NULL;
	MET *met=NULL;
	streamer._chain->SetBranchAddress("Muons1", &muons1);
	streamer._chain->SetBranchAddress("Muons2", &muons2);
	streamer._chain->SetBranchAddress("Jets", &jets);
	streamer._chain->SetBranchAddress("Vertices", &vertices);
	streamer._chain->SetBranchAddress("Event", &event);
	streamer._chain->SetBranchAddress("EventAuxiliary", &aux);
	streamer._chain->SetBranchAddress("MET", &met);

	//	init the PU reweighter
	reweight::LumiReWeighting *weighter = NULL;
	if (__isMC)
	{
		TString mc_pileupfile = __puMCfilename.c_str();
		TString data_pileupfile = __puDATAfilename.c_str();
		weighter = new reweight::LumiReWeighting(
		mc_pileupfile.Data(), data_pileupfile.Data(), "pileup", "pileup");
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
		for (uint32_t im=0; im<muons1->size(); im++)
		{
			if (!passMuons(muons1->at(im), muons2->at(im)))
				continue;
			categorize(jets, muons1->at(im), muons2->at(im), *met, *event,
				puweight);
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

int main(int argc, char** argv)
{
	/*
	 *	Register signals
	 */
	signal(SIGABRT, &sigHandler);
	signal(SIGTERM, &sigHandler);
	signal(SIGINT, &sigHandler);

	std::string none;

	/*
	 *	Pare Options
	 */
	po::options_description desc("Allowed Program Options");
	desc.add_options()
		("help", "produce help messages")
		("input", po::value<std::string>(), "a file specifying all the ROOT files to process")
		("isMC", po::value<bool>(), "type of data: DATA vs MC")
		("output", po::value<std::string>(), "output file name")
		("puMC", po::value<std::string>(&none)->default_value("None"), "MC PU Reweight file")
		("puDATA", po::value<std::string>(&none)->default_value("None"), "DATA PU Reweight file")
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
	__puMCfilename = vm["puMC"].as<std::string>();
	__puDATAfilename = vm["puDATA"].as<std::string>();

	//	start processing
	process();
	return 0;
}

#endif
