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
resultsdir = "/Users/vk/software/Analysis/files/results/vR1_20170122_1326"
#resultsdir = "/Users/vk/software/Analysis/files/results/vR2_20170125_1204"
limitspath= "/Users/vk/software/Analysis/files/fits_and_datacards"
#limitspath_modifier = "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"
#limitspath_modifier = "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8"
limitspath_modifier = "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
limitspath = os.path.join(limitspath, os.path.split(resultsdir)[1] + "__" + 
    limitspath_modifier)
mkdir(limitspath)
default = -0.999
R.gSystem.Load(libdir+"/libAnalysisNtupleProcessing.dylib")
R.gSystem.Load(libdir+"/libAnalysisCore.dylib")
aux = "Mu24"

#
#   Build Specific Models and associated variables
#
def buildModel_SingleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    category=wargs["category"]
    ws.factory("Gaussian::smodel{processName}(x, m{processName}_mass_{category}, m{processName}_width_{category})".format(processName=processName, category=category))
    return ws.pdf("smodel%s" % processName)

def createVariables_SingleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    category=wargs["category"]
    ws.factory("m{processName}_mass_{category}[125, {massmin}, {massmax}]".format(
        processName=processName, 
        category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
    ws.factory("m{processName}_width_{category}[1.0, 0.1, 10]".format(
        processName=processName, category=category))

def buildModel_DoubleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    category=wargs["category"]
    ws.factory("Gaussian::smodel{processName}_g1_{category}(x, m{processName}_g1_mass_{category}, m{processName}_g1_width_{category})".format(
        processName=processName, category=category))
    ws.factory("Gaussian::smodel{processName}_g2_{category}(x, m{processName}_g2_mass_{category}, m{processName}_g2_width_{category})".format(
        processName=processName, category=category))
    ws.factory("SUM::smodel{processName}(smodel{processName}_coef_{category}*smodel{processName}_g1_{category}, smodel{processName}_g2_{category})".format(
        processName=processName, category=category))
    return ws.pdf("smodel%s" % processName)

def createVariables_DoubleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    category=wargs["category"]
    ws.factory("m{processName}_g1_mass_{category}[125, {massmin}, {massmax}]".format(
        processName=processName,
        category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
    ws.factory("m{processName}_g2_mass_{category}[125, {massmin}, {massmax}]".format(
        processName=processName,
        category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
    ws.factory("m{processName}_g1_width_{category}[1.0, 0.1, 10]".format(
        processName=processName,
        category=category))
    ws.factory("m{processName}_g2_width_{category}[1.0, 0.1, 10]".format(
        processName=processName,
        category=category))
    ws.factory("smodel{processName}_coef_{category}[0.1, 0.0001, 1.0]".format(
        processName=processName,
        category=category))

def buildModel_ExpGaus(ws, *kargs, **wargs):
    category = wargs["category"]
    ws.factory('expr::f("-(a1_{category}*(x/100)+a2_{category}*(x/100)^2)",a1_{category},a2_{category},x)'.format(category=category))
    ws.factory('Exponential::bmodel(f, 1)')
    return ws.pdf('bmodel')

def createVariables_ExpGaus(ws, *kargs, **wargs):
    ndata = wargs["ndata"]
    category=wargs["category"]
    ws.factory('a1_%s[ 5.0, -1000, 1000]' % category)
    ws.factory('a2_%s[ 5.0, -1000, 1000]' % category)
    ws.factory("bmodel_norm[%f, %f, %f]" % (ndata, ndata/2, ndata*2))

#
#   Set/Fix Parameters for specific models
#
def setParameters_SingleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    norm = wargs["norm"]
    category=wargs["category"]
    ws.factory("smodel%s_norm[%f, 0.0, 1000]" % (processName, norm))
    ws.var("smodel%s_norm" % processName).setConstant(kTRUE)
    ws.var("m%s_mass_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("m%s_width_%s" % (processName, category)).setConstant(kTRUE)

def setParameters_DoubleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    norm = wargs["norm"]
    category=wargs["category"]
    ws.factory("smodel%s_norm[%f, 0.0, 1000]" % (processName, norm))
    ws.var("smodel%s_norm" % processName).setConstant(kTRUE)
    ws.var("m%s_g1_mass_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("m%s_g2_mass_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("m%s_g1_width_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("m%s_g2_width_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("smodel%s_coef_%s" % (processName, category)).setConstant(kTRUE)

def getEventWeights(resultpathname):
    print resultpathname
    f = R.TFile(resultpathname)
    h = f.Get("eventWeights")
    return h.GetBinContent(1)

#
#   Prepare DataHistograms
#
def prepareHistogram(hist, **wargs):
    newname = wargs["name"]
    massmin = wargs["massmin"]; massmax = wargs["massmax"]
    newhist = R.TH1D(newname, newname, massmax-massmin, massmin, massmax)
    newibin = 0
    for ibin in range(hist.GetNbinsX()):
        if hist.GetBinCenter(ibin+1)>massmin and hist.GetBinCenter(ibin+1)<massmax:
            newhist.SetBinContent(newibin+1, hist.GetBinContent(ibin+1))
            newibin+=1
    return newhist

#
#   Prepare the Signals Models - Build/Fit/Fix
#
def prepareSignalModel(ws, signals, **wargs):
    smode = wargs["smode"]
    category = wargs["category"]
    fulllimitspath = wargs["fulllimitspath"]
    if smode=="Combined":
        counter = 0
        #   Sum up all the Signals
        print "-"*40
        print "Sum up Signal Histograms"
        for name in signals:
            print "%s events = %f" % (name, signals[name].Integral())
            if counter==0:
                signal = signals[name]
            else:
                signal.Add(signals[name])
            counter+=1
        #   convert it into the RooDataHist
        newhist = prepareHistogram(signal, name="signal", massmin=wargs["massmin"],
            massmax=wargs["massmax"])
        print "%s events = %f" % (newhist.GetName(), newhist.Integral())
        roo_hist = R.RooDataHist("roo_signal", "roo_signal", RooArgList(wargs["obs"]),
            newhist)
        print "%s events = %f" % (roo_hist.GetName(), roo_hist.sumEntries())
        #   Create Vars - build model - fit - fix parameters - plot
        imc = 1
        c = TCanvas("c1", "c1", 800, 600)
        xframe = ws.var("x").frame()
        xframe.SetTitle(category)
        print "-"*40
        print roo_hist.GetName(), roo_hist.sumEntries()
        processName = "AllSignals"
        if wargs["smodel"]=="DoubleGaus":
            createVariables_DoubleGaus(ws, processName=processName, **wargs)
            smodel = buildModel_DoubleGaus(ws, processName=processName, **wargs)
            r = smodel.fitTo(roo_hist, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                wargs["fitmax"]))
            setParameters_DoubleGaus(ws, processName=processName, norm=roo_hist.sumEntries(),
                **wargs)
        elif wargs["smodel"]=="SingleGaus":
            createVariables_SingleGaus(ws, processName=processName, **wargs)
            smodel = buildModel_SingleGaus(ws, processName=processName, **wargs)
            r = smodel.fitTo(roo_hist, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                wargs["fitmax"]))
            setParameters_SingleGaus(ws, processName=processName, norm=roo_hist.sumEntries(),
                **wargs)
        r.Print("v")
        roo_hist.plotOn(xframe)
        smodel.plotOn(xframe, RooFit.Color(kRed))
        smodel.paramOn(xframe)
        xframe.Draw()
        c.SaveAs(fulllimitspath+"/%s__%s__%s__%s__%s__%s.png" % (
            processName, category, wargs["mass"], wargs["bmodel"], wargs["smode"],
            wargs["smodel"]))
    elif smode=="Separate":
        lsignals = []
        #   convert all of histos into RooDataHist
        for name in signals:
            newhist = prepareHistogram(signals[name], name=name.split("_")[0],
                massmin=wargs["massmin"], massmax=wargs["massmax"])
            print "%s events = %f" % (name, newhist.Integral())
            roo_hist = R.RooDataHist(newhist.GetName(),
                newhist.GetName(), RooArgList(wargs["obs"]),
                newhist)
            print "%s events = %f" % (roo_hist.GetName(), roo_hist.sumEntries())
            lsignals.append(roo_hist)
        imc = 1
        c = TCanvas("c1", "c1", 800, 600)
        c.cd()
        #   build Models - Fit - Fix parameters - Produce Plots
        for s in lsignals:
            xframe = ws.var("x").frame()
            xframe.SetTitle(category)
            print "-"*40
            print s.GetName(), s.sumEntries()
            processName = s.GetName()

            if wargs["smodel"]=="DoubleGaus":
                createVariables_DoubleGaus(ws, processName=processName, **wargs)
                smodel = buildModel_DoubleGaus(ws, processName=processName, **wargs)
                r = smodel.fitTo(s, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                    wargs["fitmax"]))
                setParameters_DoubleGaus(ws, processName=processName, norm=s.sumEntries(),
                    **wargs)
            elif wargs["smodel"]=="SingleGaus":
                createVariables_SingleGaus(ws, processName=processName, **wargs)
                smodel = buildModel_SingleGaus(ws, processName=processName, **wargs)
                r = smodel.fitTo(s, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                    wargs["fitmax"]))
                setParameters_SingleGaus(ws, processName=processName, norm=s.sumEntries(),
                    **wargs)

            r.Print("v")
            s.plotOn(xframe)
            smodel.plotOn(xframe, RooFit.Color(kRed))
            smodel.paramOn(xframe)
            xframe.Draw()
            c.SaveAs(fulllimitspath+"/%s__%s__%s__%s__%s__%s.png" % (
                s.GetName(), category, wargs["mass"], wargs["bmodel"], wargs["smode"],
                wargs["smodel"]))
            imc+=1

#
#   Build Datacards
#
def buildDatacard_analytic_Combined(**wargs):
    category = wargs["category"]
    mass = wargs["mass"]
    bmodel = wargs["bmodel"]
    smodel = wargs["smodel"]
    smode = wargs["smode"]
    fulllimitspath=wargs["fulllimitspath"]
    fout = open(fulllimitspath+"/datacard__analytic__%s__%s__%s__%s__%s.txt" % (category,
        mass, bmodel, smode, smodel), "w")
    fout.write("imax 1\n")
    fout.write("jmax 1\n")
    fout.write("kmax *\n")
    fout.write(("-"*40) + "\n")
    fout.write("shapes * * %s higgs:$PROCESS\n" % ("shape__analytic__%s__%s__%s__%s__%s.root" % (category, mass, bmodel, smode, smodel)))
    fout.write(("-"*40) + "\n")
    fout.write("bin %s\n" % category)
    fout.write("observation -1\n")
    fout.write(("-"*40)+"\n")
    binstr = "bin  %s  %s\n" % (category, category)
    p1str = "process  %s  %s\n" % ("smodelAllSignals", "bmodel")
    p2str = "process  0  1\n"
    ratestr = "rate  1  1\n"
    fout.write(binstr)
    fout.write(p1str)
    fout.write(p2str)
    fout.write(ratestr)
    fout.close()

def buildDatacard_analytic_Separate(**wargs):
    category = wargs["category"]
    mass = wargs["mass"]
    bmodel = wargs["bmodel"]
    smodel = wargs["smodel"]
    smode = wargs["smode"]
    lsignals = wargs["signals"]
    fulllimitspath=wargs["fulllimitspath"]
    fout = open(fulllimitspath+"/datacard__analytic__%s__%s__%s__%s__%s.txt" % (category,
        mass, bmodel, smode, smodel), "w")
    fout.write("imax 1\n")
    fout.write("jmax %d\n" % len(lsignals))
    fout.write("kmax *\n")
    fout.write(("-"*40) + "\n")
    fout.write("shapes * * %s higgs:$PROCESS\n" % ("shape__analytic__%s__%s__%s__%s__%s.root" % (category, mass, bmodel, smode, smodel)))
    fout.write(("-"*40) + "\n")
    fout.write("bin %s\n" % category)
    fout.write("observation -1\n")
    fout.write(("-"*40)+"\n")
    binstr = "bin "
    p1str = "process "
    p2str = "process "
    ratestr = "rate "
    isig = 1
    for signalName in lsignals:
        processName = signalName.split("_")[0]
        binstr+="%s " % category
        p1str+="smodel%s " % processName
        p2str+= "%d " % (-len(lsignals)+isig)
        ratestr+= "1 "
        isig+=1

    # make sure to import the right uncertainties
    from NtupleProcessing.python.Uncertainty import *
    uncertainties = uncertainties_vR2
    uncStrings = []
    for unc in uncertainties:
        uncstr = unc.name + " " + unc.uncType
        # do the signal
        for sName in lsignals:
            processName = sName.split("_")[0]
            if processName in unc.valuesMap:
                uncstr += " %f" % unc.valuesMap[processName]
            else:
                uncstr += " -"

        #now do the backgrou
        if "bmodel" in unc.valuesMap:
            uncstr += " %f" % unc.valuesMap["bmodel"]
        else:
            uncstr += " -"

        # append
        uncStrings.append(uncstr)

    binstr+="%s\n" % category
    p1str+="bmodel\n"
    p2str+="1\n"
    ratestr+="1\n"
#    binstr = "bin  %s  %s  %s\n" % (category, category, category)
#    p1str = "process  %s  %s  %s\n" % ("smodel1", "smodel2", "bmodel")
#    p2str = "process  -1  0  1\n"
#    ratestr = "rate  1  1  1\n"
    fout.write(binstr)
    fout.write(p1str)
    fout.write(p2str)
    fout.write(ratestr)
    fout.write(("-"*40) + "\n")
    for x in uncStrings:
        fout.write("%s\n" % x)
    fout.close()

def generate(variables, (data, mcbg, mcsig), **wargs):
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
        if wargs["analytic"]==0:
            #   with templates as histos
            generateTemplate(fulllimitspath, variable, hdata, mch, mchsig, **wargs)
        else:
            #   with RooFit Workspace in the outpu
            generateAnalytic(fulllimitspath, variable, hdata, mch, mchsig, **wargs)

#
#   Analytic Datacard Preparation
#
def generateAnalytic(fulllimitspath, variable, hdata, backgrounds, signals, **wargs):
    from time import sleep
    category = variable["fullpath"].split("/")[0]
    mass = wargs["mass"]
    smode = wargs["smode"]

    #
    #   Prepare the Data for Workspace
    #
    print "-"*40
    print "Prepare the Data histogram"
    hdata = prepareHistogram(hdata, name="newhdata", **wargs)
    nbins = hdata.GetNbinsX()
    massmin = hdata.GetBinLowEdge(1)
    massmax = massmin + nbins*hdata.GetBinWidth(1)
    ndata = int(hdata.Integral())

    #   suppress msgs
    R.RooMsgService.instance().setGlobalKillBelow(R.RooFit.FATAL)

    #   workspace
    wspace = R.RooWorkspace("higgs")

    #
    #   Prepare all the Observable Variables and import data
    #
    print "-"*40
    print "Create the Observable Variable and Import the RooDataHist"
    wspace.factory("x[125.0, %f, %f]" % (massmin, massmax))
    wspace.var('x').SetTitle('m_{#mu#mu}')
    wspace.var('x').setUnit('GeV')
    wspace.defineSet("obs", "x")
    obs = wspace.set("obs")
    data = R.RooDataHist("data_obs", "data_obs", RooArgList(obs), hdata)
    getattr(wspace, "import")(data, RooCmdArg())

    #
    #   prepare Signal Model
    #
    print "-"*40
    print "prepare Signal Models"
    prepareSignalModel(wspace, signals, fulllimitspath=fulllimitspath, category=category, obs=obs, **wargs)

    #
    #   Build the Background
    #
    print "-"*40
    print "Build Background Models"
    if wargs["bmodel"]=="ExpGaus":
        createVariables_ExpGaus(wspace, ndata=ndata, category=category)
        bmodel  = buildModel_ExpGaus(wspace, ndata=ndata, category=category)

    #
    #   save the workspace
    #
    print "-"*40
    print "Save Workspace"
    filename = fulllimitspath+"/shape__analytic__%s__%s__%s__%s__%s.root" % (
        category, mass, wargs["bmodel"], wargs["smode"], wargs["smodel"])
    wspace.SaveAs(filename)

    #
    #   Generate the Datacard
    #   - rates for signal are given thru the model_norm
    #
    print "-"*40
    print "Build Datacard"
    if smode=="Combined":
        buildDatacard_analytic_Combined(category=category, fulllimitspath=fulllimitspath,
            **wargs)
    elif smode=="Separate":
        buildDatacard_analytic_Separate(category=category, signals=signals, 
            fulllimitspath=fulllimitspath, **wargs)

#
#   Template Datacard Preparation
#
def generateTemplate(fulllimitspath, variable, hdata, backgrounds, signals, **wargs):
    category = variable["fullpath"].split("/")[0]
    mass =wargs["mass"]
    filename = fulllimitspath+"/shape__templates__%s__%s.root" % (category, mass)
    f = R.TFile(filename, "recreate")

    massmin = wargs["massmin"]; massmax = wargs["massmax"]; nbins = massmax - massmin
    data_obs = R.TH1D("data_obs", "data_obs", nbins, massmin, massmax)
    newibin = 0
    for ibin in range(hdata.GetNbinsX()):
        if hdata.GetBinCenter(ibin+1)>massmin and hdata.GetBinCenter(ibin+1)<massmax:
            data_obs.SetBinContent(newibin+1, hdata.GetBinContent(ibin+1))
            newibin+=1
    data_obs.Write()

    fout = open(fulllimitspath+"/datacard__templates__%s__%s.txt" % (
        category, mass), "w")
    fout.write("imax 1\n")
    fout.write("jmax %d\n" % (len(signals)+len(backgrounds)-1))
    fout.write("kmax *\n")
    fout.write(("-"*40) + "\n")
    fout.write("shapes * * %s $PROCESS\n" % ("shape__templates__%s__%s.root" % (
        category, mass)))
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
    # new categories
    category = "1bJets"
    var1bJets = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "1bJets4l"
    var1bJets4l = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "1bJets4l2Mu2e"
    var1bJets4l2Mu2e = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "1bJets4l3Mu1e"
    var1bJets4l3Mu1e = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "1bJets4l4Mu"
    var1bJets4l4Mu = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "1bJets3l"
    var1bJets3l = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "1bJets2l"
    var1bJets2l = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "0bJets"
    var0bJets = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "0bJets4l"
    var0bJets4l = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "0bJets4l2Mu1e"
    var0bJets4l2Mu1e = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "0bJets4l3Mu0e"
    var0bJets4l3Mu0e = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "0bJets4l3Mu1e"
    var0bJets4l3Mu1e = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "0bJets4l4Mu0e"
    var0bJets4l4Mu0e = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
        "max": -0.999 if x!="DiMuonMass" else 160,
        "category":category, "fullpath":"%s%s/%s"%(marker,
        category, x)} for x in varNames]
    category = "0bJets4l2Mu2e"
    var0bJets4l2Mu2e = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110,
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
    # new categories
    #s = """
    variables.extend(var1bJets)
    variables.extend(var1bJets4l)
    variables.extend(var1bJets4l2Mu2e)
    variables.extend(var1bJets4l3Mu1e)
    variables.extend(var1bJets4l4Mu)
    variables.extend(var1bJets3l)
    variables.extend(var1bJets2l)
    variables.extend(var0bJets)
    variables.extend(var0bJets4l)
    variables.extend(var0bJets4l2Mu1e)
    variables.extend(var0bJets4l3Mu0e)
    variables.extend(var0bJets4l3Mu1e)
    variables.extend(var0bJets4l4Mu0e)
    variables.extend(var0bJets4l2Mu2e)
    #"""

    #
    #   Choose the Data Results to use
    #
    datajson = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
    jsons = S.jsonfiles
    intlumi = -1
    for k in jsons:
        if jsons[k].filename==datajson:
            intlumi = jsons[k].intlumi
    resultpathname = os.path.join(resultsdir,
        "result__merged__%s__%s.root" % (datajson[:-4], aux))
    data2016_M22 = {"name" : "2016_ReReco", "label" : "2016 ReReco %.1f/fb" % (intlumi/1000),
        "result" : resultpathname,  "luminosity":intlumi,
        "json" : datajson}

    #
    #   Choose the MC Samples to be used Signal and Background
    #
    cmssws = ["80X"]
    signals = [
        'GluGlu_HToMuMu_M125_13TeV_powheg_pythia8',
        'VBF_HToMuMu_M125_13TeV_powheg_pythia8',
        "WMinusH_HToMuMu_M125_13TeV_powheg_pythia8",
        "WPlusH_HToMuMu_M125_13TeV_powheg_pythia8",
        "ZH_HToMuMu_M125_13TeV_powheg_pythia8"
    ]
    backgrounds = {
            'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' : R.kBlue,
            "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" : R.kGreen,
            "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8" : R.kYellow,
            "WWTo2L2Nu_13TeV-powheg-herwigpp" : R.kGray,
            "WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8" : R.kViolet
#            'TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8' : R.kGreen
#            'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' : R.kGreen
    }
    pus = ["68", "69", "70", "71", "72", "71p3", "69p2"]
#    pus = ["68", "69","71", "72",]
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
    smodels = ["SingleGaus", "DoubleGaus"]
    smodes = ["Separate", "Combined"]
    analytic = True
    if analytic:
        for smodel in smodels:
            for smode in smodes:
                for cmssw in ["80X"]:
                    for pu in pus:
                        generate(variables, (data2016_M22,
                            mcbkgs["%s__%s" % (cmssw, pu)],
                            mcsignals["%s__%s" % (cmssw, pu)]), analytic=1, smodel=smodel, bmodel="ExpGaus", smode=smode, mass=125, massmin=110, massmax=160, fitmin=115, fitmax=135)
    else:
        for cmssw in ["80X"]:
            for pu in pus:
                generate(variables, (data2016_M22,
                    mcbkgs["%s__%s" % (cmssw, pu)],
                    mcsignals["%s__%s" % (cmssw, pu)]), analytic=0, mass=125,
                    massmin=110, massmax=160)
