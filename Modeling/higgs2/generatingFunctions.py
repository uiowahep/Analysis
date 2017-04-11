"""
a list of functions generate certain distributions/fits/plots/etc...
"""

import ROOT as R
R.gROOT.SetBatch(R.kTRUE)

import aux, os, sys
import definitions as defs
import Configuration.higgs.Samples as S
import models

#
# a list of functions that generate certain distributions/fits/plots/etc...
#
def distributions((category, variable), data, signals, backgrounds, settings, **wargs):
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

def signalFit((category, variable), ws, signal, model, settings, **wargs):
    """
    assume Workspace exists and x-variable is already present
    """
    #
    # initliaze the values from wargs
    #
    pathToDir="/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]
    initialValuesFromTH1 = False
    if "initialValuesFromTH1" in wargs:
        initialValuesFromTH1 = wargs["initialValuesFromTH1"]

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
#    hsdata.GetXaxis().SetRange(variable["min"], variable["max"])
    rsdata = aux.buildRooHist(ws, hsdata)

    #
    # set up the model and perform the fit
    #
    model.initialize(aux.buildSignalModelName(model, settings.names2RepsToUse[category], 
        signal.mc.buildProcessName(), variable["central"]))
    if initialValuesFromTH1:
        model.setInitialValuesFromTH1(hsdata)
    model.createParameters(ws)
    pdf = model.build(ws)
    r = pdf.fitTo(rsdata, R.RooFit.Save(), 
        R.RooFit.Range(variable["fitmin"], variable["fitmax"]))

    #
    # overlay fit/roohist
    #
    rsdata.plotOn(frame)
    pdf.plotOn(frame, R.RooFit.LineColor(R.kRed))
    pdf.paramOn(frame, R.RooFit.Format("NELU", R.RooFit.AutoPrecision(2)), R.RooFit.Layout(0.5, 0.9, 0.9), R.RooFit.ShowConstants(True))
    frame.getAttText().SetTextSize(0.02)
    chiSquare = frame.chiSquare()
    ttt = R.TPaveLabel(0.1,0.7,0.3,0.78, R.Form("#chi^{2} = %f" % chiSquare),
        "brNDC")
    ttt.Draw()
    frame.addObject(ttt)
    frame.Draw()
    mods = "default"
    if initialValuesFromTH1:
        mods="TH1"
    fileName = "signalFit__{category}__{higgsMass}__{processName}__{modelId}__{mods}.png".format(
        category=category, higgsMass=variable["central"], processName=signal.mc.buildProcessName(),
        modelId=model.modelId, mods=mods)
    canvas.SaveAs(os.path.join(pathToDir, fileName))
    
    #
    # close...
    #
    fsdata.Close()

def signalFitInterpolationWithSpline(category, ws, tupleSignalModelVariable, settings,
    **wargs):
    """
    assume the Workspace already exists and x-variable is already defined
    """
    #
    # Load Combine's lib
    #
    R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

    # 
    # initialize the values from wargs
    # 
    pathToDir = "/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]

    #
    # the the canvas/frame
    #
    canvas = R.TCanvas("c1", "c1", 800, 600)
    canvas.cd()
    
    #
    # for each mass point, perform a fit.
    # initial values for each consequetive model will be derived from the 
    # previous mass point
    #
    imodel = 0
    prevSignal=None; prevModel=None; prevVariable=None
    parameters = []
    massPoints = []
    norms = []
    for (signal, model, variable) in tupleSignalModelVariable:
        frame = ws.var("x").frame()
        fsdata = R.TFile(signal.pathToFile)
        hsdata = fsdata.Get(category + "/" + variable["name"])
        hsdata.Scale(1/signal.getWeight())
        rsdata = aux.buildRooHist(ws, hsdata)
        binfirst = hsdata.FindBin(variable["min"])
        binlast = hsdata.FindBin(variable["max"])
