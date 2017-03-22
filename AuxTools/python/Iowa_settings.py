
import os
import ROOT as R

############################
###   General settings   ###
############################
job_label = 'vR1_20170217_1742'
# UF_era    = 'Moriond17_Feb08'
JSON      = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
analytic  = True

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
in_hist_dir    = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/vR1_20170217_1742"
workspaces_dir = "/Users/vk/software/Analysis/files/higgs_analysis_files/datacards_and_workspaces"
sig_fits_dir   = "/Users/vk/software/Analysis/files/higgs_analysis_files/fits/signal_precombine"
path_modifier  = "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkg"

workspaces_dir = os.path.join( workspaces_dir, os.path.split(in_hist_dir)[1] + "__" + path_modifier )
sig_fits_dir   = os.path.join( sig_fits_dir, os.path.split(in_hist_dir)[1] + "__" + path_modifier )

scale_MC     = True
sig_models   = ["SingleGaus", "DoubleGaus", "TripleGaus"]
bkg_models   = [
    {"name" : "BWZRedux", "aux" : {}},
    {"name" : "BWZGamma", "aux" : {}},
    {"name" : "SumExponentials", "aux" : {"degree" : 1}},
    {"name" : "SumExponentials", "aux" : {"degree" : 2}},
    {"name" : "SumExponentials", "aux" : {"degree" : 3}},
    {"name" : "SumExponentials", "aux" : {"degree" : 4}},
    {"name" : "SumPowers", "aux" : {"degree" : 2}},
    {"name" : "SumPowers", "aux" : {"degree" : 3}},
    {"name" : "SumPowers", "aux" : {"degree" : 4}},
    {"name" : "SumPowers", "aux" : {"degree" : 5}},
    {"name" : "SumPowers", "aux" : {"degree" : 6}},
    {"name" : "LaurentSeries", "aux" : {"degree" : 2}},
    {"name" : "LaurentSeries", "aux" : {"degree" : 3}},
    {"name" : "LaurentSeries", "aux" : {"degree" : 4}},
    {"name" : "LaurentSeries", "aux" : {"degree" : 5}},
    {"name" : "LaurentSeries", "aux" : {"degree" : 6}},
    {"name" : "LaurentSeries", "aux" : {"degree" : 7}},

    {"name" : "Polynomial", "aux" : {"degree" : 3}}, 
    {"name" : "Polynomial", "aux" : {"degree" : 4}}, 
    {"name" : "Polynomial", "aux" : {"degree" : 5}}, 
    {"name" : "Polynomial", "aux" : {"degree" : 6}}, 
    {"name" : "Polynomial", "aux" : {"degree" : 7}}, 
    {"name" : "Polynomial", "aux" : {"degree" : 8}}, 
    {"name" : "Polynomial", "aux" : {"degree" : 9}}, 
    {"name" : "ExpGaus", "aux" : {}}, 
    {"name" : "Bernstein", "aux" : {"degree" : 2}},
    {"name" : "Bernstein", "aux" : {"degree" : 3}},
    {"name" : "Bernstein", "aux" : {"degree" : 4}},
    {"name" : "Bernstein", "aux" : {"degree" : 5}},
    {"name" : "Bernstein", "aux" : {"degree" : 6}},
    {"name" : "Bernstein", "aux" : {"degree" : 7}},
    {"name" : "Bernstein", "aux" : {"degree" : 8}},
]
sig_modes    = ["Separate"]
sig_M =[125, 110, 140, 115, 135]  ## Central value, plot range, fit range

#####################################################################
###   Settings for Modeling/higgs/generate_bkgDataWorkspaces.py   ###
#####################################################################
bkg_fits_dir = "/Users/vk/software/Analysis/files/higgs_analysis_files/fits/bkg_precombine"
bkg_M =[ 91, 110, 160, 110, 160]  ## Central value, plot range, fit range

#############################################################
###   Settings for Modeling/higgs/generate_datacards.py   ###
#############################################################
datacards_dir = "/Users/vk/software/Analysis/files/higgs_analysis_files/datacards"

datacards_dir = os.path.join( datacards_dir, os.path.split(in_hist_dir)[1] + "__" + path_modifier)

##########################################################
###   Settings for Modeling/higgs/generate_limits.py   ###
##########################################################
combine_dir  = "/Users/vk/software/Analysis/files/higgs_analysis_files/combine_results/"
combine_dir += "%s__%s/%s__%s__Mu24" % (job_label, path_modifier, cmssws[0], JSON.replace('.txt',''))
limits_dir   = "/Users/vk/software/Analysis/files/higgs_analysis_files/limits/"
limits_dir  += "%s__%s/%s__%s__Mu24" % (job_label, path_modifier, cmssws[0], JSON.replace('.txt',''))


