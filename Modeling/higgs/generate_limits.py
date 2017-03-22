import ROOT as R
import os, sys, subprocess, glob
import models
from aux import *
import argparse
import AuxTools.python.common as CM

R.gROOT.SetBatch(R.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose debugging output')
parser.add_argument('-m', '--mode', type=str, default='Iowa', help='Run in Iowa, UF_AWB, or UF_AMC mode')
args = parser.parse_args()

if (args.mode == 'Iowa'):
    from Modeling.higgs.categories import *
    import AuxTools.python.Iowa_settings as SET
if (args.mode == 'UF_AWB'):
    from Modeling.higgs.categories_UF_AWB import *
    import AuxTools.python.UF_AWB_settings as SET
if (args.mode == 'UF_AMC'):
    from Modeling.higgs.categories_UF_AMC import *
    import AuxTools.python.UF_AMC_settings as SET

pus       = SET.pileups
smodels   = SET.sig_models
smodes    = SET.sig_modes
bmodel    = SET.bkg_models[0]
bmodelklass = getattr(models, bmodel["name"])
bmodel = bmodelklass(category="", **bmodel["aux"])
bmodelId = bmodel.getModelId()

type_mod  = 'analytic' if SET.analytic else 'templates'
mass      = SET.sig_M[0]
quantiles = [-1.0, 0.16, 0.84, 0.025, 0.975, 0.5]

tail = "Asymptotic.mH%s.root" % mass
head = "higgsCombine"

#categoriesToInclude = run1CategoriesForCombination
categoriesToInclude = combinationsRun1


def extractCategory(s):
    s = s.split("/")
    s = s[len(s)-1]
    s = s[len(head):-len(tail)-1]
    s = s.split("__")
    if s[2]=="NoVBFTight": return s[1]+s[2]
    
    return s[1]

def createLegend(n):
    top = 0.99
    left = 0.77
    legend = R.TLegend(left, top - n*0.1, left+0.23, top-n*.04)
    legend = R.TLegend(left, top - n*0.05, left+0.2, top)
    legend.SetBorderSize(0);
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    return legend

def main():
    for pu in pus:
        if ('UF' in args.mode):
            combineOutputDir = SET.combine_dir
            limitsDir = SET.limits_dir
        else:
            combineOutputDir = SET.combine_dir+"/"+pu
            limitsDir = SET.limits_dir+"/"+pu

        CM.mkdir(limitsDir)
        if type_mod == "analytic":
            for smodel in smodels:
                for smode in smodes:
                    filelist = glob.glob(combineOutputDir+"/*%s*%s*%s*%s*Asymptotic*.root" % (type_mod, bmodelId, smode, smodel))
                    print "generating limit for %s %s %s" % (smodel, smode, str(filelist))
                    generateLimit(filelist, combineOutputDir=combineOutputDir,
                        smode=smode, smodel=smodel, limitsDir=limitsDir)
        else:
            filelist = glob.glob(combineOutputDir+"/*%s*Asymptotic*.root" % type_mod)
            generateLimit(filelist, combineOutputDir=combineOutputDir)

                

def generateLimit(filelist, **wargs):
    combineOutputDir = wargs["combineOutputDir"]
    limitsDir = wargs["limitsDir"]
    if type_mod=="analytic":
        smode = wargs["smode"]
        smodel = wargs["smodel"]

    limitMap = {}
    for s in filelist:
        category = extractCategory(s)
	print category
        if category not in categoriesToInclude:
            continue
        print category

        try:
            f = R.TFile(s, "r")
            t = f.Get("limit")
            n = t.GetEntries()
            limitSubMap = {}
            if n<6:
                raise Exception("Wrong number of Quantiles")
            for i in range(n):
                t.GetEntry(i)
                q = float("%.3f" % t.quantileExpected)
                limitSubMap[q] = t.limit
        except Exception as exc:
            print exc.args
            continue
        limitMap[category] = limitSubMap

    expected = []; comb_expected = [] 
    y = []
    expectedm1s = []; expectedp1s = []; comb_expectedm1s = []; comb_expectedp1s = []
    expectedm2s = []; expectedp2s = []; comb_expectedm2s = []; comb_expectedp2s = []
    titles = []; comb_titles = []
    observed = []; comb_observed = []

    counter = 0
    map_explimits = {}
    for key in limitMap:
        map_explimits[key] = limitMap[key][0.5]
        if "Combination" in key:
            comb_expected.append(limitMap[key][0.5])
            comb_observed.append(limitMap[key][-1.0])
            comb_expectedm1s.append(limitMap[key][0.16])
            comb_expectedp1s.append(limitMap[key][0.84])
            comb_expectedm2s.append(limitMap[key][0.025])
            comb_expectedp2s.append(limitMap[key][0.975])
            comb_titles.append(key)
            counter+=1
            continue
        expected.append(limitMap[key][0.5])
        observed.append(limitMap[key][-1.0])
        expectedm1s.append(limitMap[key][0.16])
        expectedp1s.append(limitMap[key][0.84])
        expectedm2s.append(limitMap[key][0.025])
        expectedp2s.append(limitMap[key][0.975])
        titles.append(key)
        counter+=1


    expected.extend(comb_expected)
    observed.extend(comb_observed)
    expectedm1s.extend(comb_expectedm1s)
    expectedp1s.extend(comb_expectedp1s)
    expectedm2s.extend(comb_expectedm2s)
    expectedp2s.extend(comb_expectedp2s)
    titles.extend(comb_titles)

#
#key = "2jets"
#expected.append(limitMap[key][0.5])
#observed.append(limitMap[key][-1.0])
#expectedm1s.append(limitMap[key][0.16])
#expectedp1s.append(limitMap[key][0.84])
#expectedm2s.append(limitMap[key][0.025])
#expectedp2s.append(limitMap[key][0.975])
#titles.append(key)
#counter+=1

    y = [counter - i - 0.5 for i in range(counter)]
    yl = [0.2 for i in range(counter)]
    yh = [0.2 for i in range(counter)]
    zero = [0 for i in range(counter)]

#   use the limits
    from array import array
    rexpected = array("f", expected)
    expectedstr = ["%.3f (exp.)" % x for x in expected]
    robserved = array("f", observed)
    rexpectedm1s = array("f", ((expected[i]-expectedm1s[i]) for i in range(len(expected))))
    rexpectedp1s = array("f", ((expectedp1s[i]-expected[i]) for i in range(len(expected))))
    rexpectedm2s = array("f", ((expected[i]-expectedm2s[i]) for i in range(len(expected))))
    rexpectedp2s = array("f", ((expectedp2s[i]-expected[i]) for i in range(len(expected))))
    ry = array("f", y)
    ryl = array("f", yl)
    ryh = array("f", yh)
    rzero = array("f", zero)

    print counter
    for i in range(counter):
        print; print;
        print titles[i]
        print rexpected[i]
        print rexpectedm1s[i], rexpectedp1s[i]
        print rexpectedm2s[i], rexpectedp2s[i]

    R.gStyle.SetOptStat(0)
    xmin = 0
    xmax = 5
    n = counter
    gr2s = R.TGraphAsymmErrors(n, rexpected, ry, rexpectedm2s, rexpectedp2s, ryl, ryh)
    gr2s.SetFillColor(R.kYellow)
    gr1s = R.TGraphAsymmErrors(n, rexpected, ry, rexpectedm1s, rexpectedp1s,
        ryl, ryh)
    gr1s.SetFillColor(R.kGreen)
    gr = R.TGraphAsymmErrors(n, rexpected, ry, rzero, rzero, rzero, rzero)
    grobs = R.TGraphAsymmErrors(n, robserved, ry, rzero, rzero, rzero, rzero)
    gr.SetMarkerColor(R.kBlack)
    gr.SetMarkerSize(1.3)
    gr.SetMarkerStyle(5)
    gr.SetName("test")
    grobs.SetMarkerColor(R.kRed)
    grobs.SetMarkerSize(1.3)
    grobs.SetMarkerStyle(20)

    canvas = R.TCanvas("canvas", "", 0, 10, 1000, 800)
    canvas.SetLeftMargin(0.3)
    mg = R.TMultiGraph()
    mg.Add(gr2s)
    mg.Add(gr1s)
    mg.Add(gr)
    #mg.Add(grobs)
    mg.Draw("AP2")
    mg.GetXaxis().SetRangeUser(0, 15)

    if type_mod=="analytic":
        mg.SetTitle("mH%s %s" % (mass, smodel))
    else:
        mg.SetTitle("Mass Higgs %s" % mass)
    mg.GetXaxis().SetTitle("95% CL limit on #sigma/#sigma_{SM} (h #rightarrow #mu#mu)")
    mg.GetXaxis().SetTitleOffset(1.0)
    mg.GetXaxis().SetTitleSize(0.04)
    mg.GetXaxis().CenterTitle(True)
    mg.GetXaxis().SetLabelSize(0.03)
    #mg.GetXaxis().SetLimits(xmin, xmax)

    mg.GetYaxis().SetRangeUser(0, n)
    mg.SetMaximum(n)
    mg.GetYaxis().SetNdivisions(n*100)

    latex = R.TLatex()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(31)
    latex2 = R.TLatex()
    latex2.SetTextSize(0.04)
    latex2.SetTextAlign(31)
    for i in range(n):
        title = titles[i]
        expLimit = expectedstr[i]
        if type_mod=="analytic":
            titleIndex = 0
            expLimitIndex = 0
#            titleIndex = -20
#            expLimitIndex = -20
        else:
            titleIndex = -20
            expLimitIndex=-20
        latex.DrawLatex(titleIndex, n - i - 0.55, title)
        latex2.DrawLatex(expLimitIndex, n - i - 0.92, expLimit)

    legend = createLegend(3)
    legend.AddEntry(gr, "Expected", "p")
    legend.AddEntry(gr1s, "Expected #pm 1 #sigma", "f")
    legend.AddEntry(gr2s, "Expected #pm 2 #sigma", "f")
    #legend.AddEntry(grobs, "Observed", "p")
    legend.Draw("same")

    line = R.TLine()
    line.SetLineColor(R.kBlack)
    line.DrawLine(-180, 5, 350, 5)
    import json
    if type_mod=="analytic":
        canvas.SaveAs(limitsDir+"/limits__%s__%s__%s__%s__%s.png" % (
            type_mod, mass, bmodelId, smode, smodel))
        json.dump(map_explimits, open(limitsDir+"/explimits__%s__%s__%s__%s__%s.json" % (
            type_mod, mass, bmodelId, smode, smodel), "w"))
    else:
        canvas.SaveAs(limitsDir+"/limits__%s__%s.png" % (
            type_mod, mass))
        json.dump(map_explimits, open(limitsDir+"/explimits__%s__%s.json" % (
            type_mod, mass), "w"))

if __name__=="__main__":
    main()
