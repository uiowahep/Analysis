#!/usr/bin/python

import argparse
import os, sys
import definitions as defs
from Configuration.higgs.Iowa_settings import *
from Modeling.higgs2.aux import mkdir
import ROOT as R
R.gROOT.SetBatch(R.kTRUE)

parser = argparse.ArgumentParser(description="Post Combine: generate various plots for limits/fits; Generate tables in Latex")
parser.add_argument("--what", type=str,
    default="plotLimits", help="What you want to run: ")
parser.add_argument("--categoriesToSkip", type=str, nargs="*",
    default=[],
    help="Categories that should be skipped")
parser.add_argument("--massPoints", type=int, nargs="+",
    help="Mass Points to be used for limits/fits/etc... plotting")
parser.add_argument('--mode', type=str, 
    default='Iowa', help='Run in Iowa, UF_AWB, or UF_AMC mode')
parser.add_argument("--signalModel", type=str,
    default="SingleGaus", help="Name of the Signal Model to be used")
parser.add_argument("--outDirName", type=str,
    default="test", help="Directory Name that has been created in the .../combineoutput/$jobLabel/ folder where all the results of running combine went to. Directory Name that will be created in .../{limits | fits | ...}/$jobLabel/ folder where all the results/plots/tables will go to")
parser.add_argument('--unblind', action='store_true', default=False, help='True will be blinding mass region. For limits observed limit values will not be plotted')
parser.add_argument("--nbackgrounds", type=int,
    default=1, help="Number of background functions in the MultiPdf. TODO: This should be extracted from workspaces in principle")

args = parser.parse_args()

def listFilesByMass(mass, head, tail):
    import glob
    mass = str(mass)
    regname = "{head}*__{mass}__{signalModel}.{tail}.mH{mass}.root".format(
        head=head, mass=mass, signalModel=args.signalModel, tail=tail)
    pathFileNames = glob.glob(os.path.join(combineoutputDir, args.outDirName, regname))
    return pathFileNames

def listFilesByCategory(category, head, tail):
    import glob
    regname = "{head}{category}__*__{signalModel}.{tail}.*.root".format(
        head=head, category=category, signalModel=args.signalModel, tail=tail)
    pathFileNames = glob.glob(os.path.join(combineoutputDir, args.outDirName, regname))
    return pathFileNames

def plotLimitsByCategory(category):
    print "\n"
    print "plotLimitsByCategory..."
    print "\n"
    categoryRep = category if category in combinationsToUse else names2RepsToUse[category]
    head = "higgsCombine"
    tail = "Asymptotic"
    fileName = "{head}{category}__{mass}__{signalModel}.{tail}.mH{mass}.root"
    limitMap = {quantiles2Reps[quantile] : [] for quantile in quantiles2Reps}
    #
    # accumulate the limit values for various quantiles 
    # over all mass points
    #
    for mass in args.massPoints:
        fullPath = os.path.join(combineoutputDir, args.outDirName,
            fileName.format(head=head, category=categoryRep,
            signalModel=args.signalModel, tail=tail, mass=mass))
        f = R.TFile(fullPath)
        tree = f.Get("limit")
        nEntries = tree.GetEntries()
        for i in range(nEntries):
            tree.GetEntry(i)
            q = float("%.3f" % tree.quantileExpected)
            rep = quantiles2Reps[q]
            limitMap[rep].append(tree.limit)
    
    #
    #  convert all python lists to array.array
    #
    from array import array
    rexpected = array("f", limitMap["expected"])
    expectedstr = ["%.3f (exp.)" % x for x in limitMap["expected"]]
    robserved = array("f", limitMap["observed"])
    rexpectedm1s = array("f", ((limitMap["expected"][i] - limitMap["m1sigma"][i]) 
        for i in range(len(limitMap["expected"]))))
    rexpectedm2s = array("f", ((limitMap["expected"][i] - limitMap["m2sigma"][i]) 
        for i in range(len(limitMap["expected"]))))
    rexpectedp1s = array("f", ((limitMap["p1sigma"][i] - limitMap["expected"][i]) 
        for i in range(len(limitMap["expected"]))))
    rexpectedp2s = array("f", ((limitMap["p2sigma"][i] - limitMap["expected"][i]) 
        for i in range(len(limitMap["expected"]))))
    npoints = len(limitMap["expected"])
    rmass = array("f", args.massPoints)
    xlow = array("f", [0.2 for i in range(npoints)])
    xhigh = array("f", [0.2 for i in range(npoints)])
    zero = array("f", [0 for i in range(npoints)])
    
    #
    # Create the ROOT Graphs
    #
    R.gStyle.SetOptStat(0)
    graphExpected = R.TGraphAsymmErrors(npoints, rmass, rexpected, zero, zero, zero, zero)
    graph2Sigma = R.TGraphAsymmErrors(npoints, rmass, rexpected, xlow, xhigh, rexpectedm2s, rexpectedp2s)
    graph1Sigma = R.TGraphAsymmErrors(npoints, rmass, rexpected, xlow, xhigh, rexpectedm1s, rexpectedp1s)
    graphObserved = R.TGraphAsymmErrors(npoints, rmass, robserved, zero, zero, zero)

    #
    # Set the predraw stylee
    #
    graph2Sigma.SetFillColor(R.kOrange)
    graph1Sigma.SetFillColor(R.kGreen+1)
