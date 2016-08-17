import ROOT as R
import sys, os, subprocess

R.gROOT.SetBatch(R.kTRUE)

def mkdir(d):
    if not os.path.exists(d):
        cmd = "mkdir %s" % d
        subprocess.call(cmd, shell=True)

#
#   List all the constants and some initializations
#
treepathname = "ntuplemaker_H2DiMuonMaker/Meta"
libdir="/Users/vk/software/Analysis/build-3"
resultsdir = "/Users/vk/software/Analysis/files/results/dimuon-v3/"
filelistdir="/Users/vk/software/Analysis/files/filelist/"
xsecs = [6025.2, 831.76]
#   VBF first, ggF second
sigxsecs = [3.727*0.00022, 43.62*0.00022]
picpath = "/Users/vk/software/Analysis/docs/H2mu/pics/03082016"
default = -0.999
R.gSystem.Load(libdir+"/libAnalysisNtupleProcessing.dylib")
R.gSystem.Load(libdir+"/libAnalysisCore.dylib")
limitsfile = open(resultsdir+"blind.limits", "w")

def getEventWeights(mc):
    s = R.analysis.processing.Streamer(mc["pathfilelist"], treepathname)
    s.chainup()
    meta = R.analysis.dimuon.MetaHiggs()
    s._chain.SetBranchAddress("Meta", meta)
    weight = 0; n = s._chain.GetEntries()
    for i in range(n):
        s._chain.GetEntry(i)
        weight += meta._sumEventWeights
    return weight

def plot(variables, (data, mcbg, mcsig), pre_options=None, post_options=None):
    """
    variable is the dictionary of the form
    {
        "name" : <str>,
        "category" : <str>
        "fullpath" : <str>
        "min" : double
        "max" : double
    }
    data is the dictionary of the form
    {
        "name" : <str>,
        "label" : <str>,
        "pathfile" : <str>,
        "luminosity" : <double/int>
    }
    mc is the list of dictionaries of the form
        [mc1, mc2, mc3, ..., mcn], where mci is
        {
            "name" : <str>,
            "cmssw" : <str>,
            "dataPU" : <str>,
            "label" : <str>,
            "pathfile" : <str>,
            "pathfilelist" : <str>
            "eweight", : <double>
            "xsection" : <double>,
            "color" : <int>
        }
    """
    c = R.TCanvas("c1", "c1", 600, 400)
    c.cd()

    print data
    print mcbg
    print mcsig
    counter = 0
    numvars = len(variables)
    number_observations = 0
    number_signals = 0
    number_backgrounds = 0
    for variable in variables:
        fdata = R.TFile(data["pathfile"])
        hdata = fdata.Get(variable["fullpath"])
        if hdata.GetEntries()==0:
            continue
        hdata.SetMarkerStyle(20)
        hdata.SetMarkerSize(0.5)
        hdata.SetMarkerColor(R.kBlack)

        if variable["name"]=="DiMuonMass":
            for i in range(hdata.GetNbinsX()):
                if hdata.GetBinCenter(i+1)>120 and hdata.GetBinCenter(i+1)<130:
                    hdata.SetBinContent(i+1, 0)
        leg = R.TLegend(0.65, 0.7, 0.9, 0.9)
        leg.SetHeader("Samples")
        leg.AddEntry(hdata, data["label"]+" %s/fb" % str(data["luminosity"]/1000))

        bgstack = R.THStack("bgstack", variable["category"])
        mch = {}
        mcf = {}
        for imcbg in mcbg:
            mcf[imcbg["name"]] = R.TFile(imcbg["pathfile"])
            mch[imcbg["name"]] = mcf[imcbg["name"]].Get(variable["fullpath"])
            mch[imcbg["name"]].Scale(data["luminosity"]*imcbg["xsection"]/imcbg["eweight"])
            mch[imcbg["name"]].SetFillColor(imcbg["color"])
            bgstack.Add(mch[imcbg["name"]])
            leg.AddEntry(mch[imcbg["name"]], imcbg["label"] + " %s" % imcbg["cmssw"])
            if variable["name"]=="DiMuonMass":
                for i in range(hdata.GetNbinsX()):
                    if hdata.GetBinCenter(i+1)>115 and hdata.GetBinCenter(i+1)<135:
                        number_backgrounds += mch[imcbg["name"]].GetBinContent(i+1)

        mchsig = {}
        mcfsig = {}
        counter = 0
        for imcsig in mcsig:
            mcfsig[imcsig["name"]] = R.TFile(imcsig["pathfile"])
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
        
        savemodifier = ""
        if pre_options!=None:
            if "ylog" in pre_options.keys():
                if pre_options["ylog"]:
                    c.SetLogy()
                    savemodifier+="ylog"
                    bgstack.SetMinimum(0.001)

        bgstack.Draw("hist")
        hdata.Draw("same pe x0")
        signal.Draw("same hist")
        bgstack.GetXaxis().SetTitle(variable["name"])
        bgstack.GetYaxis().SetTitle("#Events")
        if variable["min"]!=default and variable["max"]!=default:
            bgstack.GetXaxis().SetRangeUser(variable["min"], 
                variable["max"])
        leg.Draw()
        R.gPad.Modified()

        fullpicpath = picpath+"/%s_vs_MC%s_CMSSW%s" % (data["name"], 
            mcbg[0]["dataPU"] if mcbg!=None or mcbg!=[] else "", 
            mcbg[0]["cmssw"])
        mkdir(fullpicpath)
