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
from aux import *
from models import *

#
#   List all the constants and some initializations
#
libdir="/Users/vk/software/Analysis/build-4"
resultsdir = "/Users/vk/software/Analysis/files/results/vR1_20170217_1742"
#resultsdir = "/Users/vk/software/Analysis/files/results/vR2_20170125_1204"
signalWorkspacesDir = "/Users/vk/software/Analysis/files/signal_workspaces_fits"
path_modifier = "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkg"
signalWorkspacesDir = os.path.join(
    signalWorkspacesDir, os.path.split(resultsdir)[1] + "__" + path_modifier)
mkdir(signalWorkspacesDir)
default = -0.999
R.gSystem.Load(libdir+"/libAnalysisNtupleProcessing.dylib")
R.gSystem.Load(libdir+"/libAnalysisCore.dylib")
aux = "Mu24"

def getEventWeights(resultpathname):
    print resultpathname
    f = R.TFile(resultpathname)
    h = f.Get("eventWeights")
    return h.GetBinContent(1)

#
#   Prepare the Signals Models - Build/Fit/Fix
#
def prepareSignalModel(ws, signals, **wargs):
    smode = wargs["smode"]
    category = wargs["category"]
    fullSignalWorkspacesDir = wargs["fullSignalWorkspacesDir"]
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
        newhist = sliceHistogram(signal, name="signal", massmin=wargs["massmin"],
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
            createParameters_DoubleGaus(ws, processName=processName, **wargs)
            smodel = buildModel_DoubleGaus(ws, processName=processName, **wargs)
            r = smodel.fitTo(roo_hist, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                wargs["fitmax"]))
            setParameters_DoubleGaus(ws, processName=processName, norm=roo_hist.sumEntries(),
                **wargs)
        elif wargs["smodel"]=="SingleGaus":
            createParameters_SingleGaus(ws, processName=processName, **wargs)
            smodel = buildModel_SingleGaus(ws, processName=processName, **wargs)
            r = smodel.fitTo(roo_hist, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                wargs["fitmax"]))
            setParameters_SingleGaus(ws, processName=processName, norm=roo_hist.sumEntries(),
                **wargs)
        elif wargs["smodel"]=="TripleGaus":
            createParameters_TripleGaus(ws, processName=processName, **wargs)
            smodel = buildModel_TripleGaus(ws, processName=processName, **wargs)
            r = smodel.fitTo(roo_hist, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                wargs["fitmax"]))
            setParameters_TripleGaus(ws, 
                processName=processName, norm=roo_hist.sumEntries(),**wargs)
        r.Print("v")
        roo_hist.plotOn(xframe)
        smodel.plotOn(xframe, RooFit.Color(kRed))
        smodel.paramOn(xframe)
        xframe.Draw()
        c.SaveAs(fullSignalWorkspacesDir+"/%s__%s__%s__%s__%s__%s.png" % (
            processName, category, wargs["mass"], wargs["bmodel"], wargs["smode"],
            wargs["smodel"]))
    elif smode=="Separate":
        lsignals = []
        #   convert all of histos into RooDataHist
        for name in signals:
            newhist = sliceHistogram(signals[name], name=name.split("_")[0],
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
                createParameters_DoubleGaus(ws, processName=processName, **wargs)
                smodel = buildModel_DoubleGaus(ws, processName=processName, **wargs)
                r = smodel.fitTo(s, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                    wargs["fitmax"]))
                setParameters_DoubleGaus(ws, processName=processName, norm=s.sumEntries(),
                    **wargs)
            elif wargs["smodel"]=="SingleGaus":
                createParameters_SingleGaus(ws, processName=processName, **wargs)
                smodel = buildModel_SingleGaus(ws, processName=processName, **wargs)
                r = smodel.fitTo(s, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                    wargs["fitmax"]))
                setParameters_SingleGaus(ws, processName=processName, norm=s.sumEntries(),
                    **wargs)
            elif wargs["smodel"]=="TripleGaus":
                createParameters_TripleGaus(ws, processName=processName, **wargs)
                smodel = buildModel_TripleGaus(ws, processName=processName, **wargs)
                r = smodel.fitTo(s, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                    wargs["fitmax"]))
                setParameters_TripleGaus(ws, processName=processName, norm=s.sumEntries(),
                    **wargs)

            r.Print("v")
            #s.plotOn(xframe, RooFit.DataError(RooAbsData.SumW2))
            s.plotOn(xframe)
            smodel.plotOn(xframe, RooFit.Color(kRed))
            smodel.paramOn(xframe, RooFit.Format("NELU", RooFit.AutoPrecision(2)), RooFit.Layout(0.6, 0.99, 0.9), RooFit.ShowConstants(True))
            xframe.getAttText().SetTextSize(0.02)
            chiSquare = xframe.chiSquare()
            #txt = R.TText(2, 100, "#chi^{2} = %f" % chiSquare)
            ttt = R.TPaveLabel(0.1,0.7,0.3,0.78, Form("#chi^{2} = %f" % chiSquare),
                "brNDC");
            ttt.Draw()
            xframe.addObject(ttt)
            xframe.Draw()
            #latex.DrawLatex(0.4, 0.9, "#chi^{2} = %f" % chiSquare)
            c.SaveAs(fullSignalWorkspacesDir+"/%s__%s__%s__%s__%s__%s.png" % (
                s.GetName(), category, wargs["mass"], wargs["bmodel"], wargs["smode"],
                wargs["smodel"]))

            xframe2 = ws.var("x").frame()
            xframe2.addObject(xframe.pullHist())
            xframe2.SetMinimum(-5)
            xframe2.SetMaximum(5)
            xframe2.Draw()
            c.SaveAs(fullSignalWorkspacesDir+"/pull__%s__%s__%s__%s__%s__%s.png" % (
                s.GetName(), category, wargs["mass"], wargs["bmodel"], wargs["smode"],
                wargs["smodel"]))
            
            xframe3 = ws.var("x").frame()
            xframe3.addObject(xframe.residHist())
            xframe3.SetMinimum(-5)
            xframe3.SetMaximum(5)
            xframe3.Draw()
            c.SaveAs(fullSignalWorkspacesDir+"/resid__%s__%s__%s__%s__%s__%s.png" % (
                s.GetName(), category, wargs["mass"], wargs["bmodel"], wargs["smode"],
                wargs["smodel"]))

            imc+=1

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

    #   Create the pic directory
    sub = "" if aux==None or aux=="" else "__%s" % aux
    fullSignalWorkspacesDir = os.path.join(signalWorkspacesDir, 
        "%s__%s%s" % (mcsig[0]["cmssw"],
        data["json"][:-4], sub))
    mkdir(fullSignalWorkspacesDir)
    fullSignalWorkspacesDir+="/%s"%mcsig[0]["PU"]
    mkdir(fullSignalWorkspacesDir) # is the one to be used

    counter = 0
    numvars = len(variables)
    for variable in variables:
        savemodifier = ""
        mchsig = {}
        mcfsig = {}
        category = variable["fullpath"].split("/")[0]
        # scale the signal
        for imcsig in mcsig:
            mcfsig[imcsig["name"]] = R.TFile(imcsig["result"])
            mchsig[imcsig["name"]] = mcfsig[imcsig["name"]].Get(variable["fullpath"])
            mchsig[imcsig["name"]].Scale(data["luminosity"]*imcsig["xsection"]/imcsig["eweight"])
        
        #
        # generate:
        # 1. Signal Model with RooFit Workspace
        # 2. Perform the Fit.
        # 3. Fix the parameters and save the workspace.
        # 4. Save the plots of the fit
        # 5. Save the Workspace

        # 0. create a workspace
        R.RooMsgService.instance().setGlobalKillBelow(R.RooFit.FATAL)
        ws = R.RooWorkspace("higss")
        createVariables_Mass(ws, **wargs)
        ws.defineSet("obs", "x")
        obs = ws.set("obs")

        # 1. - 4.
        prepareSignalModel(ws, mchsig, fullSignalWorkspacesDir=fullSignalWorkspacesDir,
            category=category, obs=obs, **wargs)

        # 5.
        fileName = fullSignalWorkspacesDir+\
            "/shape__signal__analytic__%s__%s__%s__%s__%s.root" % (
            category, wargs["mass"], wargs["bmodel"], wargs["smode"], wargs["smodel"])
        ws.SaveAs(fileName)

#
#   start...
#
if __name__=="__main__":
    #   define the variable
    from categories import *
    variables = dimuonMassVariablesRun1

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
#    pus = ["68", "69", "70", "71", "72", "71p3", "69p2"]
#    pus = ["68", "69","71", "72",]
    pus = ["69"]
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
#    smodels = ["SingleGaus", "DoubleGaus", "TripleGaus"]
    smodels = ["TripleGaus"]
#    smodes = ["Separate", "Combined"]
    smodes = ["Separate"]
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
