#!/usr/bin/python

import argparse
import os, sys
import definitions as defs
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
parser.add_argument("--workspacesDirName", type=str,
    default="", help="Directory name that contains the datacards and workspaces")
parser.add_argument('--unblind', action='store_true', default=False, help='True will be blinding mass region. For limits observed limit values will not be plotted')
parser.add_argument("--modelsToSkip", type=str, nargs="*", default=[],
    help="Model Names that will be skipped for Bias Scan Evaluation")

args = parser.parse_args()

if args.mode == "Iowa":
    import Configuration.higgs.Iowa_settings as settings
    from Configuration.higgs.Iowa_settings import *
elif args.mode == "UF_AWB":
    import Configuration.higgs.UF_AWB_settings as settings
    from Configuration.higgs.UF_AWB_settings import *
elif args.mode == "UF_AWC":
    import Configuration.higgs.UF_AWC_settings as settings
    from Configuration .higgs.UF_AWC_settings import *


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
    workspacesDir = os.path.join(datacardsworkspacesDir, args.workspacesDirName)
    mkdir(biasScanResultsDir)
    hMeans = {}
    hMedians = {}
    for category in categoriesToUse:
        if names2RepsToUse[category] in args.categoriesToSkip:
            continue

        # extract the multi pdf
        workspaceFileName = "workspace__{category}__{signalModel}.root".format(
            category=names2RepsToUse[category], signalModel=args.signalModel)
        refWorkspaceFile = R.TFile(os.path.join(workspacesDir, workspaceFileName))
        higgsWorkspace = refWorkspaceFile.Get("higgs")
        multipdf = higgsWorkspace.pdf("multipdf_{category}".format(
            category=names2RepsToUse[category]))

        for massPoint in args.massPoints:
            hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)] = R.TH2D("Means_{category}_{mass}".format(category=category, mass=massPoint), "Means", multipdf.getNumPdfs()+1, 0, multipdf.getNumPdfs()+1,
                multipdf.getNumPdfs()+1, 0, multipdf.getNumPdfs()+1)
            hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)] = R.TH2D("Madians_{category}_{mass}".format(category=category, mass=massPoint), "Medians", multipdf.getNumPdfs()+1, 0, multipdf.getNumPdfs()+1,
                multipdf.getNumPdfs()+1, 0, multipdf.getNumPdfs()+1)

            for iref in range(multipdf.getNumPdfs()):
                refPdfName = multipdf.getPdf(iref).GetName()
                q = False
                for xxx in args.modelsToSkip:
                    if xxx==refPdfName.split("_")[0]:
                        q = True
                if q==True: continue
                for icurrent in range(multipdf.getNumPdfs()):
                    fitPdfName = multipdf.getPdf(icurrent).GetName()
                    q = False
                    for xxx in args.modelsToSkip:
                        if xxx==fitPdfName.split("_")[0]:
                            q = True
                    if q==True: continue
                    canvas = R.TCanvas("c1", "c1", 1000, 600)
                    try:
                        fileName = "mlfit{category}__{mass}__{iref}__{icurrent}__{signalModel}.root".format(category=names2RepsToUse[category], mass=massPoint, iref=iref, icurrent=icurrent, signalModel=args.signalModel)
                        f = R.TFile(os.path.join(combineoutputPathDir, fileName))
                        tree = f.Get("tree_fit_sb")
                        tree.Draw("(mu-1)/muErr>>h(800, -20,20)")

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

                        hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].Fill(iref, icurrent, hist.GetMean()*100)
                        hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].GetXaxis().SetBinLabel(iref+1, refPdfName)
                        hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].GetYaxis().SetBinLabel(icurrent+1, fitPdfName)
                        hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].Fill(iref, icurrent, quantiles[0]*100)
                        hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].GetXaxis().SetBinLabel(iref+1, refPdfName)
                        hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].GetYaxis().SetBinLabel(icurrent+1, fitPdfName)


                        cfileName = "pull__{category}__{mass}__{iref}__{icurrent}__{signalModel}.png".format(category=names2RepsToUse[category], mass=massPoint, iref=iref, icurrent=icurrent, signalModel=args.signalModel)
                        canvas.SaveAs(os.path.join(biasScanResultsDir, cfileName))
                    except Exception as exc:
                        print "There was a problem with file: {file}\n".format(file=fileName)
                        print type(exc)
                        print exc.args
                        print exc
                    finally:
                        f.Close()
            # plot the 2D
            hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].SetTitle("Mean (#mu_{fit} - #mu_{0})/#sigma #mu_{fit} (%%), %s, %d GeV" % (category, massPoint))
            hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].SetStats(0)
            hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].GetYaxis().SetTitle("Fit Model")
            hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].GetXaxis().SetTitle("Reference Model")
#            hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].GetXaxis().SetRangeUser(0,5)
#            hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].GetYaxis().SetRangeUser(0,5)
            hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].GetZaxis().SetRangeUser(-200,+200)
            hMeans["Mean_{category}_{mass}".format(category=category, mass=massPoint)].Draw("COLZTEXT")
            canvas.SaveAs(os.path.join(biasScanResultsDir, "pullMeans2D__{category}__{mass}__{signalModel}.png".format(
                category=names2RepsToUse[category], mass=massPoint, signalModel=args.signalModel)))
            hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].SetTitle("Median (#mu_{fit} - #mu_{0})/#sigma #mu_{fit} (%%), %s, %d GeV" % (category, massPoint))
            hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].SetStats(0)
            hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].GetYaxis().SetTitle("Fit Model")
            hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].GetXaxis().SetTitle("Reference Model")
#            hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].GetXaxis().SetRangeUser(0,5)
#            hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].GetYaxis().SetRangeUser(0,5)
            hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].GetZaxis().SetRangeUser(-200,+200)
            hMedians["Median_{category}_{mass}".format(category=category, mass=massPoint)].Draw("COLZTEXT")
            canvas.SaveAs(os.path.join(biasScanResultsDir, "pullMedians2D__{category}__{mass}__{signalModel}.png".format(
                category=names2RepsToUse[category], mass=massPoint, signalModel=args.signalModel)))

def fits():
    pass

def main():
    import sys
    what = getattr(sys.modules[__name__], args.what)
    what()

if __name__=="__main__":
    main()