#        c.Print(fullpicpath+"/plots.pdf%s" % (markerending))
#        c.Print(fullpicpath+"/plots.pdf%s" % (variable["category"],
#           variable["name"], savemodifier, markerending))
        c.SaveAs(fullpicpath+"/%s_%s_%s.png" % (variable["category"],
           variable["name"], savemodifier))
        if variable["name"]=="DiMuonMass":
            limitsfile.write("\n")
            limitsfile.write(data["name"] + " : " + mcbg[0]["dataPU"] + " : "+mcbg[0]["cmssw"]+ " : " +variable["category"] + " : " + str((number_observations, number_signals, number_backgrounds)))
            limitsfile.write("\n")
            number_observations = 0
            number_signals = 0
            number_backgrounds = 0

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

    #   define the data sample
    filelabel = "_wCats"
    data2015P = {"name" : "2015_Prompt", "label" : "2015 Prompt",
        "pathfile" :  resultsdir+"data2015Prompt%s.root" % filelabel, 
        "luminosity":2169.}
    data2015R = {"name" : "2015_ReReco", "label" : "2015 ReReco",
        "pathfile" : resultsdir+"data2015ReReco%s.root" % filelabel, 
        "luminosity":2318.}
    data2016P_v1 = {"name" : "2016_Prompt_v1", "label" : "2016 Prompt",
        "pathfile" : resultsdir+"data2016Prompt_v1%s.root" % filelabel, 
        "luminosity":7648.}
    data2016P_v2 = {"name" : "2016_Prompt_v2", "label" : "2016 Prompt",
        "pathfile" : resultsdir+"data2016Prompt_v2%s.root" % filelabel, 
        "luminosity":12900.}

    #   define the mc samples
    sampleNames = ["dy_jetsToLL", "ttJets"]
    sigSampleNames = ["vbf_HToMuMu", "gg_HToMuMu"]
    xsections = {"dy_jetsToLL" : 6025.2, "ttJets" : 831.76,
        "vbf_HToMuMu" : 3.727*0.00022, "gg_HToMuMu" : 43.62*0.00022}
    colors = { "dy_jetsToLL":R.kBlue, "ttJets":R.kGreen}
    cmssw = ["74X", "76X"]
    againstWhichData = ["data2015Prompt_69mb", "data2015ReReco_69mb",
        "data2016Prompt_71p3mb"]
