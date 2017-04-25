
import os, sys
import ROOT as R
import Modeling.higgs2.models as models
import Modeling.higgs2.definitions as defs
import Modeling.higgs2.aux as aux
import Samples as S


#
# all the standard variable names
#
varNames = [
    "DiJetMass", "DiJetdeta", "DiMuonpt", "DiMuonMass",
    "DiMuoneta", "DiMuondphi", "Muonpt", "Muoneta", "Muonphi"
]

#
# Run 1 Categories list
#
run1Categories = [
    "NoCats", "2Jets", "01Jets", "VBFTight", "ggFTight",
    "ggFLoose", "01JetsTightBB", "01JetsTightBO",
    "01JetsTightBE", "01JetsTightOO", "01JetsTightOE", "01JetsTightEE",
    "01JetsLooseBB", "01JetsLooseBO", "01JetsLooseBE",
    "01JetsLooseOO", "01JetsLooseOE", "01JetsLooseEE",
]

#
# Run 2 Categories list
#
run2Categories = run1Categories[:]
run2Categories.extend(
    [
        "1bJets", "1bJets4l", "1bJets4l2Mu2e", "1bJets4l3Mu1e", "1bJets4l4Mu",
        "1bJets3l", "1bJets2l", "0bJets", "0bJets4l", "0bJets4l2Mu1e", "0bJets4l3Mu0e",
        "0bJets4l3Mu1e", "0bJets4l4Mu0e", "0bJets4l2Mu2e",
    ]
)

#
# Category Representations
#
run1CatReps = ["cat%d" % i for i in range(len(run1Categories))]
run1Reps2Names = {}
run1Names2Reps = {}
for i in range(len(run1CatReps)):
    run1Reps2Names[run1CatReps[i]] = run1Categories[i]
    run1Names2Reps[run1Categories[i]] = run1CatReps[i]

#
# Combinations for Run1
# combinations are named already so that you can use them directly
# NOTE: run1CategoriesForCombination is used rather than run1Categories!
#
run1Combinations = {
    "comb2Jets" : [
        run1Names2Reps["VBFTight"],
        run1Names2Reps["ggFLoose"],
        run1Names2Reps["ggFTight"]],
    "comb01Jets" : [
        run1Names2Reps["01JetsLooseBB"],
        run1Names2Reps["01JetsLooseBE"],
        run1Names2Reps["01JetsLooseBO"],
        run1Names2Reps["01JetsLooseEE"],
        run1Names2Reps["01JetsLooseOE"],
        run1Names2Reps["01JetsLooseOO"],
        run1Names2Reps["01JetsTightBB"],
        run1Names2Reps["01JetsTightBE"],
        run1Names2Reps["01JetsTightBO"],
        run1Names2Reps["01JetsTightEE"],
        run1Names2Reps["01JetsTightOE"],
        run1Names2Reps["01JetsTightOO"]],
    "comb2JetsggF" : [
        run1Names2Reps["ggFLoose"],
        run1Names2Reps["ggFTight"]],
    "comb01JetsTightB" : [
        run1Names2Reps["01JetsTightBB"],
        run1Names2Reps["01JetsTightBO"],
        run1Names2Reps["01JetsTightBE"]],
    "comb01JetsTightO" : [
        run1Names2Reps["01JetsTightOO"],
        run1Names2Reps["01JetsTightOE"],
        run1Names2Reps["01JetsTightEE"]],
    "comb01JetsLoose" : [
        run1Names2Reps["01JetsLooseBB"],
        run1Names2Reps["01JetsLooseBE"],
        run1Names2Reps["01JetsLooseBO"],
        run1Names2Reps["01JetsLooseEE"],
        run1Names2Reps["01JetsLooseOE"],
        run1Names2Reps["01JetsLooseOO"]],
}
run1Combinations["combTotal"] = run1Combinations["comb01Jets"] + run1Combinations["comb2Jets"]
run1Combinations["combNoVBFTight"] = run1Combinations["comb2JetsggF"] + run1Combinations["comb01Jets"]



########################
### General Settings ###
########################
#jobLabel = "vR1_20170329_1241"
jobLabel = "vR1_20170412_2336"
categoriesToUse = run1Categories
combinationsToUse = run1Combinations
reps2NamesToUse = run1Reps2Names
names2RepsToUse = run1Names2Reps

