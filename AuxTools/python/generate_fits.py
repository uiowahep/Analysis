from ROOT import *
import sys
import generate_preFitsDataCards as models

#version_data = "v0_20160824_1100"
#version_data = "vR1_20170122_1326_TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
#version_data = "vR1_20170122_1326__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
version_data = "vR2_20170125_1204__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkgs"
#version_fits = "v0p5_20160824_1100"
#version_fits = "vR1_20170122_1326_TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
#version_fits = "vR1_20170122_1326__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
#version_fits = "vR1_20170122_1326__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__wUnc"
version_fits = "vR2_20170125_1204__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkgs"

gROOT.SetBatch(kTRUE)

categories = ["VBFTight", "ggFLoose", "ggFTight",
    "01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
    "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO",
    "01JetsTightBB", "01JetsTightBE", "01JetsTightBO",
    "01JetsTightEE", "01JetsTightOE", "01JetsTightOO",
    "1bJets4l2Mu2e", "1bJets4l3Mu1e", "1bJets4l4Mu",
    "1bJets3l", "1bJets2l",
    "0bJets4l2Mu1e", "0bJets4l3Mu0e", "0bJets4l3Mu1e", "0bJets4l4Mu0e", "0bJets4l2Mu2e", 
]
combinations = {
    "2JetCombination" : ["VBFTight", "ggFLoose", "ggFTight"],
    "01JetCombination" : ["01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
        "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO",
        "01JetsTightBB", "01JetsTightBE", "01JetsTightBO",
        "01JetsTightEE", "01JetsTightOE", "01JetsTightOO"],
    "TotalCombination" : categories,
    "2JetCombinationNoVBFTight" : ["ggFLoose", "ggFTight"],
    "0bJets4lCombination" : ["0bJets4l2Mu1e", "0bJets4l3Mu1e",
         "0bJets4l2Mu2e", "0bJets4l3Mu0e", "0bJets4l4Mu0e"],
    "1bJetsCombination" : ["1bJets4l2Mu2e", "1bJets4l3Mu1e", "1bJets4l4Mu",
        "1bJets3l", "1bJets2l"]
}
#combinations["TotalCombinationNoVBFTight"] = combinations["2JetCombinationNoVBFTight"] + combinations["01JetCombination"]
#combinations["TotalCombinationNoVBFTight"] = combinations["2JetCombinationNoVBFTight"] + combinations["01JetCombination"]+ combinations["0bJets4lCombination"] + combinations["1bJetsCombination"]
combinations["012JetCombination"] = combinations["2JetCombination"]+combinations["01JetCombination"]

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
    dataworkspace_path = wargs["datapath"]
    return "{path}/shape__analytic__{category}__{mass}__{bmodel}__{smode}__{smodel}.root".format(path=dataworkspace_path, category=category, mass=mass, bmodel=bmodel,
        smode=smode, smodel=smodel)

def extractParameters_Background_ExpGaus(ws, fit, *kargs, **wargs):
    category=wargs["category"]
    modifier=wargs["modifier"]
    list_const_pars = []
    list_float_pars = ["a1_{category}".format(category=category), 
        "a2_{category}".format(category=category), 
        "shapeBkg_bmodel_{modifier}{category}__norm".format(
            modifier=modifier, category=category)]
    const_pars = fit.constPars()
    float_pars = fit.floatParsFinal()
    for c in list_const_pars:
        print "import %s" % c
        getattr(ws, "import")(const_pars.find(c))
    for fl in list_float_pars:
        print "import %s" % fl
        getattr(ws, "import")(float_pars.find(fl))

def extractParameters_Signal_DoubleGaus(ws, fit, *kargs, **wargs):
    category=wargs["category"]
    modifier=wargs["modifier"]
    processName = wargs["processName"]
