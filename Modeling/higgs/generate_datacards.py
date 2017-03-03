import ROOT as R
from ROOT import * ## We shouldn't need both this and the above - AWB 28.02.17
import sys, os, subprocess
import argparse
import AuxTools.python.common as CM

R.gROOT.SetBatch(R.kTRUE)

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose debugging output')
parser.add_argument('-m', '--mode', type=str, default='Iowa', help='Run in Iowa, UF_AWB, or UF_AMC mode')
args = parser.parse_args()

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

if (args.mode == 'Iowa'):
    from categories import *
    import AuxTools.python.Iowa_settings as SET
if (args.mode == 'UF_AWB'):
    from categories_UF_AWB import *
    import AuxTools.python.UF_AWB_settings as SET
if (args.mode == 'UF_AMC'):
    from categories_UF_AMC import *
    import AuxTools.python.UF_AMC_settings as SET

#
#   List all the constants and some initializations
#

## Modify input and output locations - AWB 23.02.17
resultsdir    = SET.in_hist_dir
workspacesDir = SET.workspaces_dir
datacardsDir  = SET.datacards_dir

CM.mkdir(datacardsDir)

default = -0.999
aux = "Mu24"

def generate(variables, (data, mcbg, mcsig), **wargs):
    if wargs["Verbose"]:
        print "-"*40
        print data
        print mcbg
        print mcsig
    shouldScale = wargs["shouldScale"]

    #   Create the pic directory
    sub = "" if aux==None or aux=="" else "__%s" % aux
    if wargs["UF"]:
        fullWorkspacesDir = SET.workspaces_dir
        fullDatacardsDir  = SET.datacards_dir
    else:
        fullDatacardsDir = os.path.join(datacardsDir,
            "%s__%s%s" % (mcsig[0].initial_cmssw,
            data.jsonToUse.filename[:-4], sub))
        fullWorkspacesDir = os.path.join(workspacesDir,
            "%s__%s%s" % (mcsig[0].initial_cmssw,
            data.jsonToUse.filename[:-4], sub))
        fullDatacardsDir+="/%s"%mcsig[0].pu
        fullWorkspacesDir+="/%s"%mcsig[0].pu

    CM.mkdir(fullDatacardsDir)

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
        print 'Wrote out datacard %s' % fileName
        f.close()

#
#   start...
#
if __name__=="__main__":

    variables = dimuonMassVariablesRun1
    jsons     = S.jsonfiles
    mcsamples = S.mcMoriond2017datasets

    #
    #   Choose the Data Results to use
    #   - some name
    #   - year
    #   - json file with integrated lumi
    #   - path to the file with histograms
    #

    datajson = SET.JSON
    jsonToUse = None
    for k in jsons:
        if jsons[k].filename==datajson:
            jsonToUse = jsons[k]
            break;
    if ('UF' in args.mode):
        resultPathName = '%s/MergedData.root' % resultsdir
    else:
        resultPathName = os.path.join(resultsdir,
            "result__merged__%s__%s.root" % (datajson[:-4], aux))

    data = DataResult(name="ReReco", year="2016",
        jsonToUse=jsonToUse, pathToFile=resultPathName)

    configs_signals = {}
    configs_bkgs = {}
    for cmssw in SET.cmssws:
        for pu in SET.pileups:
            oneconfig_signals = []
            oneconfig_bkgs = []
            for s in SET.signals:
                for k in mcsamples:
                    if s in k and cmssw==mcsamples[k].initial_cmssw:
                        pathToFile = os.path.join(resultsdir,
                            "result__%s__%s__%s__%s__%s.root" % (s, cmssw,
                            datajson[:-4], pu+"mb", aux))
                        mc = MCResult(mc=mcsamples[k], pu=pu, pathToFile=pathToFile,
                            eweight=None if not SET.scale_MC else getEventWeights(pathToFile),
                            options={"color":None})
                        oneconfig_signals.append(mc)
            for b in SET.backgrounds:
                for k in mcsamples:
                    if b[0] in k and cmssw==mcsamples[k].initial_cmssw:
                        pathToFile = os.path.join(resultsdir,
                            "result__%s__%s__%s__%s__%s.root" % (b[0], cmssw,
                            datajson[:-4], pu+"mb", aux))
                        mc = MCResult(mc=mcsamples[k], pu=pu, pathToFile=pathToFile,
                            eweight=None if not SET.scale_MC else getEventWeights(pathToFile),
                            options={"color":b[1]})
                        oneconfig_bkgs.append(mc)
            configs_signals["%s__%s" % (cmssw, pu)] = oneconfig_signals
            configs_bkgs["%s__%s" % (cmssw, pu)] = oneconfig_bkgs


    #
    #   Generate all the distributions
    #
    if SET.analytic:
        for smodel in SET.sig_models:
            for smode in SET.sig_modes:
                for cmssw in SET.cmssws:
                    for pu in SET.pileups:
                        generate( variables, (data, configs_bkgs["%s__%s" % (cmssw, pu)], configs_signals["%s__%s" % (cmssw, pu)]), 
                                  analytic=1, smodel=smodel, bmodel="ExpGaus", smode=smode, mass=SET.sig_M[0], 
                                  massmin=SET.bkg_M[1], massmax=SET.bkg_M[2], fitmin=SET.sig_M[3], fitmax=SET.sig_M[4], 
                                  shouldScale=SET.scale_MC, Verbose=args.verbose, UF=('UF' in args.mode) )
    else:
        for cmssw in SET.cmssws:
            for pu in SET.pileups:
                generate( variables, (data2016_M22, mcbkgs["%s__%s" % (cmssw, pu)], mcsignals["%s__%s" % (cmssw, pu)]), 
                          analytic=0, mass=SET.sig_M[0], massmin=SET.bkg_M[1], massmax=SET.bkg_M[2], 
                          Verbose=args.verbose, UF=('UF' in args.mode) )
