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
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
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
#include "Analysis/Core/interface/MetaHiggs.h"
#include "Analysis/Core/interface/GenParticle.h"
#include "Analysis/Core/interface/Jet.h"
#include "Analysis/Core/interface/Muon.h"
#include "Analysis/Core/interface/Vertex.h"

class H2DiMuonMaker : public edm::one::EDAnalyzer<edm::one::SharedResources>
{
	public:
		H2DiMuonMaker(edm::ParameterSet const&);
		~H2DiMuonMaker() {}

		virtual void beginJob();
		virtual void endJob();
		virtual void analyze(edm::Event const&, edm::EventSetup const&);
	private:
		bool passHLT(edm::Event const&);
		bool isHLTMatched(uint32_t, edm::Event const&,
			pat::Muon const&);
		bool passKinCuts(pat::Muon const&,
			edm::Handle<reco::BeamSpot> const&);

	private:
		//	ROOT
		TTree *_tEvents;
		TTree *_tMeta;

		//	Analysis Objects
		analysis::dimuon::MetaHiggs		_meta;
		analysis::core::Muons		_muons1; 
		analysis::core::Muons		_muons2; // [0]-[0] correspond to a pair
		analysis::core::Jets		_pfjets;
		analysis::core::Vertices	_vertices;
		analysis::core::Event		_event;
		analysis::core::EventAuxiliary		_eaux;
		analysis::core::MET			_met;
		analysis::core::GenJets		_genjets;

		analysis::core::GenParticle	_genZpreFSR;
		analysis::core::Track		_track1ZpreFSR, _track2ZpreFSR;			
		analysis::core::GenParticle	_genZpostFSR;
		analysis::core::Track		_track1ZpostFSR, _track2ZpostFSR;
		
		analysis::core::GenParticle	_genWpreFSR;
		analysis::core::Track		_trackWpreFSR;	
		analysis::core::GenParticle	_genWpostFSR;
		analysis::core::Track		_trackWpostFSR;
		
		analysis::core::GenParticle	_genHpreFSR;
		analysis::core::Track		_track1HpreFSR, _track2HpreFSR;			
		analysis::core::GenParticle	_genHpostFSR;
		analysis::core::Track		_track1HpostFSR, _track2HpostFSR;

#if 0
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

		edm::Handle<edm::TriggerResults> _hTriggerResults;
		edm::Handle<pat::TriggerObjectStandAloneCollection> _hTriggerObjects;
#endif
};

H2DiMuonMaker::H2DiMuonMaker(edm::ParameterSet const& ps)
{
	//
	//	init the Trees and create branches
	//
	edm::Service<TFileService> fs;
	_tEvents = fs->make<TTree>("Events", "Events");
	_tMeta = fs->make<TTree>("Meta", "Meta");

	using namespace analysis::core;
	using namespace analysis::dimuon;
	_tEvents->Branch("Muons1", (Muons*)&_muons1);
	_tEvents->Branch("Muons2", (Muons*)&_muons2);
	_tEvents->Branch("Jets", (Jets*)&_pfjets);
	_tEvents->Branch("Vertices", (Vertices*)&_vertices);
	_tEvents->Branch("Event", (Event*)&_event);
	_tEvents->Branch("EventAuxiliary", (EventAuxiliary*)&_eaux);
	_tEvents->Branch("MET", (MET*)&_met);
	_tMeta->Branch("Meta", (MetaHiggs*)&_meta);


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

	_meta._isMC = ps.getUntrackedParameter<bool>("isMC");
	_meta._triggerNames = ps.getUntrackedParameter<std::vector<std::string> >(
		"triggerNames");
	_meta._nMuons = ps.getUntrackedParameter<int>("nMuons");
	_meta._checkTrigger = ps.getUntrackedParameter<bool>("checkTrigger");
	_meta._isGlobalMuon = ps.getUntrackedParameter<bool>("isGlobalMuon");
	_meta._isTrackerMuon = ps.getUntrackedParameter<bool>("isTrackerMuon");
	_meta._isStandAloneMuon = ps.getUntrackedParameter<bool>("isStandAloneMuon");
	_meta._minPt = ps.getUntrackedParameter<double>("minPt");
	_meta._maxeta = ps.getUntrackedParameter<double>("maxeta");
	_meta._maxNormChi2 = ps.getUntrackedParameter<double>("maxNormChi2");
	_meta._minMuonHits = ps.getUntrackedParameter<int>("minMuonHits");
	_meta._minPixelHits = ps.getUntrackedParameter<int>("minPixelHits");
	_meta._minStripHits = ps.getUntrackedParameter<int>("minStripHits");
	_meta._minTrackerHits = ps.getUntrackedParameter<int>("minTrackerHits");
	_meta._minSegmentMatches = ps.getUntrackedParameter<int>("minSegmentMatches");
	_meta._minMatchedStations = ps.getUntrackedParameter<int>("minMatchedStations");
	_meta._minPixelLayers = ps.getUntrackedParameter<int>("minPixelLayers");
	_meta._minTrackerLayers = ps.getUntrackedParameter<int>("minTrackerLayers");
	_meta._minStripLayers = ps.getUntrackedParameter<int>("minStripLayers");
	_meta._minValidFractionTracker = 
		ps.getUntrackedParameter<double>("minValidFractionTracker");
	_meta._maxd0 = ps.getUntrackedParameter<double>("maxd0");
	_meta._maxTrackIsoSumPt = ps.getUntrackedParameter<double>(
		"maxTrackIsoSumPt");
	_meta._maxRelCombIso = ps.getUntrackedParameter<double>("maxRelCombIso");

	//	additional branching for MC
	if (_meta._isMC)
	{
		_tEvents->Branch("GenJets", (GenJets*)&_genjets);
		
		/*
		_tEvents->Branch("GenZpreFSR", (GenParticle*)&_genZpreFSR);
		_tEvents->Branch("Track1ZpreFSR", (Track*)&_track1ZpreFSR);
		_tEvents->Branch("Track2ZpreFSR", (Track*)&_track2ZpreFSR);

		_tEvents->Branch("GenZpostFSR", (GenParticle*)&_genZpostFSR);
		_tEvents->Branch("Track1ZpostFSR", (Track*)&_track1ZpostFSR);
		_tEvents->Branch("Track2ZpostFSR", (Track*)&_track2ZpostFSR);

		_tEvents->Branch("GenWpreFSR", (GenParticle*)&_genWpreFSR);
		_tEvents->Branch("TrackWpreFSR", (Track*)&_trackWpreFSR);

		_tEvents->Branch("GenWpostFSR", (GenParticle*)&_genWpostFSR);
		_tEvents->Branch("TrackWpostFSR", (Track*)&_trackWpostFSR);
		*/

		_tEvents->Branch("GenHpreFSR", (GenParticle*)&_genHpreFSR);
		_tEvents->Branch("Track1HpreFSR", (Track*)&_track1HpreFSR);
		_tEvents->Branch("Track2HpreFSR", (Track*)&_track2HpreFSR);

		_tEvents->Branch("GenHpostFSR", (GenParticle*)&_genHpostFSR);
		_tEvents->Branch("Track1HpostFSR", (Track*)&_track1HpostFSR);
		_tEvents->Branch("Track2HpostFSR", (Track*)&_track2HpostFSR);
	}
}