#        norms.append(hsdata.Integral(binfirst, binlast))
        norms.append(rsdata.sumEntries())
        model.initialize(aux.buildSignalModelName(model, 
            settings.names2RepsToUse[category],
            signal.mc.buildProcessName(), variable["central"]))
        if imodel>0:
            model.setInitialValuesFromModel(prevModel, ws, 
                massDifference=(variable["central"] - prevVariable["central"]))
        model.createParameters(ws)
        pdf = model.build(ws)
        r = pdf.fitTo(rsdata, R.RooFit.Save(),
            R.RooFit.Range(variable["fitmin"], variable["fitmax"]))
        prevSignal = signal
        prevModel = model
        prevVariable = variable
        imodel +=1
        massPoints.append(variable["central"])

        # plot this model together with signal histogram
        rsdata.plotOn(frame)
        pdf.plotOn(frame, R.RooFit.LineColor(R.kBlue))

        # draw the frame and save the canvas
        frame.Draw()
        fileName = "signalFit__{category}__{higgsMass}__{processName}__{modelId}__{mods}.png".format(
            category=category, higgsMass=variable["central"], processName=signal.mc.buildProcessName(),
            modelId=model.modelId, mods="default")
        canvas.SaveAs(os.path.join(pathToDir, fileName))

        # exctract the parameters
        lParameters = model.getParameterValuesAsList(ws)
        parameters.append(lParameters)

#        pdf.plotOn(frame, R.RooFit.LineColor(R.kBlue))
        imodel+=1

    #
    # build the Splines
    # create the spline for normalization
    # have to transpose the matrix of parameters first
    #
    frame = ws.var("x").frame()
    paramsTransposed = aux.transpose(parameters)
    print parameters
    print paramsTransposed
    finalmodel = prevModel.__class__()
    finalmodel.initialize(aux.buildSignalModelName(model, 
        settings.names2RepsToUse[category], signal.mc.buildProcessName()))
    finalpdf = finalmodel.buildWithParameterMatrix(ws, massPoints, paramsTransposed)
    finalmodel.setNormalization(ws, massPoints, norms)
    finalpdf.Print("v")

    #
    # plot for each GeV and save the canvas
    #
    for mh in [120+i for i in range(11)]:
        ws.var("MH").setVal(mh)
        finalpdf.plotOn(frame)

    #
    # save the canvas
    #
    frame.Draw()
    fileName = "signalFitInterpolationWithSpline__{category}__{processName}__{modelId}__{mods}.png".format(category=category, processName=signal.mc.buildProcessName(), modelId=model.modelId, mods="")
    canvas.SaveAs(os.path.join(pathToDir, fileName))

    #
    # return the model that you build with RooSplines
    #
    return finalmodel

def signalFitInterpolation(category, ws, tupleSignalModelVariable, settings, **wargs):
    """
    assume the Workspace already exists and x-variable is already defined
    """
    # 
    # initialize the values from wargs
    # 
    pathToDir = "/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]

    #
    # the the canvas/frame
    #
    canvas = R.TCanvas("c1", "c1", 800, 600)
    canvas.cd()
    frame = ws.var("x").frame()
    
    #
    # for each mass point, perform a fit.
    # initial values for each consequetive model will be derived from the 
    # previous mass point
    #
    imodel = 0
    prevSignal=None; prevModel=None; prevVariable=None
    for (signal, model, variable) in tupleSignalModelVariable:
        fsdata = R.TFile(signal.pathToFile)
        hsdata = fsdata.Get(category + "/" + variable["name"])
        hsdata.Scale(1/signal.getWeight())
        rsdata = aux.buildRooHist(ws, hsdata)
        model.initialize(aux.buildSignalModelName(model, 
            settings.names2RepsToUse[category],
            signal.mc.buildProcessName(), variable["central"]))
        if imodel>0:
            model.setInitialValuesFromModel(prevModel, ws, 
                massDifference=(variable["central"] - prevVariable["central"]))
        model.createParameters(ws)
        pdf = model.build(ws)
        r = pdf.fitTo(rsdata, R.RooFit.Save(),
            R.RooFit.Range(variable["fitmin"], variable["fitmax"]))
        prevSignal = signal
        prevModel = model
        prevVariable = variable

        pdf.plotOn(frame, R.RooFit.LineColor(R.kBlue))
        imodel+=1

    #
    # save the canvas
    #
    frame.Draw()
    fileName = "signalFitInterpolation__{category}__{processName}__{modelId}__{mods}.png".format(category=category, processName=signal.mc.buildProcessName(), modelId=model.modelId, mods="")
    canvas.SaveAs(os.path.join(pathToDir, fileName))

