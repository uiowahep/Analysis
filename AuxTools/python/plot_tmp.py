import ROOT as R
import sys

#
#   List all the constants
#
treepathname = "ntuplemaker_H2DiMuonMaker/Meta"
libdir="/Users/vk/software/Analysis/build-2"
resultsdir = "/Users/vk/software/Analysis/files/results/dimuon/"
#datafile = "/Users/vk/software/Analysis/files/results/dimuon/data2015ReReco.root"
datafile = "/Users/vk/software/Analysis/files/results/dimuon/data2016Prompt.root"
#datafile = "/Users/vk/software/Analysis/files/results/dimuon/data2015Prompt.root"
#dataname="2015 Prompt"
#dataname = "2015 ReReco"
dataname = "2016 Prompt"
bfiles = [
#    "/Users/vk/software/Analysis/build-2/test_dy_jetsToDLL_74X.root",
#    "/Users/vk/software/Analysis/build-2/test_ttJets_74X.root"]
#    "/Users/vk/software/Analysis/files/results/dimuon/mc_dy_jetsToLL_74X_data2015Prompt_69mb.root", 
#   "/Users/vk/software/Analysis/files/results/dimuon/mc_ttJets_74X_data2015Prompt_69mb.root"
#    resultsdir+"mc_dy_jetsToLL_74X_data2016Prompt_71p3mb.root",
#    resultsdir+"mc_ttJets_74X_data2016Prompt_71p3mb.root",
    resultsdir+"mc_dy_jetsToLL_76X_data2016Prompt_71p3mb.root",
    resultsdir+"mc_ttJets_76X_data2016Prompt_71p3mb.root"
]
xsecs = [6025.2, 831.76]
filelistsdir = "/Users/vk/software/Analysis/files/filelist/"
bfilelists = [
    filelistsdir+"mc_dy_jetsToLL_76X.files",
    filelistsdir+"mc_ttJets_76X.files"
]
#    "/Users/vk/software/Analysis/files/filelist/mc_dy_jetsToLL_74X.files", 
#    "/Users/vk/software/Analysis/files/filelist/mc_ttJets_74X.files"]
wevents = [1,1]
colors = [R.kRed, R.kGreen]
cmssw = "76X"
mcnames = ["DYJets %s" % cmssw, "ttJets %s" % cmssw]
category="_NoCats"
luminosity=7648
#luminosity=2318
#luminosity = 2169
picpath = "/Users/vk/software/Analysis/docs/H2mu/pics/14072016"
varName = "DiMuondphi"

#
#   get all the weights
#
wevents = []
R.gSystem.Load(libdir+"/libAnalysisNtupleProcessing.dylib")
R.gSystem.Load(libdir+"/libAnalysisCore.dylib")
s1 = R.analysis.processing.Streamer(bfilelists[0], treepathname)
s2 = R.analysis.processing.Streamer(bfilelists[1], treepathname)
s1.chainup(); s2.chainup();
meta1 = R.analysis.dimuon.MetaHiggs()
meta2 = R.analysis.dimuon.MetaHiggs()
s1._chain.SetBranchAddress("Meta", meta1)
s2._chain.SetBranchAddress("Meta", meta2)
n = s1._chain.GetEntries()
weight = 0
for i in range(n):
    s1._chain.GetEntry(i)
    weight += meta1._sumEventWeights
wevents.append(weight)
print "MC Sample %s with weight %d"  % (mcnames[0], wevents[0])
weight = 0
n = s2._chain.GetEntries()
for i in range(n):
    s2._chain.GetEntry(i)
    weight += meta2._sumEventWeights
wevents.append(weight)
print "MC Sample %s with weight %d"  % (mcnames[1], wevents[1])

#
#   open all the results ROOT files
#
fb1 = R.TFile(bfiles[0])
fb2 = R.TFile(bfiles[1])
fdata = R.TFile(datafile)

#
#   Initialize the canvas
#
c = R.TCanvas("c1", "c1", 600, 400)
c.cd()

#
#   background stack
#
bgstack = R.THStack("bgstack", "")

hb1 = fb1.Get(category+"/"+varName)
hb1.Scale(luminosity*xsecs[0]/wevents[0])
hb1.SetFillColor(colors[0])
bgstack.Add(hb1)

hb2 = fb2.Get(category+"/"+varName)
hb2.Scale(luminosity*xsecs[1]/wevents[1])
hb2.SetFillColor(colors[1])
bgstack.Add(hb2)

#
#   data
#
hdata = fdata.Get(category+"/"+varName)

#
#   Create a legend
#
leg = R.TLegend(0.7, 0.7, 0.9, 0.9)
leg.SetHeader("Samples")

#
#   Styling
#
hdata.SetMarkerColor(R.kBlack)
hdata.SetMarkerStyle(20)
hdata.SetMarkerSize(0.5)
leg.AddEntry(hdata, dataname)
leg.AddEntry(hb1, mcnames[0])
leg.AddEntry(hb2, mcnames[1])

#
#   Styling
#
#max1 = hdata.GetMaximum()
#max2 = bgstack.GetMaximum()
#if max1>max2:
#    hdata.SetMaximum(max1)
#    bgstack.SetMaximum(max1)
#else:
#    hdata.SetMaximum(max2)
#    bgstack.SetMaximum(max2)

#
#   Draw everything
#
bgstack.Draw("hist")
hdata.Draw("same pe")
leg.Draw()

#
#   Changes 
#
bgstack.GetXaxis().SetTitle(varName)
bgstack.GetYaxis().SetTitle("#Events")
R.gPad.Modified()

c.SaveAs(picpath+varName+(".pdf"))

def plot(variable, (data, mcbg, mcsig)):
    """
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
            "label" : <str>,
            "pathfile" : <str>,
            "pathfilelist" : <str>,

        }
    """






