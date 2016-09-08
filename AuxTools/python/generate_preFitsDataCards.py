import ROOT as R
from ROOT import *
import sys, os, subprocess

R.gROOT.SetBatch(R.kTRUE)

def mkdir(d):
    if not os.path.exists(d):
        cmd = "mkdir %s" % d
        subprocess.call(cmd, shell=True)

if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.environ["ANALYSISHOME"])
sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "NtupleProcessing/python"))
import NtupleProcessing.python.Samples as S
import NtupleProcessing.python.Dataset as DS

#
#   List all the constants and some initializations
#
libdir="/Users/vk/software/Analysis/build-4"
resultsdir = "/Users/vk/software/Analysis/files/results/v0_20160824_1100"
limitspath= "/Users/vk/software/Analysis/files/fits_and_datacards"
limitspath = os.path.join(limitspath, os.path.split(resultsdir)[1])
mkdir(limitspath)
default = -0.999
R.gSystem.Load(libdir+"/libAnalysisNtupleProcessing.dylib")
R.gSystem.Load(libdir+"/libAnalysisCore.dylib")
aux = "Mu22"

def buildModel_SingleGaus(ws, *kargs, **wargs):
    imc = wargs["imc"]
    ws.factory("m%d_mass[125, 110, 160]" % imc)
    ws.factory("m%d_width[1.0, 0.1, 10]" % imc)
    ws.factory("Gaussian::smodel%d(x, m%d_mass, m%d_width)" % (imc, imc, imc))
    return ws.pdf("smodel%d" % imc)

def buildModel_DoubleGaus(ws, *kargs, **wargs):
    imc = wargs["imc"]
    ws.factory("m%d_g1_mass[125, 110, 160]" % imc)
    ws.factory("m%d_g2_mass[125, 110, 160]" % imc)
    ws.factory("m%d_g1_width[1.0, 0.1, 10]" % imc)
    ws.factory("m%d_g2_width[1.0, 0.1, 10]" % imc)
    ws.factory("Gaussian::smodel%d_g1(x, m%d_g1_mass, m%d_g1_width)" % (imc, imc, imc))
    ws.factory("Gaussian::smodel%d_g2(x, m%d_g2_mass, m%d_g2_width)" % (imc, imc, imc))
    ws.factory("smodel%d_coef[0.1, 0.0001, 1.0]" % imc)
    ws.factory("SUM::smodel%d(smodel%d_coef*smodel%d_g1, smodel%d_g2)" % (imc, imc, imc, imc))
    return ws.pdf("smodel%d" % imc)

def setParameters_SingleGaus(ws, *kargs, **wargs):
    imc = wargs["imc"]
    norm = wargs["norm"]
    ws.factory("smodel%d_norm[%f, 0.0, 1000]" % (imc, norm))
    ws.var("smodel%d_norm" % imc).setConstant(kTRUE)
    ws.var("m%d_mass" % imc).setConstant(kTRUE)
    ws.var("m%d_width" % imc).setConstant(kTRUE)

def setParameters_DoubleGaus(ws, *kargs, **wargs):
    imc = wargs["imc"]
    norm = wargs["norm"]
    ws.factory("smodel%d_norm[%f, 0.0, 1000]" % (imc, norm))
    ws.var("smodel%d_norm" % imc).setConstant(kTRUE)
    ws.var("m%d_g1_mass" % imc).setConstant(kTRUE)
    ws.var("m%d_g2_mass" % imc).setConstant(kTRUE)
    ws.var("m%d_g1_width" % imc).setConstant(kTRUE)
    ws.var("m%d_g2_width" % imc).setConstant(kTRUE)
    ws.var("smodel%d_coef" % imc).setConstant(kTRUE)

def getEventWeights(resultpathname):
    print resultpathname
    f = R.TFile(resultpathname)
    h = f.Get("eventWeights")
    return h.GetBinContent(1)

