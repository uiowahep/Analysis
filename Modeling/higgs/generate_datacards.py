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
from uncertainty import *
uncertaintiesToUse = uncertainties_vR1

#
#   List all the constants and some initializations
#
resultsdir = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/test"
workspacesDir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/workspaces"
datacardsDir = "/Users/vk/software/Analysis/files/higgs_analysis_files/datacards"
path_modifier = "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkg"

#
# build up the path to dir
# 
datacardsDir = os.path.join(
    datacardsDir, os.path.split(resultsdir)[1] + "__" + path_modifier)
workspacesDir = os.path.join(
    workspacesDir, os.path.split(resultsdir)[1] + "__" + path_modifier)
mkdir(datacardsDir)
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
    fullDatacardsDir = os.path.join(datacardsDir,
        "%s__%s%s" % (mcsig[0].initial_cmssw,
        data.jsonToUse.filename[:-4], sub))
    fullWorkspacesDir = os.path.join(workspacesDir,
        "%s__%s%s" % (mcsig[0].initial_cmssw,
        data.jsonToUse.filename[:-4], sub))
    mkdir(fullDatacardsDir)
    fullDatacardsDir+="/%s"%mcsig[0].pu
    fullWorkspacesDir+="/%s"%mcsig[0].pu
    mkdir(fullDatacardsDir) # is the one to be used

    counter = 0
    numvars = len(variables)
    for variable in variables:
        savemodifier = ""
        mchsig = {}
        mcfsig = {}
        category = variable["fullpath"].split("/")[0]

        signalChannels = []
        iii = 0
        for mc in mcsig:
            chl = PhysicsChannel(mc, wargs["smodel"], uncertaintiesToUse,
                myId=(-len(mcsig)+iii+1), category=category)
            signalChannels.append(chl)
            iii+=1

        pathToWorkspaceFile = fullWorkspacesDir + "/" + \
            "workspace__analytic__%s__%s__%s__%s__%s.root" % (
                category, wargs["mass"], wargs["bmodel"], 
                wargs["smode"], wargs["smodel"])
        bkgchl = BackgroundChannel(wargs["bmodel"], uncertaintiesToUse, myId=1,
            category=category)
        card = Datacard(category, signalChannels, bkgchl, data, 
            pathToWorkspaceFile=pathToWorkspaceFile)
        stringCard = card.build()

        fileName = fullDatacardsDir+\
            "/datacard__analytic__%s__%s__%s__%s__%s.txt" % (
            category, wargs["mass"], wargs["bmodel"], wargs["smode"], wargs["smodel"])
        f = open(fileName, "w")
        f.write(stringCard)
        f.close()

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
                            configs_signals["%s__%s" % (cmssw, pu)]), analytic=1, smodel=smodel, bmodel="ExpGaus", smode=smode, mass=125, massmin=110, massmax=160, fitmin=115, fitmax=135, shouldScale=shouldScale)
    else:
        for cmssw in ["80X"]:
            for pu in pus:
                generate(variables, (data2016_M22,
                    mcbkgs["%s__%s" % (cmssw, pu)],
                    mcsignals["%s__%s" % (cmssw, pu)]), analytic=0, mass=125,
                    massmin=110, massmax=160)
