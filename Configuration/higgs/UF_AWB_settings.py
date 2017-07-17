
import os, sys
import ROOT as R
import Modeling.higgs2.models as models
import Modeling.higgs2.definitions as defs
import Modeling.higgs2.aux as aux
import Samples as samp  ## From Configuration/higgs/Samples.py
import AuxTools.python.common as CM ## mkdir tool


#
# all the standard variable names
#
varNames = ['DiMuonMass']

#
# Run 1 Categories list
#
run1Categories = []
run1Categories = [
    'NoCats', '2Jets', '01Jets', 'VBFTight', 'ggFTight', 'ggFLoose', 
    '01JetsTightBB', '01JetsTightBO', '01JetsTightBE', '01JetsTightOO', '01JetsTightOE', '01JetsTightEE',
    '01JetsLooseBB', '01JetsLooseBO', '01JetsLooseBE', '01JetsLooseOO', '01JetsLooseOE', '01JetsLooseEE',
]

#
# Run 2 Categories list - BDT categorization
#
# run2Categories = [
#     'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6',
#     'c7', 'c8', 'c9', 'c10', 'c11', 'c12'
#     ]
run2Categories = ['c7', 'c8']

run2Reps2Names = {}
run2Names2Reps = {}
for i in range(len(run2Categories)): ## Keep the names the same for now
    run2Reps2Names[run2Categories[i]] = run2Categories[i]
    run2Names2Reps[run2Categories[i]] = run2Categories[i]

#
# Combinations for Run2
# combinations are named already so that you can use them directly
# NOTE: run2CategoriesForCombination is used rather than run2Categories!
#
# run2Combinations = {
#     'bdt0' : [
#         run2Names2Reps['c0'],
#         run2Names2Reps['c2'],
#         run2Names2Reps['c8']],
#     'bdt1' : [
#         run2Names2Reps['c7'],
#         run2Names2Reps['c4'],
#         run2Names2Reps['c1'],
#         run2Names2Reps['c6'],
#         run2Names2Reps['c5']],
#     'bdt2' : [
#         run2Names2Reps['c3'],
#         run2Names2Reps['c10'],
#         run2Names2Reps['c11']],
#     'bdt3' : [
#         run2Names2Reps['c9'],
#         run2Names2Reps['c12']]
# }
# run2Combinations['combTotal'] = run2Combinations['bdt0'] + run2Combinations['bdt1'] + run2Combinations['bdt2'] + run2Combinations['bdt3']

run2Combinations = {
    'bdt7' : [run2Names2Reps['c7']],
    'bdt8' : [run2Names2Reps['c8']]
}
run2Combinations['combTotal'] = run2Combinations['bdt7'] + run2Combinations['bdt8']