#    againstWhichData = ["data2015Prompt_69mb", "data2015ReReco_69mb",
#        "data2016Prompt_71p3mb", "data2016Prompt_v2_71p3mb"]
    mcs = {}
    mcssig = {}
    for icmssw in cmssw:
        for idata in againstWhichData:
            l = []
            lsig = []

            #   SIGNAL
            for s in sigSampleNames:
                mcsig = {
                    "name":s, "cmssw":icmssw, "dataPU":idata,
                    "label":s, "pathfile":resultsdir+"mc_%s_%s_%s%s.root" % (
                        s, icmssw, idata, filelabel),
                    "pathfilelist":filelistdir+"mc_%s_%s.files" % (s, icmssw),
                    "xsection":xsections[s]
                }
                mcsig["eweight"] = getEventWeights(mcsig)
                print "MC=%s CMSSW=%s weight=%d" % (mcsig["name"],
                    mcsig["cmssw"], mcsig["eweight"])
                lsig.append(mcsig)

            #   BACKGROUND
            for s in sampleNames:
                mc = {"name": s, "cmssw":icmssw, "dataPU":idata,
                    "label":s, "pathfile":resultsdir+"mc_%s_%s_%s%s.root" % (
                    s, icmssw, idata, filelabel), 
                    "pathfilelist":filelistdir+"mc_%s_%s.files" % (s,icmssw),
                    "xsection": xsections[s], "color":colors[s]}
                mc["eweight"] = getEventWeights(mc)
                print "MC=%s CMSSW=%s weight=%d" % (mc["name"],
                    mc["cmssw"], mc["eweight"])
                l.append(mc)
            mcs["%s_%s" % (idata, icmssw)] = l
            mcssig["%s_%s" % (idata, icmssw)] = lsig

    print "Produce Plots for variables: %s" % str(varNames)
    for q in [True, False]:
        plot(variables, (data2015P, mcs["%s_%s" % ("data2015Prompt_69mb", "74X")],
            mcssig["%s_%s" % ("data2015Prompt_69mb", "74X")]), {"ylog":q})
        plot(variables, (data2015R, mcs["%s_%s" % ("data2015ReReco_69mb", "76X")],
            mcssig["%s_%s" % ("data2015ReReco_69mb", "76X")]), {"ylog":q})
        plot(variables, (data2015R, mcs["%s_%s" % ("data2015ReReco_69mb", "74X")],
            mcssig["%s_%s" % ("data2015ReReco_69mb", "74X")]), {"ylog":q})
        plot(variables, (data2016P_v1, 
            mcs["%s_%s" % ("data2016Prompt_71p3mb", "76X")],
            mcssig["%s_%s" % ("data2016Prompt_71p3mb", "76X")]), {"ylog":q})
        plot(variables, (data2016P_v1, 
            mcs["%s_%s" % ("data2016Prompt_71p3mb", "74X")],
            mcssig["%s_%s" % ("data2016Prompt_71p3mb", "74X")]), {"ylog":q})
#        plot(variables, (data2016P_v2, 
#            mcs["%s_%s" % ("data2016Prompt_71p3mb", "76X")],
#            mcssig["%s_%s" % ("data2016Prompt_71p3mb", "76X")]), {"ylog":q})
#        plot(variables, (data2016P_v2, 
#            mcs["%s_%s" % ("data2016Prompt_71p3mb", "74X")],
#            mcssig["%s_%s" % ("data2016Prompt_71p3mb", "74X")]), {"ylog":q})
#        plot(variables, (data2016P_v2, 
#            mcs["%s_%s" % ("data2016Prompt_v2_71p3mb", "76X")],
#            mcssig["%s_%s" % ("data2016Prompt_v2_71p3mb", "76X")]), {"ylog":q})
#        plot(variables, (data2016P_v2, 
#            mcs["%s_%s" % ("data2016Prompt_v2_71p3mb", "74X")],
#            mcssig["%s_%s" % ("data2016Prompt_v2_71p3mb", "74X")]), {"ylog":q})

