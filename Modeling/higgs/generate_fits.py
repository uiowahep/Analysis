from ROOT import *
import sys
import models
from categories import *
from aux import *

#version_data = "vR2_20170125_1204__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkgs"
#version_fits = "vR2_20170125_1204__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkgs"

version_data = "vR1_20170217_1742__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkg"
version_fits = version_data
pus = ["69"]
folder = "80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__Mu24"
dataworkspace_path = "/Users/vk/software/Analysis/files/higgs_analysis_files/datacards_and_workspaces"
fitsworkspace_path = "/Users/vk/software/Analysis/files/higgs_analysis_files/combine_results"
smodels = ["SingleGaus", "DoubleGaus"]

gROOT.SetBatch(kTRUE)

combinations = combinationsRun1

tail = "MaxLikelihoodFit.mH125.root"
head = "higgsCombine"
def extractCategory(s):
    s = s.split("/")
    s = s[len(s)-1]
    s = s.split("__")[1]
    return s

def extractModelType(s):
    s = s.split("/")[-1].split("__")
    return (s[3], s[4], s[5][:-5])

def findData(**wargs):
    category = wargs["category"]
    mass = wargs["mass"]
    bmodel = wargs["bmodel"]
    smode = wargs["smode"]
    smodel = wargs["smodel"]
    datapath = wargs["datapath"]
    return "{path}/workspace__analytic__{category}__{mass}__{bmodel}__{smode}__{smodel}.root".format(path=datapath, category=category, mass=mass, bmodel=bmodel,
        smode=smode, smodel=smodel)

def generate_1Fit(data, fit, *kargs, **wargs):
    category=wargs["category"]
    modifier = wargs["modifier"]
    smode = wargs["smode"]
    combtype = wargs["combtype"]
    smodel_name = wargs["smodel"]
    bmodel_name = wargs["bmodel"]
    fitspath = wargs["fitspath"]
    mass = wargs["mass"]
    signalNames = wargs["signalNames"]
    print category
    print smode
    print smodel_name
    print bmodel_name

    ws = RooWorkspace("higgs_fits")
    ws.factory("x[125.0, %f, %f]" % (110, 160))
    ws.var('x').SetTitle('m_{#mu#mu}')
    ws.var('x').setUnit('GeV')

    print "-"*40
    c1 = TCanvas("c1", "c1", 800, 600)
    c1.cd()
    leg = TLegend(0.6, 0.6, 0.8, 0.8)
    x = ws.var("x")
    xframe = x.frame()
    xframe.SetTitle("%s %s" % (category, smodel_name))
    data.plotOn(xframe)
    leg.AddEntry(data, "Data", "p")
    print "-"*40
    print "Building Background Model"

    modelklass = getattr(models, bmodel_name)
    bmodel = modelklass(category=category, modifier=modifier)
    bmodel.extractParameters(ws, fit)
    broomodel = bmodel.build(ws)
    bnorm = bmodel.norm.getVal()
    broomodel.plotOn(xframe, RooFit.Normalization(bnorm, 0), RooFit.LineColor(kBlack),
        RooFit.Name("new_bmodel"))
    leg.AddEntry(xframe.FindObject("new_bmodel"), "Background Model", "l")
    print "-"*40
    print "Building Signal Model"

    for sname in signalNames:
        processName = sname.split("_")[0]
        modelklass = getattr(models, smodel_name)
        smodel = modelklass(category=category, processName=processName, 
            modifier=modifier)
        smodel.extractParameters(ws, fit)
        sroomodel = smodel.build(ws, category=category, processName=processName)
        snorm = smodel.norm.getVal()
        sroomodel.plotOn(xframe, 
            RooFit.Normalization(snorm*20, 0), RooFit.LineColor(kRed),
            RooFit.Name("smodel%s" % processName))
        leg.AddEntry(xframe.FindObject("smodel%s" % processName ), 
            "%s SM Higgs x 20" % processName, "l")
    
    print "-"*40
    print "Drawing Frame"
    xframe.Draw()
    leg.Draw()
    
    print "-"*40
    print "Saving the Canvas"
    c1.SaveAs(fitspath+"/bonlyfit__{combtype}__{category}__{mass}__{bmodel}__{smode}__{smodel}.png".format(combtype=combtype, category=category, mass=mass,
        bmodel=bmodel_name, smode=smode, smodel=smodel_name))


def main():
    for pu in pus:
        generateFits(pu)

