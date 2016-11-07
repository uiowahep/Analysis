#-----------------------------------------------------------
#	Ntuple Maker Configuration for whatever object you want to store
#	Author: VK
#-----------------------------------------------------------

#-----------------------------------------------------------
#	main imports and CMS Process Def
#-----------------------------------------------------------
import FWCore.ParameterSet.Config as cms
process = cms.Process("NtupleMaker")

#
#   import samples
#
import os,sys,shelve, pickle
if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.environ["ANALYSISHOME"])
sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "NtupleProcessing/python"))
import NtupleProcessing.python.Samples as Samples
import NtupleProcessing.python.Dataset as DS

data_datasets = Samples.jethtdatasets
jsonfiles = Samples.jsonfiles
jsontag = "2016_Prompt_20100"
jsonfile = jsonfiles[jsontag]
dataset = ""
for key in data_datasets.keys():
    if data_datasets[key].name == "/JetHT/Run2016F-v1/RAW":
        dataset=data_datasets[key]
        break

tuple = DS.Ntuple(dataset,
    json="json/"+jsonfile.filename,
    cmssw="80X",
    storage=None,
    rootpath=None,
    timestamp=None
)

#-----------------------------------------------------------
#	Load whatever you need from CMSSW and then modify if neccessary
#-----------------------------------------------------------
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('CondCore.CondDB.CondDB_cfi')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('EventFilter.HcalRawToDigi.HcalRawToDigi_cfi')

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.GlobalTag.globaltag = ntuple.globaltag
process.hcalDigis.InputLabel = cms.InputTag("rawDataCollector")

#-----------------------------------------------------------
#	Pool Source
#-----------------------------------------------------------
process.maxEvents = cms.untracked.PSet(
	input = cms.untracked.int32(1000000)
)
readFiles = cms.untracked.vstring()
readFiles.extend(open("sample_file_lists/data/"+ntuple.test_file).read().splitlines())
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(readFiles)
)

#-----------------------------------------------------------
#	TFile Service definition
#-----------------------------------------------------------
process.TFileService = cms.Service(
	"TFileService",
	fileName=cms.string("qie10ntuples.root")
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

process.out = cms.OutputModule(
    "PoolOutputModule",
    filename = cms.untracked.string("test_cmssw.root")
)

process.options = cms.untracked.PSet(
	Rethrow = cms.untracked.vstring(
		'ProductNotFound',
		'TooManyProducts',
		'TooFewProducts'
	)
)










