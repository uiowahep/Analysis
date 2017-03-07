import ROOT as R
import NtupleProcessing.python.Dataset as DS
import NtupleProcessing.python.Samples as S
import models
from uncertainty import *
import os,sys

#
# slice a hist
#
def sliceHistogram(h, **wargs):
    newName = wargs["name"]
    massmin = wargs["massmin"]
    massmax = wargs["massmax"]
    newHist = R.TH1D(newName, newName, massmax - massmin, massmin, massmax)
    newibin = 0
    for ibin in range(h.GetNbinsX()):
        if h.GetBinCenter(ibin+1)>massmin and h.GetBinCenter(ibin+1)<massmax:
            newHist.SetBinContent(newibin+1, h.GetBinContent(ibin+1))
            newHist.SetBinError(newibin+1, h.GetBinError(ibin+1))
            newibin += 1
    return newHist

def getEventWeights(pathToFile):
    f = R.TFile(pathToFile)
    h = f.Get("eventWeights")
    return h.GetBinContent(1)

def mkdir(pathDir):
    if os.path.exists(pathDir):
        return
    else:
        os.system("mkdir %s" % pathDir)

def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

def blindData(hdata):
    massmin = 120
    massmax = 130
    for ibin in range(hdata.GetNbinsX()):
        if hdata.GetBinCenter(ibin+1)>massmin and hdata.GetBinCenter(ibin+1)<massmax:
            hdata.SetBinContent(ibin+1, 0)

def blindRooData(ws):
    data = ws.data("data_obs")
    hdata = data.createHistogram("hdata", ws.var("x"),
        R.RooFit.Binning(50, 110, 160))
    blindData(hdata)
    ds = R.RooDataHist("data_blind", "data_blind", R.RooArgList(ws.set("obs").Clone()), hdata)
    return ds

#
# Modeling the Results = Histograms of Mass Shapes that result from Procssing ntuples
#
class MCResult(DS.MCDataset):
    def __init__(self, mc, pu, pathToFile, eweight, options):
        DS.MCDataset.__init__(self, mc)
        self.pu = pu
        self.pathToFile=pathToFile
        self.eweight = eweight
        self.options = options

    def buildLabel(self):
        """
        For Now just production mechanism
        """
        return self.name.split("/")[1].split("_")[0]

class DataResult:
    def __init__(self, name, year, jsonToUse, pathToFile):
        self.jsonToUse = jsonToUse
        self.name = name
        self.year = year
        self.pathToFile=pathToFile

    def __str__(self):
        return "-"*80+"\n"+\
                "DataResult:" + "\n"+\
                ">>> name=" + self.name + "\n"+\
                ">>> pathToFile=" + self.pathToFile + "\n"+\
                ">>> json: " + str(self.jsonToUse) + "\n" +\
                "-"*80 + "\n"
    def __repr__(self):
        return self.__str__()

    def buildLabel(self):
        return "%s %s %.1f/fb" % (self.name, self.year, self.jsonToUse.intlumi/1000)

class PhysicsChannel:
    def __init__(self, mcresult, modelName, uncertainties, **wargs):
        self.mc = mcresult
        self.modelName = modelName
        self.wargs = wargs
        self.uncs = uncertainties

    def buildRateVector(self):
        category = self.wargs["category"]
        myId = self.wargs["myId"]
        modelklass = getattr(models, self.modelName)
        model = modelklass(category=category, processName=self.mc.buildLabel())

        nameToUse = model.getModelName()

        # note for now, rate is 1 for everything.
        # All of the normalization comes into play in workspace
        return [nameToUse, myId, 1]

    def buildRateUncertaintyVector(self):
        return ["%.3f" % unc.valuesMap[self.mc.buildLabel()] for unc in self.uncs]

class BackgroundChannel:
    def __init__(self, modelName, uncertainties, **wargs):
        self.modelName = modelName
        self.wargs = wargs
        self.uncs = uncertainties

    def buildRateVector(self):
        category = self.wargs["category"]
        myId = self.wargs["myId"]
        modelklass = getattr(models, self.modelName)
        model = modelklass(category=category)

        nameToUse = model.getModelName()

        # note for now, rate is 1 for everything.
        # All of the normalization comes into play in workspace
        return [nameToUse, myId, 1]

    def buildRateUncertaintyVector(self):
        return ["-" for x in self.uncs]

#
# Model a Combine Datacard
#
class Datacard:
    def __init__(self, category, lsignals, bkg, data, **wargs):
        self.category = category
        # signal channels as SignalChannel
        self.signals = lsignals
        # bkg channel as BackgroundChannel
        self.bkg = bkg
        # data as DataResult
        self.data = data
        # aux
        self.wargs = wargs
    
    def build(self):
        return self.generateHeaderSection() + \
                self.generateShapeDeclarationSection() + \
                self.generateCategorySection() + \
                self.generateProcessRateSection() + \
                self.generateRateUncertaintiesSection()

    def generateHeaderSection(self):
        s = "-"*40 + "\n" + \
            "imax 1\n" + \
            "jmax %d\n" % len(self.signals) + \
            "kmax *\n"
        return s

    def generateShapeDeclarationSection(self):
        s = "-"*40 + "\n" + \
            "shapes * * {pathToWorkspaceFile} higgs:$PROCESS\n".format(
                pathToWorkspaceFile=self.wargs["pathToWorkspaceFile"])
        return s

    def generateCategorySection(self):
        s = "-"*40 + "\n" + \
            "bin %s\n" % self.category + \
            "observation -1\n"
        return s

    def generateProcessRateSection(self):
        s = "-"*40 + "\n" + \
            "bin " + " ".join([self.category for i in range(len(self.signals)+1)]) + "\n"
        meta = ["process", "process", "rate"]
        signalRateSection = [x.buildRateVector() for x in self.signals]
        bkgRateSection = [self.bkg.buildRateVector()]
        rates = [meta] + signalRateSection + bkgRateSection
        trates = transpose(rates)
        rates = "\n".join([" ".join(str(item) for item in xxx) for xxx in trates])
        return s+rates+"\n"

    def generateRateUncertaintiesSection(self):
        # we need to get all the rate uncertainties
        #meta = []
        s = "-"*40 + "\n"
        uncNames,uncTypes = buildNameTypeVector(self.signals[0].uncs)
        signalRateSection = [x.buildRateUncertaintyVector() for x in self.signals]
        bkgRateSection = [self.bkg.buildRateUncertaintyVector()]
        rateUncs = [uncNames] + [uncTypes] + signalRateSection + bkgRateSection
        transposed = transpose(rateUncs)
        rates = "\n".join([" ".join(str(item) for item in xxx) for xxx in transposed])
        return s+rates+"\n"

    def generateShapeUncertaintiesSection(self):
        return ""

if __name__=="__main__":
    mc = MCResult(S.mcMoriond2017datasets["/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"],
        "69", "somePath", 100, None)
    chl1 = PhysicsChannel(mc, "SingleGaus", myId=0, category="VBFTight")
    chl2 = PhysicsChannel(mc, "SingleGaus", myId=2, category="VBFTight")
    chl3 = PhysicsChannel(mc, "SingleGaus", myId=1, category="VBFTight")
    card = Datacard("VBFTight", [chl1,chl2,chl3], chl1, None)
    print card.build()
