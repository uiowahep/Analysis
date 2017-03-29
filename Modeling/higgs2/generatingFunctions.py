"""
a list of functions generate certain distributions/fits/plots/etc...
"""

import ROOT as R
R.gROOT.SetBatch(R.kTRUE)

import aux, os, sys
import definitions as defs
import Configuration.higgs.Samples as S
import models
from Configuration.higgs.Iowa_settings import *

#
# a list of functions that generate certain distributions/fits/plots/etc...
#
def distributions((category, variable), data, signals, backgrounds, **wargs):
    """
    data, signals mc, backgrounds mc samples
    """
    #
    # initialize the values from wargs
    #
    pathToDir = "/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]
    logY = False
    if "logY" in wargs:
        logY = wargs["logY"]

    #
    # create a canvas
    # 
    canvas = R.TCanvas("c1", "c1", 800, 600)
    pad1, pad2 = aux.buildRatioPad(canvas)
    pad1.cd()

    #
    # data
    # 
    fdata = R.TFile(data.pathToFile)
    hdata = fdata.Get(category + "/" + variable["name"])
    if hdata.GetEntries() == 0: return
    hdata.SetMarkerStyle(20)
    hdata.SetMarkerSize(0.5)
    hdata.SetMarkerColor(data.color)

    #
    # signals
    #
    ssum = R.TH1D("signal", "signal", hdata.GetNbinsX(),
        hdata.GetBinLowEdge(1), hdata.GetBinLowEdge(1) + 
        hdata.GetNbinsX()*hdata.GetBinWidth(1))
    hs = {}
    fs = {}
    for signal in signals:
        fs[signal.mc.name] = R.TFile(signal.pathToFile)
        hs[signal.mc.name] = fs[signal.mc.name].Get(category + "/" + variable["name"])
        scale = data.jsonToUse.intlumi * signal.mc.cross_section / signal.getWeight()
        hs[signal.mc.name].Scale(scale)
        ssum.Add(hs[signal.mc.name])
        fs[signal.mc.name].Close()
    ssum.SetLineColor(R.kRed)

    #
    # backgrounds
    #
    bstack = R.THStack("bstack", category)
    bsum = R.TH1D("bsum", "bsum", hdata.GetNbinsX(),
        hdata.GetBinLowEdge(1), hdata.GetBinLowEdge(1) + 
        hdata.GetNbinsX()*hdata.GetBinWidth(1))
    hs = {}
    fs = {}
    for back in backgrounds:
        fs[back.mc.name] = R.TFile(back.pathToFile)
        hs[back.mc.name] = fs[back.mc.name].Get(category + "/" + variable["name"])
        scale = data.jsonToUse.intlumi * back.mc.cross_section / back.getWeight()
        hs[back.mc.name].Scale(scale)
        hs[back.mc.name].SetFillColor(back.color)
        bsum.Add(hs[back.mc.name])
        bstack.Add(hs[back.mc.name])

    #
    # pad1
    #
    bstack.SetMinimum(0.1)
    bstack.Draw("hist")
    bstack.Print("v")
    hdata.Draw("same pe")
    hdata.Print("v")
    ssum.Print("v")
    ssum.Draw("same hist")

    #
    # customization
    #
    if variable["min"]!=-0.999 and variable["max"]!=-0.999:
        bstack.GetXaxis().SetRangeUser(variable["min"], variable["max"])
    if logY:
        pad1.SetLogy()
    R.gPad.Modified()

    #
    # pad2
    #
    pad2.cd()
    hratio = aux.buildRatioHistogram(hdata, bsum)
    hratio.Draw("ep")
    if variable["min"]!=-0.999 and variable["max"]!=-0.999:
        hratio.GetXaxis().SetRangeUser(variable["min"], variable["max"])
    R.gPad.Modified()

    logYstr = "logY" if logY else ""
    fileName = "distribution__{category}__{variable}__{mods}.png".format(
        category=category, variable=variable["name"], mods="{logY}".format(
        logY=logYstr))
    canvas.SaveAs(os.path.join(pathToDir, fileName))

    #
    # close everything
    #
    fdata.Close()
    for x in fs:
        fs[x].Close()

