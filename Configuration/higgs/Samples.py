#!/usr/bin/python

import shelve, pickle
import Dataset as DS
import os,sys,subprocess
if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.environ["ANALYSISHOME"])

#
#   Specify the full list of CMSSW Datasets
#
datadatasets = {
    "/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "74X_dataRun2_v4"
    ),
    "/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "74X_dataRun2_reMiniAOD_v0"
    ),
    "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015D-PromptReco-v4/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "74X_dataRun2_Prompt_v4"
    ),
    "/SingleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "76X_dataRun2_v15"
    ),
    "/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "76X_dataRun2_v15"
    ),

    #
    #   2016 Prompt
    #
#    "/SingleMuon/Run2016B-PromptReco-v1/MINIAOD" : DS.Dataset(
#        name="/SingleMuon/Run2016B-PromptReco-v1/MINIAOD",
#        isData=True,
#        year=2016,
#        globaltag = "80X_dataRun2_Prompt_v9"
#    ),
    "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016C-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016C-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016D-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016D-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016E-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016E-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016F-PromptReco-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016F-PromptReco-v1/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016G-PromptReco-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016G-PromptReco-v1/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016H-PromptReco-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016H-PromptReco-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016H-PromptReco-v2/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016H-PromptReco-v2/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016H-PromptReco-v3/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016H-PromptReco-v3/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),

    #
    #   2016 Re Reco
    #
    "/SingleMuon/Run2016B-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016B-23Sep2016-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v3"
    ),
    "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v3"
    ),
    "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v3"
    ),
    "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v3"
    )
}

rerecoSep232016_datasets = {
    # Run2016B-v1 doesnt' have runs in the Golden Json
#    "/SingleMuon/Run2016B-23Sep2016-v1/MINIAOD" : DS.Dataset(
#        name = "/SingleMuon/Run2016B-23Sep2016-v1/MINIAOD",
#        isData = True,
#        year = 2016,
#        globaltag = "80X_dataRun2_2016SeptRepro_v5"
#    ),
    "/SingleMuon/Run2016B-23Sep2016-v3/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016B-23Sep2016-v3/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v5"
    ),
    "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v5"
    ),
    "/SingleMuon/Run2016D-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016D-23Sep2016-v1/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v5"
    ),
    "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v5"
    ),
    "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v5"
    ),
    "/SingleMuon/Run2016G-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016G-23Sep2016-v1/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v5"
    ),
    # Run2016H was collected with the same conditions as the 23Sep rereco
    "/SingleMuon/Run2016H-PromptReco-v2/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016H-PromptReco-v2/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v5"
    ),
    "/SingleMuon/Run2016H-PromptReco-v3/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016H-PromptReco-v3/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v5"
    ),
}

mcMoriond2017datasets_1 = {
    #
    # Signals
    #
    "GluGlu_125" : DS.MCDataset(
        name = "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 48.58 * 0.0002176
        cross_section = 0.009618
    ),
    "GluGlu_120" : DS.MCDataset(
        name = "/GluGlu_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016, isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 0.009618
    ),
    "GluGlu_130" : DS.MCDataset(
        name = "/GluGlu_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016, isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 0.009618
    ),
    "VBF_125" : DS.MCDataset(
        name = "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 3.782 * 0.0002176
        cross_section = 0.0008208
    ),
    "VBF_120" : DS.MCDataset(
        name = "/VBF_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 3.782 * 0.0002176
        cross_section = 0.0008208
    ),
    "VBF_130" : DS.MCDataset(
        name = "/VBF_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 3.782 * 0.0002176
        cross_section = 0.0008208
    ),
    "WM_125" : DS.MCDataset( 
        name = "/WMinusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.5331 * 0.0002176
        cross_section = 0.5331 * 0.0002176
    ),
    "WM_120" : DS.MCDataset(
        name = "/WMinusH_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.5331 * 0.0002176
        cross_section = 0.5331 * 0.0002176
    ),
    "WM_130" : DS.MCDataset(
        name = "/WMinusH_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.5331 * 0.0002176
        cross_section = 0.5331 * 0.0002176
    ),
    "WP_125" : DS.MCDataset(
        name = "/WPlusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.851 * 0.0002176
        cross_section = 0.851 * 0.0002176
    ),
    "WP_120" : DS.MCDataset(
        name = "/WPlusH_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.851 * 0.0002176
        cross_section = 0.851 * 0.0002176
    ),
    "WP_130" : DS.MCDataset(
        name = "/WPlusH_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.851 * 0.0002176
        cross_section = 0.851 * 0.0002176
    ),
    "Z_125" : DS.MCDataset(
        name = "/ZH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.8839 * 0.0002176
        cross_section = 0.0002136
    ),
    "Z_120" : DS.MCDataset(
        name = "/ZH_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.8839 * 0.0002176
        cross_section = 0.0002136
    ),
    "Z_130" : DS.MCDataset(
        name = "/ZH_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.8839 * 0.0002176
        cross_section = 0.0002136
    ),
}

