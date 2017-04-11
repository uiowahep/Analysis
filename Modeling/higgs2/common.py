"""
a list of common things, not configurations, but common...
"""

from Configuration.higgs.Iowa_settings import *
from models import *
import ROOT as R

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
singleGaus125 = SingleGaus(singleGaus125_initialValues)
singleGaus120 = SingleGaus(singleGaus120_initialValues)
singleGaus130 = SingleGaus(singleGaus130_initialValues)
doubleGaus125 = DoubleGaus(doubleGaus125_initialValues)
doubleGaus120 = DoubleGaus(doubleGaus120_initialValues)
doubleGaus130 = DoubleGaus(doubleGaus130_initialValues)
tripleGaus125 = TripleGaus(tripleGaus125_initialValues)
tripleGaus120 = TripleGaus(tripleGaus120_initialValues)
tripleGaus130 = TripleGaus(tripleGaus130_initialValues)

# background
expGaus = ExpGaus(expGaus_defaultValues)
bwzRedux = BWZRedux(bwzredux_defaultValues)
bwzGamma = BWZGamma(bwzgamma_defaultValues)
bernsteins = [Bernstein(bernstein_defaultValues, degree=i) for i in range(1, 11)]
sumExps = [SumExponentials(sumExp_defaultValues, degree=i) for i in range(1, 11)]


class ModelGroup(object):
    def __init__(self, name, models):
        self.models = models
        self.name = name
        object.__init__(self)

bernsteinModels = ModelGroup("bersteinModels", bernsteins)
sumExpModels = ModelGroup("sumExpModels", sumExps)
allPhysBkgModels = ModelGroup("allPhysBkgModels", [expGaus, bwzRedux, bwzGamma])
bernsteinsPlusPhysModels = ModelGroup("bersteinsPlusPhysModels", 
    allPhysBkgModels.models + bernsteins)
sumExpsPlusPhysModels = ModelGroup("sumExpsPlusPhysModels", allPhysBkgModels.models + sumExps)
allBackgroundModels = ModelGroup("allBackgroundModels", allPhysBkgModels.models + bernsteins + sumExps)

backgroundModelGroups = [allPhysBkgModels, bernsteinsPlusPhysModels, bernsteinModels]
modelGroupForMultiPdf = ModelGroup("modelGroupForMultiPdf", [expGaus, bwzRedux, bwzGamma,
    Bernstein(bernstein_defaultValues, degree=6)])
modelGroupTest = ModelGroup("modelGroupTest", [bwzRedux, bwzGamma])
