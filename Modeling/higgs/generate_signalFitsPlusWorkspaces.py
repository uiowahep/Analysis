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
import models

#
#   List all the constants and some initializations
#
resultsdir = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/vR1_20170217_1742"
#resultsdir = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/test"
workspacesDir = "/Users/vk/software/Analysis/files/higgs_analysis_files/datacards_and_workspaces"
fitsDir = "/Users/vk/software/Analysis/files/higgs_analysis_files/fits/signal_precombine"
path_modifier = "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkg"

#
# build up the dir structure
#
workspacesDir = os.path.join(
    workspacesDir, os.path.split(resultsdir)[1] + "__" + path_modifier)
fitsDir = os.path.join(
    fitsDir, os.path.split(resultsdir)[1] + "__" + path_modifier)
mkdir(workspacesDir)
mkdir(fitsDir)
default = -0.999
aux = "Mu24"

def generate(variables, (data, mcbg, mcsig), **wargs):
    print "-"*40
    print data
    print mcbg
    print mcsig
    shouldScale = wargs["shouldScale"]

    #   Create the pic directory
    sub = "" if aux==None or aux=="" else "__%s" % aux
    fullWorkspacesDir = os.path.join(workspacesDir,
        "%s__%s%s" % (mcsig[0].initial_cmssw,
        data.jsonToUse.filename[:-4], sub))
    fullFitsDir = os.path.join(fitsDir,
        "%s__%s%s" % (mcsig[0].initial_cmssw,
        data.jsonToUse.filename[:-4], sub))
    mkdir(fullWorkspacesDir)
    mkdir(fullFitsDir)
    fullWorkspacesDir+="/%s"%mcsig[0].pu
    fullFitsDir+="/%s"%mcsig[0].pu
    mkdir(fullFitsDir)
    mkdir(fullWorkspacesDir) # is the one to be used

    counter = 0
    numvars = len(variables)
    for variable in variables:
        savemodifier = ""
        mchsig = {}
        mcfsig = {}
        category = variable["fullpath"].split("/")[0]

        #
        # initialize the workspace
        #
        R.RooMsgService.instance().setGlobalKillBelow(R.RooFit.FATAL)

        #
        # either retrieve the existing one (if u ran background first)
        # or create a new one
        #
        try:
            fileName = fullWorkspacesDir +\
                "/workspace__analytic__%s__%s__%s__%s__%s.root" % (
                    category,
                    wargs["mass"], wargs["bmodel"], wargs["smode"], wargs["smodel"])
            wsFile = R.TFile(fileName, "UPDATE")
            ws = wsFile.Get("higgs")
            appending = True
            # this will raise if there is no ws
            print ws.allPdfs().contentsString()
            testModelName = getattr(models, wargs["smodel"])(category=category, 
                processName="VBF").getModelName()
            if testModelName in ws.allPdfs().contentsString():
                print "Duplicates are already present! Removing the file!"
                wsFile.Close()
                os.systme("rm %s" % fileName)
                ws = R.RooWorkspace("higgs")
                appending = False
                models.createVariables_Mass(ws, **wargs)
                ws.defineSet("obs", "x")
        except:
            ws = R.RooWorkspace("higgs")
            appending = False
            models.createVariables_Mass(ws, **wargs)
            ws.defineSet("obs", "x")
        
        obs = ws.set("obs")
        #models.createVariables_Mass(ws, **wargs)

        #
        # for each signal
        #   1. scale
        #   2. aux initializations/manipulations -> build a RooDatHist
        #   3. create model and fit
        #   4. plot all fits and save
        #   5. save plots
        #
        for mc in mcsig:
            print mc
            print variable
            print mc.pathToFile
            fff = R.TFile(mc.pathToFile)
            sss = fff.Get(variable["fullpath"])

            #
            # 1. scale
            #
            if shouldScale:
                sss.Scale(
                    data.jsonToUse.intlumi*mc.cross_section/mc.eweight)

            #
            # 2
            #
            ccc = TCanvas("c1", "c1", 800, 600)
            ccc.cd()
            newsss = sliceHistogram(sss, name=mc.buildLabel(),
                massmin=wargs["massmin"], massmax=wargs["massmax"])
            roo_hist = R.RooDataHist(newsss.GetName(),
                newsss.GetName(), RooArgList(obs), newsss)
            xframe = ws.var("x").frame()
            xframe.SetTitle(category)
            processName = mc.buildLabel()

            #
            # 3. model
            #
            modelklass = getattr(models, wargs["smodel"])
            model = modelklass(category=category, processName=processName)
            model.createParameters(ws, massmin=wargs["massmin"], massmax=wargs["massmax"])
            roomodel = model.build(ws)
            r = roomodel.fitTo(roo_hist, RooFit.Save(), RooFit.Range(wargs["fitmin"],
                wargs["fitmax"]))
            model.setParameters(ws, norm=roo_hist.sumEntries())

            #
            # 4. plot/save fits
            #
            r.Print("v")
            #s.plotOn(xframe, RooFit.DataError(RooAbsData.SumW2))
            roo_hist.plotOn(xframe)
            roomodel.plotOn(xframe, RooFit.Color(kRed))
            roomodel.paramOn(xframe, RooFit.Format("NELU", RooFit.AutoPrecision(2)), RooFit.Layout(0.6, 0.99, 0.9), RooFit.ShowConstants(True))
            xframe.getAttText().SetTextSize(0.02)
            chiSquare = xframe.chiSquare()
            #txt = R.TText(2, 100, "#chi^{2} = %f" % chiSquare)
            ttt = R.TPaveLabel(0.1,0.7,0.3,0.78, Form("#chi^{2} = %f" % chiSquare),
                "brNDC");
            ttt.Draw()
            xframe.addObject(ttt)
            xframe.Draw()
            #latex.DrawLatex(0.4, 0.9, "#chi^{2} = %f" % chiSquare)
            ccc.SaveAs(fullFitsDir+"/fit__%s__%s__%s__%s__%s__%s.png" % (
                roo_hist.GetName(), 
                category, wargs["mass"], wargs["bmodel"], wargs["smode"],
                wargs["smodel"]))

            xframe2 = ws.var("x").frame()
            xframe2.addObject(xframe.pullHist())
            xframe2.SetMinimum(-5)
            xframe2.SetMaximum(5)
            xframe2.Draw()
            ccc.SaveAs(fullFitsDir+"/pull__%s__%s__%s__%s__%s__%s.png" % (
                roo_hist.GetName(), category, wargs["mass"], wargs["bmodel"], wargs["smode"],
                wargs["smodel"]))

            xframe3 = ws.var("x").frame()
            xframe3.addObject(xframe.residHist())
            xframe3.SetMinimum(-5)
            xframe3.SetMaximum(5)
            xframe3.Draw()
            ccc.SaveAs(fullFitsDir+"/resid__%s__%s__%s__%s__%s__%s.png" % (
                roo_hist.GetName(), category, wargs["mass"], wargs["bmodel"], wargs["smode"],
                wargs["smodel"]))

        #
        # 5.either update or create
        #
        fileName = fullWorkspacesDir+\
            "/workspace__analytic__%s__%s__%s__%s__%s.root" % (
            category, wargs["mass"], wargs["bmodel"], wargs["smode"], wargs["smodel"])
        if not appending:
            ws.SaveAs(fileName)
        else:
            wsFile.cd()
            ws.Write()
            wsFile.Write()
            wsFile.Close()