def generate(variables, (data, mcbg, mcsig), opt=0):
    """
    variable is the dictionary of the form
    {
        "name" : <str>,
        "category" : <str>
        "fullpath" : <str>
        "min" : double
        "max" : double
        "json" : str
    }
    data is the dictionary of the form
    {
        "name" : <str>,
        "label" : <str>,
        "result" : <str>,
        "luminosity" : <double/int>
    }
    mc is the list of dictionaries of the form
        [mc1, mc2, mc3, ..., mcn], where mci is
        {
            "name" : <str>,
            "cmssw" : <str>,
            "pujson" : <str>,
            "PU" : <str>,
            "result" : <str>,
            "eweight", : <double>
            "xsection" : <double>,
            "color" : <int>
        }
    """

    print "-"*40
    print data
    print mcbg
    print mcsig

    #
    #   Create the pic directory
    #
    sub = "" if aux==None or aux=="" else "__%s" % aux
    fulllimitspath = os.path.join(limitspath, "%s__%s%s" % (mcsig[0]["cmssw"], 
        data["json"][:-4], sub))
    mkdir(fulllimitspath)
    fulllimitspath+="/%s"%mcsig[0]["PU"]
    mkdir(fulllimitspath) # is the one to be used

    counter = 0
    numvars = len(variables)
    for variable in variables:
        savemodifier = ""
        fdata = R.TFile(data["result"])
        hdata = fdata.Get(variable["fullpath"])
        if hdata.GetEntries()==0:
            continue
        hdata.SetMarkerStyle(20)
        hdata.SetMarkerSize(0.5)
        hdata.SetMarkerColor(R.kBlack)

        mch = {}
        mcf = {}
        for imcbg in mcbg:
            mcf[imcbg["name"]] = R.TFile(imcbg["result"])
            mch[imcbg["name"]] = mcf[imcbg["name"]].Get(variable["fullpath"])
            mch[imcbg["name"]].Scale(data["luminosity"]*imcbg["xsection"]/imcbg["eweight"])
            mch[imcbg["name"]].SetFillColor(imcbg["color"])

        mchsig = {}
        mcfsig = {}
        for imcsig in mcsig:
            mcfsig[imcsig["name"]] = R.TFile(imcsig["result"])
            mchsig[imcsig["name"]] = mcfsig[imcsig["name"]].Get(variable["fullpath"])
            mchsig[imcsig["name"]].Scale(data["luminosity"]*imcsig["xsection"]/imcsig["eweight"])
            
        #   generate the proper root files with   
        if opt==0:
            #   with templates as histos 
            generateTemplate(fulllimitspath, variable, hdata, mch, mchsig)
        else:
            #   with RooFit Workspace in the outpu
            generateAnalytic(fulllimitspath, variable, hdata, mch, mchsig)