#########################################
### General Combine-specific Settings ###
#########################################
quantiles2Reps = { 
    -1.0 : "observed", 
    0.16 : "m1sigma", 
    0.84 : "p1sigma", 
    0.025 : "m2sigma", 
    0.975 : "p2sigma", 
    0.5 : "expected"
}
physicsModelParametersToSet = {}
nuisancesToFreeze = ["MH"]
def map2string(m, sep=","):
    return ",".join(["{key}={value}".format(key=x, value=m[x]) for x in m])

#######################
### Directory Setup ###
#######################
projectDirLocal = "/Users/vk/software/Analysis/files/analysis_results/"
projectDirLxplus = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/analysis_results"
cmsswDir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_7_4_9/src"
projectDirToUse = projectDirLxplus
histDir = os.path.join(projectDirToUse, "results", jobLabel)
distributionsDir = os.path.join(projectDirToUse, "distributions", jobLabel);
aux.mkdir(distributionsDir)
backgroundfitsDir = os.path.join(projectDirToUse, "backgroundfits", jobLabel)
aux.mkdir(backgroundfitsDir)
signalfitsDir = os.path.join(projectDirToUse, "signalfits", jobLabel)
aux.mkdir(signalfitsDir)
singalfitinterpolationsDir = os.path.join(projectDirToUse, "signalfitinterpolations", jobLabel)
aux.mkdir(singalfitinterpolationsDir)
signalfitinterpolationswithsplineDir = os.path.join(projectDirToUse, "signalfitinterpolationswithspline", jobLabel)
aux.mkdir(signalfitinterpolationswithsplineDir)
backgroundfitswithroomultipdfDir = os.path.join(projectDirToUse, "backgroundfitswithroomultipdf", jobLabel)
aux.mkdir(backgroundfitswithroomultipdfDir)
datacardsworkspacesDir = os.path.join(projectDirToUse, "datacardsworkspaces", jobLabel)
aux.mkdir(datacardsworkspacesDir)
combineoutputDir = os.path.join(projectDirToUse, "combineoutput", jobLabel)
aux.mkdir(combineoutputDir)
combinesubmissionsDir = os.path.join(projectDirToUse, "combinesubmissions", jobLabel)
aux.mkdir(combinesubmissionsDir)
limitsDir = os.path.join(projectDirToUse, "limits", jobLabel)
aux.mkdir(limitsDir)
ftestDir = os.path.join(projectDirToUse, "ftest", jobLabel)
aux.mkdir(ftestDir)
biasScanDir = os.path.join(projectDirToUse, "biasScan", jobLabel)
aux.mkdir(biasScanDir)

#################
###  Samples  ###
#################
jsonToUse = S.jsonfiles["2016_ReReco_36460"]
dataPathToFile = histDir + "/" + "result__merged__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__Mu24.root"

inputFileUF = '/afs/cern.ch/work/a/acarnes/public/h2mumu/rootfiles/w_sig_120_130/validate_UNBLINDED_dimu_mass_Roch_110_160_categories3_tree_categorization_final_36814_dyAMC_minpt10.root'
useInputFileUF = False

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
glu125PathToFile = histDir + "/" + "result__GluGlu_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
glu120PathToFile = histDir + "/" + "result__GluGlu_HToMuMu_M120_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
glu130PathToFile = histDir + "/" + "result__GluGlu_HToMuMu_M130_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
vbf125PathToFile = histDir + "/" + "result__VBF_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
vbf120PathToFile = histDir + "/" + "result__VBF_HToMuMu_M120_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
vbf130PathToFile = histDir + "/" + "result__VBF_HToMuMu_M130_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wm125PathToFile = histDir + "/" + "result__WMinusH_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wm120PathToFile = histDir + "/" + "result__WMinusH_HToMuMu_M120_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wm130PathToFile = histDir + "/" + "result__WMinusH_HToMuMu_M130_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wp125PathToFile = histDir + "/" + "result__WPlusH_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wp120PathToFile = histDir + "/" + "result__WPlusH_HToMuMu_M120_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
wp130PathToFile = histDir + "/" + "result__WPlusH_HToMuMu_M130_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
zh125PathToFile = histDir + "/" + "result__ZH_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
zh120PathToFile = histDir + "/" + "result__ZH_HToMuMu_M120_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
zh130PathToFile = histDir + "/" + "result__ZH_HToMuMu_M130_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"

