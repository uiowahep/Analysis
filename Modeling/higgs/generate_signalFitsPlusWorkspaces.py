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
fitsDir       = SET.sig_fits_dir

CM.mkdir(workspacesDir)
CM.mkdir(fitsDir)

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
        fullFitsDir       = SET.sig_fits_dir
    else:
        fullWorkspacesDir = os.path.join(workspacesDir,
            "%s__%s%s" % (mcsig[0].initial_cmssw,
            data.jsonToUse.filename[:-4], sub))
        fullFitsDir = os.path.join(fitsDir,
            "%s__%s%s" % (mcsig[0].initial_cmssw,
            data.jsonToUse.filename[:-4], sub))
        fullWorkspacesDir+="/%s"%mcsig[0].pu
        fullFitsDir+="/%s"%mcsig[0].pu

    CM.mkdir(fullFitsDir)
    CM.mkdir(fullWorkspacesDir)

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

        #
        # for each signal
        #   1. scale
        #   2. aux initializations/manipulations -> build a RooDatHist
        #   3. create model and fit
        #   4. plot all fits and save
        #   5. save plots
        #
        for mc in mcsig:
            if wargs["Verbose"]:
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
            if wargs["UF"]:
                suffix = '%s_%s_%s.png' % (roo_hist.GetName(), category, wargs["smodel"])
            else:
                suffix = '_%s__%s__%s__%s__%s__%s.png' % (roo_hist.GetName(), category, wargs["mass"], 
                                                          wargs["bmodel"], wargs["smode"], wargs["smodel"])

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
            ccc.SaveAs(fullFitsDir+"/fit_%s" % suffix)

            xframe2 = ws.var("x").frame()
            xframe2.addObject(xframe.pullHist())
            xframe2.SetMinimum(-5)
            xframe2.SetMaximum(5)
            xframe2.Draw()
            ccc.SaveAs(fullFitsDir+"/pull_%s" % suffix)

            xframe3 = ws.var("x").frame()
            xframe3.addObject(xframe.residHist())
            xframe3.SetMinimum(-5)
            xframe3.SetMaximum(5)
            xframe3.Draw()
            ccc.SaveAs(fullFitsDir+"/resid_%s" % suffix)

        #
        # 5.either update or create
        #
        fileName = fullWorkspacesDir+\
            "/workspace__analytic__%s__%s__%s__%s__%s.root" % (
            category, wargs["mass"], wargs["bmodel"], wargs["smode"], wargs["smodel"])

            
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
        resultPathName = os.path.join(resultsdir, "result__merged__%s__%s.root" % (datajson[:-4], aux))

    data = DataResult(name="ReReco", year="2016",
        jsonToUse=jsonToUse, pathToFile=resultPathName)

    configs_signals = {}
    configs_bkgs = {}
    shouldScale = False
    for cmssw in SET.cmssws:
        for pu in SET.pileups:
            oneconfig_signals = []
            oneconfig_bkgs = []
            for s in SET.signals:
                for k in mcsamples:
                    if s in k and cmssw==mcsamples[k].initial_cmssw:
                        if ('UF' in args.mode):
                            pathToFile = '%s/%s.root' % (resultsdir, s)
                        else:
                            pathToFile = os.path.join(resultsdir,
                                "result__%s__%s__%s__%s__%s.root" % (s, cmssw,
                                datajson[:-4], pu+"mb", aux))
                        mc = MCResult(mc=mcsamples[k], pu=pu, pathToFile=pathToFile,
                            eweight=None if not shouldScale else getEventWeights(pathToFile),
                            options={"color":None})
                        oneconfig_signals.append(mc)
            for b in SET.backgrounds:
                for k in mcsamples:
                    if b[0] in k and cmssw==mcsamples[k].initial_cmssw:
                        if ('UF' in args.mode):
                            pathToFile = '%s/%s.root' % (resultsdir, b[0])
                        else:
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
    if SET.analytic:
        for smodel in SET.sig_models:
            for smode in SET.sig_modes:
                for bmodel in SET.bkg_models:
                    for cmssw in SET.cmssws:
                        for pu in SET.pileups:
                            generate( variables, (data, configs_bkgs["%s__%s" % (cmssw, pu)], configs_signals["%s__%s" % (cmssw, pu)]), 
                                      analytic=1, smodel=smodel, bmodel=bmodel, smode=smode, mass=SET.sig_M[0], 
                                      massmin=SET.sig_M[1], massmax=SET.sig_M[2], fitmin=SET.sig_M[3], fitmax=SET.sig_M[4], 
                                      shouldScale=SET.scale_MC, Verbose=args.verbose, UF=('UF' in args.mode) )
    else:
        for cmssw in SET.cmssws:
            for pu in SET.pileups:
                generate( variables, (data2016_M22, mcbkgs["%s__%s" % (cmssw, pu)], mcsignals["%s__%s" % (cmssw, pu)]), 
                          analytic=0, mass=SET.sig_M[0], massmin=SET.sig_M[1], massmax=SET.sig_M[2], 
                          Verbose=args.verbose, UF=('UF' in args.mode) )