def generateAnalytic(fulllimitspath, variable, hdata, backgrounds, signals):
    from time import sleep
    category = variable["fullpath"].split("/")[0]

    #
    #   Prepare the Data for Workspace
    #
    print "-"*40
    print "Prepare the Data histogram"
    newhdata = R.TH1D("newhdata", "newhdata", 50, 110, 160)
    newibin = 0
    massmin = 110; massmax = 160
    for ibin in range(hdata.GetNbinsX()):
        if hdata.GetBinCenter(ibin+1)>massmin and hdata.GetBinCenter(ibin+1)<massmax:
            newhdata.SetBinContent(newibin+1, hdata.GetBinContent(ibin+1))
            newibin+=1
    nbins = newhdata.GetNbinsX()
    massmin = newhdata.GetBinLowEdge(1)
    massmax = massmin + nbins*newhdata.GetBinWidth(1)
    ndata = int(newhdata.Integral())

    #   suppress msgs
    R.RooMsgService.instance().setGlobalKillBelow(R.RooFit.FATAL)

    #   workspace
    wspace = R.RooWorkspace("higgs")

    #
    #   Prepare all the Observable Variable and import data
    #
    print "-"*40
    print "Prepare the Variables"
    wspace.factory("x[125.0, %f, %f]" % (massmin, massmax))
    wspace.var('x').SetTitle('m_{#mu#mu}')
    wspace.var('x').setUnit('GeV')
    wspace.defineSet("obs", "x")
    obs = wspace.set("obs")
    data = R.RooDataHist("data_obs", "data_obs", RooArgList(obs), newhdata)
    getattr(wspace, "import")(data, RooCmdArg())
    
    #
    #   Prepare the MC histograms
    #
    print "-"*40
    print "Prepare the MC histograms"
    lsignals = []
    for name in signals:
        s = R.TH1D(name.split("_")[0], name.split("_")[0], nbins, massmin, massmax)
        newibin = 0
        for ibin in range(signals[name].GetNbinsX()):
            if signals[name].GetBinCenter(ibin+1)>massmin and signals[name].GetBinCenter(ibin+1)<massmax:
                s.SetBinContent(newibin+1, signals[name].GetBinContent(ibin+1))
                newibin+=1
        print "%s events = %f" % (name, s.Integral())
        hist_mc = R.RooDataHist("data_obs", "data_obs", RooArgList(obs), s)
        print "%s events = %f" % (s.GetName(), hist_mc.sumEntries())
        lsignals.append((s.GetName(), hist_mc))

    #
    #   Prepare the background model
    #
    wspace.factory('a1[ 5.0, -1000, 1000]')
    wspace.factory('a2[ 5.0, -1000, 1000]')
    wspace.factory('expr::f("-(a1*(x/100)+a2*(x/100)^2)",a1,a2,x)')
    wspace.factory('Exponential::bmodel(f, 1)')
    wspace.factory("bmodel_norm[%f, %f, %f]" % (ndata, ndata/2, ndata*2))
    bmodel  = wspace.pdf('bmodel')

    #
    #   Prepare the Signals - Fit the MC and fix the parameters
    #
    imc = 1
    c = TCanvas("c1", "c1", 800, 600)
    c.cd()
    for s in lsignals:
        #
        #   Fit 
        #
        xframe = wspace.var("x").frame()
        xframe.SetTitle(category)
        print "-"*40
        print s[0], s[1].sumEntries()
        model = buildModel_DoubleGaus(wspace, imc=imc)
        r = model.fitTo(s[1], RooFit.Save(), RooFit.Range(115, 135))
        r.Print()
        s[1].plotOn(xframe)
        model.plotOn(xframe)
        model.paramOn(xframe)
        xframe.Draw()
        c.SaveAs(fulllimitspath+'/%s__%s.png' % (s[0], category))

        #   fix/set
        setParameters_DoubleGaus(wspace, imc=imc, norm=s[1].sumEntries())
        imc+=1
        
    #
    #   save the workspace
    #
    category = variable["fullpath"].split("/")[0]
    filename = fulllimitspath+"/shape__analytic__%s.root" % category
    wspace.SaveAs(filename)
    
    #
    #   Generate the Datacard
    #   - rates for signal are given thru the model_norm
    #
    fout = open(fulllimitspath+"/datacard__analytic__%s.txt" % category, "w")
    fout.write("imax 1\n")
    fout.write("jmax 2\n")
    fout.write("kmax *\n")
    fout.write(("-"*40) + "\n")
    fout.write("shapes * * %s higgs:$PROCESS\n" % ("shape__analytic__%s.root" % category))
    fout.write(("-"*40) + "\n")
    fout.write("bin %s\n" % category)
    fout.write("observation -1\n")
    fout.write(("-"*40)+"\n")
    binstr = "bin  %s  %s  %s\n" % (category, category, category)
    p1str = "process  %s  %s  %s\n" % ("smodel1", "smodel2", "bmodel")
    p2str = "process  -1  0  1\n"
    ratestr = "rate  1  1  1\n" 
    fout.write(binstr)
    fout.write(p1str)
    fout.write(p2str)
    fout.write(ratestr)
    fout.close()

    sss = """wspace.factory('SUM::model(bmodel_norm*bmodel, smodel_norm*smodel)')
    model = wspace.pdf('model')

    #   fit
    print "-"*40
    b = data.sumEntries()
   # wspace.var("bmodel_norm").setVal(b)
    swatch = R.TStopwatch()
    swatch.Start()
    model.fitTo(data)
    print "real time: %10.3f s" % swatch.RealTime()

    vbkg = wspace.var('bmodel_norm')
    vsig = wspace.var('smodel_norm')
    vmass= wspace.var('mass')
    vwidth=wspace.var('w')

    bkg   = vbkg.getVal()
    ebkg  = vbkg.getError()
    sig   = vsig.getVal()
    esig  = vsig.getError()
    mass  = vmass.getVal()
    emass = vmass.getError()
    width = vwidth.getVal()
    ewidth= vwidth.getError()
#    zvalue= sig / esig
    
    print "-"*40
    print "background: %10.1f +\-%-5.1f GeV" % (bkg, ebkg)
    print "signal:     %10.1f +\-%-5.1f" % (sig, esig)
    print "mass:       %10.1f +\-%-4.1f GeV" % (mass, emass)
    print "width:      %10.1f +\-%-4.1f GeV" % (width, ewidth)
#    print "sig/esig:   %10.1f" % zvalue

    wspace.Print()

    #   save the fit plot
    x = wspace.var('x')
    xframe = x.frame()
    yframe = x.frame().Clone()
    zframe = x.frame().Clone()
    xframe.GetXaxis().SetNdivisions(505)
    xframe.SetTitle("%s" % category) 
    yframe.SetTitle("%s" % category) 
    zframe.SetTitle("%s" % category)
    data.plotOn(xframe)
    model.plotOn(xframe, RooFit.LineColor(kRed))
    bmodel.plotOn(xframe, RooFit.LineColor(kBlue), RooFit.LineStyle(kDashed))
    smodel.plotOn(xframe, RooFit.LineColor(kGreen), RooFit.LineStyle(kDashed))
    wspace.var('a1').setConstant()
    wspace.var('a2').setConstant()
    model.paramOn(xframe, RooFit.Layout(0.5, 0.9, 0.8))
    xframe.getAttText().SetTextSize(0.03)
    c1 = TCanvas('fig_hmumu_fit', 'fit', 10, 10, 500, 500)
    xframe.Draw()
    c1.SaveAs(fulllimitspath+'/%s.png' % category)

    #
    #   Generate the Datacard
    #
    fout = open(fulllimitspath+"/datacard__analytic__%s.txt" % category, "w")
    fout.write("imax 1\n")
    fout.write("jmax 1\n")
    fout.write("kmax *\n")
    fout.write(("-"*40) + "\n")
    fout.write("shapes * * %s higgs:$PROCESS\n" % ("shape__analytic__%s.root" % category))
    fout.write(("-"*40) + "\n")
    fout.write("bin %s\n" % category)
    fout.write("observation -1\n")
    fout.write(("-"*40)+"\n")
    binstr = "bin  %s  %s\n" % (category, category)
    p1str = "process  %s  %s\n" % ("smodel", "bmodel")
    p2str = "process  0  1\n"
    ratestr = "rate  1  1\n" 
    fout.write(binstr)
    fout.write(p1str)
    fout.write(p2str)
    fout.write(ratestr)
    fout.close()

    
    #   generate also the blinded plot
    h = newhdata.Clone("newh")
    for i in range(h.GetNbinsX()):
        if h.GetBinCenter(i+1)>120 and h.GetBinCenter(i+1)<130:
            h.SetBinContent(i+1, 0)
    data_blind = R.RooDataHist("data_obs_blind", "data_obs_blind", RooArgList(obs), h)
    yframe.GetXaxis().SetNdivisions(505)
    data_blind.plotOn(yframe)
#pdf->plotOn(frame,Normalization(234,RooAbsReal::NumEvent))
    model.plotOn(yframe, RooFit.LineColor(kRed), RooFit.Normalization(b, 2))
    bmodel.plotOn(yframe, RooFit.LineColor(kBlue), RooFit.LineStyle(kDashed),
        RooFit.Normalization(b, 2))
    smodel.plotOn(yframe, RooFit.LineColor(kGreen), RooFit.LineStyle(kDashed),
        RooFit.Normalization(b, 2))
    wspace.var('a1').setConstant()
    wspace.var('a2').setConstant()
#    model.paramOn(yframe, RooFit.Layout(0.5, 0.9, 0.8))
#    yframe.getAttText().SetTextSize(0.03)
    yframe.Draw()
    c1.SaveAs(fulllimitspath+"/%s_Blind.png" % category)

    zframe.GetXaxis().SetNdivisions(505)
    data_blind.plotOn(zframe)
    model.plotOn(zframe, RooFit.LineColor(kRed), RooFit.Normalization(b, 2))
    bmodel.plotOn(zframe, RooFit.LineColor(kBlue), RooFit.LineStyle(kDashed),
        RooFit.Normalization(b, 2))
    wspace.var('a1').setConstant()
    wspace.var('a2').setConstant()
    zframe.Draw()
    c1.SaveAs(fulllimitspath+"/%s_BlindnoS.png" % category)
    """