glu125MC = S.mcMoriond2017datasets_1["GluGlu_125"]
glu120MC = S.mcMoriond2017datasets_1["GluGlu_120"]
glu130MC = S.mcMoriond2017datasets_1["GluGlu_130"]
vbf125MC = S.mcMoriond2017datasets_1["VBF_125"]
vbf120MC = S.mcMoriond2017datasets_1["VBF_120"]
vbf130MC = S.mcMoriond2017datasets_1["VBF_130"]
wm125MC = S.mcMoriond2017datasets_1["WM_125"]
wm120MC = S.mcMoriond2017datasets_1["WM_120"]
wm130MC = S.mcMoriond2017datasets_1["WM_130"]
wp125MC = S.mcMoriond2017datasets_1["WP_125"]
wp120MC = S.mcMoriond2017datasets_1["WP_120"]
wp130MC = S.mcMoriond2017datasets_1["WP_130"]
zh125MC = S.mcMoriond2017datasets_1["Z_125"]
zh120MC = S.mcMoriond2017datasets_1["Z_120"]
zh130MC = S.mcMoriond2017datasets_1["Z_130"]

# sample objects
data = defs.Data("NoCats", jsonToUse, dataPathToFile, color=R.kBlack)
dy = defs.MC("NoCats", dyPathToFile, dyMC, color=R.kBlue)
tt = defs.MC("NoCats", ttPathToFile, ttMC, color=R.kGreen)
wJetsToLNu = defs.MC("NoCats", wJetsToLNuPathToFile, wJetsToLNuMC, color=R.kYellow)
wwTo2L2Nu = defs.MC("NoCats", wwTo2L2NuPathToFile, wwTo2L2NuMC, color=R.kGray)
wzTo3LNu = defs.MC("NoCats", wzTo3LNuPathToFile, wzTo3LNuMC, color=R.kViolet)
glu125 = defs.MC("NoCats", glu125PathToFile, glu125MC, color=None)
glu120 = defs.MC("NoCats", glu120PathToFile, glu120MC, color=None)
glu130 = defs.MC("NoCats", glu130PathToFile, glu130MC, color=None)
vbf125 = defs.MC("NoCats", vbf125PathToFile, vbf125MC, color=None)
vbf120 = defs.MC("NoCats", vbf120PathToFile, vbf120MC, color=None)
vbf130 = defs.MC("NoCats", vbf130PathToFile, vbf130MC, color=None)
wm125 = defs.MC("NoCats", wm125PathToFile, wm125MC, color=None)
wm120 = defs.MC("NoCats", wm120PathToFile, wm120MC, color=None)
wm130 = defs.MC("NoCats", wm130PathToFile, wm130MC, color=None)
wp125 = defs.MC("NoCats", wp125PathToFile, wp125MC, color=None)
wp120 = defs.MC("NoCats", wp120PathToFile, wp120MC, color=None)
wp130 = defs.MC("NoCats", wp130PathToFile, wp130MC, color=None)
zh125 = defs.MC("NoCats", zh125PathToFile, zh125MC, color=None)
zh120 = defs.MC("NoCats", zh120PathToFile, zh120MC, color=None)
zh130 = defs.MC("NoCats", zh130PathToFile, zh130MC, color=None)