void H2DiMuonMaker::beginJob()
{}

void H2DiMuonMaker::endJob()
{
	_tMeta->Fill();
}

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
#if 0

	// count total
	_meta._nEventsProcessed++;

	//
	//	Reset all objects or clear the containers
	//
	_event.reset();
	_eaux.reset();
	_met.reset();

	_vertices.clear();
	_pfjets.clear();
	_genjets.clear();
	_muons1.clear();
	_muons2.clear();
	_genjets.clear();

	_genZpreFSR.reset();
	_track1ZpreFSR.reset();
	_track2ZpreFSR.reset();
	
	_genZpostFSR.reset();
	_track1ZpostFSR.reset();
	_track2ZpostFSR.reset();

	_genWpreFSR.reset();
	_trackWpreFSR.reset();
	_genWpostFSR.reset();
	_trackWpostFSR.reset();

	_genHpreFSR.reset();
	_track1HpreFSR.reset();
	_track2HpreFSR.reset();
	
	_genHpostFSR.reset();
	_track1HpostFSR.reset();
	_track2HpostFSR.reset();

	//
	//	For MC
	//
	if (_meta._isMC)
	{
		//
		//	MC Weights
		//
		edm::Handle<GenEventInfoProduct> hGenEvtInfo;
		e.getByToken(_tokGenInfo, hGenEvtInfo);
		_eaux._genWeight = (hGenEvtInfo->weight() > 0)? 1 : -1;
		_meta._sumEventWeights += _eaux._genWeight;

		//
		//	MC Truth
		//
		edm::Handle<std::vector< PileupSummaryInfo > > hPUInfo;
		e.getByToken(_tokPU, hPUInfo);
		std::vector<PileupSummaryInfo>::const_iterator pus;
		for (pus=hPUInfo->begin(); pus!=hPUInfo->end(); ++pus)
		{
			int bx = pus->getBunchCrossing();
			if (bx==0)
				_eaux._nPU = pus->getTrueNumInteractions();
		}

		//	
		//	Pruned Gen Particles
		//
		edm::Handle<reco::GenParticleCollection> hPrunedGenParticles;
		e.getByToken(_tokPrunedGenParticles, hPrunedGenParticles);
		reco::GenParticleCollection hardProcessMuons;
		bool foundW(false), foundZ(false), foundH(false);
		for (reco::GenParticleCollection::const_iterator it=
			hPrunedGenParticles->begin(); it!=hPrunedGenParticles->end();
			++it)
		{
			int id = it->pdgId();
			int status = it->status();

			//	Z
			if (abs(id)==analysis::core::PDG_ID_Z && (status==22 || status==3))
			{
				foundZ = true;
				_genZpreFSR._mass = it->mass();
				_genZpreFSR._pt = it->pt();
				_genZpreFSR._eta = it->eta();
				_genZpreFSR._rapid = it->rapidity();
				_genZpreFSR._phi = it->phi();
			}
			if (abs(id)==analysis::core::PDG_ID_Z && (status==62 || status==2))
			{
				_genZpostFSR._mass = it->mass();
				_genZpostFSR._pt = it->pt();
				_genZpostFSR._eta = it->eta();
				_genZpostFSR._rapid = it->rapidity();
				_genZpostFSR._phi = it->phi();
			}

			//	W
			if (abs(id)==analysis::core::PDG_ID_W && (status==22 || status==3))
			{
				foundW = true;
				_genWpreFSR._mass = it->mass();
				_genWpreFSR._pt = it->pt();
				_genWpreFSR._eta = it->eta();
				_genWpreFSR._rapid = it->rapidity();
				_genWpreFSR._phi = it->phi();
			}
			if (abs(id)==analysis::core::PDG_ID_W && (status==62 || status==2))
			{
				_genWpostFSR._mass = it->mass();
				_genWpostFSR._pt = it->pt();
				_genWpostFSR._eta = it->eta();
				_genWpostFSR._rapid = it->rapidity();
				_genWpostFSR._phi = it->phi();
			}

			//	H
			if (abs(id)==analysis::core::PDG_ID_H && (status==22 || status==3))
			{
				foundH = true;
				_genHpreFSR._mass = it->mass();
				_genHpreFSR._pt = it->pt();
				_genHpreFSR._eta = it->eta();
				_genHpreFSR._rapid = it->rapidity();
				_genHpreFSR._phi = it->phi();
			}
			if (abs(id)==analysis::core::PDG_ID_H && (status==62 || status==2))
			{
				_genHpostFSR._mass = it->mass();
				_genHpostFSR._pt = it->pt();
				_genHpostFSR._eta = it->eta();
				_genHpostFSR._rapid = it->rapidity();
				_genHpostFSR._phi = it->phi();
			}

			//	Mu
			if (abs(id)==analysis::core::PDG_ID_Mu 
				&& (status==23 || status==3))
				hardProcessMuons.push_back(*it);
		}

		if (foundZ && hardProcessMuons.size()==2)
		{
			_track1ZpreFSR._pt = hardProcessMuons[0].pt();
			_track1ZpreFSR._eta = hardProcessMuons[0].eta();
			_track1ZpreFSR._phi = hardProcessMuons[0].phi();
			_track1ZpreFSR._charge = hardProcessMuons[0].charge();
			_track2ZpreFSR._pt = hardProcessMuons[1].pt();
			_track2ZpreFSR._eta = hardProcessMuons[1].eta();
			_track2ZpreFSR._phi = hardProcessMuons[1].phi();
			_track2ZpreFSR._charge = hardProcessMuons[1].charge();
		}
		if (foundW && hardProcessMuons.size()==1)
		{
			_trackWpreFSR._pt = hardProcessMuons[0].pt();
			_trackWpreFSR._eta = hardProcessMuons[0].eta();
			_trackWpreFSR._phi = hardProcessMuons[0].phi();
			_trackWpreFSR._charge = hardProcessMuons[0].charge();
		}
		if (foundH && hardProcessMuons.size()==2)
		{
			_track1HpreFSR._pt = hardProcessMuons[0].pt();
			_track1HpreFSR._eta = hardProcessMuons[0].eta();
			_track1HpreFSR._phi = hardProcessMuons[0].phi();
			_track1HpreFSR._charge = hardProcessMuons[0].charge();
			_track2HpreFSR._pt = hardProcessMuons[1].pt();
			_track2HpreFSR._eta = hardProcessMuons[1].eta();
			_track2HpreFSR._phi = hardProcessMuons[1].phi();
			_track2HpreFSR._charge = hardProcessMuons[1].charge();
		}

		//
		//	Packed Gen Particles
		//
		edm::Handle<pat::PackedGenParticleCollection> hPackedGenParticles;
		e.getByToken(_tokPackedGenParticles, hPackedGenParticles);
		pat::PackedGenParticleCollection finalStateGenMuons;
		for (pat::PackedGenParticleCollection::const_iterator it=
			hPackedGenParticles->begin(); it!=hPackedGenParticles->end();
			++it)
			if (abs(it->pdgId())==13)
				finalStateGenMuons.push_back(*it);
		if (foundZ && finalStateGenMuons.size()==2)
		{
			_track1ZpostFSR._pt = finalStateGenMuons[0].pt();
			_track1ZpostFSR._eta = finalStateGenMuons[0].eta();
			_track1ZpostFSR._phi = finalStateGenMuons[0].phi();
			_track1ZpostFSR._charge = finalStateGenMuons[0].charge();
			_track2ZpostFSR._pt = finalStateGenMuons[1].pt();
			_track2ZpostFSR._eta = finalStateGenMuons[1].eta();
			_track2ZpostFSR._phi = finalStateGenMuons[1].phi();
			_track2ZpostFSR._charge = finalStateGenMuons[1].charge();
		}
		if (foundW && finalStateGenMuons.size()==1)
		{
			_trackWpostFSR._pt = finalStateGenMuons[0].pt();
			_trackWpostFSR._eta = finalStateGenMuons[0].eta();
			_trackWpostFSR._phi = finalStateGenMuons[0].phi();
			_trackWpostFSR._charge = finalStateGenMuons[0].charge();
		}
		if (foundH && finalStateGenMuons.size()==2)
		{
			_track1HpostFSR._pt = finalStateGenMuons[0].pt();
			_track1HpostFSR._eta = finalStateGenMuons[0].eta();
			_track1HpostFSR._phi = finalStateGenMuons[0].phi();
			_track1HpostFSR._charge = finalStateGenMuons[0].charge();
			_track2HpostFSR._pt = finalStateGenMuons[1].pt();
			_track2HpostFSR._eta = finalStateGenMuons[1].eta();
			_track2HpostFSR._phi = finalStateGenMuons[1].phi();
			_track2HpostFSR._charge = finalStateGenMuons[1].charge();
		}

		//
		//	Gen Jet
		//
		edm::Handle < reco::GenJetCollection > hGenJets;
		e.getByToken(_tokGenJets, hGenJets);
		if (!hGenJets.isValid())
		{
			std::cout << "Gen Jet Product is not found" << std::endl;
		}
		else
		{
			reco::GenJetCollection sortedGenJets = (*hGenJets);
			sort(sortedGenJets.begin(), sortedGenJets.end(),
				[](reco::GenJet it, reco::GenJet jt) -> bool
				{return it.pt()>jt.pt();});
			int n=0; 
			for (uint32_t i=0; i<sortedGenJets.size(); i++)
			{
				if (n==10)
					break;
				analysis::core::GenJet genjet;
				genjet._px = sortedGenJets[i].px();
				genjet._py = sortedGenJets[i].py();
				genjet._pz = sortedGenJets[i].pz();
				genjet._py = sortedGenJets[i].pt();
				genjet._eta = sortedGenJets[i].eta();
				genjet._phi = sortedGenJets[i].phi();
				genjet._mass = sortedGenJets[i].mass();
				_genjets.push_back(genjet);
				n++;
			}
		}
	}

	//	
	//	HLT
	//	- Skip the event if HLT has not fired
	//
	e.getByToken(_tokTriggerResults, _hTriggerResults);
	e.getByToken(_tokTriggerObjects, _hTriggerObjects);
	if (!_hTriggerResults.isValid())
	{
		std::cout << "### Trigger Results Product is not found" << std::endl;
		return;
	}
	if (!_hTriggerObjects.isValid())
	{
		std::cout << "### Trigger Results Product is not found" << std::endl;
		return;
	}
	if (_meta._checkTrigger)
		if (!passHLT(e))
			return;

	//	
	//	Event Info
	//
	_event._run = e.id().run();
	_event._lumi = e.id().luminosityBlock();
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
	}
	else
	{
		_met._px = (*hMET)[0].px();
		_met._py = (*hMET)[0].py();
		_met._pt = (*hMET)[0].pt();
		_met._phi = (*hMET)[0].phi();
		_met._sumEt = (*hMET)[0].sumEt();
	}

	//
	//	Jet
	//
	edm::Handle < std::vector<pat::Jet> > hJets;
	e.getByToken(_tokJets, hJets);
	if (!hJets.isValid())
	{
		std::cout << "Jet Product is not found" << std::endl;
	}
	{
		int n =0;
		for (uint32_t i=0; i<hJets->size(); i++)
		{
			if (n==10)
				break;
			const pat::Jet &jet = hJets->at(i);
			analysis::core::Jet myjet;
			myjet._px = jet.px();
			myjet._py = jet.py();
			myjet._pz = jet.pz();
			myjet._pt = jet.pt();
			myjet._eta = jet.eta();
			myjet._phi = jet.phi();
			myjet._mass = jet.mass();
			myjet._partonFlavour = jet.partonFlavour();

			myjet._chf = jet.chargedHadronEnergyFraction();
			myjet._nhf = jet.neutralHadronEnergyFraction();
			myjet._cef = jet.chargedEmEnergyFraction();
			myjet._nef = jet.neutralEmEnergyFraction();
			myjet._muf = jet.muonEnergyFraction();
			myjet._hfhf = jet.HFHadronEnergyFraction();
			myjet._hfef = jet.HFEMEnergyFraction();
			
			myjet._cm = jet.chargedMultiplicity();
			myjet._chm = jet.chargedHadronMultiplicity();
			myjet._nhm = jet.neutralHadronMultiplicity();
			myjet._cem = jet.electronMultiplicity();
			myjet._nem = jet.photonMultiplicity();
			myjet._mum = jet.muonMultiplicity();
			myjet._hfhm = jet.HFHadronMultiplicity();
			myjet._hfem = jet.HFEMMultiplicity();

			myjet._jecu = -1.;
			myjet._jecf = jet.jecFactor("Uncorrected");
//			myjet._csv = jet.bDiscriminator(
//				"combinedSecondaryVertexBJetTags");
			myjet._puid = jet.userFloat("pileupJetId:fullDiscriminant");

			//	matche gen jet
			const reco::GenJet *genJet = jet.genJet();
			if (genJet!=NULL)
			{
				myjet._genMatched=true;
				myjet._genjet._px = genJet->px();
				myjet._genjet._py = genJet->py();
				myjet._genjet._pz = genJet->pz();
				myjet._genjet._pt = genJet->pt();
				myjet._genjet._eta = genJet->eta();
				myjet._genjet._phi = genJet->phi();
				myjet._genjet._mass = genJet->mass();
				myjet._genemf = genJet->emEnergy()/genJet->energy();
				myjet._genhadf = genJet->hadEnergy()/genJet->energy();
				myjet._geninvf = genJet->invisibleEnergy()/genJet->energy();
				myjet._genauxf = genJet->auxiliaryEnergy()/genJet->energy();
			}
			else
				myjet._genMatched=false;

			_pfjets.push_back(myjet);
			n++;
		}
	}

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
		//	global vs tracker vs standalone
		if (!it->isGlobalMuon() && _meta._isGlobalMuon)
			continue;
		if (!it->isTrackerMuon() && _meta._isTrackerMuon)
			continue;
		if (!it->isGlobalMuon() && !it->isTrackerMuon())
			continue;

		//	kinematic
		if (!passKinCuts(*it, hBS))
			continue;

		muonsSelected.push_back(*it);
	}

	//	skip the event if the #muons is not what we need
	if (muonsSelected.size()<_meta._nMuons)
		return;

	//	
	//	Muon Pre-Selection 2 based on #muons @1
	//
	if (muonsSelected.size()==0 || muonsSelected.size()==1) // 0 muons
		return;
	else // 2 or more muons
	{
		//	construct dimuon candidates
		typedef std::pair<pat::Muon, pat::Muon> MuonPair;
		typedef std::vector<MuonPair> MuonPairs;
		MuonPairs muonPairs;
		for (pat::MuonCollection::const_iterator it=muonsSelected.begin();
			it!=muonsSelected.end(); ++it)
			for (pat::MuonCollection::const_iterator jt=(it+1);
				jt!=muonsSelected.end(); ++jt)
				muonPairs.push_back(MuonPair(*it, *jt));
		std::sort(muonPairs.begin(), muonPairs.end(), 
			[](MuonPair p1, MuonPair p2)
			{
				TLorentzVector m11, m12, d1;
				reco::Track const t11 = *(p1.first.innerTrack());
				reco::Track const t12 = *(p1.second.innerTrack());
				TLorentzVector m21, m22, d2;
				reco::Track const t21 = *(p2.first.innerTrack());
				reco::Track const t22 = *(p2.second.innerTrack());

				m11.SetPtEtaPhiM(t11.pt(), t11.eta(), t11.phi(),
					analysis::core::PDG_MASS_Mu);
				m12.SetPtEtaPhiM(t12.pt(), t12.eta(), t12.phi(),
					analysis::core::PDG_MASS_Mu);
				m21.SetPtEtaPhiM(t21.pt(), t21.eta(), t21.phi(),
					analysis::core::PDG_MASS_Mu);
				m22.SetPtEtaPhiM(t22.pt(), t22.eta(), t22.phi(),
					analysis::core::PDG_MASS_Mu);

				d1 = m11 + m12;
				d2 = m21 + m22;
				return fabs(d1.M()-analysis::core::PDG_MASS_Z)<
					fabs(d2.M()-analysis::core::PDG_MASS_Z);
			}
		);

		for (MuonPairs::const_iterator it=muonPairs.begin();
			it!=muonPairs.end(); ++it)
		{
			pat::Muon mu1 = it->first; 
			analysis::core::Muon _muon1;
			pat::Muon mu2 = it->second;
			analysis::core::Muon _muon2;

			double isovar1 = mu1.isolationR03().sumPt;
			isovar1+= mu1.isolationR03().hadEt;
			isovar1/=mu1.pt();
			
			double isovar2 = mu2.isolationR03().sumPt;
			isovar2+= mu2.isolationR03().hadEt;
			isovar2/=mu2.pt();

			_muon1._relCombIso = isovar1;
			_muon2._relCombIso = isovar2;
			_muon1._trackIsoSumPt = mu1.isolationR03().sumPt;
			_muon2._trackIsoSumPt = mu2.isolationR03().sumPt;
			_muon1._trackIsoSumPtCorr = mu1.isolationR03().sumPt;
			_muon2._trackIsoSumPtCorr = mu2.isolationR03().sumPt;

			if (mu1.innerTrack().isNonnull())
			{
				double deta = mu1.track()->eta()-mu2.track()->eta();
				double dphi = fabs(mu1.track()->phi()-mu2.track()->phi());
				if (dphi>analysis::core::NUM_PI)
					dphi = 2.*analysis::core::NUM_PI - dphi;
				if (sqrt(deta*deta + dphi*dphi)<0.3 &&
					_muon2._trackIsoSumPt>0.9*mu1.track()->pt())
					_muon2._trackIsoSumPtCorr = 
						_muon2._trackIsoSumPt-mu1.track()->pt();
			}
			if (mu2.innerTrack().isNonnull())
			{
				double deta = mu2.track()->eta()-mu1.track()->eta();
				double dphi = fabs(mu2.track()->phi()-mu1.track()->phi());
				if (dphi>analysis::core::NUM_PI)
					dphi = 2.*analysis::core::NUM_PI - dphi;
				if (sqrt(deta*deta + dphi*dphi)<0.3 &&
					_muon1._trackIsoSumPt>0.9*mu2.track()->pt())
					_muon1._trackIsoSumPtCorr = 
						_muon1._trackIsoSumPt-mu2.track()->pt();
			}

			_muon1._isPF = mu1.isPFMuon(); _muon2._isPF = mu2.isPFMuon();
			if (mu1.isPFMuon())
			{
				reco::Candidate::LorentzVector pfm = mu1.pfP4();
				_muon1._pt = pfm.Pt();
				_muon1._eta = pfm.Eta();
				_muon1._phi = pfm.Phi();
				_muon1._sumChargedHadronPtR03 = 
					mu1.pfIsolationR03().sumChargedHadronPt;
				_muon1._sumChargedParticlePtR03 = 
					mu1.pfIsolationR03().sumChargedParticlePt;
				_muon1._sumNeutralHadronEtR03 = 
					mu1.pfIsolationR03().sumNeutralHadronEt;
				_muon1._sumPhotonEtR03 = mu1.pfIsolationR03().sumPhotonEt;
				_muon1._sumPUPtR03 = mu1.pfIsolationR03().sumPUPt;
				_muon1._sumChargedHadronPtR04 = 
					mu1.pfIsolationR04().sumChargedHadronPt;
				_muon1._sumChargedParticlePtR04 = 
					mu1.pfIsolationR04().sumChargedParticlePt;
				_muon1._sumNeutralHadronEtR04 = 
					mu1.pfIsolationR04().sumNeutralHadronEt;
				_muon1._sumPhotonEtR04 = mu1.pfIsolationR04().sumPhotonEt;
				_muon1._sumPUPtR04 = mu1.pfIsolationR04().sumPUPt;
			}
			if (mu2.isPFMuon())
			{
				reco::Candidate::LorentzVector pfm = mu2.pfP4();
				_muon2._pt = pfm.Pt();
				_muon2._eta = pfm.Eta();
				_muon2._phi = pfm.Phi();
				_muon2._sumChargedHadronPtR03 = 
					mu2.pfIsolationR03().sumChargedHadronPt;
				_muon2._sumChargedParticlePtR03 = 
					mu2.pfIsolationR03().sumChargedParticlePt;
				_muon2._sumNeutralHadronEtR03 = 
					mu2.pfIsolationR03().sumNeutralHadronEt;
				_muon2._sumPhotonEtR03 = mu2.pfIsolationR03().sumPhotonEt;
				_muon2._sumPUPtR03 = mu2.pfIsolationR03().sumPUPt;
				_muon2._sumChargedHadronPtR04 = 
					mu2.pfIsolationR04().sumChargedHadronPt;
				_muon2._sumChargedParticlePtR04 = 
					mu2.pfIsolationR04().sumChargedParticlePt;
				_muon2._sumNeutralHadronEtR04 = 
					mu2.pfIsolationR04().sumNeutralHadronEt;
				_muon2._sumPhotonEtR04 = mu2.pfIsolationR04().sumPhotonEt;
				_muon2._sumPUPtR04 = mu2.pfIsolationR04().sumPUPt;
			}

			if (_muon1._trackIsoSumPt > _meta._maxTrackIsoSumPt) return;
			if (_muon2._trackIsoSumPt > _meta._maxTrackIsoSumPt) return;
			if (_muon1._relCombIso > _meta._maxRelCombIso) return;
			if (_muon2._relCombIso > _meta._maxRelCombIso) return;
			if (!(passKinCuts(mu1, hBS) && passKinCuts(mu2, hBS)))
				return;
	
			//	fill the muon1 information
			_muon1._isGlobal = mu1.isGlobalMuon();
			_muon1._isTracker = mu1.isTrackerMuon();
			_muon1._isStandAlone = mu1.isStandAloneMuon();
			reco::Track track1;
			if (mu1.isGlobalMuon()) track1 = *(mu1.globalTrack());
			else if (mu1.isTrackerMuon()) track1 = *(mu1.innerTrack());
			else
				return;

			_muon1._charge = mu1.charge();
			_muon1._pt = mu1.pt();
			_muon1._pterr = track1.ptError();
			_muon1._eta = mu1.eta();
			_muon1._phi = mu1.phi();
			if (mu1.isTrackerMuon())
			{
				_muon1._track._pt = mu1.innerTrack()->pt();
				_muon1._track._pterr = mu1.innerTrack()->ptError();
				_muon1._track._eta  = mu1.innerTrack()->eta();
				_muon1._track._phi = mu1.innerTrack()->phi();
			}
			_muon1._normChi2 = track1.normalizedChi2();
			_muon1._d0BS = track1.dxy(hBS->position());
			_muon1._dzBS = track1.dz(hBS->position());
			reco::Vertex bestVtx1;
			for (reco::VertexCollection::const_iterator vt=hVertices->begin();
				vt!=hVertices->end(); ++vt)
			{
				if (!vt->isValid()) continue;
				_muon1._d0PV = track1.dxy(vt->position());
				_muon1._dzPV = track1.dz(vt->position());
				bestVtx1 = *vt;
				break;
			}
			_muon1._isTight = muon::isTightMuon(mu1, bestVtx1);
			_muon1._isMedium = muon::isMediumMuon(mu1);
			_muon1._isLoose = muon::isLooseMuon(mu1);
			_muon1._nTLs = 
				mu1.innerTrack()->hitPattern().trackerLayersWithMeasurement();
			_muon1._nPLs = 
				mu1.innerTrack()->hitPattern().pixelLayersWithMeasurement();
			_muon1._nSLs = 
				mu1.innerTrack()->hitPattern().stripLayersWithMeasurement();

			_muon1._vfrTrk = mu1.innerTrack()->validFraction();
			_muon1._nvMHits = track1.hitPattern().numberOfValidMuonHits();
			_muon1._nvPHits = 
				mu1.innerTrack()->hitPattern().numberOfValidPixelHits();
			_muon1._nvTHits = 
				mu1.innerTrack()->hitPattern().numberOfValidTrackerHits();
			_muon1._nvSHits = 
				mu1.innerTrack()->hitPattern().numberOfValidStripHits();
			_muon1._nSegMts = mu1.numberOfMatches();
			_muon1._nMtsStations = mu1.numberOfMatchedStations();
			_muon1._eIso = mu1.isolationR03().emEt;
			_muon1._hIso = mu1.isolationR03().hadEt;
			_muon1._segmentCompatibility = muon::segmentCompatibility(mu1);
			_muon1._combinedQChi2LocalPosition = 
				mu1.combinedQuality().chi2LocalPosition;
			_muon1._combinedQTrkKink = mu1.combinedQuality().trkKink;
			for (uint32_t i=0; i<_meta._triggerNames.size(); i++)
			{
				bool match = isHLTMatched(i, e, mu1);
				_muon1._isHLTMatched.push_back(match);
			}

			//	muon2
			_muon2._isGlobal = mu2.isGlobalMuon();
			_muon2._isTracker = mu2.isTrackerMuon();
			_muon2._isStandAlone = mu2.isStandAloneMuon();
			reco::Track track2;
			if (mu2.isGlobalMuon()) track2 = *(mu2.globalTrack());
			else if (mu2.isTrackerMuon()) track2 = *(mu2.innerTrack());
			else
				return;

			_muon2._charge = mu2.charge();
			_muon2._pt = mu2.pt();
			_muon2._pterr = track2.ptError();
			_muon2._eta = mu2.eta();
			_muon2._phi = mu2.phi();
			if (mu2.isTrackerMuon())
			{
				_muon2._track._pt = mu2.innerTrack()->pt();
				_muon2._track._pterr = mu2.innerTrack()->ptError();
				_muon2._track._eta  = mu2.innerTrack()->eta();
				_muon2._track._phi = mu2.innerTrack()->phi();
			}
			_muon2._normChi2 = track2.normalizedChi2();
			_muon2._d0BS = track2.dxy(hBS->position());
			_muon2._dzBS = track2.dz(hBS->position());
			reco::Vertex bestVtx2;
			for (reco::VertexCollection::const_iterator vt=hVertices->begin();
				vt!=hVertices->end(); ++vt)
			{
				if (!vt->isValid()) continue;
				_muon2._d0PV = track2.dxy(vt->position());
				_muon2._dzPV = track2.dz(vt->position());
				bestVtx2 = *vt;
				break;
			}
			_muon2._isTight = muon::isTightMuon(mu2, bestVtx2);
			_muon2._isMedium = muon::isMediumMuon(mu2);
			_muon2._isLoose = muon::isLooseMuon(mu2);
			_muon2._nTLs = 
				mu2.innerTrack()->hitPattern().trackerLayersWithMeasurement();
			_muon2._nPLs = 
				mu2.innerTrack()->hitPattern().pixelLayersWithMeasurement();
			_muon2._nSLs = 
				mu2.innerTrack()->hitPattern().stripLayersWithMeasurement();

			_muon2._vfrTrk = mu2.innerTrack()->validFraction();
			_muon2._nvMHits = track2.hitPattern().numberOfValidMuonHits();
			_muon2._nvPHits = 
				mu2.innerTrack()->hitPattern().numberOfValidPixelHits();
			_muon2._nvTHits = 
				mu2.innerTrack()->hitPattern().numberOfValidTrackerHits();
			_muon2._nvSHits = 
				mu2.innerTrack()->hitPattern().numberOfValidStripHits();
			_muon2._nSegMts = mu2.numberOfMatches();
			_muon2._nMtsStations = mu2.numberOfMatchedStations();
			_muon2._eIso = mu2.isolationR03().emEt;
			_muon2._hIso = mu2.isolationR03().hadEt;
			_muon2._segmentCompatibility = muon::segmentCompatibility(mu2);
			_muon2._combinedQChi2LocalPosition = 
				mu2.combinedQuality().chi2LocalPosition;
			_muon2._combinedQTrkKink = mu2.combinedQuality().trkKink;
			for (uint32_t i=0; i<_meta._triggerNames.size(); i++)
			{
				bool match = isHLTMatched(i, e, mu2);
				_muon2._isHLTMatched.push_back(match);
			}

			//
			//	Below DiMuon variables - which could be obtained from 
			//	other ones....
			//
			/*
			reco::Track const mt1 = *(mu1.innerTrack());
			reco::Track const mt2 = *(mu2.innerTrack());
			TLorentzVector p4_dimuon = TLorentzVector().SetPtEtaPhiM(
				mt1.pt(), mt1.eta(), mt1.phi(),
				analysis::PDG_MASS_Mu) + TLorentzVector().SetPtEtaPhiM(
				mt2.pt(), mt2.eta(), mt2.phi(), 
				anallysis::PDG_MASS_Mu);

			_dimuon._mass = p4_dimuon.M();
			_dimuon._pt = p4_dimuon.Pt();
			_dimuon._eta = p4_dimuon.PseudoRapidity();
			_dimuon._rapid = p4_dimuon.Rapidity();
			_dimuon._phi = p4_dimuon.Phi();
			*/

			_muons1.push_back(_muon1);
			_muons2.push_back(_muon2);
		}
	}

	//
	//	Dump objects to The ROOT Tree - ONLY after passing all the cuts
	//
	_tEvents->Fill();