def generateTemplate(fulllimitspath, variable, hdata, backgrounds, signals):
    category = variable["fullpath"].split("/")[0]
    filename = fulllimitspath+"/shape__templates__%s.root" % category
    f = R.TFile(filename, "recreate")

    massmin = 115; massmax = 135; nbins = massmax - massmin
    data_obs = R.TH1D("data_obs", "data_obs", nbins, massmin, massmax)
    newibin = 0
    for ibin in range(hdata.GetNbinsX()):
        if hdata.GetBinCenter(ibin+1)>massmin and hdata.GetBinCenter(ibin+1)<massmax:
            data_obs.SetBinContent(newibin+1, hdata.GetBinContent(ibin+1))
            newibin+=1
    data_obs.Write()
    
    fout = open(fulllimitspath+"/datacard__templates__%s.txt" % category, "w")
    fout.write("imax 1\n")
    fout.write("jmax %d\n" % (len(signals)+len(backgrounds)-1))
    fout.write("kmax *\n")
    fout.write(("-"*40) + "\n")
    fout.write("shapes * * %s $PROCESS\n" % ("shape__templates__%s.root" % category))
    fout.write(("-"*40)+"\n")
    fout.write("bin %s\n" % category)
    fout.write("observation -1\n")
    fout.write(("-"*40) + "\n")

    print "-"*40
    print "Category : %s" % category
    print "data observed events = " + str(data_obs.Integral())
    lsignals = []; lbackgrounds = []
    for name in signals:
        s = R.TH1D(name.split("_")[0], name.split("_")[0], nbins, massmin, massmax)
        newibin = 0
        for ibin in range(signals[name].GetNbinsX()):
            if signals[name].GetBinCenter(ibin+1)>massmin and signals[name].GetBinCenter(ibin+1)<massmax:
                s.SetBinContent(newibin+1, signals[name].GetBinContent(ibin+1))
                newibin+=1
        print "%s events = %f" % (name, s.Integral())
        lsignals.append((s.GetName(), s.Integral()))
        s.Write()
    for name in backgrounds:
        b = R.TH1D(name.split("_")[0], name.split("_")[0], nbins, massmin, massmax)
        newibin = 0
        for ibin in range(backgrounds[name].GetNbinsX()):
            if backgrounds[name].GetBinCenter(ibin+1)>massmin and backgrounds[name].GetBinCenter(ibin+1)<massmax:
                b.SetBinContent(newibin+1, backgrounds[name].GetBinContent(ibin+1))
                newibin+=1
        print "%s events = %f" % (name, b.Integral())
        lbackgrounds.append((b.GetName(), b.Integral()))
        b.Write()
    f.Close()
    binstr = "bin  "
    p1str = "process  "
    p2str = "process  "
    ratestr = "rate  "
    nums = -len(lsignals)+1
    for s in lsignals:
        binstr += category+"  "
        p1str += s[0] + "  "
        p2str += "%d  " % nums
        ratestr += str(s[1]) + "  "
        nums+=1
    for b in lbackgrounds:
        binstr += category+"  "
        p1str += b[0] + "  "
        p2str += "%d  " % nums
        ratestr += str(b[1]) + "  "
        nums+=1
    binstr+="\n"
    p1str+="\n"
    p2str+="\n"
    ratestr+="\n"
    fout.write(binstr)
    fout.write(p1str)
    fout.write(p2str)
    fout.write(ratestr)
    fout.close()