#    imc = wargs["imc"]
    list_const_pars = [
        "m{processName}_g1_mass_{category}".format(
            processName=processName, category=category), 
        "m{processName}_g1_width_{category}".format(
            category=category, processName = processName), 
        "m{processName}_g2_mass_{category}".format(
            category=category, processName = processName), 
        "m{processName}_g2_width_{category}".format(
            category=category, processName = processName),
        "shapeSig_smodel{processName}_{modifier}{category}__norm".format(
            modifier=modifier, category=category, processName=processName), 
        "smodel{processName}_coef_{category}".format(
            category=category, processName = processName)]
    list_float_pars = []
    const_pars = fit.constPars()
    float_pars = fit.floatParsFinal()
    for c in list_const_pars:
        print c
        getattr(ws, "import")(const_pars.find(c))
    for fl in list_float_pars:
        getattr(ws, "import")(float_pars.find(fl))

def extractParameters_Signal_SingleGaus(ws, fit, *kargs, **wargs):
    category=wargs["category"]
    modifier=wargs["modifier"]
#    imc = wargs["imc"]
    processName = wargs["processName"]
    list_const_pars = [
        "m{processName}_mass_{category}".format(
            category=category, processName = processName), 
        "m{processName}_width_{category}".format(
            category=category, processName = processName), 
        "shapeSig_smodel{processName}_{modifier}{category}__norm".format(
            modifier=modifier, category=category, processName=processName)]
    list_float_pars = []
    const_pars = fit.constPars()
    float_pars = fit.floatParsFinal()
    for c in list_const_pars:
        getattr(ws, "import")(const_pars.find(c))
    for fl in list_float_pars:
        getattr(ws, "import")(float_pars.find(fl))

def generate_1Fit(data, fit, *kargs, **wargs):
    category=wargs["category"]
    modifier = wargs["modifier"]
    smode = wargs["smode"]
    combtype = wargs["combtype"]
    smodel_name = wargs["smodel"]
    bmodel_name = wargs["bmodel"]
    fitsworkspace_path = wargs["fitspath"]
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
    if bmodel_name=="ExpGaus":
        extractParameters_Background_ExpGaus(ws, fit, 
            category=category, modifier=modifier)
        bmodel = models.buildModel_ExpGaus(ws, category=category)
        bnorm = ws.var("shapeBkg_bmodel_%s%s__norm"% (modifier, category)).getVal()
        bmodel.plotOn(xframe, RooFit.Normalization(bnorm, 0), RooFit.LineColor(kBlack),
            RooFit.Name("new_bmodel"))
        leg.AddEntry(xframe.FindObject("new_bmodel"), "Background Model", "l")
    print "-"*40
    print "Building Signal Model"
    if smode=="Separate":
        if smodel_name=="SingleGaus":
            for x in signalNames:
                processName = x.split("_")[0]
                extractParameters_Signal_SingleGaus(ws, fit, category=category,
                    modifier=modifier, processName=processName)
                smodel = models.buildModel_SingleGaus(ws, processName=processName,
                    category=category)
                snorm = ws.var("shapeSig_smodel%s_%s%s__norm" % 
                    (processName, modifier, category)).getVal()*20
                smodel.plotOn(xframe, 
                    RooFit.Normalization(snorm, 0), RooFit.LineColor(kRed),
                    RooFit.Name("smodel%s" % processName))
                leg.AddEntry(xframe.FindObject("smodel%s" % processName ), 
                    "%s SM Higgs x 20" % processName, "l")
        elif smodel_name=="DoubleGaus":
            for x in signalNames:
                processName = x.split("_")[0]
                extractParameters_Signal_DoubleGaus(ws, fit, category=category,
                    modifier=modifier, processName=processName)
                smodel = models.buildModel_DoubleGaus(ws, processName=processName,
                    category=category)
                snorm = ws.var("shapeSig_smodel%s_%s%s__norm" % 
                    (processName, modifier, category)).getVal()*20
                smodel.plotOn(xframe, 
                    RooFit.Normalization(snorm, 0), RooFit.LineColor(kRed),
                    RooFit.Name("smodel%s" % processName))
                leg.AddEntry(xframe.FindObject("smodel%s" % processName ), 
                    "%s SM Higgs x 20" % processName, "l")
    elif smode=="Combined":
        if smodel_name=="SingleGaus":
            processName = "AllSignals"
            extractParameters_Signal_SingleGaus(ws, fit, category=category,
                modifier=modifier, processName = processName)
            smodel1 = models.buildModel_SingleGaus(ws, processName=processName, 
                category=category)
            snorm1 = ws.var("shapeSig_smodel%s_%s%s__norm" % 
                (processName, modifier, category)).getVal()*20
            smodel1.plotOn(xframe, 
                RooFit.Normalization(snorm1, 0), RooFit.LineColor(kRed),
                RooFit.Name("smodel%s" % processName))
            leg.AddEntry(xframe.FindObject("smodel%s" % processName), 
                "SM Higgs x 20", "l")
        elif smodel_name=="DoubleGaus":
            print "-"*40
            print "Extract Parameters"
            processName = "AllSignals"
            extractParameters_Signal_DoubleGaus(ws, fit, category=category,
                modifier=modifier, processName = processName)
            print "-"*40
            print "Obtain the Model"
            smodel1 = models.buildModel_DoubleGaus(ws, 
                processName = processName, category=category)
            print "-"*40
            print "Get the Norm Factor"
            snorm1 = ws.var("shapeSig_smodel%s_%s%s__norm" % 
                (processName, modifier, category)).getVal()*20
            print "-"*40
            print "Plot"
            smodel1.plotOn(xframe, 
                RooFit.Normalization(snorm1, 0), RooFit.LineColor(kRed),
                RooFit.Name("smodel%s" % processName))
            leg.AddEntry(xframe.FindObject("smodel%s" % processName) , 
                "SM Higgs x 20", "l")
    print "-"*40
    xframe.Draw()
    leg.Draw()
    c1.SaveAs(fitsworkspace_path+"/fit__{combtype}__{category}__{mass}__{bmodel}__{smode}__{smodel}.png".format(combtype=combtype, category=category, mass=mass,
        bmodel=bmodel_name, smode=smode, smodel=smodel_name))


