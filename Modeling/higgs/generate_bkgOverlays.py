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
from overlays import *

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

resultsdir    = SET.in_hist_dir
workspacesDir = SET.workspaces_dir
fitsDir       = SET.bkg_fits_dir

CM.mkdir(workspacesDir)
CM.mkdir(fitsDir)

default = -0.999
aux = "Mu24"

def generate(variables, (data, groupName, lModels), **wargs):
    if wargs["Verbose"]:
        print "-"*40
        print data
        print mcbg
        print mcsig

    smode = wargs["smode"]
    smodel = wargs["smodel"]
    mass = wargs["mass"]

    #   Create the pic directory
    sub = "" if aux==None or aux=="" else "__%s" % aux
    if wargs["UF"]:
        fullWorkspacesDir = SET.workspaces_dir
        fullFitsDir       = SET.bkg_fits_dir
    else:
        fullWorkspacesDir = os.path.join(workspacesDir,
            "%s__%s%s" % (mcsig[0].initial_cmssw,
            data.jsonToUse.filename[:-4], sub))
        fullFitsDir = os.path.join(fitsDir,
            "%s__%s%s" % (mcsig[0].initial_cmssw,
            data.jsonToUse.filename[:-4], sub))
        fullWorkspacesDir+="/%s"%mcsig[0].pu
        fullFitsDir+="/%s" % mcsig[0].pu

    CM.mkdir(fullFitsDir)
    CM.mkdir(fullWorkspacesDir)

    counter = 0
    numvars = len(variables)
    for variable in variables:
        savemodifier = ""
        category = variable["fullpath"].split("/")[0]

        firstFileName = fullWorkspacesDir + \
            "/workspace__analytic__%s__%s__%s__%s__%s.root" % (
                category, mass, )
        for model in lModels:

        
        #
        # Initialize the Model Class
        #
        modelklass = getattr(models, wargs["bmodel"])
        model = modelklass(category=category, **auxParameters)
        modelId = model.getModelId()

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
                mch[imcbg.name].Scale(
        # 0. create a workspace or extract from the existing
        try:
            fileName = fullWorkspacesDir +\
                "/workspace__analytic__%s__%s__%s__%s__%s.root" % (
                    category, 
                    wargs["mass"], modelId, wargs["smode"], wargs["smodel"])
            wsFile = R.TFile(fileName, "UPDATE")
            ws = wsFile.Get("higgs")
            # this will raise if there is no ws
            print ws.allPdfs().contentsString()
            appending = True
            testModelName = getattr(models, wargs["bmodel"])(category=category,
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
        R.RooMsgService.instance().setGlobalKillBelow(R.RooFit.FATAL)
        obs = ws.set("obs")

        #
        # Data RooDataHist creation and preserving in Workspace
        #
        roodata = R.RooDataHist("data_obs", "data_obs", RooArgList(obs), slicedhdata)
        getattr(ws, "import")(roodata, RooCmdArg())

        #
        # Create parameters for background and create the actual pdf
        #
        model.createParameters(ws, ndata=ndata)
        roomodel = model.build(ws)
        if wargs["Verbose"]: ws.Print("v")
        
        #
        # just do some fit
        #
        r = roomodel.fitTo(roodata, RooFit.Save())
        ccc = TCanvas("c1", "c1", 800, 600)
        ccc.cd()
        frame = ws.var("x").frame()
        frame.SetTitle(category)
        blindRooData(ws).plotOn(frame)
        roomodel.plotOn(frame, RooFit.Color(kRed),
            RooFit.Normalization(ndata, 0))
        roomodel.paramOn(frame, RooFit.Format("NELU", RooFit.AutoPrecision(2)), 
            RooFit.Layout(0.6, 0.99, 0.9), RooFit.ShowConstants(True))
        frame.getAttText().SetTextSize(0.02)
        chiSquare = frame.chiSquare()
        ttt = R.TPaveLabel(0.1,0.7,0.3,0.78, Form("#chi^{2} = %f" % chiSquare),
            "brNDC")
        ttt.Draw()
        frame.addObject(ttt)
        frame.Draw()

        if wargs["UF"]:
            suffix = '%s_%s.png' % (category, wargs["bmodel"])
        else:
            suffix = '_%s__%s__%s__%s__%s.png' % ( category, wargs["mass"], modelId,
                                                   wargs["smode"], wargs["smodel"] )

        ccc.SaveAs(fullFitsDir+"/bkgfit_%s" % suffix)

        fileName = fullWorkspacesDir+\
            "/workspace__analytic__%s__%s__%s__%s__%s.root" % (
            category, wargs["mass"], modelId, wargs["smode"], wargs["smodel"])
        if not appending:
            ws.SaveAs(fileName)
        else:
            wsFile.cd() ## Necessary to prevent write errors - AWB 28.02.17
            ws.Write()
            wsFile.Write()
            wsFile.Close()

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


    #
    #   Generate all the distributions
    #
    smode = "Separate"
    smodel = "SingleGaus"
    pu = "69"
    cmssw = "80X"
    mass = "125"
    for mGroup in modelGroups:
        generate(variables, (data, mGroup, modelGroups[mGroup]), 
            smode=smode, smodel=smodel, mass=mass)

    if SET.analytic:
        for smodel in SET.sig_models:
            for smode in SET.sig_modes:
                for bmodel in SET.bkg_models:
                    for cmssw in SET.cmssws:
                        for pu in SET.pileups:
                            generate( variables, (data, configs_bkgs["%s__%s" % (cmssw, pu)], configs_signals["%s__%s" % (cmssw, pu)]),
                                      analytic=1, smodel=smodel, bmodel=bmodel["name"], smode=smode, mass=SET.sig_M[0], 
                                      massmin=SET.bkg_M[1], massmax=SET.bkg_M[2], fitmin=SET.sig_M[3], fitmax=SET.sig_M[4], 
                                      shouldScale=SET.scale_MC, auxParameters=bmodel["aux"],
                                      Verbose=args.verbose, UF=('UF' in args.mode) )
    else:
        for cmssw in SET.cmssws:
            for pu in SET.pileups:
                generate( variables, (data2016_M22, mcbkgs["%s__%s" % (cmssw, pu)], mcsignals["%s__%s" % (cmssw, pu)]),
                          analytic=0, mass=SET.sig_M[0], massmin=SET.bkg_M[1], massmax=SET.bkg_M[2], 
                          Verbose=args.verbose, UF=('UF' in args.mode) )

