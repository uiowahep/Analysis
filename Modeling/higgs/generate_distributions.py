import ROOT as R
import sys, os, subprocess
from time import *

R.gROOT.SetBatch(R.kTRUE)

def mkdir(d):
    if not os.path.exists(d):
        cmd = "mkdir %s" % d
        subprocess.call(cmd, shell=True)

if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.environ["ANALYSISHOME"])
sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "Configuration/python"))
import NtupleProcessing.python.Samples as S
import NtupleProcessing.python.Dataset as DS

#
#   List all the constants and some initializations
#
resultsdir = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/vR1_20170217_1742"
picpath = "/Users/vk/software/Analysis/files/higgs_analysis_files/distributions"
#picpath_modifier = "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__allBkgs"
#picpath_modifier = "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8"
picpath_modifier = "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__allBkgs"
picpath = os.path.join(picpath, os.path.split(resultsdir)[1]  +"__"+ picpath_modifier)
mkdir(picpath)
default = -0.999
aux = "Mu24"

def plot(variables, (data, mcbg, mcsig), pre_options=None, post_options=None):
    c = R.TCanvas("c1", "c1", 800, 600)
    c.cd()
    pad1 = R.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)
    pad1.Draw()
    c.cd()

    pad2 = R.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.Draw()
    pad2.cd()
    pad2.SetTopMargin(0.05)
    pad2.SetBottomMargin(0.2)
    pad2.SetGridy()

    print "-"*40
    print data
    print mcbg
    print mcsig

    #
    #   Create the pic directory
    #
    sub = "" if aux==None or aux=="" else "__%s" % aux
    fullpicpath = os.path.join(picpath, "%s__%s%s" % (mcsig[0].initial_cmssw, 
        data.jsonToUse.filename[:-4], sub))
    mkdir(fullpicpath)
    fullpicpath+="/%s"%mcsig[0].pu
    mkdir(fullpicpath) # is the one to be used

    counter = 0
    numvars = len(variables)
    number_observations = 0
    number_signals = 0
    for variable in variables:
        print "*"*80
        print variable["fullpath"]
        print "*"*80
        pad1.cd()
        savemodifier = ""
        fdata = R.TFile(data.pathToFile)
        hdata = fdata.Get(variable["fullpath"])
        if hdata.GetEntries()==0:
            continue
        hdata.Print()
        hdata.SetMarkerStyle(20)
        hdata.SetMarkerSize(0.5)
        hdata.SetMarkerColor(R.kBlack)

        if pre_options!=None:
            if "BlindMass" in pre_options.keys():
                if pre_options["BlindMass"]:
                    if variable["name"]=="DiMuonMass":
                        savemodifier+="Blind"
                        for i in range(hdata.GetNbinsX()):
                            if hdata.GetBinCenter(i+1)>120 and hdata.GetBinCenter(i+1)<130:
                                hdata.SetBinContent(i+1, 0)
        leg = R.TLegend(0.65, 0.6, 0.9, 0.9)
        leg.SetHeader("Samples")
        leg.AddEntry(hdata, data.buildLabel())