########################
### Models' Settings ###
########################
# single gaus
singleGaus125_initialValues = {
    "mean":125, "meanmin":123, "meanmax":127,
    "sigma":1.0, "sigmamin":0.1, "sigmamax":10
}
singleGaus120_initialValues = {
    "mean":120, "meanmin":118, "meanmax":122,
    "sigma":1.0, "sigmamin":0.1, "sigmamax":10
}
singleGaus130_initialValues = {
    "mean":130, "meanmin":128, "meanmax":132,
    "sigma":1.0, "sigmamin":0.1, "sigmamax":10
}
doubleGaus125_initialValues = {
    "mean1":125, "mean1min":123, "mean1max":127,
    "sigma1":1.0, "sigma1min":0.5, "sigma1max":4,
    "mean2":125, "mean2min":121, "mean2max":129,
    "sigma2":1.0, "sigma2min":1.7, "sigma2max":7,
    "coef" : 0.8, "coefmin" : 0.0001, "coefmax": 1
}
doubleGaus120_initialValues = {
    "mean1":120, "mean1min":118, "mean1max":122,
    "sigma1":1.0, "sigma1min":0.5, "sigma1max":4,
    "mean2":120, "mean2min":116, "mean2max":124,
    "sigma2":1.0, "sigma2min":1.7, "sigma2max":7,
    "coef" : 0.8, "coefmin" : 0.0001, "coefmax": 1
}
doubleGaus130_initialValues = {
    "mean1":130, "mean1min":128, "mean1max":132,
    "sigma1":1.0, "sigma1min":0.5, "sigma1max":4,
    "mean2":130, "mean2min":126, "mean2max":134,
    "sigma2":1.0, "sigma2min":1.7, "sigma2max":7,
    "coef" : 0.8, "coefmin" : 0.0001, "coefmax": 1
}
tripleGaus125_initialValues = {
    "mean1":125, "mean1min":123, "mean1max":127,
    "sigma1":1.1, "sigma1min":0.5, "sigma1max":1.7,
    "mean2":125, "mean2min":123, "mean2max":127,
    "sigma2":2.5, "sigma2min":1.7, "sigma2max":4,
    "mean3":121, "mean3min":116, "mean3max":123,
    "sigma3":4.5, "sigma3min":3, "sigma3max":7,
    "coef1" : 0.78, "coef1min" : 0.0001, "coef1max" : 1,
    "coef2" : 0.16, "coef2min" : 0.0001, "coef2max" : 1,
}
tripleGaus120_initialValues = {
    "mean1":120, "mean1min":118, "mean1max":122,
    "sigma1":1.1, "sigma1min":0.5, "sigma1max":1.7,
    "mean2":120, "mean2min":118, "mean2max":122,
    "sigma2":2.5, "sigma2min":1.7, "sigma2max":4,
    "mean3":116, "mean3min":111, "mean3max":118,
    "sigma3":4.5, "sigma3min":3, "sigma3max":7,
    "coef1" : 0.78, "coef1min" : 0.0001, "coef1max" : 1,
    "coef2" : 0.16, "coef2min" : 0.0001, "coef2max" : 1,
}
tripleGaus130_initialValues = {
    "mean1":130, "mean1min":128, "mean1max":132,
    "sigma1":1.1, "sigma1min":0.5, "sigma1max":1.7,
    "mean2":130, "mean2min":128, "mean2max":132,
    "sigma2":2.5, "sigma2min":1.7, "sigma2max":4,
    "mean3":126, "mean3min":121, "mean3max":128,
    "sigma3":4.5, "sigma3min":3, "sigma3max":7,
    "coef1" : 0.78, "coef1min" : 0.0001, "coef1max" : 1,
    "coef2" : 0.16, "coef2min" : 0.0001, "coef2max" : 1,
}

# expGaus
expGaus_defaultValues = {
    "a1" : 1.0, "a1min" : -20, "a1max" : 20,
    "a2" : 0.3, "a2min" : -20, "a2max" : 20
}

# BWZ
bwz_defaultValues = {
    "zmass" : 91.2, "zmassmin": 90, "zmassmax" : 92,
    "zwidth" : 2.5, "zwidthmin" : 0, "zwidthmax" : 30,
    "expParam" : -1e-03, "expParammin" : -1e-02, "expParammax" : 1e-02
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
    "expParam" : -0.1, "expParammin": -1, "expParammax": -0.001,
#    "expParam" : -0.0053, "expParammin" : -0.0073, "expParammax" : -0.0033,
    "fraction" : 0.379, "fractionmin" : 0.2, "fractionmax" : 1
}
# bernsteins
bernstein_defaultValues = aux.buildDefaultValuesBerstein(20)
# sum exponentials
sumExp_defaultValues = aux.buildDefaultValuesSumExponentials(20)
# power Law
powLaw_defaultValues = aux.buildDefaultValuesPowerLaw(20)
# laurent series
exponents = [-4, -3, -5, -2, -6, -1, -7, 0, -8, 1, -9, 2, -10, 3, -11]
laurent_defaultValues = aux.buildDefaultValuesLaurentSeries(20)

################################################
### Mass Variables/Fit Ranges/Drawing Ranges ###
################################################
diMuonMass125 = {"name":"DiMuonMass", "central":125, "min":110, "max":250,
    "fitmin" : 115, "fitmax" : 135}
diMuonMass120 = {"name":"DiMuonMass", "central":120, "min":110, "max":250,
    "fitmin" : 110, "fitmax" : 130}
diMuonMass130 = {"name":"DiMuonMass", "central":130, "min":110, "max":250,
    "fitmin" : 120, "fitmax" : 140}

