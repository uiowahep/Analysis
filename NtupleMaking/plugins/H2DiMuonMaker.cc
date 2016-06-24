/*
 *	Author:
 *	Date:
 *	Description:
 */

// system include files
#include <memory>
#include <vector>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <algorithm>
#include <boost/regex.hpp>

#include "TLorentzVector.h"
#include "TTree.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TBranch.h"

//	CMSSW
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/MuonIsolation.h"
#include "DataFormats/MuonReco/interface/MuonChamberMatch.h"
#include "DataFormats/MuonReco/interface/MuonSegmentMatch.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include <Geometry/Records/interface/MuonGeometryRecord.h>
#include <Geometry/CSCGeometry/interface/CSCGeometry.h>
#include <Geometry/CSCGeometry/interface/CSCLayer.h>
#include <Geometry/CSCGeometry/interface/CSCLayerGeometry.h>
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/MuonDetId/interface/MuonSubdetId.h"
#include "DataFormats/MuonDetId/interface/DTWireId.h"
#include "DataFormats/MuonDetId/interface/CSCDetId.h"
#include "DataFormats/MuonDetId/interface/RPCDetId.h"
#include "DataFormats/CSCRecHit/interface/CSCSegmentCollection.h"
#include "DataFormats/CSCRecHit/interface/CSCRecHit2DCollection.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/CSCRecHit/interface/CSCSegmentCollection.h"
#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"
#include "Geometry/Records/interface/GlobalTrackingGeometryRecord.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Candidate/interface/CompositePtrCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/MuonReco/interface/MuonCocktails.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Common/interface/View.h"

//	MY Classes
#include "Analysis/Core/interface/GenJet.h"
#include "Analysis/Core/interface/Constants.h"
#include "Analysis/Core/interface/MET.h"
#include "Analysis/Core/interface/Track.h"
#include "Analysis/Core/interface/Event.h"
#include "Analysis/Core/interface/GenParticle.h"
#include "Analysis/Core/interface/Jet.h"
#include "Analysis/Core/interface/Muon.h"
#include "Analysis/Core/interface/Vertex.h"

class H2DiMuonMaker : public edm::EDAnalyzer
{
	public:
		H2DiMuonMaker(edm::ParameterSet const&);
		~H2DiMuonMaker() {}

		virtual void beginJob();
		virtual void endJob();
		virtual void analyze(edm::Event const&, edm::EventSetup const&);

	private:
		//	ROOT
		TTree *_tEvents;
		TTree *_tMeta;

		//	Analysis Objects
		analysis::core::Muons		_muons;
		analysis::core::Jets		_pfjets;
		analysis::core::Vertices	_vertices;
		analysis::core::Tracks		_tracks;
		analysis::core::Event		_event;
		analysis::core::MET			_met;
		analysis::core::GenJets		_genjets;
		analysis::core::GenParticles _genparts;

		//	Input Tags/Tokens
		edm::InputTag _tagMuons;
		edm::InputTag _tagBS;
		edm::InputTag _tagPrunedGenParticles;
		edm::InputTag _tagPackedGenParticles;
		edm::InputTag _tagPV;
		edm::InputTag _tagTriggerResults;
		edm::InputTag _tagTriggerObjects;
		edm::InputTag _tagMET;
		edm::InputTag _tagPFJets;
		edm::InputTag _tagGenJets;

		edm::EDGetTokenT<GenEventInfoProduct> _tokGenInfo;
		edm::EDGetTokenT<edm::TriggerResults> _tokTriggerResults;
		edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> 
			_tokTriggerObjects;
		edm::EDGetTokenT<reco::VertexCollection> _tokPV;
		edm::EDGetTokenT<std::vector<PileupSummaryInfo> > _tokPU;
		edm::EDGetTokenT<reco::BeamSpot> _tokBS;
		edm::EDGetTokenT<reco::GenParticleCollection> _tokPrunedGenParticles;
		edm::EDGetTokenT<pat::PackedGenParticleCollection> 
			_tokPackedGenParticles;
		edm::EDGetTokenT<std::vector<pat::MET> > _tokMET;
		edm::EDGetTokenT<std::vector<pat::Jet> > _tokJets;
		edm::EDGetTokenT<reco::GenJetCollection> _tokGenJets;
		edm::EDGetTokenT<pat::MuonCollection> _tokMuons;
		edm::EDGetTokenT<edm::ValueMap<float> > _tokPUJetIdFloat;
		edm::EDGetTokenT<edm::ValueMap<float> > _tokPUJetIdInt;

		//	Trigger
		std::vector<std::string> _triggerNames;
};

