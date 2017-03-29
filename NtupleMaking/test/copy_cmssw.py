import FWCore.ParameterSet.Config as cms

# Give the process a name
process = cms.Process("PickEvent")

# Tell the process which files to use as the sourdce
process.source = cms.Source ("PoolSource",
          fileNames = cms.untracked.vstring(
            "root://cms-xrd-global.cern.ch//store/data/Run2016H/SinglePhoton/RECO/PromptReco-v2/000/283/877/00000/106D46AC-6F9C-E611-A8BA-02163E011BB4.root")
)


# tell the process to only run over 100 events (-1 would mean run over
#  everything
process.maxEvents = cms.untracked.PSet(
            input = cms.untracked.int32 (1000)

)

# Tell the process what filename to use to save the output
process.Out = cms.OutputModule("PoolOutputModule",
         fileName = cms.untracked.string ("ecal_test_file.root")
)

# make sure everything is hooked up
process.end = cms.EndPath(process.Out)
