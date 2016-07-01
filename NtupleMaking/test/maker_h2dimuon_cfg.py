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

from Samples_v3 import singleMuon_RunC25nsOct_MINIAOD as s
#from Samples_v3 import gg_HToMuMu as s

#
#   a few settings
#
thisIsData = s.isData
globalTag = s.globaltag
readFiles = cms.untracked.vstring();
readFiles.extend(s.files);
jsontouse = 1

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

print "Sample Name:    " +  s.name
print "Sample DAS DIR: " +  s.dir
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
		s.jsonfiles[jsontouse]).getVLuminosityBlockRange()

#
#   TFile Service to handle output
#
process.TFileService = cms.Service("TFileService", fileName = cms.string("ntuplemaking_"+s.name+".root") )

#
#   Execution Path
#
process.p = cms.Path(process.ntuplemaker_H2DiMuonMaker)
