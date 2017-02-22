import ROOT as R
import NtupleProcessing.python.Dataset as DS
import NtupleProcessing.python.Samples as S

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

#
# Model a Combine Datacard
#
class SimpleDatacard:
    def __init__(self, category, lsignals, bkg, data):
        self.category = category
        self.signals = lsignals
        self.bkg = bkg
        self.data = data

    def generateHeaderSection(self):
        s = "-"*40 + "\n" + \
            "imax 1\n" + \
            "jmax %d\n" % len(self.signals) + \
            "kmax *\n"
        return s

    def generateShapeDeclarationSection(self):
        s = "-"*40 + "\n" + \
            "shapes * * {pathToSignalWorkspaceFile} higgs:$PROCESS\n" + \
            "shapes * * {pathToBackgroundWorkspaceFile} higgs:$PROCESS\n"
        return s

    def generateCategorySection(self):
        s = "-"*40 + "\n" + \
            "bin %s\n" % category + \
            "observation -1\n"
        return s

    def generateProcessRateSection(self):
        s = "-"*40 + "\n"
        meta = ["bin", "process", "process", "rate"]
#        for s in self.signals: 

if __name__=="__main__":
    mc = MCResult(S.mcMoriond2017datasets["/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"])
    print mc
