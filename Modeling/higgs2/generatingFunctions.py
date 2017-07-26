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

    hdata_name = category + "/" + variable["name"]
    if settings.useInputFileUF: 
        hdata_name = "net_histos/"+category+"_Net_Data"

    hdata = fdata.Get(hdata_name)
    if variable["name"] == "DiMuonMass":
        hdata.Rebin(settings.rebinGroup)
    hdata.SetMarkerStyle(20)
    hdata.SetMarkerSize(0.5)
    hdata.SetMarkerColor(data.color)
    hdata.SetTitle(category)
    hdata.SetStats(R.kFALSE)

    leg = R.TLegend(0.75, 0.7, 1.0, 1.0)
    leg.SetHeader("Samples")
    leg.AddEntry(hdata, "Data")

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

        if settings.useInputFileUF: 
            hs_name = "signal_histos/" + category + "_" + signal.mc.uflabel
            hs_wgt  = 1.0
        else:
            hs_name = category + "/" + variable["name"]
            hs_wgt  = signal.getWeight()

        hs[signal.mc.name] = fs[signal.mc.name].Get(hs_name)
        if variable["name"] == "DiMuonMass":
            hs[signal.mc.name].Rebin(settings.rebinGroup)
        scale = data.jsonToUse.intlumi * signal.mc.cross_section / hs_wgt
        hs[signal.mc.name].Scale(scale)
        ssum.Add(hs[signal.mc.name])
        fs[signal.mc.name].Close()
    ssum.SetLineColor(R.kRed)
    ssum.SetLineWidth(2)
    leg.AddEntry(ssum, "Signal")

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

        if settings.useInputFileUF: 
            hs_name = "net_histos/" + category + "_" + back.mc.uflabel
            hs_wgt  = 1.0
            scale = 1.0
        else:
            hs_name = category + "/" + variable["name"]
            hs_wgt  = back.getWeight()
            scale = data.jsonToUse.intlumi * back.mc.cross_section / hs_wgt
            
        hs[back.mc.name] = fs[back.mc.name].Get(hs_name)
        if variable["name"] == "DiMuonMass":
            hs[back.mc.name].Rebin(settings.rebinGroup)
        hs[back.mc.name].Scale(scale)
        hs[back.mc.name].SetFillColor(back.color)
        bsum.Add(hs[back.mc.name])
        bstack.Add(hs[back.mc.name])

        if settings.useInputFileUF:
            leg.AddEntry(hs[back.mc.name], back.mc.ufPlotLabel)
        else:
            leg.AddEntry(hs[back.mc.name], back.mc.plotLabel)

    #
    # pad1
    #
    hdata.SetMinimum(0.001)
    hdata.Draw("pe")
    hdata.Print("v")
    if len(backgrounds) > 0:
        bstack.Draw("histsame")
        bstack.Print("v")
    ssum.Print("v")
    ssum.Draw("same hist")

    #
    # customization
    #
    if variable["min"]!=-0.999 and variable["max"]!=-0.999:
        hdata.GetXaxis().SetRangeUser(variable["min"], variable["max"])
    if logY:
        pad1.SetLogy()
    leg.Draw()
    R.gPad.Modified()

    #
    # pad2
    #
    pad2.cd()
    hratio = aux.buildRatioHistogram(hdata, bsum)
    hratio.SetTitle("")
    hratio.GetYaxis().SetTitle("Data / MC")
    hratio.GetXaxis().SetTitle(variable["name"])
    hratio.GetYaxis().SetNdivisions(6, R.kFALSE)
    hratio.GetYaxis().SetTitleSize(10)
    hratio.GetYaxis().SetTitleFont(43)
    hratio.GetYaxis().SetTitleOffset(1.55)
    hratio.GetYaxis().SetLabelFont(43)
    hratio.GetYaxis().SetLabelSize(15)
    hratio.GetXaxis().SetTitleSize(20)
    hratio.GetXaxis().SetTitleFont(43)
    hratio.GetXaxis().SetTitleOffset(4)
    hratio.GetXaxis().SetLabelFont(43)
    hratio.GetXaxis().SetLabelSize(15)
    hratio.Draw("ep")
    hratio.SetStats(R.kFALSE)
    if variable["min"]!=-0.999 and variable["max"]!=-0.999:
        hratio.GetXaxis().SetRangeUser(variable["min"], variable["max"])
    hratio.SetMaximum(1.6)
    hratio.SetMinimum(0.4)
    hratio.SetMarkerStyle(20)
    hratio.SetMarkerSize(0.5)
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

