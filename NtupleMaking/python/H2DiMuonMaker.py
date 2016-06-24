import FWCore.ParameterSet.Config as cms

ntuplemaker_H2DiMuonMaker = cms.EDAnalyzer('H2DiMuonMaker',
    #   Tags
    tagMuons = cms.untracked.InputTag("slimmedMuons"),
    tagPV = cms.untracked.InputTag("offlineSlimmedPrimaryVertices"),
    tagBS = cms.untracked.InputTag("offlineBeamSpot"),
    tagPrunedGenParticles = cms.untracked.InputTag("prunedGenParticles"),
    tagPackedGenParticles = cms.untracked.InputTag("packedGenParticles"),
    tagTriggerResults = cms.untracked.InputTag("TriggerResults", "HLT"),
    tagTriggerObjects = cms.untracked.InputTag("selectedPatTrigger"),
    tagMET = cms.untracked.InputTag("slimmedMETs"),
    tagPFJets = cms.untracked.InputTag("slimmedJets"),
    tagGenJets = cms.untracked.InputTag("slimmedGenJets"),

    #   Trigger Names to select
    triggerNames = cms.untracked.vstring(
        "HLT_IsoMu20", "HLT_IsoTkMu20", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"
    ),
)