#endif
}

//
//	true - passes HLT selections
//	false - doesn't pass
//
bool H2DiMuonMaker::passHLT(edm::Event const& e)
{
#if 0
	const boost::regex re("_v[0-9]+");
	edm::TriggerNames const& triggerNames = e.triggerNames(*_hTriggerResults);

	bool pass=false;
	for (uint32_t i=0; i<_hTriggerResults->size(); i++)
	{
		std::string triggerName = triggerNames.triggerName(i);
		string tstripped = boost::regex_replace(triggerName, re, "",
			boost::match_default | boost::format_sed);
		for (std::vector<std::string>::const_iterator dit=
			_meta._triggerNames.begin(); dit!=_meta._triggerNames.end(); ++dit)
			if (*dit == tstripped)
			{
				if (_hTriggerResults->accept(i))
				{
					_eaux._hasHLTFired.push_back(true);
					pass=true;
				}
				else
					_eaux._hasHLTFired.push_back(false);
			}
	}

	return pass;
#endif
    return true;
}

//	
//	true - matched
//	false - didn't match
//
bool H2DiMuonMaker::isHLTMatched(uint32_t itrigger, edm::Event const& e,
	pat::Muon const& mu)
{
#if 0
	const boost::regex re("_v[0-9]+");
	edm::TriggerNames const& triggerNames = e.triggerNames(*_hTriggerResults);
	for (uint32_t i=0; i<_hTriggerResults->size(); i++)
	{
		std::string triggerName = triggerNames.triggerName(i);
		std::string tstripped = boost::regex_replace(triggerName, re, "",
			boost::match_default | boost::format_sed);
		if (_meta._triggerNames[itrigger]==tstripped &&
			_hTriggerResults->accept(i))
		{
			for (pat::TriggerObjectStandAloneCollection::const_iterator it=
				_hTriggerObjects->begin(); it!=_hTriggerObjects->end(); ++it)
			{
				pat::TriggerObjectStandAlone tmp(*it);
				tmp.unpackPathNames(triggerNames);
				bool right = tmp.hasPathName(triggerName, true, true);
				if (right && (deltaR(tmp, mu)<0.2))
					return true;
			}
		}
	}

	return false;
#endif

    return true;
}

