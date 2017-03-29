"""
List of Generator functions, like:
    - distributions
    - signalFits
    - backgroundFits
    - workspaces
    - datacards
"""

import os, sys
import definitions as defs
import aux
sys.path.append(os.environ["ANALYSISHOME"])
sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "Configuration/higgs"))
import Configuration.higgs.Samples as S
import ROOT as R
import models
R.gROOT.SetBatch(R.kTRUE)

class Event(object):
    """
    dummry object
    """
    def __init__(self):
        object.__init__(self)

class Settings(object):
    """
    dummry object
    """
    def __init__(self):
        object.__init__(self)

class Pipeline(object):
    """
    Represents a simple pipeline of executors or other pipelines that do not share Event
    object!
    """
    def __init__(self, settings, execs):
        self.execs = execs
        self.settings = settings

    def execute(self, *kargs):
        # drop all defs
        event = Event()
        event.settings = self.settings
        # run
        for e in self.execs:
            e.execute(event)

class SharedPipeline(object):
    """
    Represents a simple pipeline of executors or other pipelines that do not share Event
    object!
    """
    def __init__(self, settings, execs):
        self.execs = execs
        self.settings = settings

    def execute(self, *kargs):
        # drop all defs
        self.event = kargs[0]
        self.event.settings = self.settings
        # run
        for e in self.execs:
            e.execute(self.event)

class Executor(object): 
    def __init__(self, **wargs):
        object.__init__(self)

class CanvasCreator(Executor):
    def __init__(self, name):
        Executor.__init__(self)
        self.name = name
        self.c = R.TCanvas(name, name, 800, 600)

    def execute(self, event):
        # attach the canvas to the event
        event.canvas = self.c
        event.canvas.cd()

class RatioPlotCreator(Executor):
    def __init__(self):
        Executor.__init__(self)
        pass

    def execute(self, event):
        pad1,pad2 = aux.buildRatioPad(event.canvas)
        event.pad1 = pad1
        event.pad2 = pad2

class CanvasSaver(Executor):
    def __init__(self, fileName):
        Executor.__init__(self)
        self.fileName = fileName
        pass

    def execute(self, event):
        event.canvas.SaveAs(self.fileName)

class CanvasCustomizer(Executor):
    def __init__(self, func):
        Executor.__init__(self)
        self.func = func
        pass

    def execute(self, event):
        self.func(event.canvas)

class EventCustomizer(Executor):
    def __init__(self, func):
        Executor.__init__(self)
        self.func = func
        pass

    def execute(self, event):
        self.func(event)

class LumiCreator(Executor):
    def __init__(self, data):
        Executor.__init__(self)
        self.data = data

    def execute(self, event):
        event.luminosity = self.data.jsonToUse.intlumi

class DataSource(Executor):
    def __init__(self, data):
        Executor.__init__(self)
        self.data = data

    def execute(self, event):
        event.data = self.data
        event.data.fromFile(None)

class SignalSource(Executor):
    def __init__(self, *s):
        Executor.__init__(self)
        self.s = s

    def execute(self, event):
        if hasattr(event, "signals"):
            event.signals.extend(self.s)
        else:
            event.signals = [s for s in self.s]

class BackgroundSource(Executor):
    def __init__(self, b):
        Executor.__init__(self)
        self.b = b

    def execute(self, event):
        if hasattr(event, "backgrounds"):
            event.backgrounds.append(self.b)
        else:
            event.backgrounds = [self.b]

class DefaultWorkspaceSource(Executor):
    def __init__(self, name):
        Executor.__init__(self)
        self.name = name

    def execute(self, event):
        event.ws = R.RooWorkspace(self.name)

class MassVariableGen(Executor):
    def __init__(self):
        Executor.__init__(self)

    def execute(self, event):
        event.ws.factory("x[{mean}, {massmin}, {massmax}]".format(
            mean=event.settings.higgsMass, massmin=event.settings.massRangeMin, 
            massmax=event.settings.massRangeMax))
        event.ws.var("x").SetTitle("m_{#mu#mu}")
        event.ws.var("x").setUnit("GeV")
        event.ws.defineSet("obs", "x")

