from ROOT import *
import sys

pu = sys.argv[1]
dataworkspace_path = "/Users/vk/software/Analysis/files/fits_and_datacards/v0_20160824_1100/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22/%s" % pu
fitsworkspace_path = "/Users/vk/software/Analysis/files/limits_higsscombined_results/v0p3_20160824_1100/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22/%s" % pu

gROOT.SetBatch(kTRUE)

tail = "MaxLikelihoodFit.mH125.root"
head = "higgsCombine"
def extractCategory(s):
    s = s.split("/")
    s = s[len(s)-1]
    s = s.split("__")[1][:-5]
    return s

def findData(category):
    return "%s/shape__analytic__%s.root" % (dataworkspace_path,category)

def extractParameters_Background(ws, fit, *kargs, **wargs):
    category=wargs["category"]
    modifier=wargs["modifier"]
    list_const_pars = []
    list_float_pars = ["a1", "a2", "shapeBkg_bmodel_%s%s__norm" % (modifier,category)]
    const_pars = fit.constPars()
    float_pars = fit.floatParsFinal()
    for c in list_const_pars:
        getattr(ws, "import")(const_pars.find(c))
    for fl in list_float_pars:
        getattr(ws, "import")(float_pars.find(fl))

def extractParameters_DoubleGaus(ws, fit, *kargs, **wargs):
    category=wargs["category"]
    modifier=wargs["modifier"]
    list_const_pars = ["m1_g1_mass", "m1_g1_width", "m1_g2_mass", "m1_g2_width",
        "m2_g1_mass", "m2_g1_width", "m2_g2_mass", "m2_g2_width",
        "shapeSig_smodel1_%s%s__norm" % (modifier, category), 
        "shapeSig_smodel2_%s%s__norm" % (modifier, category),
        "smodel1_coef", "smodel2_coef"]
    list_float_pars = []
    const_pars = fit.constPars()
    float_pars = fit.floatParsFinal()
    for c in list_const_pars:
        getattr(ws, "import")(const_pars.find(c))
    for fl in list_float_pars:
        getattr(ws, "import")(float_pars.find(fl))

def buildModel_Background(ws, *kargs, **wargs):
    ws.factory('expr::f("-(a1*(x/100)+a2*(x/100)^2)",a1,a2,x)')
    ws.factory('Exponential::bmodel(f, 1)')
    return ws.pdf("bmodel")

def buildModel_DoubleGaus(ws, *kargs, **wargs):
    imc = wargs["imc"]
    ws.factory("Gaussian::smodel%d_g1(x, m%d_g1_mass, m%d_g1_width)" % (imc, imc, imc))
    ws.factory("Gaussian::smodel%d_g2(x, m%d_g2_mass, m%d_g2_width)" % (imc, imc, imc))
    ws.factory("SUM::smodel%d(smodel%d_coef*smodel%d_g1, smodel%d_g2)" % (imc, imc, imc, imc))
    return ws.pdf("smodel%d" % imc)

def generate(data, fit, *kargs, **wargs):
    category=wargs["category"]
    modifier = wargs["modifier"]
    ws = RooWorkspace("higgs_fits")
    ws.factory("x[125.0, %f, %f]" % (110, 160))
    ws.var('x').SetTitle('m_{#mu#mu}')
    ws.var('x').setUnit('GeV')

    print "-"*40
    extractParameters_Background(ws, fit, category=category, modifier=modifier)
    print "-"*40
    extractParameters_DoubleGaus(ws, fit, category=category, modifier=modifier)
    print "-"*40
    bmodel = buildModel_Background(ws, category=category, modifier=modifier)
    print "-"*40
    smodel1 = buildModel_DoubleGaus(ws, imc=1, category=category, modifier=modifier)
    print "-"*40
    smodel2 = buildModel_DoubleGaus(ws, imc=2, category=category, modifier=modifier)
    print "-"*40

    c1 = TCanvas("c1", "c1", 800, 600)
    c1.cd()
    leg = TLegend(0.4, 0.6, 0.6, 0.8)
    x = ws.var("x")
    xframe = x.frame()
    xframe.SetTitle(category)
    data.plotOn(xframe)
    plot_DoubleGaus(smodel1=smodel1, bmodel=bmodel, smodel2=smodel2,
        frame=xframe, 
        snorm1=(ws.var("shapeSig_smodel1_%s%s__norm"% (modifier, category)).getVal()*20),
        snorm2=(ws.var("shapeSig_smodel2_%s%s__norm"% (modifier, category)).getVal()*20),
        bnorm=ws.var("shapeBkg_bmodel_%s%s__norm"% (modifier, category)).getVal(),
        )
    xframe.Draw()
    leg = createLegend_DoubleGaus(data=data, S1=smodel1, S2=smodel2, BG=bmodel)
    leg.Draw()
    c1.SaveAs(fitsworkspace_path+"/%s.png" % category)

def plot_DoubleGaus(**wargs):
    smodel1 = wargs["smodel1"]
    smodel2 = wargs["smodel2"]
    bmodel = wargs["bmodel"]
    snorm1 = wargs["snorm1"]
    snorm2 = wargs["snorm2"]
    bnorm = wargs["bnorm"]
    frame = wargs["frame"]
    bmodel.plotOn(frame, RooFit.Normalization(bnorm, 0), RooFit.LineColor(kBlack))
    smodel1.plotOn(frame, RooFit.Normalization(snorm1, 0), RooFit.LineColor(kRed))
    smodel2.plotOn(frame, RooFit.Normalization(snorm2, 0), RooFit.LineColor(kRed))

def blindData(hdata):
    massmin = 120
    massmax = 130
    for ibin in range(hdata.GetNbinsX()):
        print hdata.GetBinContent(ibin+1)
        if hdata.GetBinCenter(ibin+1)>massmin and hdata.GetBinCenter(ibin+1)<massmax:
            print hdata.GetBinCenter(ibin+1)
            print hdata.GetBinContent(ibin+1)
            hdata.SetBinContent(ibin+1, 0)
            print hdata.GetBinContent(ibin+1)

def createLegend_DoubleGaus(**wargs):
    leg = TLegend(0.6, 0.6, 0.8, 0.8)
    leg.AddEntry(wargs["data"], "Data")
    leg.AddEntry(wargs["S1"], "S1 SM Higgs*20")
    leg.AddEntry(wargs["S2"], "S2 SM Higgs*20")
    leg.AddEntry(wargs["BG"], "Background Model")
    return leg

def main():
    import glob
    filelist = glob.glob(fitsworkspace_path+"/*mlfit*.root")
    ccc = 0
    for f in filelist:
        try:
            category = extractCategory(f)
            print "category = %s" % category
            print "fit filename = %s" % f
            modifier = ""
            if "01Jet" in category: modifier="bin"

            fdata = TFile(findData(category))
            wsdata = fdata.Get("higgs")
            data = wsdata.data("data_obs")
            hdata = data.createHistogram("hdata", wsdata.var("x"), 
                RooFit.Binning(50, 110, 160))
            hdata.Print()
            blindData(hdata)
            hdata.Print()
            ds = RooDataHist("data", "data", RooArgList(wsdata.set("obs").Clone()), hdata)
#            data = RooDataHist("data_obs_1", "data_obs_1", RooArgList(wsdata.set("obs")), 
#                hdata)
            ffit = TFile(f)
            fit = ffit.Get("fit_b")
            fit.Print("v")
            generate(ds, fit, category=category, modifier=modifier)
        except Exception as exc:
            print exc.args

if __name__=="__main__":
    main()