########################
### General Settings ###
########################
jobLabel          = 'AWB_Jul17_biasTest_v1'
categoriesToUse   = run2Categories
combinationsToUse = run2Combinations
reps2NamesToUse   = run2Reps2Names
names2RepsToUse   = run2Names2Reps
massListToUse     = [120, 125, 130]
signalModelNames  = ['TripleGaus']


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
cmsswDir                             = '/afs/cern.ch/user/a/abrinke1/CMSSW_7_4_7/src/'
projectDirToUse                      = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits2/'
CM.mkdir(projectDirToUse)
histDir                              = os.path.join(projectDirToUse, 'results', jobLabel)
CM.mkdir(histDir)
distributionsDir                     = os.path.join(projectDirToUse, 'distributions', jobLabel);
CM.mkdir(distributionsDir)
backgroundfitsDir                    = os.path.join(projectDirToUse, 'backgroundfits', jobLabel)
CM.mkdir(backgroundfitsDir)
signalfitsDir                        = os.path.join(projectDirToUse, 'signalfits', jobLabel)
CM.mkdir(signalfitsDir)
singalfitinterpolationsDir           = os.path.join(projectDirToUse, 'signalfitinterpolations', jobLabel)
CM.mkdir(singalfitinterpolationsDir)
signalfitinterpolationswithsplineDir = os.path.join(projectDirToUse, 'signalfitinterpolationswithspline', jobLabel)
CM.mkdir(signalfitinterpolationswithsplineDir)
backgroundfitswithroomultipdfDir     = os.path.join(projectDirToUse, 'backgroundfitswithroomultipdf', jobLabel)
CM.mkdir(backgroundfitswithroomultipdfDir)
datacardsworkspacesDir               = os.path.join(projectDirToUse, 'datacardsworkspaces', jobLabel)
CM.mkdir(datacardsworkspacesDir)
combineoutputDir                     = os.path.join(projectDirToUse, 'combineoutput', jobLabel)
CM.mkdir(combineoutputDir)
combinesubmissionsDir                = os.path.join(projectDirToUse, 'combinesubmissions', jobLabel)
CM.mkdir(combinesubmissionsDir)
limitsDir = os.path.join(projectDirToUse, "limits", jobLabel)
CM.mkdir(limitsDir)
ftestDir = os.path.join(projectDirToUse, "ftest", jobLabel)
CM.mkdir(ftestDir)
biasScanDir = os.path.join(projectDirToUse, "biasScan", jobLabel)
CM.mkdir(biasScanDir)


#################
###  Samples  ###
#################
## inputFileUF = '/afs/cern.ch/work/a/acarnes/public/h2mumu/rootfiles/sys_and_fine_binning/validate_UNBLINDED_dimu_mass_Roch_110_160_categories3_tree_categorization_final_36814_dyAMC_minpt10.root'
inputFileUF = '/afs/cern.ch/work/a/acarnes/public/h2mumu/rfiles/validate_UNBLINDED_dimu_mass_Roch_90_200_categories3_tree_categorization_final_36814_dyAMC-J_minpt10_b-4_sig-xlumi0.root'
useInputFileUF = True

systematicsPathToFile = "/afs/cern.ch/work/v/vkhriste/public/Higgs2Mu/systematics/nuisances_Andrea_BDT.csv"
nuisances = aux.readInSystematics(systematicsPathToFile)
nuisance_lumi = "1.027"
nuisance_br = "1.017"
nuisance_xsecs = {
    "GluGlu" : "1.05",
    "VBF" : "1.022",
    "WPlusH" : "1.02",
    "WMinusH" : "1.02",
    "ZH" : "0.965/1.041"
}

jsonToUse = samp.jsonfiles['2016_ReReco_36460']

glu125MC = samp.mcMoriond2017datasets_1['GluGlu_125']
glu120MC = samp.mcMoriond2017datasets_1['GluGlu_120']
glu130MC = samp.mcMoriond2017datasets_1['GluGlu_130']
vbf125MC = samp.mcMoriond2017datasets_1['VBF_125']
vbf120MC = samp.mcMoriond2017datasets_1['VBF_120']
vbf130MC = samp.mcMoriond2017datasets_1['VBF_130']
wm125MC  = samp.mcMoriond2017datasets_1['WM_125']
wm120MC  = samp.mcMoriond2017datasets_1['WM_120']
wm130MC  = samp.mcMoriond2017datasets_1['WM_130']
wp125MC  = samp.mcMoriond2017datasets_1['WP_125']
wp120MC  = samp.mcMoriond2017datasets_1['WP_120']
wp130MC  = samp.mcMoriond2017datasets_1['WP_130']
zh125MC  = samp.mcMoriond2017datasets_1['Z_125']
zh120MC  = samp.mcMoriond2017datasets_1['Z_120']
zh130MC  = samp.mcMoriond2017datasets_1['Z_130']

# sample objects
data = defs.Data('NoCats', jsonToUse, inputFileUF, color=R.kBlack)

