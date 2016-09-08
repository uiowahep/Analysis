import ROOT as R
import os, sys, subprocess, glob

#R.gROOT.SetBatch(R.kTRUE)

pu = sys.argv[1]

version = "v0p3_20160824_1100"
limitsdir = "/Users/vk/software/Analysis/files/limits_higsscombined_results/%s/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22/%s" % (version, pu)
pus = ["68", "69", "70", "71", "71p3", "72"]
type_modifier = "analytic"
filelist = glob.glob(limitsdir+"/*%s*Asymptotic*.root" % type_modifier)
quantiles = [-1.0, 0.16, 0.84, 0.025, 0.975, 0.5]

tail = "Asymptotic.mH125.root"
head = "higgsCombine"

def extractCategory(s):
    s = s.split("/")
    s = s[len(s)-1]
    s = s[len(head):-len(tail)-1]
    return s.split("__")[1]

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

limitMap = {}
for s in filelist:
    category = extractCategory(s)
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

expected = []
y = []
expectedm1s = []; expectedp1s = []
expectedm2s = []; expectedp2s = []
titles = []
observed = []

counter = 0
for key in limitMap:
    if key=="2jets":
        continue
    expected.append(limitMap[key][0.5])
    observed.append(limitMap[key][-1.0])
    expectedm1s.append(limitMap[key][0.16])
    expectedp1s.append(limitMap[key][0.84])
    expectedm2s.append(limitMap[key][0.025])
    expectedp2s.append(limitMap[key][0.975])
    titles.append(key)
    counter+=1
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

#for i in range(counter):
#    print; print;
#    print titles[i]
#    print rexpected[i]
#    print rexpectedm1s[i], rexpectedp1s[i]
#    print rexpectedm2s[i], rexpectedp2s[i]

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
grobs.SetMarkerColor(R.kRed)
grobs.SetMarkerSize(1.3)
grobs.SetMarkerStyle(20)

canvas = R.TCanvas("canvas", "", 0, 10, 800, 600)
canvas.SetLeftMargin(0.3)
mg = R.TMultiGraph()
mg.Add(gr2s)
mg.Add(gr1s)
mg.Add(gr)
#mg.Add(grobs)
mg.Draw("AP2")

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
latex.SetTextSize(0.035)
latex2 = R.TLatex()
latex2.SetTextSize(0.018)
for i in range(n):
    title = titles[i]
    expLimit = expectedstr[i]
    titleIndex = -140
    expLimitIndex = -125
    latex.DrawLatex(titleIndex, n- i - 0.55, title)
    latex2.DrawLatex(expLimitIndex, n - i - 0.9, expLimit)

legend = createLegend(3)
legend.AddEntry(gr, "Expected", "p")
legend.AddEntry(gr1s, "Expected #pm 1 #sigma", "f")
legend.AddEntry(gr2s, "Expected #pm 2 #sigma", "f")
#legend.AddEntry(grobs, "Observed", "p")
legend.Draw("same")

#line = R.TLine()
#line.SetLineColor(R.kBlack)
#line.DrawLine(xmin, 1, 100, 1)
canvas.SaveAs(limitsdir+"/limits__%s.pdf" % type_modifier)