def signalFit((category, variable), ws, signal, model, **wargs):
    """
    assume Workspace exists and x-variable is already present
    """
    #
    # initliaze the values from wargs
    #
    pathToDir="/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]
    higgsMass = 125
    if "higgsMass" in wargs:
        higgsMass = wargs["higgsMass"]

    #
    # get the frame
    #
    canvas = R.TCanvas("c1", "c1", 800, 600)
    canvas.cd()
    frame = ws.var("x").frame()

    #
    # get the histogram
    #
    fsdata = R.TFile(signal.pathToFile)
    hsdata = fsdata.Get(category + "/" + variable["name"])
    hsdata.Scale(1/signal.getWeight())
    rsdata = aux.buildRooHist(ws, hsdata)

    #
    # set up the model and perform the fit
    #
    model.initialize(aux.buildSignalModelName(model, category, signal.mc.buildProcessName()))
    model.createParameters(ws)
    pdf = model.build(ws)
    r = pdf.fitTo(rsdata, R.RooFit.Range(variable["fitmin"], variable["fitmax"]))

    #
    # overlay fit/roohist
    #
    rsdata.plotOn(frame)
    pdf.plotOn(frame, R.RooFit.LineColor(R.kRed))
    pdf.paramOn(frame, R.RooFit.Format("NELU", R.RooFit.AutoPrecision(2)), R.RooFit.Layout(0.6, 0.99, 0.9), R.RooFit.ShowConstants(True))
    frame.getAttText().SetTextSize(0.02)
    frame.Draw()
    fileName = "signalFit__{category}__{higgsMass}__{processName}__{modelId}.png".format(
        category=category, higgsMass=higgsMass, processName=signal.mc.buildProcessName(),
        modelId=model.modelId)
    canvas.SaveAs(os.path.join(pathToDir, fileName))
    
    #
    # close...
    #
    fsdata.Close()

def signalInterpolationFits(signals):
    pass

def backgroundFits((category, variable), ws, data, models, **wargs):
    #
    # initialize the values from wargs
    #
    pathToDir = "/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]
    groupName = "someGroup"
    if "groupName" in wargs:
        groupName = wargs["groupName"]

    #
    # get the canvas
    #
    canvas = R.TCanvas("c1", "c1", 800, 600)
    canvas.cd()
    frame = ws.var("x").frame()

    #
    # get the data histogram
    #
    fdata = R.TFile(data.pathToFile)
    hdata = fdata.Get(category + "/" + variable["name"])
    rdata = aux.buildRooHist(ws, hdata)

    #
    # iterate thru all the models/fit/plot
    #
    counter = 0
    pdfs = {}
    rdata.plotOn(frame)
    for model in models:
        modelName = aux.buildBackgroundModelName(model, category)
        model.initialize(modelName)
        model.createParameters(ws)
        pdfs[modelName] = model.build(ws)
        r = pdfs[modelName].fitTo(rdata, R.RooFit.Save())
        pdfs[modelName].plotOn(frame, R.RooFit.LineColor(model.color))
    frame.Draw()
    
    #
    # save the canvas
    # 
    fileName = "backgroundFits__{category}__{groupName}.png".format(
        category=category,
        groupName=groupName)
    canvas.SaveAs(os.path.join(pathToDir, fileName))

    #
    # close...
    #
    fdata.Close()

if __name__=="__main__":
    singleGaus = models.SingleGaus(singleGaus_initialValues)

    #distributions(("NoCats", "DiMuonMass"), data, [glu, vbf, wm, wp, zh], [wJetsToLNu, wwTo2L2Nu, wzTo3LNu, tt, dy])
    #distributions(("NoCats", "DiMuonpt"), data, [glu, vbf, wm, wp, zh], [wJetsToLNu, wwTo2L2Nu, wzTo3LNu, tt, dy])
    #distributions(("NoCats", "Muonpt"), data, [glu, vbf, wm, wp, zh], [wJetsToLNu, wwTo2L2Nu, wzTo3LNu, tt, dy])

    ws = R.RooWorkspace("higgs")
    ws.Print("v")
    aux.buildMassVariable(ws, **diMuonMass125)
    signalFit(("VBFTight", diMuonMass125), ws, vbf, singleGaus, pathToDir=signalfitsDir)
    signalFit(("ggFTight", diMuonMass125), ws, vbf, singleGaus, pathToDir=signalfitsDir)

    expGaus = models.ExpGaus(expGaus_defaultValues)
    expGaus.color = R.kRed
    bwzRedux = models.BWZRedux(bwzredux_defaultValues)
    bwzRedux.color = R.kBlue
    bwzGamma = models.BWZGamma(bwzgamma_defaultValues)
    bwzGamma.color = R.kGreen
    b5 = models.Bernstein(bernstein_defaultValues, degree=6)
    b5.color = R.kYellow
    sumExp5 = models.SumExponentials(sumExp_defaultValues, degree=5)
    sumExp5.color = R.kViolet
    backgroundFits(("VBFTight", diMuonMass125), ws, data, [expGaus, bwzRedux, bwzGamma, b5,
        sumExp5], pathToDir=backgroundfitsDir, groupName="testGroup")