def ftestPerFamily():
    pass

def datacardAnalytic(category, ws, data, signalModels, backgroundPdf, settings, **wargs):
    #
    # defuaults from wargs
    #
    pathToDir = "/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]
    workspaceFileName = "workspace__testCategory__testSignalModelId.root"
    if "workspaceFileName" in wargs:
        workspaceFileName = wargs["workspaceFileName"]
    workspaceName = "higgs"
    if "workspaceName" in wargs:
        workspaceName = wargs["workspaceName"]

    #
    # datacard content as a list of strings.
    # NOTE: no \n termination, we will join with '\n' in the end
    #
    content = []
    delimString = "-"*90

    #
    # Header
    #
    content.append(delimString)
    imaxString = "imax 1 number of bins"
    content.append(imaxString)
    jmaxString = "jmax {nProcessesMinus1} number of processes minus 1".format(nProcessesMinus1=len(signalModels))
    content.append(jmaxString)
    kmaxString = "kmax * number of nuisance parameters"
    content.append(kmaxString)
    content.append(delimString)

    #
    # Full path to the TFile with Workspace Section
    # In principle the full list of all models/data should come in here
    # but we go with *...
    #
    dataShapeString = "shapes data_obs * {workspaceFileName} {workspaceName}:data_obs_$CHANNEL".format(workspaceFileName=workspaceFileName, workspaceName=workspaceName)
    bkgShapeString = "shapes BKG * {workspaceFileName} {workspaceName}:multipdf_$CHANNEL".format(workspaceFileName=workspaceFileName, workspaceName=workspaceName)
    sigShapesString = "shapes * * {workspaceFileName} {workspaceName}:{className}_$CHANNEL_$PROCESS".format(
        workspaceFileName=workspaceFileName, workspaceName=workspaceName,
        className=signalModels[0].__class__.__name__)
    content.append(dataShapeString)
    content.append(bkgShapeString)
    content.append(sigShapesString)
    content.append(delimString)

    #
    # observation per bin
    #
    binString = "bin {category}".format(category=settings.names2RepsToUse[category])
    content.append(binString)
    obsString = "observation -1"
    content.append(obsString)
    content.append(delimString)
    
    #
    # MC processes/rates
    #
    categoryList = [settings.names2RepsToUse[category] for i in range(len(signalModels)+1)]
    processNamesList = [aux.unpackSignalModelName(model.modelName)[-1]
        for model in signalModels] + ["BKG"]
    processNumbersList = ["%d" % (-len(signalModels)+i) for i in range(1, len(signalModels)+2)]
    rateString = ["%.2f" % data.jsonToUse.intlumi for i in range(len(signalModels))] + ["1"]
    binString = "bin {CategoryList}".format(CategoryList=" ".join(categoryList))
    content.append(binString)
    processNamesString = "process {ProcessNamesList}".format(
        ProcessNamesList=" ".join(processNamesList))
    content.append(processNamesString)
    processNumbersString = "process {ProcessNumbersList}".format(
        ProcessNumbersList=" ".join(processNumbersList))
    content.append(processNumbersString)
    rateString = "rate {rateString}".format(rateString=" ".join(rateString))
    content.append(rateString)
    content.append(delimString)

    #
    # Rate Parameters: Branching Fraction/Cross-section values
    #
    for signal in signalModels:
        processName = aux.unpackSignalModelName(signal.modelName)[-1]
        combineSignalName = settings.mapDASNames2Combine[processName]
        brString = "hmm rateParam * {processName} $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/sm_br_yr4.root:br".format(processName=processName)
        content.append(brString)
        xsString = "{combineSignalName} rateParam * {processName} $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/data/lhc-hxswg/sm/sm_yr4_13TeV.root:xs_13TeV".format(
            processName=processName, combineSignalName=combineSignalName)
        content.append(xsString)
    content.append(delimString)
    
    # 
    # fake uncertainty to make RooMultiPdf work
    #
    fakeUncList = ["1.0001"] + ["-" for i in range(len(signalModels))]
    fakeUncString = "fake lnN {fakeUncList}".format(fakeUncList=" ".join(fakeUncList))
    content.append(fakeUncString)

    #
    # add pdf index
    #
    content.append("pdfindex_{category} discrete".format(category=settings.names2RepsToUse[category]))
    content.append(delimString)

    #
    # join all the lines in content with "\n"
    #
    fileName = "datacard__{category}__{signalModelId}.txt".format(category=settings.names2RepsToUse[category],
        signalModelId=signalModels[0].modelId)
    outputFile = file(os.path.join(pathToDir, fileName), "w")
    outputFile.write("\n".join(content) + "\n")
    outputFile.close()
    