def generateFits(pu):
    fullDataworkspace_path = "%s/%s/%s/%s" % (dataworkspace_path,
        version_data, folder, pu)
    fullFitsworkspace_path = "%s/%s/%s/%s" % (fitsworkspace_path, 
        version_fits, folder, pu)
    type_setting = "analytic"
    mass = "125"
    import glob
    filelist = glob.glob(fullFitsworkspace_path+"/*mlfit*{type_setting}*.root".format(
        type_setting=type_setting))
    ccc = 0
    combfilelist = []
    generate_Single = True
    generate_Combined = True
    generate_Single_test = False
    signals = [
        'GluGlu_HToMuMu_M125_13TeV_powheg_pythia8',
        'VBF_HToMuMu_M125_13TeV_powheg_pythia8',
        "WMinusH_HToMuMu_M125_13TeV_powheg_pythia8",
        "WPlusH_HToMuMu_M125_13TeV_powheg_pythia8",
        "ZH_HToMuMu_M125_13TeV_powheg_pythia8"
    ]

    #   this will do only separate fitting
    for f in filelist:
        try:
            if extractCategory(f) in combinations:
                if not generate_Combined: continue
                generate_1FitCombined(pathfile=f,
                    datapath=fullDataworkspace_path, fitspath=fullFitsworkspace_path,
                    mass=mass, type_setting=type_setting, 
                    signalNames=signals)
                continue
            if not generate_Single: continue
            if generate_Single_test and ccc>0:
                break
            combtype = "Single"
            category = extractCategory(f)
            (bmodel, smode, smodel) = extractModelType(f)
            if smodel not in smodels: continue

            print "category = %s" % category
            print "fit filename = %s" % f
            modifier = ""
            ints = ['%d' % x for x in range(10)]
            if category[0] in ints: modifier="bin"

            fdata = TFile(findData(category=category, 
                mass=mass, bmodel=bmodel, smode=smode, smodel=smodel,
                datapath=fullDataworkspace_path))
            wsdata = fdata.Get("higgs")
            data = wsdata.data("data_obs")
            hdata = data.createHistogram("hdata", wsdata.var("x"), 
                RooFit.Binning(50, 110, 160))
            hdata.Print()
            blindData(hdata)
            hdata.Print()
            ds = RooDataHist("data", "data", RooArgList(wsdata.set("obs").Clone()), hdata)
#            data = RooDataHist("data_obs_1", "data_obs_1", RooArgList(wsdata.set("obs")), 
#                hdata)
            ffit = TFile(f)
            fit = ffit.Get("fit_b")
            fit.Print("v")
            print "-"*40
            generate_1Fit(ds, fit, category=category, modifier=modifier,
                bmodel=bmodel, smode = smode, smodel=smodel, fitspath=fullFitsworkspace_path,
                combtype=combtype, mass=mass, signalNames=signals)
            print "-"*40
        except Exception as exc:
            print exc.args
        ccc+=1


def generate_1FitCombined(**wargs):
    pathfile = wargs["pathfile"]
    datapath = wargs["datapath"]
    fitspath = wargs["fitspath"]
    mass = wargs["mass"]
    type_setting = wargs["type_setting"]
    signalNames = wargs["signalNames"]
    try:
        print "-"*40
        print pathfile
        category_combtype=extractCategory(pathfile)
        categories = combinations[category_combtype]
        combtype = category_combtype
        for category in categories:
            print "-"*40
            print category
            (bmodel, smode, smodel) = extractModelType(pathfile)
            if smodel not in smodels: continue
            print bmodel
            print smode
            print smodel
            modifier = "bin"
            fdata = TFile(findData(category=category,
                mass=mass, bmodel=bmodel, smode=smode, smodel=smodel,
                datapath=datapath))
            wsdata = fdata.Get("higgs")
            data = wsdata.data("data_obs")
            hdata = data.createHistogram("hdata", wsdata.var("x"),
                RooFit.Binning(50, 110, 160))
            hdata.Print()
            blindData(hdata)
            hdata.Print()
            ds = RooDataHist("data", "data", RooArgList(wsdata.set("obs").Clone()),
                hdata)
            ffit = TFile(pathfile)
            fit = ffit.Get("fit_b")
            fit.Print("v")
            print "-"*40
            generate_1Fit(ds, fit, category=category, modifier=modifier,
                bmodel=bmodel, smode=smode, smodel=smodel,
                fitspath=fitspath, combtype=combtype, mass=mass,
                signalNames=signalNames)
            print "-"*40 
    except Exception as exc:
        print exc.args

if __name__=="__main__":
    main()
