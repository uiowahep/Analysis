import FWCore.ParameterSet.Config as cms
pt = 24

name = "H2DiMuonMaker_NoPairing"
hlt = "HLT"

ntuplemaker_H2DiMuonMaker = cms.EDAnalyzer(name,
    #   Tags
    tagMuons = cms.untracked.InputTag("slimmedMuons"),
    tagElectrons = cms.untracked.InputTag("slimmedElectrons"),
    tagTaus = cms.untracked.InputTag("slimmedTaus"),
    tagPV = cms.untracked.InputTag("offlineSlimmedPrimaryVertices"),
    tagBS = cms.untracked.InputTag("offlineBeamSpot"),
    tagPrunedGenParticles = cms.untracked.InputTag("prunedGenParticles"),
    tagPackedGenParticles = cms.untracked.InputTag("packedGenParticles"),
    tagTriggerResults = cms.untracked.InputTag("TriggerResults", "", hlt),
    tagTriggerObjects = cms.untracked.InputTag("selectedPatTrigger"),
    tagMET = cms.untracked.InputTag("slimmedMETs"),
    tagPFJets = cms.untracked.InputTag("slimmedJets"),
    tagGenJets = cms.untracked.InputTag("slimmedGenJets"),
    tagConversions = cms.untracked.InputTag("reducedEgamma:reducedConversions"),

    # electron cut based id
    tagElectronCutBasedId_veto = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto"),
    tagElectronCutBasedId_loose = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose"),
    tagElectronCutBasedId_medium = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium"),
    tagElectronCutBasedId_tight = cms.untracked.InputTag("egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight"),

    # mva based id
    tagElectornMVAGPId_medium = cms.untracked.InputTag("egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp90"),
    tagElectronMVAGPId_tight = cms.untracked.InputTag("egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp80"),

    tagElectronMVAGP_values = cms.untracked.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),
    tagElectronMVAGP_categories = cms.untracked.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Categories"),

    # mva HZZ based id
    tagElectronMVAHZZId_loose = cms.untracked.InputTag("egmGsfElectronIDs:mvaEleID-Spring16-HZZ-V1-wpLoose"),
    tagElectronMVAHZZ_values = cms.untracked.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1Values"),
    tagElectronMVAHZZ_categories = cms.untracked.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16HZZV1Categories"),

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
    btagNames = cms.untracked.vstring(["pfCombinedInclusiveSecondaryVertexV2BJetTags"]),
    tauIDNames = cms.untracked.vstring(["byCombinedIsolationDeltaBetaCorrRaw3Hits",
        "againstElectronLooseMVA6", "againstElectronVLooseMVA6",
        "decayModeFindingNewDMs",
        "byLooseCombinedIsolationDeltaBetaCorr3Hits", "byMediumCombinedIsolationDeltaBetaCorr3Hits", "byTightCombinedIsolationDeltaBetaCorr3Hits", "againstMuonLoose3", "againstMuonTight3", "againstElectronVTightMVA6", "againstElectronTightMVA6", "againstElectronMediumMVA6"]),

        #
        #   Some flags
        #
    useElectrons = cms.untracked.bool(True),
    useTaus = cms.untracked.bool(True)
)
