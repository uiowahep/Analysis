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

## Modify input and output locations - AWB 23.02.17
resultsdir    = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/input_hists'
workspacesDir = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/workspaces'
fitsDir       = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/bkg_fits'
path_modifier = 'AWB_Feb23_test'

workspacesDir= os.path.join(workspacesDir, os.path.split(resultsdir)[1] + "__" +
    path_modifier)
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
    mkdir(fullWorkspacesDir) # is the one to be used
    mkdir(fullFitsDir)

    counter = 0
    numvars = len(variables)
    for variable in variables:
        savemodifier = ""
        mchsig = {}
        mcfsig = {}
        category = variable["fullpath"].split("/")[0]

        #
        # Procedure:
        # 1. Get data, slice histo and convert to RooDataHist
        # 2. [Optional] Scale all bkgs, add them up and....
        # 3. Create all parameters, create the background model
        # 4. Save the workspace with data and background model
        #

        #
        # Get data and prepare Data HIstogram
        #
        fdata = R.TFile(data.pathToFile)
        hdata = fdata.Get(variable["fullpath"])
        if hdata.GetEntries()==0:
            continue
        slicedhdata = sliceHistogram(hdata, name="newhdata", **wargs)
        ndata = int(slicedhdata.Integral())

        #
        # Background Histograms
        #
        mch = {}
        mcf = {}
        for imcbg in mcbg:
            mcf[imcbg.name] = R.TFile(imcbg.pathToFile)
            mch[imcbg.name] = mcf[imcbg.name].Get(variable["fullpath"])
            mch[imcbg.name].Scale(
                data.jsonToUse.intlumi*imcbg.cross_section/imcbg.eweight)

        # 0. create a workspace or extract from the existing
        try:
            fileName = fullWorkspacesDir +\
                "/workspace__analytic__%s__%s__%s__%s__%s.root" % (
                    category, 
                    wargs["mass"], wargs["bmodel"], wargs["smode"], wargs["smodel"])
            wsFile = R.TFile(fileName, "UPDATE")
            ws = wsFile.Get("higgs")
            # this will raise if there is no ws
            print ws.allPdfs().contentsString()
            appending = True
        except:
            ws = R.RooWorkspace("higgs")
            appending = False
        R.RooMsgService.instance().setGlobalKillBelow(R.RooFit.FATAL)
#        ws = R.RooWorkspace("higgs")
        models.createVariables_Mass(ws, **wargs)
        ws.defineSet("obs", "x")
        obs = ws.set("obs")

        #
        # Data RooDataHist creation and preserving in Workspace
        #
        roodata = R.RooDataHist("data_obs", "data_obs", RooArgList(obs), slicedhdata)
        getattr(ws, "import")(roodata, RooCmdArg())

        #
        # Create parameters for background
        #
        modelklass = getattr(models, wargs["bmodel"])
        model = modelklass(category=category)
        model.createParameters(ws, ndata=ndata)
        roomodel = model.build(ws)
        ws.Print("v")
        
        #
        # just do some fit
        #
        r = roomodel.fitTo(roodata, RooFit.Save())
        ccc = TCanvas("c1", "c1", 800, 600)
        ccc.cd()
        frame = ws.var("x").frame()
        frame.SetTitle(category)
        roodata.plotOn(frame)
        roomodel.plotOn(frame, RooFit.Color(kRed))
        roomodel.paramOn(frame, RooFit.Format("NELU", RooFit.AutoPrecision(2)), 
            RooFit.Layout(0.6, 0.99, 0.9), RooFit.ShowConstants(True))
        frame.getAttText().SetTextSize(0.02)
        chiSquare = frame.chiSquare()
        ttt = R.TPaveLabel(0.1,0.7,0.3,0.78, Form("#chi^{2} = %f" % chiSquare),
            "brNDC")
        ttt.Draw()
        frame.addObject(ttt)
        frame.Draw()
        ccc.SaveAs(fullFitsDir + 
            "/bkgfit__%s__%s__%s__%s__%s.png" % (
            category, wargs["mass"], wargs["bmodel"], wargs["smode"], wargs["smodel"]))

        fileName = fullWorkspacesDir+\
            "/workspace__analytic__%s__%s__%s__%s__%s.root" % (
            category, wargs["mass"], wargs["bmodel"], wargs["smode"], wargs["smodel"])
        if not appending:
            ws.SaveAs(fileName)
        else:
            ws.Write()
            wsFile.Write()
            wsFile.Close()

#
#   start...
#
if __name__=="__main__":
    ## Use UF categories - AWB 23.02.17
    from categories_UF_AWB import *
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

    ## I *think* this is just used as a label ... the file is never used - AWB 23.02.17
    # datajson = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
    datajson = "Moriond17_Feb08.txt"

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

    ## Leave out all MC backgrounds for now, only one PU - AWB 23.02.17
    backgrounds = []
    pus = ["69"]

    configs_signals = {}
    configs_bkgs = {}
    shouldScale = False
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
#    smodels = ["TripleGaus"]
#    smodes = ["Separate", "Combined"]
    smodes = ["Separate"]
    analytic = True
    if analytic:
        for smodel in smodelNames:
            for smode in smodes:
                for cmssw in ["80X"]:
                    for pu in pus:
                        generate(variables, (data,
                            configs_bkgs["%s__%s" % (cmssw, pu)],
                            configs_signals["%s__%s" % (cmssw, pu)]), analytic=1, smodel=smodel, bmodel="ExpGaus", smode=smode, mass=125, massmin=110, massmax=160, fitmin=115, fitmax=135)
    else:
        for cmssw in ["80X"]:
            for pu in pus:
                generate(variables, (data2016_M22,
                    mcbkgs["%s__%s" % (cmssw, pu)],
                    mcsignals["%s__%s" % (cmssw, pu)]), analytic=0, mass=125,
                    massmin=110, massmax=160)
