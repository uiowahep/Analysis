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

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

// user include files
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

//
// math classes
//
#include "DataFormats/Math/interface/deltaR.h"
//
// trigger
// 
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"

//
// vertexing
//
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

//
// gen particles
//
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Candidate/interface/CompositePtrCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"

// 2010.11.21 Adding the Muon Cocktail
#include "DataFormats/MuonReco/interface/MuonCocktails.h"
#include "DataFormats/Math/interface/deltaR.h"

// pfJets and MET
//#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"

// PU Info
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "DataFormats/Common/interface/View.h"

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
		using namespace analysis::core;
		Muons		_muons;
		Jets		_pfjets;
		Vertices	_vertices;
		Tracks		_tracks;
		Event		_event;
		MET			_met;
		GenJets		_genjets;
		GenParticles _genparts;

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
		edm::EDGetTokenT<reco::VertexCollection> _tokVertex;
		edm::EDGetTokenT<std::vector<PileupSummaryInfo> > _tokPU;
		edm::EDGetTokenT<reco::BeamSpot> _tokBS;
		edm::EDGetTokenT<reco::GenParticleCollection> _tokPrunedGenParticle;
		edm::EDGetTokenT<pat::PackedGenParticleCollection> 
			_tokPackedGenParticle;
		edm::EDGetTokenT<std::vector<pat::MET> > _tokMET;
		edm::EDGetTokenT<std::vector<pat::Jet> > _tokJet;
		edm::EDGetTokenT<reco::GenJetCollection> _tokGenJet;
		edm::EDGetTokenT<pat::MuonCollection> _tokMuon;
		edm::EDGetTokenT<edm::ValueMap<float> > _tokPUJetIdFloat;
		edm::EDGetTokenT<edm::ValueMap<float> > _tokPUJetIdInt;
};

H2DiMuonMaker::H2DiMuonMaker(edm::ParameterSet const& ps)
{
	//
	//	init the Trees and create branches
	//
	edm::Service<TFileService> fs;
	_tEvents = fs->make<TTree>("Events", "Events");
	_tMeta = fs->make<TTree>("Meta", "Meta");

	using namespace analysis::core
	_tEvents->Branch("Muons", (Muons*)&_muons);
	_tEvents->Branch("Jets", (Jets*)&_pfjets);
	_tEvents->Branch("Vertices", (Vertices*)&_vertices);
	_tEvents->Branch("Tracks", (Tracks*)&_tracks);
	_tEvents->Branch("Event", (Event*)&_event);
	_tEvents->Branch("MET", (MET*)&_met);
	_tEvents->Branch("GenJets", (GenJets*)&_genjets);
	_tEvents->Branch("GenParticles", (GenParticles*)&_genparts);

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
}

void H2DiMuonMaker::beginJob()
{}

void H2DiMuonMaker::endJob()
{}

void H2DiMuonMaker::analyze()
{
	std::cout << "Processing..." << std::endl;
}

DEFINE_FWK_MODULE(H2DiMuonMaker);
