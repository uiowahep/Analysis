import FWCore.ParameterSet.Config as cms
pt = 22

ntuplemaker_H2DiMuonMaker = cms.EDAnalyzer('H2DiMuonMaker',
    #   Tags
    tagMuons = cms.untracked.InputTag("slimmedMuons"),
    tagPV = cms.untracked.InputTag("offlineSlimmedPrimaryVertices"),
    tagBS = cms.untracked.InputTag("offlineBeamSpot"),
    tagPrunedGenParticles = cms.untracked.InputTag("prunedGenParticles"),
    tagPackedGenParticles = cms.untracked.InputTag("packedGenParticles"),
    tagTriggerResults = cms.untracked.InputTag("TriggerResults", "", "HLT"),
    tagTriggerObjects = cms.untracked.InputTag("selectedPatTrigger"),
    tagMET = cms.untracked.InputTag("slimmedMETs"),
    tagPFJets = cms.untracked.InputTag("slimmedJets"),
    tagGenJets = cms.untracked.InputTag("slimmedGenJets"),

	#
	#	Meta Data
	#
    triggerNames = cms.untracked.vstring(
        "HLT_IsoMu%d" % pt, "HLT_IsoTkMu%d" % pt, "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"
    ),
    checkTrigger = cms.untracked.bool(True),
	isMC = cms.untracked.bool(True),
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
)
