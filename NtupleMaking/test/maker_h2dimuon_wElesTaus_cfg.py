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
data_datasets = Samples.mcdatasets
jsonfiles = Samples.jsonfiles
jsontag = "2016_Prompt_29530"
jsonfile = jsonfiles[jsontag]
dataset = None
for key in data_datasets.keys():
    if "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM"==data_datasets[key].name:
        dataset = data_datasets[key]
        break
#    if "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD"==data_datasets[key].name:
#        dataset=data_datasets[key]
#        break

if dataset==None:
    print "-"*40
    print "dataset is None"
    print "-"*40
    sys.exit(1)

ntuple = DS.Ntuple(dataset, 
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
readFiles.extend(open(("sample_file_lists/%s/" % ("data" if ntuple.isData else "mc"))+ntuple.test_file).read().splitlines());

#
#   Differentiate between DATA and MC
#
if not thisIsData:
    process.load("Analysis.NtupleMaking.H2DiMuonMaker_MC")
else:
    process.load("Analysis.NtupleMaking.H2DiMuonMaker_Data")

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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000000) )
process.source = cms.Source("PoolSource",fileNames = readFiles)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange()
if thisIsData:
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = 
		ntuple.json).getVLuminosityBlockRange()

#
#   Electron ID Setup - cut based
#
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
dataFormat = DataFormat.MiniAOD
switchOnVIDElectronIdProducer(process, dataFormat)
my_id_modules = [
#    'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronHLTPreselecition_Summer16_V1_cff',
    'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff'
]
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

process.TFileService = cms.Service("TFileService", fileName = cms.string("ntuples"+ntuple.label+".root") )
process.p = cms.Path(process.egmGsfElectronIDSequence * process.ntuplemaker_H2DiMuonMaker)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string("test.root")
)
#process.finalize = cms.EndPath(process.out)
