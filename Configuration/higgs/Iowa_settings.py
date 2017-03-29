
import os, sys
import ROOT as R
import Modeling.higgs2.models as models
import Modeling.higgs2.definitions as defs
import Modeling.higgs2.aux as aux
import Samples as S

########################
### General Settings ###
########################
jobLabel = "vR1_20170217_1742"

#######################
### Directory Setup ###
#######################
projectDir = "/Users/vk/software/Analysis/files/analysis_results/"
histDir = os.path.join(projectDir, "results", jobLabel)
distributionsDir = os.path.join(projectDir, "distributions", jobLabel);
aux.mkdir(distributionsDir)
backgroundfitsDir = os.path.join(projectDir, "backgroundfits", jobLabel)
aux.mkdir(backgroundfitsDir)
signalfitsDir = os.path.join(projectDir, "signalfits", jobLabel)
aux.mkdir(signalfitsDir)

#################
###  Samples  ###
#################
jsonToUse = S.jsonfiles["2016_ReReco_36460"]
dataPathToFile = histDir + "/" + "result__merged__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__Mu24.root"

# background files
dyPathToFile = histDir + "/" + "result__DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
ttPathToFile = histDir + "/" + "result__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wJetsToLNuPathToFile = histDir + "/" + "result__WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wwTo2L2NuPathToFile = histDir + "/" + "result__WWTo2L2Nu_13TeV-powheg-herwigpp__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wzTo3LNuPathToFile = histDir + "/" + "result__WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"