def blindData(hdata):
    massmin = 120
    massmax = 130
    for ibin in range(hdata.GetNbinsX()):
#        print hdata.GetBinContent(ibin+1)
        if hdata.GetBinCenter(ibin+1)>massmin and hdata.GetBinCenter(ibin+1)<massmax:
#            print hdata.GetBinCenter(ibin+1)
#            print hdata.GetBinContent(ibin+1)
            hdata.SetBinContent(ibin+1, 0)
#            print hdata.GetBinContent(ibin+1)

def main():
#    pus = ["68", "69", "71","72", "70", "71p3", "69p2"]
    pus = ["69"]
    for pu in pus:
        generateFits(pu)

def generateFits(pu):
    folder = "80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__Mu24"
    dataworkspace_path = "/Users/vk/software/Analysis/files/fits_and_datacards/%s/%s/%s" % (
        version_data, folder, pu)
    fitsworkspace_path = "/Users/vk/software/Analysis/files/limits_higsscombined_results/%s/%s/%s" % (
    version_fits, folder, pu)
    type_setting = "analytic"
    mass = "125"
    import glob
    filelist = glob.glob(fitsworkspace_path+"/*mlfit*{type_setting}*.root".format(
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
            if ("Combination" in f):
                if not generate_Combined: continue
                generate_1FitCombined(pathfile=f,
                    datapath=dataworkspace_path, fitspath=fitsworkspace_path,
                    mass=mass, type_setting=type_setting, 
                    signalNames=signals)
                continue
            if not generate_Single: continue
            if generate_Single_test and ccc>0:
                break
            combtype = "Single"
            category = extractCategory(f)
            (bmodel, smode, smodel) = extractModelType(f)
            print "category = %s" % category
            print "fit filename = %s" % f
            modifier = ""
            ints = ['%d' % x for x in range(10)]
            if category[0] in ints: modifier="bin"

            fdata = TFile(findData(category=category, 
                mass=mass, bmodel=bmodel, smode=smode, smodel=smodel,
                datapath=dataworkspace_path))
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
                bmodel=bmodel, smode = smode, smodel=smodel, fitspath=fitsworkspace_path,
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