mcMoriond2017datasets = {
    #
    # DY HT Samples
    #
    "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 5765.
    ),

    #
    # Signals
    #
    "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 48.58 * 0.0002176
        cross_section = 0.009618
    ),
    "/GluGlu_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/GluGlu_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016, isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 0.009618
    ),
    "/GluGlu_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/GluGlu_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016, isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 0.009618
    ),
    "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 3.782 * 0.0002176
        cross_section = 0.0008208
    ),
    "/VBF_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/VBF_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 3.782 * 0.0002176
        cross_section = 0.0008208
    ),
    "/VBF_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/VBF_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 3.782 * 0.0002176
        cross_section = 0.0008208
    ),
    "/WMinusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WMinusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.5331 * 0.0002176
        cross_section = 0.5331 * 0.0002176
    ),
    "/WMinusH_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WMinusH_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.5331 * 0.0002176
        cross_section = 0.5331 * 0.0002176
    ),
    "/WMinusH_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WMinusH_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.5331 * 0.0002176
        cross_section = 0.5331 * 0.0002176
    ),
    "/WPlusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WPlusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.851 * 0.0002176
        cross_section = 0.851 * 0.0002176
    ),
    "/WPlusH_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WPlusH_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.851 * 0.0002176
        cross_section = 0.851 * 0.0002176
    ),
    "/WPlusH_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WPlusH_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.851 * 0.0002176
        cross_section = 0.851 * 0.0002176
    ),
    "/ZH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/ZH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.8839 * 0.0002176
        cross_section = 0.0002136
    ),
    "/ZH_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/ZH_HToMuMu_M120_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.8839 * 0.0002176
        cross_section = 0.0002136
    ),
    "/ZH_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/ZH_HToMuMu_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 0.8839 * 0.0002176
        cross_section = 0.0002136
    ),

    #
    # Backgrounds
    #
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 6025.2
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-herwigpp_30M/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-herwigpp_30M/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 6025.2
        cross_section = 5765.
    ),
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 6025.2
        cross_section = 5765.
    ),
    # this TTJets should be changed to the Moriond2017 one!
#    "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
#        name = "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
#        year = 2016, 
#        isData = False,
#        isSignal = False,
#        initial_cmssw = "80X",
#        globaltag = "80X_mcRun2_asymptotic_v14",
#        cross_section = 831.76
#    ),
    "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
#        cross_section = 831.76 * 1.0
        cross_section = 85.656
    ),

    # don't know much about these
    "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 61526.7 * 1.0
    ),
    "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 61526.7
    ),
    "/WWTo2L2Nu_13TeV-powheg-herwigpp/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WWTo2L2Nu_13TeV-powheg-herwigpp/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 10.481
    ),
    "/WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 4.712
    ),
    "/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 0.564
    ),
    "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 3.22
    ),
    "/ZZTo4L_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" : DS.MCDataset(
        name = "/ZZTo4L_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 1.212
    ),
    "/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 0.2086
    ),
    "/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 0.1651
    ),
    "/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 0.05565
    ),
    "/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 0.01398
    ),

    "/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" : DS.MCDataset(
        name = "/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM",
        isData = False,
        year = 2016,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_2016_TrancheIV_v6",
        cross_section = 831.76
    )
}

