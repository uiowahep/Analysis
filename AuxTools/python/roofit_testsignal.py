from ROOT import *

f = TFile("/Users/vk/software/Analysis/files/fits_and_datacards/v0_20160824_1100/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22/71p3/shape__templates__ggFLoose.root")
h_VBF = f.Get("VBF")
h_Glu = f.Get("GluGlu")

ws = RooWorkspace("test")
ws.factory("x[125, 110, 160]")
x = ws.var("x")
ws.factory("mass1[125, 110, 160]")
ws.factory("mass2[123, 110, 160]")
ws.factory("width1[1.0, 0.1, 10]")
ws.factory('width2[5.0, 0.1, 10]')
ws.defineSet("obs", "x")
obs = ws.set("obs")
data_VBF = RooDataHist("VBF", "VBF", RooArgList(obs), h_VBF)
data_Glu = RooDataHist("Glu", "Glu", RooArgList(obs), h_Glu)
getattr(ws, "import")(data_VBF, RooCmdArg())

ws.factory("Gaussian::smodel1(x, mass1, width1)")
smodel1 = ws.pdf("smodel1")
ws.factory("Gaussian::smodel2(x, mass2, width2)")
smodel2 = ws.pdf("smodel2")

ws.factory("smodel1norm[1.0, 0, 100]")
ws.factory("smodel2norm[2.0, 0, 100]")
ws.factory("SUM::smodel(smodel1norm*smodel1, smodel2norm*smodel2)")
smodelsum = ws.pdf("smodel")

smodel = smodelsum
data = data_Glu
#smodel.fitTo(data, RooFit.Range(120, 130))
r = smodel.fitTo(data, RooFit.Save())

print "-"*40
r.Print()

xframe = x.frame()
data.plotOn(xframe)
smodel.plotOn(xframe)
smodel.Print("v")
xframe.Draw()

print "-"*40
print data_VBF.sumEntries()
print data_Glu.sumEntries()
r.Print()
#print r.floatParsFinal().find("mass2").getVal()
#print r.floatParsFinal().find("mass2").getError()
#print ws.var("mass2").getVal()