#
#   start...
#
if __name__=="__main__":
    from categories import *
    from aux import *
    variables = dimuonMassVariablesRun1
    #variables = dimuonMassVariablesRun1
    jsons = S.jsonfiles
    mcsamples = S.mcMoriond2017datasets

    #
    #   Choose the Data Results to use
    #   - some name
    #   - year
    #   - json file with integrated lumi
    #   - path to the file with histograms
    #
    datajson = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
    jsonToUse = None
    for k in jsons:
        if jsons[k].filename==datajson:
            jsonToUse = jsons[k]
            break;
    resultPathName = os.path.join(resultsdir,
        "result__merged__%s__%s.root" % (datajson[:-4], aux))
    data = DataResult(name="ReReco", year="2016",
        jsonToUse=jsonToUse, pathToFile=resultPathName)

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
    backgrounds = [
            ("WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",R.kYellow),
            ("WWTo2L2Nu_13TeV-powheg-herwigpp",R.kGray),
            ("WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8", R.kViolet),
            ("TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",R.kGreen),
            ('DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',R.kBlue),
#            'TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8' : R.kGreen
#            'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' : R.kGreen
    ]
#    pus = ["68", "69", "70", "71", "72", "71p3", "69p2"]
    #pus = ["68", "69", "71", "72", "70", "69p2", "71p3"]
    pus = ["69"]
    configs_signals = {}
    configs_bkgs = {}
    shouldScale = True
    for cmssw in cmssws:
        for pu in pus:
            oneconfig_signals = []
            oneconfig_bkgs = []
            for s in signals:
                for k in mcsamples:
                    if s in k and cmssw==mcsamples[k].initial_cmssw:
                        pathToFile = os.path.join(resultsdir,
                            "result__%s__%s__%s__%s__%s.root" % (s, cmssw,
                            datajson[:-4], pu+"mb", aux))
                        mc = MCResult(mc=mcsamples[k], pu=pu, pathToFile=pathToFile,
                            eweight=None if not shouldScale else getEventWeights(pathToFile),
                            options={"color":None})
                        oneconfig_signals.append(mc)
            for b in backgrounds:
                for k in mcsamples:
                    if b[0] in k and cmssw==mcsamples[k].initial_cmssw:
                        pathToFile = os.path.join(resultsdir,
                            "result__%s__%s__%s__%s__%s.root" % (b[0], cmssw,
                            datajson[:-4], pu+"mb", aux))
                        mc = MCResult(mc=mcsamples[k], pu=pu, pathToFile=pathToFile,
                            eweight=None if not shouldScale else getEventWeights(pathToFile),
                            options={"color":b[1]})
                        oneconfig_bkgs.append(mc)
            configs_signals["%s__%s" % (cmssw, pu)] = oneconfig_signals
            configs_bkgs["%s__%s" % (cmssw, pu)] = oneconfig_bkgs


    #
    #   Generate all the distributions
    #
    smodelNames = ["SingleGaus", "DoubleGaus", "TripleGaus"]
    bmodelNames = ["ExpGaus", "Polynomial", "Bernstein"]
#    smodels = ["TripleGaus"]
#    smodes = ["Separate", "Combined"]
    smodes = ["Separate"]
    analytic = True
    if analytic:
        for smodel in smodelNames:
            for smode in smodes:
                for bmodel in bmodelNames:
                    for cmssw in ["80X"]:
                        for pu in pus:
                            generate(variables, (data,
                                configs_bkgs["%s__%s" % (cmssw, pu)],
                                configs_signals["%s__%s" % (cmssw, pu)]), analytic=1, smodel=smodel, bmodel=bmodel, smode=smode, mass=125, massmin=110, massmax=160, fitmin=115, fitmax=135, shouldScale=shouldScale)
    else:
        for cmssw in ["80X"]:
            for pu in pus:
                generate(variables, (data2016_M22,
                    mcbkgs["%s__%s" % (cmssw, pu)],
                    mcsignals["%s__%s" % (cmssw, pu)]), analytic=0, mass=125,
                    massmin=110, massmax=160)
