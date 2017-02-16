import ROOT as R
import os, sys, subprocess, glob

R.gROOT.SetBatch(R.kTRUE)

#version = "vR1_20170122_1326_TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
#version = "vR1_20170122_1326__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
#version = "vR2_20170125_1204__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkgs"
version = "vR1_20170122_1326__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__AndrewRequests2"
#limitsdir = "/Users/vk/software/Analysis/files/limits_higsscombined_results/%s/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22/%s" % (version, pu)
#pus = ["68", "69", "70", "71", "71p3", "72"]
pus = ["68", "69", "71", "72", "70", "71p3", "69p2"]
#pus = ["69"]
#pus = ["68", "69", "71", "72"]
smodels = ["SingleGaus", "DoubleGaus"]
#smodes = ["Combined", "Separate"]
smodes = ["Separate"]
type_modifier = "analytic"
bmodel = "ExpGaus"
mass = "125"
quantiles = [-1.0, 0.16, 0.84, 0.025, 0.975, 0.5]

tail = "Asymptotic.mH%s.root" % mass
head = "higgsCombine"

categoriesToInclude = ["2JetsggF", "01JetsTightNoEndcap", "01JetsTightEndcap",
    "01JetsLoose", "VBFTight", "TotalCombination"]

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
        folder = "80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__Mu24"
        limitsdir = "/Users/vk/software/Analysis/files/limits_higsscombined_results/%s/%s/%s" % (version, folder, pu)
        if type_modifier == "analytic":
            for smodel in smodels:
                for smode in smodes:
                    filelist = glob.glob(limitsdir+"/*%s*%s*%s*Asymptotic*.root" % (type_modifier, smode, smodel))
                    generateLimit(filelist, limitsdir=limitsdir,
                        smode=smode, smodel=smodel)
        else:
            filelist = glob.glob(limitsdir+"/*%s*Asymptotic*.root" % type_modifier)
            generateLimit(filelist, limitsdir=limitsdir)

                

def generateLimit(filelist, **wargs):
    limitsdir = wargs["limitsdir"]
    if type_modifier=="analytic":
        smode = wargs["smode"]
        smodel = wargs["smodel"]

    limitMap = {}
    for s in filelist:
        category = extractCategory(s)
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

    if type_modifier=="analytic":
        mg.SetTitle("mH%s %s %s" % (mass, smodel, smode))
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
        if type_modifier=="analytic":
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
    if type_modifier=="analytic":
        canvas.SaveAs(limitsdir+"/limits__%s__%s__%s__%s__%s.png" % (
            type_modifier, mass, bmodel, smode, smodel))
        json.dump(map_explimits, open(limitsdir+"/explimits__%s__%s__%s__%s__%s.json" % (
            type_modifier, mass, bmodel, smode, smodel), "w"))
    else:
        canvas.SaveAs(limitsdir+"/limits__%s__%s.png" % (
            type_modifier, mass))
        json.dump(map_explimits, open(limitsdir+"/explimits__%s__%s.json" % (
            type_modifier, mass), "w"))

if __name__=="__main__":
    main()