class FrameCreator(Executor):
    def __init__(self):
        Executor.__init__(self)

    def execute(self, event):
        event.frame = event.ws.var("x").frame()
        print event.frame
        print event.canvas
        print event.ws
        print event.ws.var("x")

class FramePlotter(Executor):
    def __init__(self):
        Executor.__init__(self)

    def execute(self, event):
        event.frame.Draw()

class SignalDistributions(Executor):
    def __init__(self, custSum, drawOptions):
        Executor.__init__(self)
        self.custSumFunc = custSum
        self.drawOptions = drawOptions

    def execute(self, event):
        event.pad1.cd()
        ssum = None
        mapH = {}
        for sig in event.signals:
            mapH[sig.mc.name] = sig.fromFile(None)
            scale = event.luminosity * sig.mc.cross_section/sig.weight
            mapH[sig.mc.name].Scale(scale)
            if ssum==None:
                sig = mapH[sig.mc.name]
                ssum = sig.Clone()
            else:
                ssum.Add(mapH[sig.mc.name])
        self.custSumFunc(ssum, event)
        ssum.Draw(self.drawOptions)
        self.ssum = ssum
        R.gPad.Modified()

class SingleSignalFit(Executor):
    def __init__(self, isignal):
        Executor.__init__(self)
        self.isignal = isignal

    def execute(self, event):
        print event.frame
        if event.frame==None:
            event.frame = event.ws.var("x").frame()
        signal = event.signals[self.isignal]
        print event.frame
        hist = signal.fromFile(None)
        hist.Scale(1/signal.weight)
        print event.frame
        print event.canvas
        print event.ws
        print event.ws.var("x")
        print event.ws.var("x").frame()
        print event.frame
        self.roo_hist = R.RooDataHist(hist.GetName(), hist.GetName(),
            R.RooArgList(event.ws.set("obs")), hist)
        print event.frame
        signal.model.createParameters(event) 
        model = signal.model.build(event)
        r = model.fitTo(self.roo_hist, R.RooFit.Save(),
            R.RooFit.Range(event.settings.massFitMin, event.settings.massFitMax))
        signal.model.fixParameters(event)
        print event.frame
        self.roo_hist.plotOn(event.frame)
        model.plotOn(event.frame, R.RooFit.LineColor(R.kRed))

class DataDistribution(Executor):
    def __init__(self, customizeFunction, drawOptions):
        Executor.__init__(self)
        self.customizeFunction = customizeFunction
        self.drawOptions = drawOptions

    def execute(self, event):
        event.pad1.cd()
        hdata = event.data.fromFile(None)
        self.customizeFunction(hdata, event)
        hdata.Draw(self.drawOptions)
        event.h1 = hdata
        R.gPad.Modified()

class BackgroundDistributions(Executor):
    def __init__(self, custEach, custStack, drawOptions):
        Executor.__init__(self)
        self.custEachFunc = custEach
        self.custStackFunc = custStack
        self.drawOptions = drawOptions

    def execute(self, event):
        #  backgrounds
        event.pad1.cd()
        bstack = R.THStack("bstack", event.backgrounds[0].category)
        bsum = None
        mapH = {}
        for bkg in event.backgrounds:
            mapH[bkg.mc.name] = bkg.fromFile(None)
            scale = event.luminosity * bkg.mc.cross_section/bkg.weight
            mapH[bkg.mc.name].Scale(scale)
            self.custEachFunc(mapH[bkg.mc.name], bkg)
            bstack.Add(mapH[bkg.mc.name])
            if bsum==None:
                bsum = mapH[bkg.mc.name].Clone()
            else:
                bsum.Add(mapH[bkg.mc.name])
        self.custStackFunc(bstack, event)
        bstack.Draw(self.drawOptions)
        bstack.Print("v")
        self.bstack = bstack
        event.h2 = bsum
        R.gPad.Modified()

class RatioGenerator(Executor):
    def __init__(self):
        Executor.__init__(self)

    def execute(self, event):
        event.pad2.cd()
        h = aux.buildRatioHistogram(event.h1, event.h2)
        h.Draw("ep")
        self.h = h
        R.gPad.Modified

