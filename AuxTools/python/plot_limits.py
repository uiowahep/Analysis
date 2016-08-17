import ROOT as R
import os, sys, subprocess, glob

#R.gROOT.SetBatch(R.kTRUE)

limitsdir = "/Users/vk/software/Analysis/files/limits/dimuon-v1/"
filelist = glob.glob(limitsdir+"*")
quantiles = [-1.0, 0.16, 0.84, 0.025, 0.975, 0.5]

tail = "Asymptotic.mH125.root"
head = "higgsCombine"

c = R.TCanvas("c1", "c1", 600, 400)
pad = R.TPad("pad", "", 0, 0, 1, 1)
pad.SetGrid()
pad.Draw()
pad.cd()
h = pad.DrawFrame(-0.4, 0, 1.2, 12)

def extractCategory(s):
    s = s.split("/")
    s = s[len(s)-1]
    return s[len(head):-len(tail)-1]

limitMap = {}
for s in filelist:
    category = extractCategory(s)
    f = R.TFile(s, "r")
    t = f.Get("limit")
    n = t.GetEntries()
    limitSubMap = {}
    for i in range(n):
        t.GetEntry(i)
        q = float("%.3f" % t.quantileExpected)
        print q
        limitSubMap[q] = t.limit
    limitMap[category] = limitSubMap


print limitMap
expected = []
y = []
expectedm1s = []; expectedp1s = []
expectedm2s = []; expectedp2s = []
titles = []

counter = 0
for key in limitMap:
    print key
    expected.append(limitMap[key][0.5])
    expectedm1s.append(limitMap[key][0.16])
    expectedp1s.append(limitMap[key][0.84])
    expectedm2s.append(limitMap[key][0.025])
    expectedp2s.append(limitMap[key][0.975])
    titles.append(key)
    counter+=1

y = [i+0.5 for i in range(counter)]
yl = [0.1 for i in range(counter)]
yh = [0.2 for i in range(counter)]
zero = [0 for i in range(counter)]

#   use the limits
from array import array
rexpected = array("f", expected)
rexpectedm1s = array("f", ((expected[i]-expectedm1s[i]) for i in range(len(expected))))
rexpectedp1s = array("f", ((expectedp1s[i]-expected[i]) for i in range(len(expected))))
rexpectedm2s = array("f", ((expected[i]-expectedm2s[i]) for i in range(len(expected))))
rexpectedp2s = array("f", ((expectedp2s[i]-expected[i]) for i in range(len(expected))))
ry = array("f", y)
ryl = array("f", yl)
ryh = array("f", yh)
gr = R.TGraphAssymErrors(counter, rexpected, ry, zero, zero, zero, zero)
gr1s = R.TGraphAsymmErrors(counter, rexpected, ry,rexpectedm1s, rexpectedp1s, ryl, ryh)
gr2s = R.TGraphAsymmErrors(counter, rexpected, ry,rexpectedm2s, rexpectedp2s, ryl, ryh)

gr.SetMarkerColor(R.kBlack)
gr.SetMarkerSize(1.3)
gr.SetMarkerStyle(5)

canvas = R.TCanvas("c2", "", 0, 10, 610, 800)
mg = R.TMultiGraph()
mg.Add(gr2s)
mg.Add(gr1s)
mg.Add(gr)
mg.Draw("AP2")

mg.GetXaxis().SetTitle("X Title")
mg.GetXaxis().SetTitleOffset(0.8)
mg.GetXaxis().SetTitleSize(0.055)
mg.GetXaxis().CenterTitle(True)
mg.GetXaxis().SetLabelSize(0.045)
mg.GetXaxis().SetLimits(xmin, xmax)

mg.GetYaxis().SetRangeUser(0, counter)
mg.SetMaximum(counter)
mg.GetYaxis().SetNdivisions(counter + 100)

latex = R.TLatex()
latex2 = R.TLatex()
latex.SetTextSize(0.035)
latex2.SetTextSize(0.018)
for i in range(counter):
    title = titles[i]
    expLimit = expected[i]
    titleIndex = -0.62
    expLimitIndex = -0.6
    if (xmax==10):
        titleIndex = -1.25
        expLimitIndex = -1.2
    latex.DrawLatex(titleIndex, counter - i - 0.45, title)
