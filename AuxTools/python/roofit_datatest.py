import ROOT as R

f = R.TFile("/Users/vk/software/Analysis/build/process_2015Prompt.root")
h = f.Get("DiMuonMass")

x = R.RooRealVar("mass", "mass", 110, 160)
rdata = R.RooDataHist("roohist", "roohist", R.RooArgList(x), h)

l = R.RooRealVar("l", "l", 0, 1000)
bkg = R.RooExponential("bkg", "bkg", x, l)

mean = R.RooRealVar("mean", "mean", 60, 140)
width = R.RooRealVar("width", "width", 0, 100)
bkg1 = R.RooBreitWigner("bkg1", "bkg1", x, mean, width)
#model = R.RooAddPdf("model", "model", R.RooArgList(bkg))
#model = bkg

#model.fitTo(rdata, R.RooFit.Extended(R.kTRUE))
bkg1.fitTo(rdata)

xframe = x.frame()
rdata.plotOn(xframe)
bkg1.plotOn(xframe)
#model.plotOn(xframe)
xframe.Draw()