dyMC = S.mcMoriond2017datasets["/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
ttMC = S.mcMoriond2017datasets["/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
wJetsToLNuMC = S.mcMoriond2017datasets["/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
wwTo2L2NuMC = S.mcMoriond2017datasets["/WWTo2L2Nu_13TeV-powheg-herwigpp/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
wzTo3LNuMC = S.mcMoriond2017datasets["/WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]

# signal files
gluPathToFile = histDir + "/" + "result__GluGlu_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
vbfPathToFile = histDir + "/" + "result__VBF_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wmPathToFile = histDir + "/" + "result__WMinusH_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wpPathToFile = histDir + "/" + "result__WPlusH_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
zhPathToFile = histDir + "/" + "result__ZH_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"

gluMC = S.mcMoriond2017datasets["/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
vbfMC = S.mcMoriond2017datasets["/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
wmMC = S.mcMoriond2017datasets["/WMinusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
wpMC = S.mcMoriond2017datasets["/WPlusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
zhMC = S.mcMoriond2017datasets["/ZH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]

# sample objects
data = defs.Data("NoCats", jsonToUse, dataPathToFile, color=R.kBlack)
dy = defs.MC("NoCats", dyPathToFile, dyMC, color=R.kBlue)
tt = defs.MC("NoCats", ttPathToFile, ttMC, color=R.kGreen)
wJetsToLNu = defs.MC("NoCats", wJetsToLNuPathToFile, wJetsToLNuMC, color=R.kYellow)
wwTo2L2Nu = defs.MC("NoCats", wwTo2L2NuPathToFile, wwTo2L2NuMC, color=R.kGray)
wzTo3LNu = defs.MC("NoCats", wzTo3LNuPathToFile, wzTo3LNuMC, color=R.kViolet)
glu = defs.MC("NoCats", gluPathToFile, gluMC, color=None)
vbf = defs.MC("NoCats", vbfPathToFile, vbfMC, color=None)
wm = defs.MC("NoCats", wmPathToFile, wmMC, color=None)
wp = defs.MC("NoCats", wpPathToFile, wpMC, color=None)
zh = defs.MC("NoCats", zhPathToFile, zhMC, color=None)

########################
### Models' Settings ###
########################
# single gaus
singleGaus_initialValues = {
    "mean":125, "meanmin":115, "meanmax":135,
    "sigma":1.0, "sigmamin":0.1, "sigmamax":10
}
doubleGaus_initialValues = {
    "mean1":125, "mean1min":115, "mean1max":135,
    "sigma1":1.0, "sigma1min":0.1, "sigma1max":10,
    "mean2":125, "mean2min":115, "mean2max":135,
    "sigma2":1.0, "sigma2min":0.1, "sigma2max":10,
    "coef" : 0.8, "coefmin" : 0, "coefmax": 1
}
tripleGaus_initialValues = {
    "mean1":125, "mean1min":115, "mean1max":135,
    "sigma1":1.0, "sigma1min":0.1, "sigma1max":10,
    "mean2":125, "mean2min":115, "mean2max":135,
    "sigma2":1.0, "sigma2min":0.1, "sigma2max":10,
    "mean3":125, "mean3min":115, "mean3max":135,
    "sigma3":1.0, "sigma3min":0.1, "sigma3max":10,
    "coef1" : 0.3, "coef1min" : 0, "coef1max" : 1,
    "coef2" : 0.3, "coef2min" : 0, "coef2max" : 1,
}
# expGaus
expGaus_defaultValues = {
    "a1" : 5.0, "a1min" : -1000, "a1max" : 1000,
    "a2" : 5.0, "a2min" : -1000, "a2max" : 1000
}
# BWZ Redux
bwzredux_defaultValues = {
    "a1" : 1.39, "a1min" : 0.7, "a1max" : 2.1,
    "a2" : 0.47, "a2min" : 0.30, "a2max" : 0.62,
    "a3" : -0.26, "a3min" : -0.40, "a3max" : -0.12
}
# BWZ Gamma
bwzgamma_defaultValues = {
    "zwidth" : 2.5, "zwidthmin" : 0, "zwidthmax" : 30,
    "zmass" : 91.2, "zmassmin" : 90, "zmassmax" : 92,
    "expParam" : -0.0053, "expParammin" : -0.0073, "expParammax" : -0.0033,
    "fraction" : 0.379, "fractionmin" : 0.2, "fractionmax" : 1
}
# bernsteins
bernstein_defaultValues = aux.buildDefaultValuesBerstein(20)
# sum exponentials
sumExp_defaultValues = aux.buildDefaultValuesSumExponentials(20)

################################################
### Mass Variables/Fit Ranges/Drawing Ranges ###
################################################
diMuonMass125 = {"name":"DiMuonMass", "central":125, "min":110, "max":160,
    "fitmin" : 115, "fitmax" : 135}

############################
###   General settings   ###
############################
job_label = 'vR1_20170217_1742'
UF_era    = 'Moriond17_Feb08'
JSON      = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
analytic  = True
productionModifier = "Mu24"

#######################
###   Data to use   ###
#######################
cmssws  = ["80X"]
pileups = ["69"]
# pileups = ["68", "69", "70", "71", "72", "71p3", "69p2"]

signals = [ "GluGlu_HToMuMu_M125_13TeV_powheg_pythia8",
            "VBF_HToMuMu_M125_13TeV_powheg_pythia8",
            "WMinusH_HToMuMu_M125_13TeV_powheg_pythia8",
            "WPlusH_HToMuMu_M125_13TeV_powheg_pythia8",
            "ZH_HToMuMu_M125_13TeV_powheg_pythia8" ]

backgrounds = [ ("WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",      R.kYellow),
                ("WWTo2L2Nu_13TeV-powheg-herwigpp",                         R.kGray),
                ("WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",        R.kViolet),
                ("TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",    R.kGreen),
                ("DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8", R.kBlue) ]
                # ("TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8",        R.kGreen),
                # ("TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",          R.kGreen) ]

####################################################
###  Settings for AuxTools/python/convert_UF.py  ###
####################################################
orig_file    = '/afs/cern.ch/work/a/acarnes/public/h2mumu/rootfiles/validate_UNBLINDED_dimu_mass_PF_110_160_run1categories_36814.root'
orig_sig_dir = 'signal_histos'

############################################################################
###   Settings for Modeling/higgs/generate_signalFitsPlusWorkspaces.py   ###
############################################################################
in_hist_dir    = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/%s" % job_label
workspaces_dir = "/Users/vk/software/Analysis/files/higgs_analysis_files/datacards_and_workspaces"
sig_fits_dir   = "/Users/vk/software/Analysis/files/higgs_analysis_files/fits/signal_precombine"
path_modifier  = "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkg"

workspaces_dir = os.path.join( workspaces_dir, os.path.split(in_hist_dir)[1] + "__" + path_modifier )
sig_fits_dir   = os.path.join( sig_fits_dir, os.path.split(in_hist_dir)[1] + "__" + path_modifier )

scale_MC     = True
sig_models   = ["DoubleGaus"]
bkg_models   = [
#    {"name" : "BWZRedux", "aux" : {}},
#    {"name" : "BWZGamma", "aux" : {}},
#    {"name" : "SumExponentials", "aux" : {"degree" : 1}},
#    {"name" : "SumExponentials", "aux" : {"degree" : 2}},
#    {"name" : "SumExponentials", "aux" : {"degree" : 3}},
#    {"name" : "SumExponentials", "aux" : {"degree" : 4}},
#    {"name" : "SumPowers", "aux" : {"degree" : 2}},
#    {"name" : "SumPowers", "aux" : {"degree" : 3}},
#    {"name" : "SumPowers", "aux" : {"degree" : 4}},
#    {"name" : "SumPowers", "aux" : {"degree" : 5}},
#    {"name" : "SumPowers", "aux" : {"degree" : 6}},
#    {"name" : "LaurentSeries", "aux" : {"degree" : 2}},
#    {"name" : "LaurentSeries", "aux" : {"degree" : 3}},
#    {"name" : "LaurentSeries", "aux" : {"degree" : 4}},
#    {"name" : "LaurentSeries", "aux" : {"degree" : 5}},
#    {"name" : "LaurentSeries", "aux" : {"degree" : 6}},
#    {"name" : "LaurentSeries", "aux" : {"degree" : 7}},

#    {"name" : "Polynomial", "aux" : {"degree" : 3}},
#    {"name" : "Polynomial", "aux" : {"degree" : 4}},
#    {"name" : "Polynomial", "aux" : {"degree" : 5}},
#    {"name" : "Polynomial", "aux" : {"degree" : 6}},
#    {"name" : "Polynomial", "aux" : {"degree" : 7}},
#    {"name" : "Polynomial", "aux" : {"degree" : 8}},
#    {"name" : "Polynomial", "aux" : {"degree" : 9}},
#    {"name" : "ExpGaus", "aux" : {}},
#    {"name" : "Bernstein", "aux" : {"degree" : 2}},
#    {"name" : "Bernstein", "aux" : {"degree" : 3}},
#    {"name" : "Bernstein", "aux" : {"degree" : 4}},
    {"name" : "Bernstein", "aux" : {"degree" : 5}},
#    {"name" : "Bernstein", "aux" : {"degree" : 6}},
#    {"name" : "Bernstein", "aux" : {"degree" : 7}},
#    {"name" : "Bernstein", "aux" : {"degree" : 8}},
]
sig_modes    = ["Separate"]
sig_M =[125, 110, 160, 115, 135]  ## Central value, plot range, fit range

#####################################################################
###   Settings for Modeling/higgs/generate_bkgDataWorkspaces.py   ###
#####################################################################
bkg_fits_dir = "/Users/vk/software/Analysis/files/higgs_analysis_files/fits/bkg_precombine"
bkg_fits_dir   = os.path.join( bkg_fits_dir, os.path.split(in_hist_dir)[1] + "__" + path_modifier )
bkg_M =[ 91, 110, 160, 110, 160]  ## Central value, plot range, fit range

#############################################################
###   Settings for Modeling/higgs/generate_datacards.py   ###
#############################################################
datacards_dir = "/Users/vk/software/Analysis/files/higgs_analysis_files/datacards_and_workspaces"

datacards_dir = os.path.join( datacards_dir, os.path.split(in_hist_dir)[1] + "__" + path_modifier)

##########################################################
###   Settings for Modeling/higgs/generate_limits.py   ###
##########################################################
combine_dir  = "/Users/vk/software/Analysis/files/higgs_analysis_files/combine_results/"
combine_dir += "%s__%s/%s__%s__Mu24" % (job_label, path_modifier, cmssws[0], JSON.replace('.txt',''))
limits_dir   = "/Users/vk/software/Analysis/files/higgs_analysis_files/limits/"
limits_dir  += "%s__%s/%s__%s__Mu24" % (job_label, path_modifier, cmssws[0], JSON.replace('.txt',''))