class DistributionsGenerator(Executor):
    def __init__(self, data, signals, backgrounds, **wargs):
        Executor.__init__(self)
        self.data = data
        self.signals = signals
        self.backgrounds = backgrounds

    def execute(self, event):
        """
        generate distributions for this variable/category
        given data/signals/backgrounds
        """
        event.pad1.cd()
        # customize data
        hdata = self.data.fromFile(None)
        hdata.SetMarkerStyle(20)
        hdata.SetMarkerSize(0.5)
        hdata.SetMarkerColor(self.data.color)

        #  backgrounds
        bstack = R.THStack("bstack", self.data.category)
        bsum = R.TH1D("bsum", "bsum", hdata.GetNbinsX(),
            hdata.GetBinLowEdge(1), hdata.GetBinLowEdge(1) +
            hdata.GetNbinsX()*hdata.GetBinWidth(1))
        mapH = {}
        for bkg in self.backgrounds:
            mapH[bkg.mc.name] = bkg.fromFile(None)
            scale = self.data.jsonToUse.intlumi * bkg.mc.cross_section/bkg.weight
            mapH[bkg.mc.name].Scale(scale)
            mapH[bkg.mc.name].SetFillColor(bkg.color)
            bstack.Add(mapH[bkg.mc.name])
            bsum.Add(mapH[bkg.mc.name])

        # signals
        ssum = R.TH1D("ssum", "ssum", hdata.GetNbinsX(),
            hdata.GetBinLowEdge(1), hdata.GetBinLowEdge(1) +
            hdata.GetNbinsX()*hdata.GetBinWidth(1))
        mapH = {}
        for sig in self.signals:
            mapH[sig.mc.name] = sig.fromFile(None)
            scale = self.data.jsonToUse.intlumi * sig.mc.cross_section/sig.weight
            mapH[sig.mc.name].Scale(scale)
            ssum.Add(mapH[sig.mc.name])
        if len(self.signals)>0:
            ssum.SetLineColor(self.signals[0].color)

        event.pad1.SetLogy()
        # plot distributions
        bstack.SetMinimum(0.1)
        bstack.Draw("hist")
        bstack.Print("v")
        hdata.Draw("same pe")
        ssum.Print("v")
        ssum.Draw("same hist")
        R.gPad.Modified()

        #
        # ratio plot
        #
        event.pad2.cd()
        self.hratio = aux.buildRatioHistogram(hdata, bsum)
        self.hratio.Draw("ep")
        R.gPad.Modified()

