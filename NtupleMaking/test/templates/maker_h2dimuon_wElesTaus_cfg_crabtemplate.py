"""
CMSSW Cfg Template to be submitted with crab
"""
import FWCore.ParameterSet.Config as cms
process = cms.Process("NtupleMaking")

process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load('Configuration.EventContent.EventContent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

thisIsData = s.isData
globalTag = s.globaltag

if not thisIsData:
    process.load("Analysis.NtupleMaking.H2DiMuonMaker_MC")
    process.ntuplemaker_H2DiMuonMaker.tagTriggerResults = cms.untracked.InputTag("TriggerResults", "", "HLTTYPE")
else:
    process.load("Analysis.NtupleMaking.H2DiMuonMaker_Data")

#
#
#
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
dataFormat = DataFormat.MiniAOD
switchOnVIDElectronIdProducer(process, dataFormat)
my_id_modules = [
    "RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff",
    #"RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff",
    #"RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff"
]
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

#
#
#
process.GlobalTag.globaltag = globalTag
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source("PoolSource",fileNames = cms.untracked.vstring())
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.TFileService = cms.Service("TFileService", fileName = cms.string("ntuple.root") )
process.p = cms.Path(process.egmGsfElectronIDSequence * process.ntuplemaker_H2DiMuonMaker)