mcdatasets = {
        #
        #   Signal Datasets
        #
    "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" : DS.MCDataset(
        name="/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        isData=False,
        year=2015,
        isSignal=True,
        initial_cmssw = "74X",
        globaltag = "74X_mcRun2_asymptotic_v2",
        cross_section =  43.62*0.00022
    ),
    "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "76X",
        globaltag = "76X_mcRun2_asymptotic_v12",
        cross_section =  43.62*0.00022
    ),

    "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year=2016,
        isData=False,
        isSignal=True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 43.62*0.00022
    ),

    "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" : DS.MCDataset(
        name="/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "74X",
        globaltag = "74X_mcRun2_asymptotic_v2",
        cross_section = 3.727*0.00022
    ),
    "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "76X",
        globaltag = "76X_mcRun2_asymptotic_v12",
        cross_section = 3.727*0.00022
    ),

    "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM" : DS.MCDataset(
        name = "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM",
        year = 2016,
        isData=False,
        isSignal=True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 3.727*0.00022
    ),

    "/WMinusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WMinusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year=2016,
        isData=False,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 1.373*0.00022
    ),

    "/WPlusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WPlusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year = 2016,
        isData=False,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 1.373*0.00022
    ),

    "/ZH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/ZH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal  = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 8.839*0.00022
    ),

    #
    #   Background Datasets
    #
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" : DS.MCDataset(
        name="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        year=2015,isData=False,
        isSignal=False,
        initial_cmssw = "74X",
        globaltag = "74X_mcRun2_asymptotic_v2",
        cross_section = 6025.2
    ),
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=False,
        initial_cmssw = "76X",
        globaltag = "76X_mcRun2_asymptotic_v12",
        cross_section = 6025.2
    ),

    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 6025.2
    ),

    "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM" : DS.MCDataset(
        name="/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=False,
        initial_cmssw="74X",
        globaltag = "74X_mcRun2_asymptotic_v2",
        cross_section = 831.76
    ),
    "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=False,
        initial_cmssw="76X",
        globaltag = "76X_mcRun2_asymptotic_v12",
        cross_section = 831.76
    ),

    "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year = 2016, 
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 831.76
    )
}

#
#   jsons
#
jsonfiles = {
    #   ReReco of 2015
    "2015_ReReco" : DS.JsonFile(
        filename="Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt",
        intlumi = 2318.
    ),

    #   Prompt of 2015
    "2015_Prompt" : DS.JsonFile(
        filename="Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt",
        intlumi = 2169.
    ),

    #   Prompt of 2016 up to the point where MC/Data Mismatch was not present
    "2016_Prompt_7648" : DS.JsonFile(
        filename="Cert_271036-276097_13TeV_PromptReco_Collisions16_JSON_NoL1T_v2.txt",
        intlumi = 7648.
    ),

    #   Prompt of 2016 - MC/Data Mismatch is present - Trigger inefficiency!???
    "2016_Prompt_12900" : DS.JsonFile(
        filename="Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt",
        intlumi = 12900.
    ),

    #   latest
    "2016_Prompt_16900" : DS.JsonFile(
        filename="Cert_271036-277148_13TeV_PromptReco_Collisions16_JSON.txt",
        intlumi = 16900.
    ),
    "2016_Prompt_20100" : DS.JsonFile(
        filename = "Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt",
        intlumi = 20100.
    ),
    "2016_Prompt_26400" : DS.JsonFile(
        filename = "Cert_271036-280385_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt",
        intlumi = 26400.
    ),
    "2016_Prompt_29530" : DS.JsonFile(
        filename = "Cert_271036-282037_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt",
        intlumi = 29530.
    ),
    "2016_Prompt_36150" : DS.JsonFile(
        filename = "Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt",
        intlumi = 36150.
    ),
    "2016_ReReco_36460" : DS.JsonFile(
        filename = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt",
        intlumi = 36460.
    ),
    ## UF NTuple tag name, for easier human-readable tracking - AWB 23.02.17
    "Moriond17_Feb08" : DS.JsonFile(
        filename = "Moriond17_Feb08.txt", ## This is just a dummy file, not a real JSON
        intlumi = 36460.
        )
}

#
#   list all the pileup files
#
pileups = {}
for k in jsonfiles.keys():
    jfilename = jsonfiles[k].filename
    for cs in ["68", "69", "69p2", "70", "71", "72", "71p3"]:
        s = "pileup__%s__%s" % (jfilename[:-4], cs)
        pileups[s] = DS.PileUp(
            cross_section=cs, datajson=jfilename
        )

#
#   Useful functions to build up the name
#
def buildDatasetTagName(ntuple):
    if ntuple.isData:
	    s = "%s__%s" % (ntuple.label.split("__")[1],ntuple.json[:-4])
    else:
        s = "%s" % (ntuple.cmssw)
    if ntuple.aux!=None and ntuple.aux!="":
        s+="__%s" % ntuple.aux
    print "22222222222222"
    return s

def buildRequestName(ntuple, *kargs):
    if ntuple.isData:
        s = ntuple.label.split("__")[1]
        s += "__%s"%kargs[0]
    else:
        if ntuple.isSignal:
            s = ntuple.label.split("__")[0] + "__%s" % ntuple.initial_cmssw
        else:
