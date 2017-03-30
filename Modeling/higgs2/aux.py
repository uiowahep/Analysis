import ROOT as R
import Configuration.higgs.Dataset as DS
import Configuration.higgs.Samples as S
import os,sys

#
# slice a hist
#
def sliceHistogram(h, **wargs):
    newName = wargs["name"]
    massmin = wargs["massmin"]
    massmax = wargs["massmax"]
    newHist = R.TH1D(newName, newName, massmax - massmin, massmin, massmax)
    newibin = 0
    for ibin in range(h.GetNbinsX()):
        if h.GetBinCenter(ibin+1)>massmin and h.GetBinCenter(ibin+1)<massmax:
            newHist.SetBinContent(newibin+1, h.GetBinContent(ibin+1))
            newHist.SetBinError(newibin+1, h.GetBinError(ibin+1))
            newibin += 1
    return newHist

def getEventWeights(pathToFile):
    f = R.TFile(pathToFile)
    h = f.Get("eventWeights")
    return h.GetBinContent(1)

def mkdir(pathDir):
    if os.path.exists(pathDir):
        return
    else:
        os.system("mkdir %s" % pathDir)

def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

def blindHistogram(hdata, mmin, mmax):
    massmin = mmin
    massmax = mmax
    for ibin in range(hdata.GetNbinsX()):
        if hdata.GetBinCenter(ibin+1)>massmin and hdata.GetBinCenter(ibin+1)<massmax:
            hdata.SetBinContent(ibin+1, 0)

def blindRooData(ws):
    data = ws.data("data_obs")
    hdata = data.createHistogram("hdata", ws.var("x"),
        R.RooFit.Binning(50, 110, 160))
    blindData(hdata)
    ds = R.RooDataHist("data_blind", "data_blind", R.RooArgList(ws.set("obs").Clone()), hdata)
    return ds

def buildRatioPad(canvas):
    canvas.cd()
    pad1 = R.TPad("p1", "p1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)
    pad1.Draw()
    canvas.cd()

    pad2 = R.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.Draw()
    pad2.cd()
    pad2.SetTopMargin(0.05)
    pad2.SetBottomMargin(0.2)
    pad2.SetGridy()
    return pad1,pad2

def buildRatioHistogram(h1, h2):
    h = h1.Clone()
    h.Divide(h2)
    return h
   
def buildMassVariable(ws, **wargs):
    print wargs
    print "x[{central}, {min}, {max}]".format(**wargs)
    ws.factory("x[{central}, {min}, {max}]".format(**wargs))
    ws.var("x").SetTitle("m_{#mu#mu}")
    ws.var("x").setUnit("GeV")
    ws.defineSet("obs", "x")

def buildMH(ws, **wargs):
    print wargs
    ws.factory("x[{mhmin}, {mhmax}]".format(**wargs))

def buildRooHist(ws, hist):
    roo_hist = R.RooDataHist(hist.GetName(), hist.GetName(),
        R.RooArgList(ws.set("obs")), hist)
    return roo_hist

def buildSignalModelName(smodel, category, processName, mass=""):
    return "{className}_{category}_{processName}{mass}".format(className=smodel.__class__.__name__, category=category, processName=processName, mass=mass)

def buildBackgroundModelName(bmodel, category):
    if hasattr(bmodel, "degree"):
        return "{className}_{degree}_{category}".format(className=bmodel.__class__.__name__, category=category, degree=bmodel.degree)
    else:
        return "{className}_{category}".format(className=bmodel.__class__.__name__, 
            category=category)

def buildDefaultValuesBerstein(degree):
    d = {}
    for i in range(1, degree+1):
        d["b%d" % i] = 10
        d["b%dmin" % i] = -1000
        d["b%dmax" % i] = 1000
    return d
def buildDefaultValuesSumExponentials(degree):
    d = {}
    for i in range(1, degree+1):
        d["beta%d" % i] = 10
        d["beta%dmin" % i] = -1000000
        d["beta%dmax" % i] = 1000000
        d["alpha%d" % i] = 1
        d["alpha%dmin" % i] = -20
        d["alpha%dmax" % i] = 20
    return d