"""
a list of common things, not configurations, but common...
"""

######################
### Pool of Colors ###
######################
colors = [
    R.kBlack, R.kRed, R.kGreen, R.kBlue, R.kYellow, R.kViolet, R.kGray,
    R.kOrange, R.kPink, R.kMagenta, R.kAzure, R.kCyan, R.kTeal,
    R.kSpring
]

#########################################################
### Map CMS DAS Higgs Signal Name to Combine Notation ###
#########################################################
mapDASNames2Combine = {
    "VBF" : "vbfH_13TeV",
    "GluGlu" : "ggH_13TeV",
    "WMinusH" : "WminusH_13TeV",
    "WPlusH" : "WplusH_13TeV",
    "ZH" : "ZH_13TeV",
    "ttH" : "ttH_13TeV"
}

##################################
### predefined lists of models ###
##################################
# signal
singleGaus125 = models.SingleGaus(singleGaus125_initialValues)
singleGaus120 = models.SingleGaus(singleGaus120_initialValues)
singleGaus130 = models.SingleGaus(singleGaus130_initialValues)
doubleGaus125 = models.DoubleGaus(doubleGaus125_initialValues)
doubleGaus120 = models.DoubleGaus(doubleGaus120_initialValues)
doubleGaus130 = models.DoubleGaus(doubleGaus130_initialValues)
tripleGaus125 = models.TripleGaus(tripleGaus125_initialValues)
tripleGaus120 = models.TripleGaus(tripleGaus120_initialValues)
tripleGaus130 = models.TripleGaus(tripleGaus130_initialValues)

# background
expGaus = models.ExpGaus(expGaus_defaultValues)
bwz = models.BWZ(bwz_defaultValues)
bwzRedux = models.BWZRedux(bwzredux_defaultValues)
bwzGamma = models.BWZGamma(bwzgamma_defaultValues)
bernsteinsFast = [models.BernsteinFast(bernstein_defaultValues, degree=i) for i in range(1, 8)]
bernsteins = [models.Bernstein(bernstein_defaultValues, degree=i) for i in range(1, 11)]
sumExps = [models.SumExponentials(sumExp_defaultValues, degree=i) for i in range(1, 8)]
powerLaw = [models.PowerLaw(powLaw_defaultValues, degree=i) for i in range(1, 10)]
laurentSeries = [models.LaurentSeries(laurent_defaultValues, degree=i, exponents=exponents) for i in range(2, 10)]

class ModelGroup(object):
    def __init__(self, name, models):
        self.models = models
        self.name = name
        object.__init__(self)

bernsteinModels = ModelGroup("bersteinModels", bernsteins)
sumExpModels = ModelGroup("sumExpModels", sumExps)
allPhysBkgModels = ModelGroup("allPhysBkgModels", [bwz, expGaus, bwzRedux, bwzGamma])
laurentModels = ModelGroup("LaurentSeries", laurentSeries)
powerLawModels = ModelGroup("PowerLaw", powerLaw)
bernsteinsPlusPhysModels = ModelGroup("bersteinsPlusPhysModels",
    allPhysBkgModels.models + bernsteins)
bernsteinsFastModels = ModelGroup("bernsteinFastModels", bernsteinsFast)
sumExpsPlusPhysModels = ModelGroup("sumExpsPlusPhysModels", allPhysBkgModels.models + sumExps)
allBackgroundModels = ModelGroup("allBackgroundModels", allPhysBkgModels.models + bernsteinsFastModels.models)

#backgroundModelGroups = [allPhysBkgModels, bernsteinsPlusPhysModels, bernsteinModels]
backgroundModelGroups = [bernsteinsFastModels, allPhysBkgModels, allBackgroundModels]
modelGroupForMultiPdf = ModelGroup("modelGroupForMultiPdf", [expGaus, bwzRedux, bwzGamma,
    models.Bernstein(bernstein_defaultValues, degree=6)])
modelGroupTest = ModelGroup("modelGroupTest", [bwzRedux, bwzGamma, 
    models.BernsteinFast(bernstein_defaultValues, degree=5)])
physGroupTest = ModelGroup("physModelsGroup", [bwzRedux, bwzGamma, expGaus, bwz])
orderedGroupsTest = [bernsteinsFastModels, sumExpModels]
orderedModelGroups = [bernsteinsFastModels, sumExpModels, powerLawModels]