def backgroundsWithRooMultiPdf((category, variable), ws, data, models, settings, **wargs):
    #
    # load the combine lib
    #
    R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

    #
    # run the background Fits
    #
    backgroundFits((category, variable), ws, data, models, settings, **wargs)

    #
    # build the RooMultiPdf and the _norm
    #
    pdfs = R.RooArgList()
    for model in models:
        pdfs.add(ws.pdf(model.modelName))
    ccc = R.RooCategory("pdfindex_{category}".format(category=settings.names2RepsToUse[category]),
        "Index of the currently active or selected pdf")
    multipdf = R.RooMultiPdf("multipdf_{category}".format(category=settings.names2RepsToUse[category]),
        "Background Models Envelope", ccc, pdfs)
    ws.factory("multipdf_{category}_norm[0, 100000000]".format(category=settings.names2RepsToUse[category]))
    getattr(ws, "import")(ccc, R.RooFit.RecycleConflictNodes())
    getattr(ws, "import")(multipdf, R.RooFit.RecycleConflictNodes())
    ws.Print("v")

def backgroundFits((category, variable), ws, data, models, settings, **wargs):
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
    # get the canvas and legend set up
    #
    canvas = R.TCanvas("c1", "c1", 800, 600)
    canvas.cd()
    frame = ws.var("x").frame()
    legend = R.TLegend(0.65, 0.6, 0.9, 0.9)

    #
    # get the data histogram
    #
    fdata = R.TFile(data.pathToFile)
    hdata = fdata.Get(category + "/" + variable["name"])
    hdata_blind = hdata.Clone("Blind")
    aux.blindHistogram(hdata_blind, 120, 130)
    rdata = aux.buildRooHist(ws, hdata)
    rdata_blind = aux.buildRooHist(ws, hdata_blind)
    norm = rdata.sumEntries()
    
    #
    # iterate thru all the models/fit/plot
    #
    counter = 0
    pdfs = {}
    rdata_blind.plotOn(frame)
    for model in models:
        modelName = aux.buildBackgroundModelName(model, settings.names2RepsToUse[category])
        model.initialize(modelName)
        model.createParameters(ws)
        pdfs[modelName] = model.build(ws)
        r = pdfs[modelName].fitTo(rdata, R.RooFit.Save())
        pdfs[modelName].plotOn(frame, R.RooFit.Name(model.modelId), 
            R.RooFit.LineColor(model.color), R.RooFit.Normalization(norm, 0))
        legend.AddEntry(frame.findObject(model.modelId), model.modelId, "l")
        print model.modelId
    frame.Draw()
    
    #
    # save the canvas
    # 
    fileName = "backgroundFits__{category}__{groupName}.png".format(
        category=category,
        groupName=groupName)
    legend.Draw()
    R.gPad.Modified()
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