# Fits signal model to signal histogram for that category
# Saves model and fit params to the workspace
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
    # get the histogram from the input root file
    # and convert to a roo hist
    #
    fsdata = R.TFile(signal.pathToFile)

    hsdata_name = category + "/" + variable["name"]
    if settings.useInputFileUF: 
        hsdata_name = "signal_histos/" + category + "_" + signal.mc.uflabel

    hsdata = fsdata.Get(hsdata_name)
    if not settings.useInputFileUF:
        hsdata.Scale(1/signal.getWeight())
#    hsdata.GetXaxis().SetRange(variable["min"], variable["max"])
    rsdata = aux.buildRooHist(ws, hsdata)

    #
    # set up the model and perform the fit
    #

    # Simply set the name for the model based upon the model, category, and M=120,125,or 130 
    model.initialize(aux.buildSignalModelName(model, settings.names2RepsToUse[category], 
        signal.mc.buildProcessName(), variable["central"]))

    # Set the initial signal model parameters based upon the mean and rms of the signal histogram
    # for this category, seems reasonable for single gauss, but not sure what it does for double
    # and triple gauss
    if initialValuesFromTH1:
        model.setInitialValuesFromTH1(hsdata)
    model.createParameters(ws)                 # Create params for model and add to workspace
    pdf = model.build(ws, category=category)   # Create model using the params we just added to the workspace
                                               # Add model to workspace

    # Fit the model and get the result
    # !!!! SHOULD MAKE SURE THE FIT CONVERGED AND MATRIX IS CORRECT !!!!
    # RooFitResult::covQual()==3
    #   status = -1 :  not available (inversion failed or Hesse failed)
    #   status =  0 : available but not positive defined
    #   status =  1 : covariance only approximate
    #   status =  2 : full matrix but forced pos def
    #   status =  3 : full accurate matrix
    # RooFitResult::status()==0
    #   status = 0    : OK
    #   status = 1    : Covariance was mad  epos defined
    #   status = 2    : Hesse is invalid
    #   status = 3    : Edm is above max
    #   status = 4    : Reached call limit
    #   status = 5    : Any other failure
    # status = 100 * hesseStatus + 10 * minosStatus +  minuit2SummaryStatus
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
    frame.SetTitle("{category}_{higgsMass}_{processName}".format(category=category, higgsMass=variable["central"], processName=signal.mc.buildProcessName()))
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
    # initial values for each consecutive model will be derived from the 
    # previous mass point
    #
    imodel = 0
    prevSignal=None; prevModel=None; prevVariable=None
    parameters = []
    massPoints = []
    norms = []
    for (signal, model, variable) in tupleSignalModelVariable:
        fsdata = R.TFile(signal.pathToFile)
        frame = ws.var("x").frame()

        hsdata_name = category + "/" + variable["name"]
        if settings.useInputFileUF: 
            hsdata_name = "signal_histos/" + category + "_" + signal.mc.uflabel

        hsdata = fsdata.Get(hsdata_name)
        if not settings.useInputFileUF:
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
        pdf = model.build(ws, category=category)
        #
        # Fit twice???
        # Andrea has it like that??? May be second time has better initial values???
        #
        r = pdf.fitTo(rsdata, R.RooFit.Save(),
            R.RooFit.Range(variable["fitmin"], variable["fitmax"]),
            R.RooFit.SumW2Error(R.kTRUE))
        prevSignal = signal
        prevModel = model
        prevVariable = variable
        imodel +=1
        massPoints.append(variable["central"])

        # plot this model together with signal histogram
        rsdata.plotOn(frame)
        pdf.plotOn(frame, R.RooFit.LineColor(R.kBlue))

        # draw the frame and save the canvas
        frame.SetTitle("{category}_{higgsMass}_{processName}".format(category=category, higgsMass=variable["central"], processName=signal.mc.buildProcessName()))
        frame.Draw()
        fileName = "signalFit__{category}__{higgsMass}__{processName}__{modelId}__{mods}.png".format(
            category=category, higgsMass=variable["central"], processName=signal.mc.buildProcessName(),
            modelId=model.modelId, mods="default")
        canvas.SaveAs(os.path.join(pathToDir, fileName))

        # exctract the parameters
        lParameters = model.getParameterValuesAsList(ws)
        parameters.append(lParameters)
        print "*"*90 + "\n"
        print "*"*90 + "\n"
        print lParameters
        print parameters
        r.Print("v")

