import ROOT as R

picpath = "/Users/vk/software/Analysis/docs/H2mu/pics/"
varName = "DiMuonMass"
year = 2016

datapath = "../"
mcnames = ["DY Jets", "tt Jets", "VBF H", "ggH2MuMu"]
dataname = str(year) + " Prompt Reco"
if year==2015:
    mcbgfiles = [
        datapath+"process_dyjetsToLL_PU2015Prompt.root",
        datapath+"process_ttJets_PU2015Prompt.root"
    ]
elif year==2016:
    mcbgfiles = [
        datapath+"process_dyjetsToLL_2016Prompt.root",
        datapath+"process_ttJets_2016Prompt.root"
    ]

mcsigfiles = [
        datapath+"process_vbfHToMuMu_PU2015Prompt.root",
        datapath+"process_ggHToMuMu_PU2015Prompt.root"
    ]
datafile = datapath+("process_%dPrompt.root"%year)

if year==2015:
    lumi = 2169
elif year==2016:
    lumi = 3990
mcbgxsec = [6025.2, 831.76]
mcsigxsec = [3.727*0.00022, 43.62*0.00022]
mcbgevsnumber = [16607060. ,12246093.]
colors = [R.kRed, R.kGreen]
sigcolors = [R.kBlue, R.kGray]
mcsigevsnumber = [248812., 250000.]

bgstack = R.THStack("bgstack", "")
mcbghists = []
c = R.TCanvas("c1", "c1", 600, 400)

# bg
counter = 0
f0 = R.TFile(mcbgfiles[counter])
h0 = f0.Get(varName)
h0.Scale(lumi*mcbgxsec[counter]/mcbgevsnumber[counter])
h0.SetFillColor(colors[counter])
if varName=="DiMuonMass":
    for i in range(h0.GetNbinsX()):
        if h0.GetBinCenter(i+1)>120 and h0.GetBinCenter(i+1)<130:
            h0.SetBinContent(i+1, 0)
bgstack.Add(h0)
#h0.Draw("hist")

counter = 1
f1 = R.TFile(mcbgfiles[counter])
h1 = f1.Get(varName)
h1.Scale(lumi*mcbgxsec[counter]/mcbgevsnumber[counter])
h1.SetFillColor(colors[counter])
if varName=="DiMuonMass":
    for i in range(h1.GetNbinsX()):
        if h1.GetBinCenter(i+1)>120 and h1.GetBinCenter(i+1)<130:
            h1.SetBinContent(i+1, 0)
bgstack.Add(h1)
#h1.Draw("hist")

# sig
counter = 0
f2 = R.TFile(mcsigfiles[counter])
h2 = f2.Get(varName)
h2.Scale(lumi*mcsigxsec[counter]/mcsigevsnumber[counter])
h2.SetLineColor(sigcolors[counter])

counter = 1
f3 = R.TFile(mcsigfiles[counter])
h3 = f3.Get(varName)
h3.Scale(lumi*mcsigxsec[counter]/mcsigevsnumber[counter])
h3.SetLineColor(sigcolors[counter])

#data
fdata = R.TFile(datafile)
hdata = fdata.Get(varName)
if varName=="DiMuonMass":
    for i in range(hdata.GetNbinsX()):
        if hdata.GetBinCenter(i+1)>120 and hdata.GetBinCenter(i+1)<130:
            hdata.SetBinContent(i+1, 0)

leg = R.TLegend(0.7, 0.7, 0.9, 0.9)
leg.SetHeader("Samples")

hdata.SetMarkerColor(R.kBlack)
hdata.SetMarkerStyle(20)
hdata.SetMarkerSize(0.5)
leg.AddEntry(hdata, dataname)
leg.AddEntry(h0, mcnames[0])
leg.AddEntry(h1, mcnames[1])
#leg.AddEntry(h2, mcnames[2])
#leg.AddEntry(h3, mcnames[3])

max1 = hdata.GetMaximum()
max2 = bgstack.GetMaximum()
if max1>max2:
    hdata.SetMaximum(max1)
    bgstack.SetMaximum(max1)
else:
    hdata.SetMaximum(max2)
    bgstack.SetMaximum(max2)

bgstack.Draw("hist")
hdata.Draw("same pe")
#h2.Draw("same hist")
#h3.Draw("same hist")
leg.Draw()
bgstack.GetXaxis().SetTitle(varName)
bgstack.GetYaxis().SetTitle("#Events")
R.gPad.Modified()
c.SaveAs(picpath+varName+("_%d.pdf"%year))