glu125 = defs.MC('NoCats', inputFileUF, glu125MC, color=R.kBlue)
glu120 = defs.MC('NoCats', inputFileUF, glu120MC, color=R.kBlue)
glu130 = defs.MC('NoCats', inputFileUF, glu130MC, color=R.kBlue)
vbf125 = defs.MC('NoCats', inputFileUF, vbf125MC, color=R.kRed)
vbf120 = defs.MC('NoCats', inputFileUF, vbf120MC, color=R.kRed)
vbf130 = defs.MC('NoCats', inputFileUF, vbf130MC, color=R.kRed)
wm125  = defs.MC('NoCats', inputFileUF, wm125MC, color=R.kGreen)
wm120  = defs.MC('NoCats', inputFileUF, wm120MC, color=R.kGreen)
wm130  = defs.MC('NoCats', inputFileUF, wm130MC, color=R.kGreen)
wp125  = defs.MC('NoCats', inputFileUF, wp125MC, color=R.kGreen)
wp120  = defs.MC('NoCats', inputFileUF, wp120MC, color=R.kGreen)
wp130  = defs.MC('NoCats', inputFileUF, wp130MC, color=R.kGreen)
zh125  = defs.MC('NoCats', inputFileUF, zh125MC, color=R.kViolet)
zh120  = defs.MC('NoCats', inputFileUF, zh120MC, color=R.kViolet)
zh130  = defs.MC('NoCats', inputFileUF, zh130MC, color=R.kViolet)

########################
### Models' Settings ###
########################
# single gaus
singleGaus125_initialValues = {
    'mean':125, 'meanmin':115, 'meanmax':135,
    'sigma':1.0, 'sigmamin':0.1, 'sigmamax':10
}
singleGaus120_initialValues = {
    'mean':120, 'meanmin':110, 'meanmax':130,
    'sigma':1.0, 'sigmamin':0.1, 'sigmamax':10
}
singleGaus130_initialValues = {
    'mean':130, 'meanmin':120, 'meanmax':140,
    'sigma':1.0, 'sigmamin':0.1, 'sigmamax':10
}
doubleGaus125_initialValues = {
    'mean1':125, 'mean1min':115, 'mean1max':135,
    'sigma1':1.0, 'sigma1min':0.1, 'sigma1max':10,
    'mean2':125, 'mean2min':115, 'mean2max':135,
    'sigma2':1.0, 'sigma2min':0.1, 'sigma2max':10,
    'coef' : 0.1, 'coefmin' : 0.0001, 'coefmax': 1
}
doubleGaus120_initialValues = {
    'mean1':120, 'mean1min':110, 'mean1max':130,
    'sigma1':1.0, 'sigma1min':0.1, 'sigma1max':10,
    'mean2':120, 'mean2min':110, 'mean2max':130,
    'sigma2':1.0, 'sigma2min':0.1, 'sigma2max':10,
    'coef' : 0.1, 'coefmin' : 0.0001, 'coefmax': 1
}
doubleGaus130_initialValues = {
    'mean1':130, 'mean1min':120, 'mean1max':140,
    'sigma1':1.0, 'sigma1min':0.1, 'sigma1max':10,
    'mean2':130, 'mean2min':120, 'mean2max':140,
    'sigma2':1.0, 'sigma2min':0.1, 'sigma2max':10,
    'coef' : 0.1, 'coefmin' : 0.0001, 'coefmax': 1
}
tripleGaus125_initialValues = {
    'mean1':125, 'mean1min':124, 'mean1max':126,
    'sigma1':1.5, 'sigma1min':0.8, 'sigma1max':4,
    'mean2':125, 'mean2min':115, 'mean2max':135,
    'sigma2':1.0, 'sigma2min':0.1, 'sigma2max':10,
    'mean3':125, 'mean3min':115, 'mean3max':135,
    'sigma3':1.0, 'sigma3min':2, 'sigma3max':20,
    'coef1' : 0.7, 'coef1min' : 0.4, 'coef1max' : 1,
    'coef2' : 0.1, 'coef2min' : 0.0001, 'coef2max' : 1,
}
tripleGaus120_initialValues = {
    'mean1':120, 'mean1min':119, 'mean1max':121,
    'sigma1':1.5, 'sigma1min':0.8, 'sigma1max':4,
    'mean2':120, 'mean2min':110, 'mean2max':130,
    'sigma2':1.0, 'sigma2min':0.1, 'sigma2max':10,
    'mean3':120, 'mean3min':110, 'mean3max':130,
    'sigma3':1.0, 'sigma3min':2, 'sigma3max':20,
    'coef1' : 0.7, 'coef1min' : 0.4, 'coef1max' : 1,
    'coef2' : 0.1, 'coef2min' : 0.0001, 'coef2max' : 1,
}
tripleGaus130_initialValues = {
    'mean1':130, 'mean1min':129, 'mean1max':131,
    'sigma1':1.5, 'sigma1min':0.8, 'sigma1max':4,
    'mean2':130, 'mean2min':120, 'mean2max':140,
    'sigma2':1.0, 'sigma2min':0.1, 'sigma2max':10,
    'mean3':130, 'mean3min':120, 'mean3max':140,
    'sigma3':1.0, 'sigma3min':2, 'sigma3max':20,
    'coef1' : 0.7, 'coef1min' : 0.4, 'coef1max' : 1,
    'coef2' : 0.1, 'coef2min' : 0.0001, 'coef2max' : 1,
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
    "a1" : 2.0, "a1min" : -10., "a1max" : 10.,
    "a2" : 0.7, "a2min" : -10., "a2max" : 10.,
    "a3" : 0.5, "a3min" : -10., "a3max" : 10.
}