//
//	true - passes Kinematic Cuts
//	false - doesn't pass
//
bool H2DiMuonMaker::passKinCuts(pat::Muon const& muon,
	edm::Handle<reco::BeamSpot> const& hBS)
{
	reco::Track track;
	if (muon.isGlobalMuon()) track = *(muon.globalTrack());
	else if (muon.isTrackerMuon())
		track = *(muon.innerTrack());
	else
		return false;

	if (muon.pt() < _meta._minPt) return false;
	if (fabs(muon.eta()) > _meta._maxeta) return false;
	if (track.hitPattern().numberOfValidTrackerHits() < 
		_meta._minTrackerHits)
		return false;
	if (fabs(track.dxy(hBS->position())) > _meta._maxd0) return false;
	if (track.hitPattern().pixelLayersWithMeasurement() < 
		_meta._minPixelLayers)
		return false;
	if (track.hitPattern().trackerLayersWithMeasurement() < 
		_meta._minTrackerLayers)
		return false;
	if (track.hitPattern().stripLayersWithMeasurement() < 
		_meta._minStripLayers)
		return false;
	if (track.validFraction() < _meta._minValidFractionTracker)
		return false;
	if (track.hitPattern().numberOfValidMuonHits() < 
		_meta._minMuonHits)
		return false;
	if (track.hitPattern().numberOfValidPixelHits() < 
		_meta._minPixelHits)
		return false;
	if (track.hitPattern().numberOfValidStripHits() <
		_meta._minStripHits)
		return false;
	if (muon.numberOfMatches() < _meta._minSegmentMatches)
		return false;
	if (muon.numberOfMatchedStations() < _meta._minMatchedStations)
		return false;
	if (track.normalizedChi2() > _meta._maxNormChi2)
		return false;

	return true;
}

DEFINE_FWK_MODULE(H2DiMuonMaker);
