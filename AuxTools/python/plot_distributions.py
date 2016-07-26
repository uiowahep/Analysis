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
libdir="/Users/vk/software/Analysis/build-2"
resultsdir = "/Users/vk/software/Analysis/files/results/dimuon/"
filelistdir="/Users/vk/software/Analysis/files/filelist/"
xsecs = [6025.2, 831.76]
picpath = "/Users/vk/software/Analysis/docs/H2mu/pics/20072016"
default = -0.999
R.gSystem.Load(libdir+"/libAnalysisNtupleProcessing.dylib")
R.gSystem.Load(libdir+"/libAnalysisCore.dylib")

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
    counter = 0
    numvars = len(variables)
    for variable in variables:
        fdata = R.TFile(data["pathfile"])
        hdata = fdata.Get(variable["fullpath"])
        if hdata.GetEntries()==0:
            continue
        hdata.SetMarkerColor(R.kBlack)
        hdata.SetMarkerStyle(20)
        hdata.SetMarkerSize(0.5)

#        if variable["name"]=="DiMuonMass":
#            for i in range(hdata.GetNbinsX()):
#                if hdata.GetBinCenter(i+1)>120 and hdata.GetBinCenter(i+1)<130:
#                    hdata.SetBinContent(i+1, 0)

        leg = R.TLegend(0.7, 0.7, 0.9, 0.9)
        leg.SetHeader("Samples")
        leg.AddEntry(hdata, data["label"])

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
        
        savemodifier = ""
        if pre_options!=None:
            if "ylog" in pre_options.keys():
                if pre_options["ylog"]:
                    c.SetLogy()
                    savemodifier+="ylog"

        bgstack.Draw("hist")
        hdata.Draw("same pe")
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
        markerending = ""
        if counter==0:
            markerending = "["
        elif counter==numvars-1:
            markerending = "]"
        else:
            markerending = ""
#        c.Print(fullpicpath+"/plots.pdf%s" % (markerending))
#        c.Print(fullpicpath+"/plots.pdf%s" % (variable["category"],
#           variable["name"], savemodifier, markerending))
        c.SaveAs(fullpicpath+"/%s_%s_%s.png" % (variable["category"],
           variable["name"], savemodifier))
        counter+=1

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
    category = "01JetsLoose"
    var01JetsLoose = [{"name":x, "min":-0.999 if x!="DiMuonMass" else 110, 
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

    #   define the data sample
    filelabel = "_allcats"
    data2015P = {"name" : "2015_Prompt", "label" : "2015 Prompt",
        "pathfile" :  resultsdir+"data2015Prompt%s.root" % filelabel, 
        "luminosity":2169}
    data2015R = {"name" : "2015_ReReco", "label" : "2015 ReReco",
        "pathfile" : resultsdir+"data2015ReReco%s.root" % filelabel, 
        "luminosity":2318}
    data2016P = {"name" : "2016_Prompt", "label" : "2016 Prompt",
        "pathfile" : resultsdir+"data2016Prompt%s.root" % filelabel, 
        "luminosity":7648}

    #   define the mc samples
    sampleNames = ["dy_jetsToLL", "ttJets"]
    xsections = {"dy_jetsToLL" : 6025.2, "ttJets" : 831.76}
    colors = { "dy_jetsToLL":R.kRed, "ttJets":R.kGreen}
    cmssw = ["74X", "76X"]
    againstWhichData = ["data2015Prompt_69mb", "data2015ReReco_69mb",
        "data2016Prompt_71p3mb"]
    mcs = {}
    for icmssw in cmssw:
        for idata in againstWhichData:
            l = []
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

    print "Produce Plots for variables: %s" % str(varNames)
    for q in [True, False]:
        plot(variables, (data2015P, mcs["%s_%s" % ("data2015Prompt_69mb", "74X")],
         None), {"ylog":q})
        plot(variables, (data2015R, mcs["%s_%s" % ("data2015ReReco_69mb", "76X")],
            None), {"ylog":q})
        plot(variables, (data2015R, mcs["%s_%s" % ("data2015ReReco_69mb", "74X")],
            None), {"ylog":q})
        plot(variables, (data2016P, 
            mcs["%s_%s" % ("data2016Prompt_71p3mb", "76X")],
         None), {"ylog":q})
        plot(variables, (data2016P, 
            mcs["%s_%s" % ("data2016Prompt_71p3mb", "74X")],
            None), {"ylog":q})