# BWZ Redux Fixed
bwzreduxfixed_defaultValues = {
    "a2" : 0.7, "a2min" : -10., "a2max" : 10.,
    "a3" : 0.5, "a3min" : -10., "a3max" : 10.
}

# BWZ Redux x Line
bwzreduxtimesline_defaultValues = {
    "a1" : 2.0, "a1min" : -10., "a1max" : 10.,
    "a2" : 0.7, "a2min" : -10., "a2max" : 10.,
    "a3" : 0.5, "a3min" : -10., "a3max" : 10.,
    "a4" : 0.1, "a4min" : -6.4, "a4max" : 6.4  ## +/- 2*pi 
}

# BWZ Redux + Line
bwzreduxplusline_defaultValues = {
    "a1" : 2.0, "a1min" : -10., "a1max" : 10.,
    "a2" : 0.7, "a2min" : -10., "a2max" : 10.,
    "a3" : 0.5, "a3min" : -10., "a3max" : 10.,
    "a4" : 0.1, "a4min" : -6.4, "a4max" : 6.4,  ## +/- 2*pi 
    "a5" : 1.0, "a5min" : -10., "a5max" : 10.,
}

# BWZ Redux x Line + Line
bwzreduxtimesplusline_defaultValues = {
    "a1" : 2.0, "a1min" : -10., "a1max" : 10.,
    "a2" : 0.7, "a2min" : -10., "a2max" : 10.,
    "a3" : 0.5, "a3min" : -10., "a3max" : 10.,
    "a4" : 0.1, "a4min" : -6.4, "a4max" : 6.4,  ## +/- 2*pi 
    "a5" : 1.0, "a5min" : -10., "a5max" : 10.,
    "a6" : 0.1, "a6min" : -6.4, "a6max" : 6.4  ## +/- 2*pi 
}