#
#   start...
#
if __name__=="__main__":
    #   define the variable
    marker = ""
    varNames = ["DiMuonMass"]
    category = "NoCats"
    variables = [{"name":x, "min":-0.999, "max":-0.999,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "2Jets"
    var2jets = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01Jets"
    var01jets = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "VBFTight"
    varVBFTight = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "ggFTight"
    varggFTight = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "ggFLoose"
    varggFLoose = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsTight"
    var01JetsTight = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsTightBB"
    var01JetsTightBB = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsTightBO"
    var01JetsTightBO = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsTightBE"
    var01JetsTightBE = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsTightOO"
    var01JetsTightOO = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsTightOE"
    var01JetsTightOE = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsTightEE"
    var01JetsTightEE = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsLoose"
    var01JetsLoose = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsLooseBB"
    var01JetsLooseBB = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsLooseBO"
    var01JetsLooseBO = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsLooseBE"
    var01JetsLooseBE = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsLooseOO"
    var01JetsLooseOO = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsLooseOE"
    var01JetsLooseOE = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "01JetsLooseEE"
    var01JetsLooseEE = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    variables.extend(var2jets)
    variables.extend(var01jets)
    variables.extend(varVBFTight)
    variables.extend(varggFTight)
    variables.extend(varggFLoose)
    variables.extend(var01JetsTight)
    variables.extend(var01JetsLoose)
    variables.extend(var01JetsTightBB)
    variables.extend(var01JetsTightBO)
    variables.extend(var01JetsTightBE)
    variables.extend(var01JetsTightOO)
    variables.extend(var01JetsTightOE)
    variables.extend(var01JetsTightEE)
    variables.extend(var01JetsLooseBB)
    variables.extend(var01JetsLooseBO)
    variables.extend(var01JetsLooseBE)
    variables.extend(var01JetsLooseOO)
    variables.extend(var01JetsLooseOE)
    variables.extend(var01JetsLooseEE)

    #
    #   Choose the Data Results to use
    #
    datajson = "Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt"
    jsons = S.jsonfiles
    intlumi = -1
    for k in jsons:
        if jsons[k].filename==datajson:
            intlumi = jsons[k].intlumi
    resultpathname = os.path.join(resultsdir,  
        "result__merged__%s__%s.root" % (datajson[:-4], aux))
    data2016_M22 = {"name" : "2016_Prompt", "label" : "2016 Prompt %.1f/fb" % (intlumi/1000),
        "result" : resultpathname,  "luminosity":intlumi,
        "json" : datajson}

    #
    #   Choose the MC Samples to be used Signal and Background
    #
    cmssws = ['74X', '76X']
    signals = [
        'GluGlu_HToMuMu_M125_13TeV_powheg_pythia8',
        'VBF_HToMuMu_M125_13TeV_powheg_pythia8'
    ]
    backgrounds = {
            'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' : R.kBlue,
            'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' : R.kGreen
    }
    pus = ["68", "69", "70", "71", "72", "71p3"]
    mcsignals = {}
    mcbkgs = {}
    for cmssw in cmssws:
        for pu in pus:
            list_signals = []
            list_backgrounds = []
            for s in signals:
                cross_section = -1
                resultpathname = os.path.join(resultsdir,
                    "result__%s__%s__%s__%s__%s.root" % (s, cmssw,
                    datajson[:-4], pu+"mb", aux))
                for k in S.mcdatasets:
                    if s in S.mcdatasets[k].name and cmssw==S.mcdatasets[k].initial_cmssw:
                        cross_section = S.mcdatasets[k].cross_section
                mcsig = {
                    "name" : s, "cmssw" : cmssw,
                    "pujson" : datajson[:-4], "PU" : pu,
                    "label" : s, "result" : resultpathname,
                    "xsection" : cross_section,
                    "eweight" : getEventWeights(resultpathname)
                }
                list_signals.append(mcsig)

            for b in backgrounds:
                cross_section = -1
                for k in S.mcdatasets:
                    if b in S.mcdatasets[k].name and cmssw==S.mcdatasets[k].initial_cmssw:
                        cross_section = S.mcdatasets[k].cross_section
                resultpathname = os.path.join(resultsdir,
                    "result__%s__%s__%s__%s__%s.root" % (b, cmssw,
                    datajson[:-4], pu+"mb", aux))
                mcbkg = {
                    "name" : b, "cmssw" : cmssw,
                    "pujson" : datajson[:-4], "PU" : pu,
                    "label" : b, "result" : resultpathname,
                    "xsection" : cross_section,
                    "eweight" : getEventWeights(resultpathname),
                    "color" : backgrounds[b]
                }
                list_backgrounds.append(mcbkg)
            mcsignals["%s__%s" % (cmssw, pu)] = list_signals
            mcbkgs["%s__%s" % (cmssw, pu)] = list_backgrounds
                   


    #
    #   Generate all the distributions
    #
    print "Produce Plots for variables: %s" % str(varNames)
    for cmssw in ["76X"]:
        for pu in pus:
            generate(variables, (data2016_M22, 
                mcbkgs["%s__%s" % (cmssw, pu)],
                mcsignals["%s__%s" % (cmssw, pu)]), 1)
