#
#   Ntuple Making Stage
#

import FWCore.ParameterSet.Config as cms
process = cms.Process("NtupleMaking")

#
#   loading sequences
#
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load('Configuration.EventContent.EventContent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

import os,sys,shelve, pickle
if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.environ["ANALYSISHOME"])
sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "NtupleProcessing/python"))
import NtupleProcessing.python.Samples as Samples
import NtupleProcessing.python.Dataset as DS

#   example of how to get the dataset
filename = Samples.filename
ds = pickle.load(open(filename, "r"))
data_datasets = ds["DataDatasets"]
jsonfiles = ds["jsonfiles"]
jsontag = "2016_Prompt_16900"
jsonfile = jsonfiles[jsontag]
dataset = ""
for key in data_datasets.keys():
    if data_datasets[key].label=="SingleMuon.Run2016B-PromptReco-v2.MINIAOD":
        dataset=data_datasets[key]
        break

ntunple = DS.Ntuple(dataset, 
    globaltag="80X_dataRun2_Prompt_v9",
    json="json/"+jsonfile.filename,
    cmssw="80X",
    storage=None,
    rootpath=None,
    timestamp=None
)

#
#   a few settings
#
thisIsData = ntuple.isData
globalTag = ntuple.globaltag
readFiles = cms.untracked.vstring();
readFiles.extend(open(ntuple.test_file).read().splitlines());

#
#   Differentiate between DATA and MC
#
if not thisIsData:
    process.load("Analysis.NtupleMaking.H2DiMuonMaker_MC")
else:
    process.load("Analysis.NtupleMaking.H2DiMuonMaker_Data")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")

#
#   Debug/Loggin
#
print ""; print ""
print 'Loading Global Tag: ' + globalTag
process.GlobalTag.globaltag = globalTag
print ""; print ""
if thisIsData:
    print 'Running over data sample'
else:
    print 'Running over MC sample'

print "Sample Name:    " +  ntuple.name
print ""; print ""

#
#   Pool Source with proper LSs
#
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000000) )
process.source = cms.Source("PoolSource",fileNames = readFiles)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange()
if thisIsData:
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = 
		ntuple.json).getVLuminosityBlockRange()

#
#   TFile Service to handle output
#
process.TFileService = cms.Service("TFileService", fileName = cms.string("ntuples"+s.label+".root") )

#
#   Execution Path
#
process.p = cms.Path(process.ntuplemaker_H2DiMuonMaker)
