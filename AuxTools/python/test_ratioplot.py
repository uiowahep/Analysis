import ROOT as R

path = "/Users/vk/software/Analysis/files/limits_and_fits/v0_20160824_1100/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22/71p3"
filename = "shape__templates__NoCats.root"

name1 = "data_obs"
name2 = "DYJetsToLL"

f = R.TFile(path+"/"+filename)
h1 = f.Get(name1)
h2 = f.Get(name2)
stack = R.THStack("stack", "stack")
stack.Add(h2)

c = R.TCanvas("c1", "c1", 800, 600)
pad1 = R.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
pad1.SetBottomMargin(0)
pad1.Draw()
pad1.cd()

h1.Draw()
h2.Draw("same")
h1.GetXaxis().SetLabelSize(0)
axis = R.TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
axis.SetLabelFont(43)
axis.SetLabelSize(15)
axis.Draw()

c.cd()
pad2 = R.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0.05)
pad2.SetBottomMargin(0.2)
pad2.SetGridy()

hratio = h1.Clone()
hratio.SetTitle("")
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

sum = R.TH1D("sum", "sum", h2.GetNbinsX(),
    h2.GetBinLowEdge(1), h2.GetBinLowEdge(1) + h2.GetNbinsX()*h2.GetBinWidth(1))
sum.Add(h2)
hratio.Divide(sum)
hratio.SetStats(R.kFALSE)
hratio.Draw("ep")
hratio.SetMaximum(1.6)
hratio.SetMinimum(0.4)
hratio.SetMarkerStyle(20)
hratio.SetMarkerSize(0.5)
hratio.GetYaxis().SetLabelSize(0.1)
R.gPad.Modified()


