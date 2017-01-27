import ROOT as R
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
resultsdir = "/Users/vk/software/Analysis/files/results/vR1_20170122_1326"
picpath = "/Users/vk/software/Analysis/files/distributions"
picpath_modifier = "TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"
#picpath_modifier = "TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8"
#picpath_modifier = "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
picpath = os.path.join(picpath, os.path.split(resultsdir)[1]  +"__"+ picpath_modifier)
mkdir(picpath)
default = -0.999
aux = "Mu24"

def getEventWeights(resultpathname):
    print resultpathname
    f = R.TFile(resultpathname)
    h = f.Get("eventWeights")
    return h.GetBinContent(1)

def plot(variables, (data, mcbg, mcsig), pre_options=None, post_options=None):
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
    fullpicpath = os.path.join(picpath, "%s__%s%s" % (mcsig[0]["cmssw"], 
        data["json"][:-4], sub))
    mkdir(fullpicpath)
    fullpicpath+="/%s"%mcsig[0]["PU"]
    mkdir(fullpicpath) # is the one to be used

    counter = 0
    numvars = len(variables)
    number_observations = 0
    number_signals = 0
    number_backgrounds = 0
    for variable in variables:
        print "*"*80
        print variable["fullpath"]
        print "*"*80
        pad1.cd()
        savemodifier = ""
        fdata = R.TFile(data["result"])
        hdata = fdata.Get(variable["fullpath"])
        if hdata.GetEntries()==0:
            continue
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
        leg.AddEntry(hdata, data["label"])

        bgstack = R.THStack("bgstack", variable["category"])
        bgsum = R.TH1D("bgsum", "", hdata.GetNbinsX(),
            hdata.GetBinLowEdge(1), hdata.GetBinLowEdge(1) + 
            hdata.GetNbinsX()*hdata.GetBinWidth(1))
        mch = {}
        mcf = {}
        for imcbg in mcbg:
            mcf[imcbg["name"]] = R.TFile(imcbg["result"])
            mch[imcbg["name"]] = mcf[imcbg["name"]].Get(variable["fullpath"])
            mch[imcbg["name"]].Scale(data["luminosity"]*imcbg["xsection"]/imcbg["eweight"])
            mch[imcbg["name"]].SetFillColor(imcbg["color"])
            bgstack.Add(mch[imcbg["name"]])
            bgsum.Add(mch[imcbg["name"]])
            leg.AddEntry(mch[imcbg["name"]], imcbg["name"].split("_")[0]+" %s" % imcbg["cmssw"])
#            leg.AddEntry(mch[imcbg["name"]], imcbg["label"] + " %s" % imcbg["cmssw"])
            if variable["name"]=="DiMuonMass":
                for i in range(hdata.GetNbinsX()):
                    if hdata.GetBinCenter(i+1)>115 and hdata.GetBinCenter(i+1)<135:
                        number_backgrounds += mch[imcbg["name"]].GetBinContent(i+1)

        mchsig = {}
        mcfsig = {}
        counter = 0
        for imcsig in mcsig:
            mcfsig[imcsig["name"]] = R.TFile(imcsig["result"])
            mchsig[imcsig["name"]] = mcfsig[imcsig["name"]].Get(variable["fullpath"])
            mchsig[imcsig["name"]].Scale(data["luminosity"]*imcsig["xsection"]/imcsig["eweight"])
            if counter==0:
                signal = mchsig[imcsig["name"]]
            else:
                signal.Add(mchsig[imcsig["name"]])
            counter += 1
        
        if variable["name"]=="DiMuonMass":
            for i in range(hdata.GetNbinsX()):
                if hdata.GetBinCenter(i+1)>115 and hdata.GetBinCenter(i+1)<135:
                    number_observations += hdata.GetBinContent(i+1)
                    number_signals += signal.GetBinContent(i+1)
        
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
        hdata.SetStats(R.kFALSE)
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
        c.SaveAs(picname)

#
#   start...
#
if __name__=="__main__":
    #   define the variable
    marker = ""
    varNames = ["DiJetMass", "DiJetdeta", "DiMuonpt", "DiMuonMass",
        "DiMuoneta", "DiMuondphi", "Muonpt", "Muoneta", "Muonphi"]
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
    s = """
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
    """

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
#            "TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8" : R.kGreen
#            'TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8' : R.kGreen
            'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8' : R.kGreen
    }
#    pus = ["68", "69", "70", "71", "72", "71p3", "69p2"]
    pus = ["68", "69", "71", "72", "70", "69p2", "71p3"]
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
    print "Produce Plots for variables: %s" % str(varNames)
    for q in [True, False]:
        for cmssw in ["80X"]:
            for pu in pus:
                for isb in [True, False]:
                    plot(variables, (data2016_M22, 
                        mcbkgs["%s__%s" % (cmssw, pu)],
                        mcsignals["%s__%s" % (cmssw, pu)]),
                        {"ylog":q, "BlindMass":isb})