# BWZ Gamma
bwzgamma_defaultValues = {
    "zwidth" : 2.5, "zwidthmin" : 0, "zwidthmax" : 30,
    "zmass" : 91.2, "zmassmin" : 80, "zmassmax" : 100,
    "expParam" : -0.1, "expParammin": -100, "expParammax": -0.00001,
    "fraction" : 0.379, "fractionmin" : 0.001, "fractionmax" : 1
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
sumpoly_defaultValues = aux.buildDefaultValuesSumPoly(20)

################################################
### Mass Variables/Fit Ranges/Drawing Ranges ###
################################################
diMuonMass125 = {"name":"DiMuonMass", "central":125, "min":110, "max":150,
    "fitmin" : 115, "fitmax" : 135}
diMuonMass120 = {"name":"DiMuonMass", "central":120, "min":110, "max":150,
    "fitmin" : 110, "fitmax" : 130}
diMuonMass130 = {"name":"DiMuonMass", "central":130, "min":110, "max":150,
    "fitmin" : 120, "fitmax" : 140}

"""
a list of common things, not configurations, but common...
"""

######################
### Pool of Colors ###
######################
colors = [
    R.kRed, R.kGreen, R.kBlue, R.kYellow, R.kViolet, R.kGray,
    R.kOrange, R.kPink, R.kMagenta, R.kAzure, R.kCyan, R.kTeal,
    R.kSpring, R.kRed+1, R.kGreen+1, R.kBlue+1, R.kYellow+1, 
    R.kViolet+1, R.kGray+1, R.kOrange+1, R.kPink+1, R.kMagenta+1
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
bwzReduxFixed = models.BWZReduxFixed(bwzreduxfixed_defaultValues)
bwzReduxTimesLine = models.BWZReduxTimesLine(bwzreduxtimesline_defaultValues)
bwzReduxPlusLine = models.BWZReduxPlusLine(bwzreduxplusline_defaultValues)
bwzReduxTimesPlusLine = models.BWZReduxTimesPlusLine(bwzreduxtimesplusline_defaultValues)
bwzGamma = models.BWZGamma(bwzgamma_defaultValues)
bernsteinsFast = [models.BernsteinFast(bernstein_defaultValues, degree=i) for i in range(1, 8)]
bernsteins = [models.Bernstein(bernstein_defaultValues, degree=i) for i in range(1, 11)]
sumExps = [models.SumExponentials(sumExp_defaultValues, degree=i) for i in range(1, 11)]
powerLaw = [models.PowerLaw(powLaw_defaultValues, degree=i) for i in range(1, 10)]
laurentSeries = [models.LaurentSeries(laurent_defaultValues, degree=i, exponents=exponents) for i in range(2, 10)]
sumPolys = [models.SumPoly(sumpoly_defaultValues, degree=i) for i in range(2, 20)]

class ModelGroup(object):
    def __init__(self, name, models):
        self.models = models
        self.name = name
        object.__init__(self)

bernsteinModels      = ModelGroup("bersteinModels",      bernsteins)
bernsteinsFastModels = ModelGroup("bernsteinFastModels", bernsteinsFast)
sumPolysModels       = ModelGroup("SumPoly",             sumPolys)
sumExpModels         = ModelGroup("sumExpModels",        sumExps)
laurentModels        = ModelGroup("LaurentSeries",       laurentSeries)
powerLawModels       = ModelGroup("PowerLaw",            powerLaw)

allPhysBkgModels    = ModelGroup("allPhysBkgModels", [bwzRedux, bwzReduxPlusLine])
physGroupTest       = ModelGroup("physModelsGroup",  [bwzRedux, bwzReduxPlusLine])

backgroundModelGroups = [bernsteinModels, sumPolysModels, allPhysBkgModels]

modelGroupForMultiPdf = ModelGroup(
    "modelGroupForMultiPdf", 
    [ bwzRedux, bwzReduxPlusLine, 
      models.SumPoly        (sumpoly_defaultValues,   degree=19),
      models.SumExponentials(sumExp_defaultValues,    degree=3),
      models.Bernstein      (bernstein_defaultValues, degree=10) ] )

orderedGroupsTest  = [sumPolysModels, sumExpModels, bernsteinModels]
orderedModelGroups = [sumPolysModels, sumExpModels, bernsteinModels]