if __name__=="__main__":
    resultsDir = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/vR1_20170217_1742"
    dataPath = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/vR1_20170217_1742/result__merged__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__Mu24.root"
    dyPath = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/vR1_20170217_1742/result__DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
    ttPath = "/Users/vk/software/Analysis/files/higgs_analysis_files/results/vR1_20170217_1742/result__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
    dyMC = S.mcMoriond2017datasets["/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
    ttMC = S.mcMoriond2017datasets["/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
    glugluPath = resultsDir + "/" + "result__GluGlu_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
    vbfPath = resultsDir + "/" + "result__VBF_HToMuMu_M125_13TeV_powheg_pythia8__80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__69mb__Mu24.root"
    glugluMC = S.mcMoriond2017datasets["/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]
    vbfMC = S.mcMoriond2017datasets["/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]

    def CustomizeData(h, event):
        h.SetMarkerStyle(20)
        h.SetMarkerSize(0.5)
        h.SetMarkerColor(event.data.color)

    def CustomizeSignalSum(h, event):
        h.SetLineColor(event.signals[0].color)

    def CustomizeBkg(h, bkg):
        h.SetFillColor(bkg.color)

    def CustomizeBkgStack(h, event):
        h.SetMinimum(0.1)

    var = defs.Variable()
    jsonToUse = S.jsonfiles["2016_ReReco_36460"]
    d = defs.Data("NoCats", var, jsonToUse, dataPath, color=R.kBlack)

    model1 = models.SingleGaus(initFunc=models.defaultSingleGausInit)
    model2 = models.SingleGaus(initFunc=models.defaultSingleGausInit)

    b = defs.MC("NoCats", var, dyPath, dyMC, None, color=R.kBlue)
    t = defs.MC("NoCats", var, ttPath, ttMC, None, color=R.kGreen)
    glu = defs.MC("NoCats", var, glugluPath, glugluMC, model1, color=R.kRed)
    vbf = defs.MC("NoCats", var, vbfPath, vbfMC, model2, color=R.kRed)
    distrs = DistributionsGenerator(d, [glu, vbf], [t, b], something="")
    dataDistr = DataDistribution(CustomizeData, "same pe")
    sigDistrs = SignalDistributions(CustomizeSignalSum, "same hist")
    bkgDistrs = BackgroundDistributions(CustomizeBkg, CustomizeBkgStack, 
        "hist")
    lumi = LumiCreator(d)
    canvasStart = CanvasCreator("c1")
    def custLog(event): event.pad1.SetLogy()
    logPadCust = EventCustomizer(custLog)
    fileName1 = "/tmp/test1.png"
    canvasStop1 = CanvasSaver(fileName1)
    fileName2 = "/tmp/test2.png"
    canvasStop2 = CanvasSaver(fileName2)
    ratio = RatioPlotCreator()
    ratioGen = RatioGenerator()

    settings = Settings()
    settings.pu = "69"
    settings.massRangeMin = 110
    settings.massRangeMax = 160
    settings.massFitMin = 115
    settings.massFitMax = 135
    settings.higgsMass = 125
    settings.higgsResolution = 1.0

    pipe1 = Pipeline(settings, [canvasStart, ratio, 
                    lumi, 
                    DataSource(d),
                    SignalSource(vbf),
                    SignalSource(glu),
                    BackgroundSource(t),
                    BackgroundSource(b),
                    bkgDistrs, sigDistrs, dataDistr, 
                    ratioGen, logPadCust, canvasStop1])
    pipe2 = Pipeline(settings, [canvasStart, ratio, 
                    lumi, 
                    DataSource(d),
                    SignalSource(vbf),
                    SignalSource(glu),
                    BackgroundSource(t),
                    BackgroundSource(b),
                    bkgDistrs, sigDistrs, dataDistr, 
                    ratioGen, canvasStop2])

    wss = DefaultWorkspaceSource("higgs")
    mass = MassVariableGen()
    fc = FrameCreator()
    fp = FramePlotter()
    sigFit = SingleSignalFit(0)
    canvasStop3 = CanvasSaver("/tmp/test_3.png")
    pipe3 = Pipeline(settings, [canvasStart, wss, 
        mass, fc, SignalSource(vbf), sigFit, fp, canvasStop3])
    
    pipeVBF = Pipeline(settings, 
        [
            canvasStart, wss, 
            mass, fc, SignalSource(vbf), sigFit, fp, canvasStop3
        ]
    )
    
    pipeVBF1 = SharedPipeline(settings,
        [
            CanvasCreator("c2"), FrameCreator(),  SingleSignalFit(0),
            FramePlotter(), CanvasSaver("/tmp/test4.png")
        ]
    )
    pipeGLU = SharedPipeline(settings,
        [
            CanvasCreator("c3"), FrameCreator(), SingleSignalFit(1),
            FramePlotter(), CanvasSaver("/tmp/test5.png")
        ]
    )
#    pipeFits = Pipeline(settings, [CanvasCreator("some"), DefaultWorkspaceSource("higgs"), 
#        MassVariableGen(), SignalSource(vbf, glu),
#        pipeVBF1, pipeGLU])
    pipeVBF = Pipeline(settings, [CanvasCreator("VBF"), DefaultWorkspaceSource("higgs"),
        MassVariableGen(), FrameCreator(), SignalSource(vbf), SingleSignalFit(0),
        FramePlotter(), CanvasSaver("/tmp/test6.png")])


    # empty event!
    e1 = Event()
#    pipe1.execute(e1)
    e2 = Event()
#    pipe2.execute(e2)
    pipe = Pipeline(None, [pipe1, pipe2])
    pipe.execute(e1)
    eee = Event()
    pipe3.execute()
    print; print; print
    pipeVBF.execute()
#    pipeFits.execute(Event())
