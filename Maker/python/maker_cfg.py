#-----------------------------------------------------------
#	Ntuple Maker Configuration for whatever object you want to store
#	Author: VK
#-----------------------------------------------------------

#-----------------------------------------------------------
#	main imports and CMS Process Def
#-----------------------------------------------------------
import FWCore.ParameterSet.Config as cms
process = cms.Process("Maker")

#-----------------------------------------------------------
#	Input Options
#-----------------------------------------------------------
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing()

options.register(
	"inputFiles",
	"root://eoscms.cern.ch//eos/cms/store/group/dpg_hcal/comm_hcal/LS1/USC_248441.root",
	VarParsing.VarParsing.multiplicity.list,
	VarParsing.VarParsing.varType.string,
	"Input Files"
)

options.register(
	"outFileName",
	"test.root",
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.string
)

options.register(
	'processEvents',
	-1,
	VarParsing.VarParsing.multiplicity.singleton,
	VarParsing.VarParsing.varType.int,
	"Number of Events to process"
)

options.parseArguments()

#-----------------------------------------------------------
#	Load whatever you need from CMSSW and then modify if neccessary
#-----------------------------------------------------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('CondCore.DBCommon.CondDBCommon_cfi')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('EventFilter.HcalRawToDigi.HcalRawToDigi_cfi')

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.GlobalTag.globaltag = "GR_P_V56"
process.hcalDigis.InputLabel = cms.InputTag("source")

#-----------------------------------------------------------
#	Pool Source
#-----------------------------------------------------------
process.maxEvents = cms.untracked.PSet(
	input = cms.untracked.int32(options.processEvents)
)
process.source = cms.Source("HcalTBSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
)

#-----------------------------------------------------------
#	TFile Service definition
#-----------------------------------------------------------
path = ""
process.TFileService = cms.Service(
	"TFileService",
	fileName=cms.string(path + options.outFileName)
)

#-----------------------------------------------------------
#	Define the EDAnalyzer for Stage1
#-----------------------------------------------------------
process.maker = cms.EDAnalyzer(
	'Maker',
	verbosity = cms.untracked.int32(0),
)

#-----------------------------------------------------------
#	for PF HF Clusters/Candidates
#-----------------------------------------------------------
#process.pfHF = cms.Sequence(process.particleFlowRecHitHF*process.particleFlowClusterHF)

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