#    graph2Sigma.SetLineStyle(3)
#    graph1Sigma.SetLineStyle(3)
    graphExpected.SetMarkerColor(R.kBlack)
    graphExpected.SetName("Expected")
    graphExpected.SetLineStyle(7)
    graphExpected.SetLineColor(1)
    graphObserved.SetMarkerStyle(20)
    graphObserved.SetMarkerSize(0.8)
    graphObserved.SetLineColor(1)
    graphObserved.SetLineWidth(2)
#    graphObserved.SetLineStyle()
#    graphExpected.SetFillStyle(0)

    #
    # Canvas and Drawing
    #
    canvas = R.TCanvas("canvas", "canvas", 1000, 800)
    #canvas.SetLeftMargin(0.3)
    mg = R.TMultiGraph()
    mg.Add(graph2Sigma)
    mg.Add(graph1Sigma)
    mg.Add(graphExpected)
    if args.unblind:
        mg.Add(graphObserved)
    mg.Draw("APE3 L")
    
    #
    # Set post drawing styles
    #
    #mg.GetXaxis().SetRangeUser(0, 15)
    mg.SetTitle("{category}".format(category=category))
    mg.GetYaxis().SetTitle("95% CL limit on #sigma/#sigma_{SM} (h #rightarrow #mu#mu)")
    mg.GetYaxis().SetTitleOffset(1.0)
    mg.GetYaxis().SetTitleSize(0.04)
    mg.GetYaxis().CenterTitle(True)
    mg.GetYaxis().SetLabelSize(0.03)
    mg.GetYaxis().SetRangeUser(0, max(rexpected)*4)
#    mg.SetMaximum(npoints)
    mg.GetXaxis().SetRangeUser(120, 130)
    
    #
    # Dummy
    #
    dummy = R.TH1D("dummy", "dummy", 100, 120, 130)
    dummy.Draw("AXIS SAME")
    dummy.Draw("AXIS X+ Y+ SAME")
    dummy.Draw("AXIG SAME")

    #
    # Save the Canvas
    #
    canvas.SaveAs(os.path.join(
        limitsDir, args.outDirName, "limitsByCategory__{category}__{signalModel}.png".format(
        category=category, signalModel=args.signalModel)))

def plotLimitsByMass(mass):
    print "\n"
    print "plotLimitsByMass..."
    print "\n"
    mass = str(mass)
    head = "higgsCombine"
    tail = "Asymptotic"
    fileName = "{head}{category}__{mass}__{signalModel}.{tail}.mH{mass}.root"
    limitMap = {quantiles2Reps[quantile] : [] for quantile in quantiles2Reps}
    titlesToUse = []
    catscombsToUse = combinationsToUse.keys() + reps2NamesToUse.keys()
    for category in catscombsToUse:
        if category in args.categoriesToSkip:
            continue
        fullPath = os.path.join(combineoutputDir, args.outDirName, fileName.format(
            head=head, category=category, mass=mass, signalModel=args.signalModel,
            tail=tail))
        # get the file and tree
        f = R.TFile(fullPath)
        tree = f.Get("limit") 
        nEntries = tree.GetEntries()
        for i in range(nEntries):
            tree.GetEntry(i)
            # shorten the float as it seems to be causing troubles
            q = float("%.3f" % tree.quantileExpected)
            # convert to a string representation
            rep = quantiles2Reps[q]
            limitMap[rep].append(tree.limit)
        titlesToUse.append(category if category in combinationsToUse else reps2NamesToUse[category])

    #
    # convert all python lists to array.array
    #
    from array import array
    rexpected = array("f", limitMap["expected"])
    expectedstr = ["%.3f (exp.)" % x for x in limitMap["expected"]]
    rexpectedm1s = array("f", ((limitMap["expected"][i] - limitMap["m1sigma"][i]) 
        for i in range(len(limitMap["expected"]))))
    rexpectedm2s = array("f", ((limitMap["expected"][i] - limitMap["m2sigma"][i]) 
        for i in range(len(limitMap["expected"]))))
    rexpectedp1s = array("f", ((limitMap["p1sigma"][i] - limitMap["expected"][i]) 
        for i in range(len(limitMap["expected"]))))
    rexpectedp2s = array("f", ((limitMap["p2sigma"][i] - limitMap["expected"][i]) 
        for i in range(len(limitMap["expected"]))))
    npoints = len(limitMap["expected"])
    y = array("f", [npoints - i - 0.5 for i in range(npoints)])
    ylow = array("f", [0.2 for i in range(npoints)])
    yhigh = array("f", [0.2 for i in range(npoints)])
    zero = array("f", [0 for i in range(npoints)])

    #
    # Create the ROOT Graphs
    #
    R.gStyle.SetOptStat(0)
    graphExpected = R.TGraphAsymmErrors(npoints, rexpected, y, zero, zero, zero, zero)
    graph2Sigma = R.TGraphAsymmErrors(npoints, rexpected, y, rexpectedm2s, rexpectedp2s,
        ylow, yhigh)
    graph1Sigma = R.TGraphAsymmErrors(npoints, rexpected, y, rexpectedm1s, rexpectedp1s,
        ylow, yhigh)

    #
    # Set the predraw stylee
    #
    graph2Sigma.SetFillColor(R.kYellow)
    graph1Sigma.SetFillColor(R.kGreen)
    graphExpected.SetMarkerColor(R.kBlack)
    graphExpected.SetMarkerSize(2)
    graphExpected.SetMarkerStyle(5)
    graphExpected.SetName("Expected")
    graphExpected.SetLineStyle(3)

    #
    # Canvas and Drawing
    #
    canvas = R.TCanvas("canvas", "canvas", 1000, 800)
    canvas.SetLeftMargin(0.3)
    mg = R.TMultiGraph()
    mg.Add(graph2Sigma)
    mg.Add(graph1Sigma)
    mg.Add(graphExpected)
    mg.Draw("AP2")

    #
    # Set post drawing styles
    #
    #mg.GetXaxis().SetRangeUser(0, 15)
    mg.SetTitle("mH {mass}".format(mass=mass))
    mg.GetXaxis().SetTitle("95% CL limit on #sigma/#sigma_{SM} (h #rightarrow #mu#mu)")
    mg.GetXaxis().SetTitleOffset(1.0)
    mg.GetXaxis().SetTitleSize(0.04)
    mg.GetXaxis().CenterTitle(True)
    mg.GetXaxis().SetLabelSize(0.03)
    mg.GetYaxis().SetRangeUser(0, npoints)
    mg.SetMaximum(npoints)
    mg.GetYaxis().SetNdivisions(npoints*100)
    mg.GetXaxis().SetLabelSize(0.03)

    #
    # Draw the labels
    #
    latex = R.TLatex()
    latex.SetTextSize(0.02)
    latex.SetTextAlign(31)
    latex2 = R.TLatex()
    latex2.SetTextSize(0.013)
    latex2.SetTextAlign(31)
    for i in range(npoints):
        title = titlesToUse[i]
        expLimit = expectedstr[i]
        titleIndex = -5
        expLimitIndex = -5
        latex.DrawLatex(titleIndex, npoints - i - 0.55, title)
        latex2.DrawLatex(expLimitIndex, npoints - i - 0.92, expLimit)

    #
    # Save the Canvas
    #
    canvas.SaveAs(os.path.join(
        limitsDir, args.outDirName, "limitsByMass__{mass}__{signalModel}.png".format(
        mass=mass, signalModel=args.signalModel)))

