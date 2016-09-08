from ROOT import *

filename2 = "/Users/vk/software/Analysis/files/test/shape__analytic__ggFLoose.root"
f1 = TFile(filename2)
ws1 = f1.Get("higgs")
data = ws1.data("data_obs")
data.Print()

filename = "/Users/vk/software/Analysis/files/limits_higsscombined_results/v0p3_20160824_1100/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22/68/mlfitanalytic__ggFLoose.root"
f = TFile(filename)

fit_b = f.Get("fit_b")
fit_b.Print("v")

const_parameters = fit_b.constPars()
list_const_pars = ["m1_g1_mass", "m1_g1_width", "m1_g2_mass", "m1_g2_width",
    "m2_g1_mass", "m2_g1_width", "m2_g2_mass", "m2_g2_width",
    "shapeSig_smodel1_ggFLoose__norm", "shapeSig_smodel2_ggFLoose__norm",
    "smodel1_coef", "smodel2_coef"]
floating_parameters = fit_b.floatParsFinal()
list_floating_pars = ["a1", "a2", "shapeBkg_bmodel_ggFLoose__norm"]

ws = RooWorkspace("test")
for c in list_const_pars:
    getattr(ws, "import")(const_parameters.find(c))
for ff in list_floating_pars:
    getattr(ws, "import")(floating_parameters.find(ff))

ws.factory("x[125.0, %f, %f]" % (110, 160))
ws.factory('expr::f("-(a1*(x/100)+a2*(x/100)^2)",a1,a2,x)')
ws.factory('Exponential::bmodel(f, 1)')
bmodel = ws.pdf("bmodel")
x = ws.var("x")

imc = 1
ws.factory("Gaussian::smodel%d_g1(x, m%d_g1_mass, m%d_g1_width)" % (imc, imc, imc))
ws.factory("Gaussian::smodel%d_g2(x, m%d_g2_mass, m%d_g2_width)" % (imc, imc, imc))
ws.factory("SUM::smodel%d(smodel%d_coef*smodel%d_g1, smodel%d_g2)" % (imc, imc, imc, imc))
imc = 2
ws.factory("Gaussian::smodel%d_g1(x, m%d_g1_mass, m%d_g1_width)" % (imc, imc, imc))
ws.factory("Gaussian::smodel%d_g2(x, m%d_g2_mass, m%d_g2_width)" % (imc, imc, imc))
ws.factory("SUM::smodel%d(smodel%d_coef*smodel%d_g1, smodel%d_g2)" % (imc, imc, imc, imc))
smodel1 = ws.pdf("smodel1")
smodel2 = ws.pdf("smodel2")

xframe = x.frame()
data.plotOn(xframe)
bmodel.plotOn(xframe, RooFit.Normalization(ws.var("shapeBkg_bmodel_ggFLoose__norm").getVal(), 0))
smodel1.plotOn(xframe, RooFit.Normalization(ws.var("shapeSig_smodel1_ggFLoose__norm").getVal()*20, 2))
smodel2.plotOn(xframe, RooFit.Normalization(ws.var("shapeSig_smodel2_ggFLoose__norm").getVal()*20, 2))
xframe.Draw()
