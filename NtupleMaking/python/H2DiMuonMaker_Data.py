import FWCore.ParameterSet.Config as cms
pt = 24

#   to switch between modules
name = "H2DiMuonMaker_NoPairing"

ntuplemaker_H2DiMuonMaker = cms.EDAnalyzer(name,
    #   Tags
    tagMuons = cms.untracked.InputTag("slimmedMuons"),
    tagElectrons = cms.untracked.InputTag("slimmedElectrons"),
    tagTaus = cms.untracked.InputTag("slimmedTaus"),
    tagPV = cms.untracked.InputTag("offlineSlimmedPrimaryVertices"),
    tagBS = cms.untracked.InputTag("offlineBeamSpot"),
    tagPrunedGenParticles = cms.untracked.InputTag("prunedGenParticles"),
    tagPackedGenParticles = cms.untracked.InputTag("packedGenParticles"),
    tagTriggerResults = cms.untracked.InputTag("TriggerResults", "", "HLT"),
    tagTriggerObjects = cms.untracked.InputTag("selectedPatTrigger"),
    tagMET = cms.untracked.InputTag("slimmedMETs"),
    tagPFJets = cms.untracked.InputTag("slimmedJets"),
    tagGenJets = cms.untracked.InputTag("slimmedGenJets"),
    
    #   for electron id
    tagElectronCutBasedId_veto = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto"),
    tagElectronCutBasedId_loose = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose"),
    tagElectronCutBasedId_medium = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium"),
    tagElectronCutBasedId_tight = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight"),

	#
	#	Meta Data
	#
    triggerNames = cms.untracked.vstring(
        "HLT_IsoMu%d" % pt, "HLT_IsoTkMu%d" % pt, "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"
    ),
    checkTrigger = cms.untracked.bool(True),
	isMC = cms.untracked.bool(False),
	nMuons = cms.untracked.int32(2),
	isGlobalMuon = cms.untracked.bool(False),
	isStandAloneMuon = cms.untracked.bool(False),
	isTrackerMuon = cms.untracked.bool(True),
	minPt = cms.untracked.double(10),
	maxeta = cms.untracked.double(2.4),
	maxNormChi2 = cms.untracked.double(999),
	minMuonHits = cms.untracked.int32(-999),
	minPixelHits = cms.untracked.int32(-999),
	minStripHits = cms.untracked.int32(-999),
	minTrackerHits = cms.untracked.int32(-999),
	minSegmentMatches = cms.untracked.int32(-999),
	minMatchedStations = cms.untracked.int32(-999),
	minPixelLayers  = cms.untracked.int32(-999),
	minTrackerLayers = cms.untracked.int32(-999),
	minStripLayers = cms.untracked.int32(-999),
	minValidFractionTracker = cms.untracked.double(-999),
	maxd0 = cms.untracked.double(999),
	maxTrackIsoSumPt = cms.untracked.double(999),
	maxRelCombIso = cms.untracked.double(999),

        #
        #   Some flags
        #
    useElectrons = cms.untracked.bool(True),
    useTaus = cms.untracked.bool(False)
)
