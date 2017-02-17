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
resultsdir = "/Users/vk/software/Analysis/files/results/vR1_20170122_1326"
#resultsdir = "/Users/vk/software/Analysis/files/results/vR2_20170125_1204"
workspacesDir = "/Users/vk/software/Analysis/files/bkgdata_workspaces"
path_modifier = "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkg"
path = os.path.join(workspacesDir, os.path.split(resultsdir)[1] + "__" + 
    path_modifier)
mkdir(workspacesDir)
default = -0.999
R.gSystem.Load(libdir+"/libAnalysisNtupleProcessing.dylib")
R.gSystem.Load(libdir+"/libAnalysisCore.dylib")
aux = "Mu24"

def getEventWeights(resultpathname):
    print resultpathname
    f = R.TFile(resultpathname)
    h = f.Get("eventWeights")
    return h.GetBinContent(1)

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
    fullWorkspacesDir = os.path.join(workspacesDir, 
        "%s__%s%s" % (mcsig[0]["cmssw"],
        data["json"][:-4], sub))
    mkdir(fullWorkspacesDir)
    fullWorkspacesDir+="/%s"%mcsig[0]["PU"]
    mkdir(fullWorkspacesDir) # is the one to be used

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
        fdata = R.TFile(data["result"])
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
            mcf[imcbg["name"]] = R.TFile(imcbg["result"])
            mch[imcbg["name"]] = mcf[imcbg["name"]].Get(variable["fullpath"])
            mch[imcbg["name"]].Scale(data["luminosity"]*imcbg["xsection"]/imcbg["eweight"])
            mch[imcbg["name"]].SetFillColor(imcbg["color"])

        # 0. create a workspace
        R.RooMsgService.instance().setGlobalKillBelow(R.RooFit.FATAL)
        ws = R.RooWorkspace("higss")
        createVariables_Mass(ws, **wargs)
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
        createParameters_ExpGaus(ws, ndata=ndata, category=category)
        bmodel  = buildModel_ExpGaus(ws, ndata=ndata, category=category)

        fileName = fullWorkspacesDir+\
            "/shape__bkgdata__analytic__%s__%s__%s__%s__%s.root" % (
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