#            s = ntuple.label.split("__")[0].split("-")[0]+"__%s" % ntuple.initial_cmssw
            s = ntuple.label.split("__")[0]+"__%s" % ntuple.initial_cmssw
    if ntuple.aux!=None and ntuple.aux!="":
        s+="__%s" % ntuple.aux
    return s

def isReReco(dataset):
	if dataset.year==2015:
		if "16Dec2015" in dataset.name:
			return True
		else:
			return False
	else:
		return False

def buildPUfilename(ntuple):
    if ntuple.isData:
        sdata = "pileup__%s__%smb.root" % (ntuple.pileupdata.datajson[:-4],
            ntuple.pileupdata.cross_section)
        return sdata
    else:
        smc = "pileup__%s__%s.root" % (ntuple.label.split("__")[0],
            ntuple.cmssw)
        return smc

def buildPUfilenames(result):
    sdata = "pileup__%s__%smb.root" % (result.pileupdata.datajson[:-4],
        result.pileupdata.cross_section)
    smc = "pileup__%s__%s.root" % (result.label.split("__")[0],
        result.cmssw)
    return (smc, sdata)

def eos_system(cmd, args):
    import subprocess
    if cmd=="eos":
        cmd = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select"
    proc = subprocess.Popen([cmd, args], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out

def buildTimeStamp(ntuple):
    fullpattern = os.path.join(ntuple.rootpath,
        ntuple.label.split("__")[0],
        buildDatasetTagName(ntuple), "*")
    print fullpattern
    cmd = "ls" if ntuple.storage=="local" else "eos"
    print cmd
    if ntuple.storage=="local":
        args = fullpattern
    else:
        args = "ls %s" % os.path.join("/eos/cms", fullpattern)
    print "%s %s" % (cmd, args)
    print "4444444"
    x = eos_system(cmd, args).split("\n")[0]
    print x
    return x

def discoverFileList(ntuple):
    print "-1-1-1-1-1-1-1-"
    fullpath= os.path.join(ntuple.rootpath,
        ntuple.label.split("__")[0],
        buildDatasetTagName(ntuple), buildTimeStamp(ntuple), "0000")
    print "1111111111"
    print fullpath
    fullpattern = os.path.join(fullpath, "*.root")
    cmd = "ls" if ntuple.storage=="local" else "eos"
    args = "-d %s" % fullpattern if ntuple.storage=="local" else "ls %s" % (
        os.path.join("/eos/cms", fullpattern))
    print (cmd,args)
    x = eos_system(cmd, args).split("\n")[:-1]
    if ntuple.storage=="EOS":
        xxx = []
        for f in x:
            fullpathname = os.path.join("root://eoscms.cern.ch//", "eos/cms")
            fullpathname = fullpathname+os.path.join(fullpath, f)
            xxx.append(fullpathname)
        return xxx
    return x

def buildFileListName(ntuple):
    if ntuple.isData:
        s = "filelist__%s__%s" % (ntuple.label.split("__")[1],
                ntuple.json[:-4])
    else:
        s = "filelist__%s__%s" % (ntuple.label.split("__")[0],
            ntuple.cmssw)
    if ntuple.aux!=None and ntuple.aux!="":
        s += "__%s" % ntuple.aux
    s+=".files"
    return s

def buildResultOutputPathName(result):
    s = "result"
    if result.isData:
        s+="__%s__%s" % (result.label.split("__")[1],
            result.json[:-4])
    else:
        s += "__%s__%s__%s__%smb" % (result.label.split("__")[0],
            result.cmssw, result.pileupdata.datajson[:-4], 
            result.pileupdata.cross_section)
    if result.aux!=None and result.aux!="":
        s += "__%s" % result.aux
    s += ".root"
    return s

def discoverNtuples(ntuple):
    prefix = ""
    if ntuple.storage=="EOS":
        prefix+="/eos/cms"
        tstamp = getTimeStamp(ntuple)
        ntuple.timestamp = tstamp
        pathstring = os.path.join(prefix, ntuple.rootpath, ntuple.name.split("/")[0],
            buildDatasetTagName(ntuple), tstamp, "0000")
        x = eos_system("eos", "ls %s/*.root" % pathstring).split("\n")
        return pathstring,x
    else:
        pathstring = os.path.join(prefix, ntuple.rootpath, ntuple.name.split("/")[0],
            buildDatasetTagName(ntuple))
        x = eos_system("eos", "ls %s/*.root" % pathstring).split("\n")
        return pathstring,x

def getFileList(ntuple):
    pass

if __name__=="__main__":
    pass
