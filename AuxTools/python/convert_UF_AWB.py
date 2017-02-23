
import ROOT as R

signalPPConversion = {
    "_gg" : "GluGlu_HToMuMu_M125_13TeV_powheg_pythia8",
    "_VBF" : "VBF_HToMuMu_M125_13TeV_powheg_pythia8",
    "_ZH" : "ZH_HToMuMu_M125_13TeV_powheg_pythia8",
    "_WH_pos" : "WPlusH_HToMuMu_M125_13TeV_powheg_pythia8",
    "_WH_neg" : "WMinusH_HToMuMu_M125_13TeV_powheg_pythia8"
}

f = R.TFile("/afs/cern.ch/work/a/acarnes/public/validate_dimu_mass_PF_110_160_x69p2_8_0_X_MC_run1categories_36814.root")
f.ls()
signalsDir = f.GetDirectory("signal_histos")
mapPP2ListOfCats = {}

def determineCategory(ccc):
    if len(ccc)==1:
        if ccc[0]=="ALL":
            category = "NoCats"
        else:
            category = "UNKNOWN"
            raise
    elif len(ccc)==2:
        if ccc[0]=="01":
            category = "01Jets"
        elif ccc[0]=="2":
            category = "2Jets"
        else:
            category = "UNKNOWN"
            raise
    elif len(ccc)==4:
        if ccc[0]=="01":
            category = ccc[0]+ccc[1]+"s"+ccc[2]+ccc[3]
        elif ccc[0]=="2":
            if ccc[2]=="GGF":
                category = "ggFTight"
            elif ccc[2]=="VBF":
                if ccc[3]=="Tight":
                    category = "VBFTight"
                elif ccc[3]=="Loose":
                    category = "ggFLoose"
            else:
                category = "UNKNOWN"
    return category

#
# Signals
#
for key in signalsDir.GetListOfKeys():
    hist = key.ReadObj()
    name = hist.GetName()
    first = name.split("H2Mu")[0]
    second = name.split("H2Mu")[1]
    fullpp = signalPPConversion[second]

    ccc = first.split("_")[1:-1]
    if len(ccc)==1:
        if ccc[0]=="ALL":
            category = "NoCats"
        else:
            category = "UNKNOWN"
            raise
    elif len(ccc)==2:
        if ccc[0]=="01":
            category = "01Jets"
        elif ccc[0]=="2":
            category = "2Jets"
        else:
            category = "UNKNOWN"
            raise
    elif len(ccc)==4:
        if ccc[0]=="01":
            category = ccc[0]+ccc[1]+"s"+ccc[2]+ccc[3]
        elif ccc[0]=="2":
            if ccc[2]=="GGF":
                category = "ggFTight"
            elif ccc[2]=="VBF":
                if ccc[3]=="Tight":
                    category = "VBFTight"
                elif ccc[3]=="Loose":
                    category = "ggFLoose"
            else:
                category = "UNKNOWN"
    if fullpp in mapPP2ListOfCats:
        mapPP2ListOfCats[fullpp].append((category, hist))
    else:
        mapPP2ListOfCats[fullpp] = [(category,hist)]
print mapPP2ListOfCats

## Output file path - AWB 23.02.17
path = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/input_hists'
for pp in mapPP2ListOfCats:
    resultFile = R.TFile(path+"/result__%s__80X__Moriond17_Feb08__69mb__Mu24.root" % pp, "RECREATE")
    for category,hist in mapPP2ListOfCats[pp]:
        resultFile.mkdir(category)
        resultFile.cd(category)
        hist.SetName("DiMuonMass")
        hist.Write()
        resultFile.cd("..")
    resultFile.Close()

#
# Data
# 
mapRun2ListOfCats = {}
dataDir = f.GetDirectory("data_histos")
for key in dataDir.GetListOfKeys():
    hist = key.ReadObj()
    name = hist.GetName()
    run = name[-4:]
    rest = name[:-5].split("_")[1:]
    category = determineCategory(rest)
    print category
    if run in mapRun2ListOfCats:
        mapRun2ListOfCats[run].append((category, hist))
    else:
        mapRun2ListOfCats[run] = [(category, hist)]

print mapRun2ListOfCats
for run in mapRun2ListOfCats:
    resultFile = R.TFile(path+"/result__%s__Moriond17_Feb08__Mu24.root" % run, "RECREATE")
    for category,hist in mapRun2ListOfCats[run]:
        resultFile.mkdir(category)
        resultFile.cd(category)
        hist.SetName("DiMuonMass")
        hist.Write()
        resultFile.cd("..")
    resultFile.Close()