def plotLimits():
    mkdir(os.path.join(limitsDir, args.outDirName))
    for mass in args.massPoints:
        plotLimitsByMass(mass)
    for category in categoriesToUse:
        if names2RepsToUse[category] in args.categoriesToSkip:
            continue
        plotLimitsByCategory(category)
    for combination in combinationsToUse:
        if combination in args.categoriesToSkip:
            continue
        plotLimitsByCategory(combination)

def biasScan():
    biasScanResultsDir = os.path.join(biasScanDir, args.outDirName)
    combineoutputPathDir = os.path.join(combineoutputDir, args.outDirName)
    mkdir(biasScanResultsDir)
    for category in categoriesToUse:
        if names2RepsToUse[category] in args.categoriesToSkip:
            continue
        for massPoint in args.massPoints:
            for iref in range(args.nbackgrounds):
                for icurrent in range(args.nbackgrounds):
                    canvas = R.TCanvas("c1", "c1", 1000, 600)
                    try:
                        fileName = "mlfit{category}__{mass}__{iref}__{icurrent}__{signalModel}.root".format(category=names2RepsToUse[category], mass=massPoint, iref=iref, icurrent=icurrent, signalModel=args.signalModel)
                        f = R.TFile(os.path.join(combineoutputPathDir, fileName))
                        tree = f.Get("tree_fit_sb")
                        tree.Draw("(mu-1)/muErr>>h(200, -10,10)")

                        # get the histogram and perform some manipulations
                        hist = R.gFile.Get("h")
                        import array
                        probs = array.array("d", [0.5])
                        quantiles = array.array("d", [0])
                        hist.GetQuantiles(1, quantiles, probs)

                        latex = R.TLatex()
                        latex.SetNDC()
                        latex.SetTextSize(0.02)
                        latex.SetTextAlign(13) # align at top
                        latex.SetTextSize(0.03)
                        latex.DrawLatex(0.2, 0.8, "Median = " + str(quantiles[0]))

                        cfileName = "pull__{category}__{mass}__{iref}__{icurrent}__{signalModel}.png".format(category=names2RepsToUse[category], mass=massPoint, iref=iref, icurrent=icurrent, signalModel=args.signalModel)
                        canvas.SaveAs(os.path.join(biasScanResultsDir, cfileName))
                    except:
                        print "There was a problem with file: {file}".format(file=fileName)

def fits():
    pass

def main():
    import sys
    what = getattr(sys.modules[__name__], args.what)
    what()

if __name__=="__main__":
    main()
