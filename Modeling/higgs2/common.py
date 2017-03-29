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
singleGaus = SingleGaus(singleGaus_initialValues)
doubleGaus = DoubleGaus(doubleGaus_initialValues)
tripleGaus = TripleGaus(tripleGaus_initialValues)

# background
expGaus = ExpGaus(expGaus_defaultValues)
bwzRedux = BWZRedux(bwzredux_defaultValues)
bwzGamma = BWZGamma(bwzgamma_defaultValues)
bernsteins = [Bernstein(bernstein_defaultValues, degree=i) for i in range(1, 11)]
sumExps = [SumExponentials(sumExp_defaultValues, degree=i) for i in range(1, 11)]

allPhysBkgModels = [expGaus, bwzRedux, bwzGamma]
bersteinsPlusPhysModels = allPhysBkgModels + bernsteins
allBackgroundModels = allPhysBkgModels + bernsteins + sumExps
