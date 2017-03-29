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

allPhysBkgModels = [expGaus, bwzRedux, bwzGamma]
bersteinsPlusPhysModels = allPhysBkgModels + bernsteins
allBackgroundModels = allPhysBkgModels + bernsteins + sumExps