#        leg.SetTextSize(0.04)

        bgstack = R.THStack("bgstack", variable["category"])
        bgsum = R.TH1D("bgsum", "", hdata.GetNbinsX(),
            hdata.GetBinLowEdge(1), hdata.GetBinLowEdge(1) + 
            hdata.GetNbinsX()*hdata.GetBinWidth(1))
        mch = {}
        mcf = {}
        for imcbg in mcbg:
            print imcbg
            mcf[imcbg.name] = R.TFile(imcbg.pathToFile)
            mch[imcbg.name] = mcf[imcbg.name].Get(variable["fullpath"])
            scale = data.jsonToUse.intlumi*imcbg.cross_section/imcbg.eweight
            print scale
            mch[imcbg.name].Scale(scale)
            mch[imcbg.name].SetFillColor(imcbg.options["color"])
            mch[imcbg.name].Print()
            bgstack.Add(mch[imcbg.name])
            bgsum.Add(mch[imcbg.name])
            leg.AddEntry(mch[imcbg.name], imcbg.buildLabel())
        bgsum.Print()
        bgstack.Print()

        mchsig = {}
        mcfsig = {}
        counter = 0
        for imcsig in mcsig:
            print imcsig
            mcfsig[imcsig.name] = R.TFile(imcsig.pathToFile)
            mchsig[imcsig.name] = mcfsig[imcsig.name].Get(variable["fullpath"])
            scale = data.jsonToUse.intlumi*imcsig.cross_section/imcsig.eweight
            print scale
            mchsig[imcsig.name].Scale(scale)
            if counter==0:
                signal = mchsig[imcsig.name]
            else:
                signal.Add(mchsig[imcsig.name])
            mchsig[imcsig.name].Print()
            counter += 1
        
        signal.SetLineColor(R.kRed)
        signal.SetLineWidth(2)
        leg.AddEntry(signal, "Signal")
        
        if pre_options!=None:
            if "ylog" in pre_options.keys():
                if pre_options["ylog"]:
                    pad1.SetLogy()
                    savemodifier+="ylog"
                    bgstack.SetMinimum(0.001)

        #   
        #   drawing options
        #
        s = hdata.SetStats(R.kFALSE)
        hdata.GetXaxis().SetLabelSize(0)
        bgstack.Draw("hist")
        hdata.Draw("same pe")
        signal.Draw("same hist")
        bgstack.GetXaxis().SetTitle(variable["name"])
        bgstack.GetYaxis().SetTitle("#Events")
        if variable["min"]!=default and variable["max"]!=default:
            bgstack.GetXaxis().SetRangeUser(variable["min"], 
                variable["max"])
        leg.Draw()
        R.gPad.Modified()
        

        #
        #   Ratio Plot
        #
        pad2.cd()
        hratio = hdata.Clone()
        hratio.SetTitle("")
        hratio.GetYaxis().SetTitle("Data / MC")
        hratio.GetXaxis().SetTitle(variable["name"])
        hratio.GetYaxis().SetNdivisions(6, R.kFALSE)
        hratio.GetYaxis().SetTitleSize(10)
        hratio.GetYaxis().SetTitleFont(43)
        hratio.GetYaxis().SetTitleOffset(1.55)
        hratio.GetYaxis().SetLabelFont(43)
        hratio.GetYaxis().SetLabelSize(15)
        hratio.GetXaxis().SetTitleSize(20)
        hratio.GetXaxis().SetTitleFont(43)
        hratio.GetXaxis().SetTitleOffset(4)
        hratio.GetXaxis().SetLabelFont(43)
        hratio.GetXaxis().SetLabelSize(15)
        hratio.Divide(bgsum)
        hratio.SetStats(R.kFALSE)
        hratio.Draw("ep")
        if variable["min"]!=default and variable["max"]!=default:
            hratio.GetXaxis().SetRangeUser(variable["min"], 
                variable["max"])
        hratio.SetMaximum(1.6)
        hratio.SetMinimum(0.4)
        hratio.SetMarkerStyle(20)
        hratio.SetMarkerSize(0.5)
        R.gPad.Modified()

        #
        #   save distributions
        #
        picname = fullpicpath+"/%s__%s__%s.png" % (variable["category"],
            variable["name"], savemodifier)
        print "picName = %s" % picname
        print c
        print c.GetName()
#        c.Draw()
        c.SaveAs(picname)
#        sleep(10000)

#
#   start...
#
if __name__=="__main__":
    #   define the variable
    from categories import *
    from aux import *
    variables = allVariablesRun1
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
                            eweight=getEventWeights(pathToFile),
                            options={"color":None})
                        oneconfig_signals.append(mc)
            for b in backgrounds:
                for k in mcsamples:
                    if b[0] in k and cmssw==mcsamples[k].initial_cmssw:
                        pathToFile = os.path.join(resultsdir,
                            "result__%s__%s__%s__%s__%s.root" % (b[0], cmssw,
                            datajson[:-4], pu+"mb", aux))
                        mc = MCResult(mc=mcsamples[k], pu=pu, pathToFile=pathToFile,
                            eweight=getEventWeights(pathToFile),
                            options={"color":b[1]})
                        oneconfig_bkgs.append(mc)
            configs_signals["%s__%s" % (cmssw, pu)] = oneconfig_signals
            configs_bkgs["%s__%s" % (cmssw, pu)] = oneconfig_bkgs

    #
    #   Generate all the distributions
    #
    print "Produce Plots for variables: %s" % str(varNames)
    for q in [True, False]:
        for cmssw in ["80X"]:
            for pu in pus:
                for isb in [True, False]:
                    plot(variables, (data, 
                        configs_bkgs["%s__%s" % (cmssw, pu)],
                        configs_signals["%s__%s" % (cmssw, pu)]),
                        {"ylog":q, "BlindMass":isb})
