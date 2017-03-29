#
# Common Definitions
#
import ROOT as R
from aux import blindHistogram
import os,sys
sys.path.append(os.environ["ANALYSISHOME"])
sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "Configuration/higgs"))

class Empty(object):
    def __init__(self):
        object.__init__(self)

class Sample(object):
    def __init__(self, category, pathToFile, **wargs):
        object.__init__(self)
        self.category = category
        self.pathToFile = pathToFile
        self.color = wargs["color"]

class Data(Sample):
    def __init__(self, category, jsonToUse, pathToFile, **wargs):
        Sample.__init__(self, category, pathToFile, **wargs)
        self.jsonToUse = jsonToUse

class MC(Sample):
    def __init__(self, category, pathToFile, mc, **wargs):
        """
        MC Sample
        """
        Sample.__init__(self, category, pathToFile, **wargs)
        self.mc = mc

    def getWeight(self, *kargs, **wargs):
        f = R.TFile(self.pathToFile)
        h = f.Get("eventWeights")
        self.weight = h.GetBinContent(1)
        f.Close()
        return self.weight