H2DiMuonMaker::H2DiMuonMaker(edm::ParameterSet const& ps)
{
	//
	//	init the Trees and create branches
	//
	edm::Service<TFileService> fs;
	_tEvents = fs->make<TTree>("Events", "Events");
	_tMeta = fs->make<TTree>("Meta", "Meta");

	//
	//	Tags/Tokens
	//
	_tagMuons = ps.getUntrackedParameter<edm::InputTag>(
		"tagMuons");
	_tagBS = ps.getUntrackedParameter<edm::InputTag>(
		"tagBS");
	_tagPrunedGenParticles = ps.getUntrackedParameter<edm::InputTag>(
		"tagPrunedGenParticles");
	_tagPackedGenParticles = ps.getUntrackedParameter<edm::InputTag>(
		"tagPackedGenParticles");
	_tagPV = ps.getUntrackedParameter<edm::InputTag>(
		"tagPV");
	_tagTriggerResults = ps.getUntrackedParameter<edm::InputTag>(
		"tagTriggerResults");
	_tagTriggerObjects = ps.getUntrackedParameter<edm::InputTag>(
		"tagTriggerObjects");
	_tagMET = ps.getUntrackedParameter<edm::InputTag>(
		"tagMET");
	_tagPFJets = ps.getUntrackedParameter<edm::InputTag>(
		"tagPFJets");
	_tagGenJets = ps.getUntrackedParameter<edm::InputTag>(
		"tagGenJets");

	_tokGenInfo = consumes<GenEventInfoProduct>(
		edm::InputTag("generator"));
	_tokTriggerResults = consumes<edm::TriggerResults>(
		_tagTriggerResults);
	_tokTriggerObjects = consumes<pat::TriggerObjectStandAloneCollection>(
		_tagTriggerObjects);
	_tokPV = consumes<reco::VertexCollection>(
		_tagPV);
	_tokPU = consumes<std::vector<PileupSummaryInfo> >(
		edm::InputTag("slimmedAddPileupInfo"));
	_tokBS = consumes<reco::BeamSpot>(
		_tagBS);
	_tokPrunedGenParticles = consumes<reco::GenParticleCollection>(
		_tagPrunedGenParticles);
	_tokPackedGenParticles = consumes<pat::PackedGenParticleCollection>(
		_tagPackedGenParticles);
	_tokMET = consumes<std::vector<pat::MET> >(
		_tagMET);
	_tokJets = consumes<std::vector<pat::Jet> >(
		_tagPFJets);
	_tokGenJets = consumes<reco::GenJetCollection>(
		_tagGenJets);
	_tokMuons = consumes<pat::MuonCollection>(
		_tagMuons);
	
	using namespace analysis::core;
	_tEvents->Branch("Muons", (Muons*)&_muons);
	_tEvents->Branch("Jets", (Jets*)&_pfjets);
	_tEvents->Branch("Vertices", (Vertices*)&_vertices);
	_tEvents->Branch("Tracks", (Tracks*)&_tracks);
	_tEvents->Branch("Event", (Event*)&_event);
	_tEvents->Branch("MET", (MET*)&_met);
	if (_isMC)
	{
		_tEvents->Branch("GenJets", (GenJets*)&_genjets);
		_tEvents->Branch("GenParticles", (GenParticles*)&_genparts);
	}
}

void H2DiMuonMaker::beginJob()
{}

void H2DiMuonMaker::endJob()
{}