#        pdf.plotOn(frame, R.RooFit.LineColor(R.kBlue))
        imodel+=1

    #
    # build the Splines
    # create the spline for normalization
    # have to transpose the matrix of parameters first
    #
    frame = ws.var("x").frame()
    paramsTransposed = aux.transpose(parameters)
    print "*"*90 + "\n"
    print "*"*90 + "\n"
    print "*"*90 + "\n"
    print "*"*90 + "\n"
    print parameters
    print paramsTransposed
    finalmodel = prevModel.__class__()
    finalmodel.initialize(aux.buildSignalModelName(finalmodel, 
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
    frame.SetTitle("{category}_{processName}".format(category=category, processName=signal.mc.buildProcessName()))
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
    # initial values for each consecutive model will be derived from the 
    # previous mass point
    #
    imodel = 0
    prevSignal=None; prevModel=None; prevVariable=None
    for (signal, model, variable) in tupleSignalModelVariable:
        fsdata = R.TFile(signal.pathToFile)

        hsdata_name = category + "/" + variable["name"]
        if settings.useInputFileUF: 
            hsdata_name = "signal_histos/" + category + "_" + signal.mc.uflabel

        hsdata = fsdata.Get(hsdata_name)
        if not settings.useInputFileUF:
            hsdata.Scale(1/signal.getWeight())
        rsdata = aux.buildRooHist(ws, hsdata)
        model.initialize(aux.buildSignalModelName(model, 
            settings.names2RepsToUse[category],
            signal.mc.buildProcessName(), variable["central"]))
        if imodel>0:
            model.setInitialValuesFromModel(prevModel, ws, 
                massDifference=(variable["central"] - prevVariable["central"]))
        model.createParameters(ws)
        pdf = model.build(ws, category=category)
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
    frame.SetTitle("{category}_{processName}".format(category=category, processName=signal.mc.buildProcessName()))
    frame.Draw()
    fileName = "signalFitInterpolation__{category}__{processName}__{modelId}__{mods}.png".format(category=category, processName=signal.mc.buildProcessName(), modelId=model.modelId, mods="")
    canvas.SaveAs(os.path.join(pathToDir, fileName))

def ftestPerFamily((category, variable), ws, data, familyModelGroup, settings, **wargs):
    #
    # initialize the values from wargs
    #
    pathToDir = "/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]
    unblind = False
    if "unblind" in wargs:
        unblind = wargs["unblind"]

    #
    # canvas 
    #
    canvas = R.TCanvas("c1", "c1", 1000, 800)
    canvas.cd()
    frame = ws.var("x").frame()
    legend = R.TLegend(0.65, 0.6, 0.9, 0.9)

    #
    # Get the data histogram
    #
    fdata = R.TFile(data.pathToFile)

    hdata_name = category + "/" + variable["name"]
    if settings.useInputFileUF: 
        hdata_name = "net_histos/"+category+"_Net_Data"

    hdata = fdata.Get(hdata_name)
    hdata_blind = hdata.Clone("Blind")
    aux.blindHistogram(hdata_blind, 120, 130)
    rdata = aux.buildRooHist(ws, hdata)
    rdata_blind = aux.buildRooHist(ws, hdata_blind)
    norm = rdata.sumEntries()
    print "Integral = %f" % hdata.Integral()
    print "SumEntries = %f" % rdata.sumEntries()

    #
    # perform the actual test
    #
    alpha = 0.05; prevNLL = -1.0; prevModel=None; prevDegree=0
    modelToBeUsed = None
    prob=0
    pdfs = {}
    if not unblind:
        rdata_blind.plotOn(frame)
    else:
        rdata.plotOn(frame)
    values = []
    fTestResults = []
    found = False
    for model in familyModelGroup.models:
        modelName = aux.buildBackgroundModelName(model, 
            settings.names2RepsToUse[category])
        model.initialize(modelName)
        model.createParameters(ws)
        pdfs[modelName] = model.build(ws, category=category)
        r = pdfs[modelName].fitTo(rdata,
            R.RooFit.Minimizer("Minuit2", "minimize"),
            R.RooFit.Save(1))
        pdfs[modelName].plotOn(frame, R.RooFit.Name(model.modelId),
            R.RooFit.LineColor(model.color), R.RooFit.Normalization(norm, 
                    R.RooAbsReal.NumEvent))

        # compute the Chi2 and the probability to which that value corresponds to 
        NLL = r.minNll()
        chi2 = -2.0 * (NLL - prevNLL)
        if chi2<0. and model.degree>1: 
            chi2 = 0.
        if prevModel is not None:
            prob = R.TMath.Prob(chi2, model.getNDF() - prevModel.getNDF())
            print "probability = %f\n" % prob
        else:
            prob = 0.
        #
        # (1 - prob) < 95% => we are (1 - prob) confident in our current model of 
        # degree N to be rejected
        # We are looking for the first model of degree N in which we have less than 
        # 95% confidence to be reject
        #
        if prob >= alpha and not found:
            modelToBeUsed = prevModel
            found = True
        legend.AddEntry(frame.findObject(model.modelId), model.modelId + "  %.2f %.2f %.2f" % (prob, chi2, NLL), "l")
        values.append("{modelId},{prob},{chi2},{NLL}".format(modelId=model.modelId,
            prob=prob, chi2=chi2, NLL=NLL))
        fTestResults.append(prob)
        prevNLL = float(NLL)
        prevModel = model

    frame.SetTitle("{category}_{familyName}".format(category=category, familyName=familyModelGroup.name))
    frame.Draw()

    #
    # save the canvas
    #
    fileName = "ftest__{category}__{familyName}.png".format(
        category = category, familyName=familyModelGroup.name)
    legend.Draw()
    R.gPad.Modified()
    canvas.SaveAs(os.path.join(pathToDir, fileName))

    #
    # save the values
    #
    fileName = "ftest__{category}__{familyName}.csv".format(
        category = category, familyName=familyModelGroup.name)
    fff = open(os.path.join(pathToDir, fileName), "w")
    for line in values:
        fff.write(line + "\n")
    fff.close()

    #
    # close the ROOT file
    #
    fdata.Close()

    return modelToBeUsed, fTestResults

def plotFTestResults(fTestResults, **wargs):
    #
    # initialize the values from wargs
    #
    pathToDir = "/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]
    
    #
    # canvas 
    #
    canvas = R.TCanvas("c1", "c1", 1000, 800)
    canvas.cd()
    R.gStyle.SetOptStat(0)
    #legend = R.TLegend(0.65, 0.6, 0.9, 0.9)

    #
    # Plot Probability(family, Order)
    #
    for category in fTestResults:
        h = R.TH2D("probabilityBycategory__{category}".format(category=category), 
            "probabilityBycategory {category}".format(category=category),
            len(fTestResults[category].keys()), 0, len(fTestResults[category].keys()),
            10, 1, 11)
        binX = 1
        for groupName in fTestResults[category]:
            h.GetXaxis().SetBinLabel(binX, groupName)
            binX += 1
        binY=1
        for i in range(10):
            h.GetYaxis().SetBinLabel(binY, "%d" % binY)
            binY += 1
        for groupName in fTestResults[category]:
            values = fTestResults[category][groupName]
            order = 1
            for prob in values:
                if order>1:
                    h.Fill(groupName, "%d" % (order-1), float("%.2f" % (prob*100.)))
                order += 1
        h.Draw("TEXT")

        h.SetTitle("{category}".format(category=category))
        h.GetXaxis().SetTitle("Family")
        h.GetYaxis().SetTitle("Reference Order")
        R.gPad.Modified()
        fileName = "ftestresults__probability__{category}.png".format(category=category)
        canvas.SaveAs(os.path.join(pathToDir, fileName))

    #
    # Probability(Category, Order)
    #
    histos = {}
    binX = 1
    for category in fTestResults:
        for groupName in fTestResults[category]:
            if groupName not in histos:
                histos[groupName] = R.TH2D("probability{groupName}".format(groupName=groupName), "probability {groupName}".format(groupName=groupName), len(fTestResults.keys()),
                    0, len(fTestResults.keys()), 10, 1, 11)
                for i in range(10):
                    histos[groupName].GetYaxis().SetBinLabel(i+1, "%d" % (i+1))
            histos[groupName].GetXaxis().SetBinLabel(binX, category)
            values = fTestResults[category][groupName]
            order = 1
            for prob in values:
                if order>1:
                    histos[groupName].Fill(category, "%d" % (order-1), float("%.2f" % (prob*100.)))
                order += 1
        binX += 1
    for groupName in histos:
        histos[groupName].SetTitle("{category}".format(category=category))
        histos[groupName].Draw("TEXT")
        histos[groupName].GetXaxis().SetTitle("Category")
        histos[groupName].GetYaxis().SetTitle("Reference Order")
        R.gPad.Modified()
        fileName = "ftestresults__probability__{groupName}.png".format(groupName=groupName)
        canvas.SaveAs(os.path.join(pathToDir, fileName))

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
    withSystematics = False
    if "withSystematics" in wargs:
        withSystematics = wargs["withSystematics"]

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
    processNamesList = ["BKG"] + [aux.unpackSignalModelName(model.modelName)[-1]
        for model in signalModels]
    processNumbersList = ["%d" % (1 - i) for i in range(len(signalModels)+1)]
    rateString = ["1"] + ["%.2f" % data.jsonToUse.intlumi for i in range(len(signalModels))]
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
    # fake goes on signal.
    #
    fakeUncList = ["-" for i in range(len(signalModels))] + ["1.0001"]
    fakeUncString = "fake lnN {fakeUncList}".format(fakeUncList=" ".join(fakeUncList))
    content.append(fakeUncString)

    #
    # add pdf index
    #
    content.append("pdfindex_{category} discrete".format(category=settings.names2RepsToUse[category]))
    content.append(delimString)

    #
    # add the systematics
    #
    if withSystematics:
        # computed nuisances
        for uncname in settings.nuisances:
            values = settings.nuisances[uncname][settings.names2RepsToUse[category]]
            content.append("{uncname} lnN - {uncsPerProcessList}".format(
                uncname=uncname, uncsPerProcessList=" ".join(
                ["%s/%s" % (values[aux.unpackSignalModelName(model.modelName)[-1]][0],
                    values[aux.unpackSignalModelName(model.modelName)[-1]][1]) for model in signalModels])))

        # lumi/br/xsec
        lumistring = "lumi_13TeV lnN - {lll}".format(lll=" ".join([
            settings.nuisance_lumi for x in signalModels]))
        content.append(lumistring)
        brstring = "br_hmm lnN - {lll}".format(lll=" ".join([
            settings.nuisance_br for x in signalModels]))
        content.append(brstring)
        xsecgluglustring = "xsec_ggH lnN - {lll}".format(lll=" ".join([
            settings.nuisance_xsecs["GluGlu"] if "GluGlu" in model.modelName else "-"
            for model in signalModels]))
        xsecvbfstring = "xsec_qqH lnN - {lll}".format(lll=" ".join([
            settings.nuisance_xsecs["VBF"] if "VBF" in model.modelName else "-"
            for model in signalModels]))
        xsecwhstring = "xsec_WH lnN - {lll}".format(lll=" ".join([
            settings.nuisance_xsecs["WPlusH"] if "WPlusH" in model.modelName or "WMinusH" in model.modelName else "-"
            for model in signalModels]))
        xseczhstring = "xsec_ZH lnN - {lll}".format(lll=" ".join([
            settings.nuisance_xsecs["ZH"] if "ZH" in model.modelName else "-"
            for model in signalModels]))
        content.append(xsecgluglustring)
        content.append(xsecvbfstring)
        content.append(xsecwhstring)
        content.append(xseczhstring)

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
    fdata = R.TFile(data.pathToFile)

    hdata_name = category + "/" + variable["name"]
    if settings.useInputFileUF: 
        hdata_name = "net_histos/"+category+"_Net_Data"

    hdata = fdata.Get(hdata_name)
    rdata = aux.buildRooHist(ws, hdata)
    norm = rdata.sumEntries()

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
    ws.factory("multipdf_{category}_norm[{central}, {minval}, {maxval}]".format(category=settings.names2RepsToUse[category], central=norm, minval=norm/2.0, maxval=norm*2.0))
    getattr(ws, "import")(ccc, R.RooFit.RecycleConflictNodes())
    getattr(ws, "import")(multipdf, R.RooFit.RecycleConflictNodes())
    ws.Print("v")

def backgroundFits((category, variable), ws, data, models, settings, **wargs):
    R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
    #
    # initialize the values from wargs
    #
    pathToDir = "/tmp"
    if "pathToDir" in wargs:
        pathToDir = wargs["pathToDir"]
    groupName = "someGroup"
    if "groupName" in wargs:
        groupName = wargs["groupName"]
    unblind = False
    if "unblind" in wargs:
        unblind = wargs["unblind"]

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

    hdata_name = category + "/" + variable["name"]
    if settings.useInputFileUF: 
        hdata_name = "net_histos/"+category+"_Net_Data"

    hdata = fdata.Get(hdata_name)
    hdata_blind = hdata.Clone("Blind")
    aux.blindHistogram(hdata_blind, 120, 130)
    rdata = aux.buildRooHist(ws, hdata)
    rdata.SetTitle(category)
    rdata_blind = aux.buildRooHist(ws, hdata_blind)
    norm = rdata.sumEntries()
    print "Integral = %f" % hdata.Integral()
    print "SumEntries = %f" % rdata.sumEntries()
    
    #
    # iterate thru all the models/fit/plot
    #
    counter = 0
    pdfs = {}
    if not unblind:
        rdata_blind.plotOn(frame)
    else:
        rdata.plotOn(frame)
#    rdata.plotOn(frame)
    for model in models:
        modelName = aux.buildBackgroundModelName(model, settings.names2RepsToUse[category])
        model.initialize(modelName)
        model.createParameters(ws)
        pdfs[modelName] = model.build(ws, category=category)
        r = pdfs[modelName].fitTo(rdata, R.RooFit.Save())
        pdfs[modelName].plotOn(frame, R.RooFit.Name(model.modelId), 
            R.RooFit.LineColor(model.color), R.RooFit.Normalization(norm, R.RooAbsReal.NumEvent))
#        pdfs[modelName].plotOn(frame, R.RooFit.Name(model.modelId), 
#            R.RooFit.LineColor(model.color))
        legend.AddEntry(frame.findObject(model.modelId), model.modelId, "l")
        print model.modelId
    frame.SetTitle("{category}_{groupName}".format(category=category, groupName=groupName))
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
