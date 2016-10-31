#-----------------------------------------------------------
#	Ntuple Maker Configuration for whatever object you want to store
#	Author: VK
#-----------------------------------------------------------

#-----------------------------------------------------------
#	main imports and CMS Process Def
#-----------------------------------------------------------
import FWCore.ParameterSet.Config as cms
process = cms.Process("NtupleMaker")

#-----------------------------------------------------------
#	Load whatever you need from CMSSW and then modify if neccessary
#-----------------------------------------------------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('CondCore.CondDB.CondDB_cfi')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('EventFilter.HcalRawToDigi.HcalRawToDigi_cfi')

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.GlobalTag.connect = "frontier://(serverurl=http://frontier1.cms:8000/FrontierOnProd)(serverurl=http://frontier2.cms:8000/FrontierOnProd)(retrieve-ziplevel=0)/CMS_CONDITIONS"
process.GlobalTag.globaltag = "80X_dataRun2_Prompt_v9"
process.hcalDigis.InputLabel = cms.InputTag("source")

#-----------------------------------------------------------
#	Pool Source
#-----------------------------------------------------------
process.maxEvents = cms.untracked.PSet(
	input = cms.untracked.int32(-1)
)
process.source = cms.Source("HcalTBSource",
    fileNames = cms.untracked.vstring(
        "file:/hcaldepot1/data/USC_284256.root"
    )
)

#-----------------------------------------------------------
#	TFile Service definition
#-----------------------------------------------------------
process.TFileService = cms.Service(
	"TFileService",
	fileName=cms.string("ntuples_local.root")
)

#-----------------------------------------------------------
#	Define the EDAnalyzer for Stage1
#-----------------------------------------------------------
process.maker = cms.EDAnalyzer(
	'QIE10Maker',
	verbosity = cms.untracked.int32(0),
)

#-----------------------------------------------------------
#	Final Path Execution Sequence
#-----------------------------------------------------------
process.p = cms.Path(
	process.hcalDigis
	*process.maker
)

process.options = cms.untracked.PSet(
	Rethrow = cms.untracked.vstring(
		'ProductNotFound',
		'TooManyProducts',
		'TooFewProducts'
	)
)