//
//	The logic is simple:
//	- retrieve all the objects needed and save them
//		1. MC Weights
//		2. HLT
//		3.
//	- accumulate meta information
//
void H2DiMuonMaker::analyze(edm::Event const& e, edm::EventSetup const&)
{
	std::cout << "Processing..." << std::endl;

	//
	//	For MC
	//
	if (_isMC)
	{
		//
		//	MC Weights
		//
		edm::Handle<GenEventInfoProduct> genEvtInfo;
		_genWeight = (genEvtInfo->weight() > 0)? 1 : -1;
		_sumEventWeights += _genWeight;

		//
		//	MC Truth
		//
		edm::Handle<std::vector< PileupSummaryInfo > > hPUInfo;
		e.getByToken(_tokPU, PupInfo);
		std::vector<PileupSummaryInfo>::const_iterator pus;
		for (pus=hPUInfo->begin(); pus!=hPUInfo->end(); ++pus)
		{
			int bx = pus->getBunchCrossing();
			if (bx==0)
				_nPU = pus->getTrueNumInteractions();
		}

		//	
		//	Pruned Gen Particles
		//
		edm::Handle<reco::GenParticleCollection> hPrunedGenParticles;
		e.getByToken(_tokPrunedGenParticle, hPrunedGenParticles);
		reco::GenParticleCollection hardProcessMuons;
		bool foundW(false), foundZ(false), foundH(false);
		for (reco::GenParticleCollection::const_iterator it=
			hPrunedGenParticles->begin(); it!=hPrunedGenParticles->end();
			++it)
		{
			int id = it->pdgId();
			int status = it->status();

			if (abs(id)==PDG_ID_Z && (status==22 || status==3))
			{
				foundZ = true;

			}
		}

		//
		//	Packed Gen Particles
		//
		edm::Handle<pat::PackedGenParticleCollection> hPackedGenParticles;
		e.getByToken(_tokPackedGenParticle, hPackedGenParticles);
		pat::PackedGenParticleCollection finalStateGenMuons;
		for (pat::PackedGenParticleCollection::const_iterator it=
			hPackedGenParticles->begin(); it!=hPackedGenParticles->end();
			++it)
		{
			int id = it->pdgId();
			if (abs(id)==13)
				finalStateGenMuons.push_back(*it);
		}

		//
		//	Gen Jet
		//
		edm::Handle < reco::GenJetCollection > hGenJets;
		e.getByToken(_tokGenJet, hGenJets);
		if (!hGenJets->isValid())
		{
			std::cout << "Gen Jet Product is not found" << std::endl;
		}
		else
		{

		}
	}

	//	
	//	HLT
	//	- Skip the event if HLT has not fired
	//
	e.getByToken(_tokTriggerResults, _hTriggerResults);
	e.getByToken(_tokTriggerObjects, _hTriggerObjects);
	if (!hTriggerResults.isValid())
	{
		std::cout << "### Trigger Results Product is not found" << std::endl;
		return;
	}
	if (!hTriggerObjects.isValid())
	{
		std::cout << "### Trigger Results Product is not found" << std::endl;
		return;
	}
	if (_checkTrigger)
		if (!passHLT(e))
			return;

	//	
	//	Event Info
	//
	_event._run = e.id().run();
	_event._lumi = e.id().lumi();
	_event._event = e.id().event();
	_event._bx = e.bunchCrossing();
	_event._orbit = e.orbitNumber();

	//	
	//	Vertices
	//
	edm::Handle<reco::VertexCollection> hVertices;
	e.getByToken(_tokPV, hVertices);
	if (!hVertices.isValid())	
		std::cout << "### VertexCollection Product is not found" << std::endl;
	else
	{
		for (reco::VertexCollection::const_iterator it=hVertices->begin();
			it!=hVertices->end(); ++it)
		{
			analysis::core::Vertex vtx;
			if (!it->isValid())
				vtx._isValid = 0;
			else
			{
				vtx._isValid = 1;
				vtx._x = it->position().X();
				vtx._y = it->position().Y();
				vtx._z = it->position().Z();
				vtx._xerr = it->xError();
				vtx._yerr = it->yError();
				vtx._zerr = it->zError();
				vtx._chi2 = it->chi2();
				vtx._ndf = it->ndof();
				vtx._normChi2 = it->normalizedChi2();
			}
			_vertices.push_back(vtx);
		}
	}

	//
	//	Beam Spot
	//
	edm::Handle<reco::BeamSpot> hBS;
	e.getByToken(_tokBS, hBS);

	//
	//	MET
	//
	edm::Handle < std::vector<pat::MET> > hMET;
	e.getByToken(_tokMET, hMET);
	if (!hMET.isValid())
	{
		std::cout << "MET Product is not found" << std::endl;
		return;
	}

	//
	//	Jet
	//
	edm::Handle < std::vector<pat::Jet> > hJets;
	e.getByToken(_tokJets, hJets);
	if (!hJets.isValid())
	{
		std::cout << "Jet Product is not found" << std::enld;
		return;
	}
	for (uint32_t i=0; i<hJets->size(); i++)
	{
		const pat::Jet &jet = hJets->at(i);
		//	 fill in
	}

	edm::Handle < reco::GenJetCollection > hGenJets;
	e.getByToken(_tokGenJet, hGenJets);

	//
	//	Muons
	//
	edm::Handle<pat::MuonCollection> hMuons;
	e.getByToken(_tokMuons, hMuons);
	pat::MuonCollection muonsSelected;

	//
	//	Muon Pre-Selection 1
	//
	for (pat::MuonCollection::const_iterator it=hMuons->begin();
		it!=hMuons->end(); ++it)
	{
		muonsSelected.push_back(*it);
	}

	//	
	//	Muon Pre-Selection 2 based on #muons @1
	//
	if (muonsSelected.size()==0) // 0 muons
	{

	}
	else if (muonsSelected.size()==1) // 1 muon
	{

	}
	else // 2 or more muons
	{
		//	construct dimuon candidates
	}

	//
	//	Dump objects to The ROOT Tree
	//
	_tEvents->Fill();
	
	//
	//	Reset all objects or clear the containers
	//
	_event.reset();
	_vertices.clear();

}

//
//	true - passes HLT selections
//	false - doesn't pass
//
bool H2DiMuonMaker::passHLT(edm::Event const& e)
{
	const boost::regex re("_v[0-9]+");
	TriggerNames const& triggerNames = e.triggerNames(*_hTriggerResults);
	for (uint32_t i=0; i<_hTriggerResults->size(); i++)
	{
		std::string triggerName = triggerNames.triggerName(i);
		string tstripped = boost::regex_replace(triggerName, re, "",
			boost::match_default | boost::format_sed);
		for (std::vector<std::string>::const_iterator dit=
			_triggerNames.begin(); dit!=_triggerNames.end(); ++dit)
			if (*dit == tstripped &&
				_hTriggerResults->accept(i))
				return true;
	}

	return false;
}

DEFINE_FWK_MODULE(H2DiMuonMaker);
