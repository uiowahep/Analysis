"""
All the Model Declaration/Definitions used are provided below
"""

import sys, os
import ROOT as R
import array 

#
# Model
#
class Model(object):
    def __init__(self, initialValues=None, **wargs):
        """
        Each Model Constructor is just dummy
        The only thing we could want is the parameter initialization function
        """
        object.__init__(self)
        self.initialValues = initialValues
        self.modelId = self.__class__.__name__
        if hasattr(self, "degree"):
            self.modelId += "_%d" % self.degree

    def initialize(self, modelName, *kargs, **wargs):
        self.modelName = modelName

    def build(self, ws, **wargs):
        return None

    def createParameters(self, ws, **wargs):
        pass

    def setParameters(self, ws, **wargs):
        pass

    def extractParameters(self, ws, fitws, **wargs):
        pass

    def extract(self, ws, **wargs):
        return None

    def __str__(self):
        return self.modelId

    def __repr__(self):
        return self.__str__()

    def getModelName(self):
        return self.modelName

    def getModelId(self):
        return self.modelId

    def getNDF(self):
        return 0

class SingleGaus(Model):
    def __init__(self, initialValues=None, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def __str__(self):
        return "Single Gaus Model"

    def build(self, ws, **wargs):
        ws.factory("Gaussian::{modelName}(x, mean_{modelName}, sigma_{modelName})".format(
            modelName=self.modelName))
        return ws.pdf(self.modelName)

    def buildWithParameterMatrix(self, ws, massPoints, pmatrix, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
        means = pmatrix[0]
        sigmas = pmatrix[1]
        meansArray = array.array("f", means)
        sigmasArray = array.array("f", sigmas)
        massPointsArray = array.array("f", massPoints)
        # print meansArray
        # print sigmasArray
        # print massPointsArray
        meansSpline = R.RooSpline1D("mean_{modelName}".format(modelName=self.modelName),
            "mean_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(means), massPointsArray, meansArray)
        sigmasSpline = R.RooSpline1D("sigma_{modelName}".format(modelName=self.modelName),
            "sigma_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(means), massPointsArray, sigmasArray)
        meansSpline.Print("v")
        sigmasSpline.Print("v")
        getattr(ws, "import")(meansSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(sigmasSpline, R.RooFit.RecycleConflictNodes())
        ws.factory("Gaussian::{modelName}(x, mean_{modelName}, sigma_{modelName})".format(
            modelName=self.modelName))
        ws.Print("v")
        return ws.pdf(self.modelName)
    
    def setNormalization(self, ws, massPoints, norms, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
        massPointsArray = array.array("f", massPoints)
        normsArray = array.array("f", norms)
        normsSpline = R.RooSpline1D("{modelName}_norm".format(modelName=self.modelName),
            "{modelName}_norm".format(modelName=self.modelName),
            ws.var("MH"), len(massPoints), massPointsArray, normsArray)
        getattr(ws, "import")(normsSpline, R.RooFit.RecycleConflictNodes())

    def extract(self, cfg, **wargs):
        return ws.pdf(self.modelName)

    def setInitialValuesFromTH1(self, th1, **wargs):
        self.initialValues = {
            "mean" : th1.GetMean(), "meanmin" : th1.GetMean() - 2*th1.GetRMS(),
            "meanmax" : th1.GetMean() + 2*th1.GetRMS(),
            "sigma" : th1.GetRMS(), "sigmamin" : 0,
            "sigmamax" : 2*th1.GetRMS()
        }
        # print self.initialValues
    
    def getParameterValuesAsList(self, ws, **args):
        return \
            [
                ws.var("mean_{modelName}".format(modelName=self.modelName)).getVal(), 
                ws.var("sigma_{modelName}".format(modelName=self.modelName)).getVal()
            ]

    def setInitialValuesFromModel(self, model, ws, **wargs):
        massDifference = wargs["massDifference"]
        self.initialValues["mean"] = (ws.var("mean_{modelName}".format(modelName=model.modelName)).getVal()+massDifference)
        self.initialValues["sigma"] = ws.var("sigma_{modelName}".format(modelName=model.modelName)).getVal()

    def createParameters(self, ws, **wargs):
        # below we create model parameters
        ws.factory("mean_{modelName}[{mean}, {meanmin}, {meanmax}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("sigma_{modelName}[{sigma}, {sigmamin}, {sigmamax}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.var("mean_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
        ws.var("sigma_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
    
    def extractParameters(self, ws, **wargs):
        pass

    def fixParameters(self, ws, **wargs):
        ws.var("mean_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("sigma_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)

class DoubleGaus(Model):
    def __init__(self, initialValues=None, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)
    
    def build(self, ws, **wargs):
        g1 = ws.factory("Gaussian::g1_{modelName}(x, mean1_{modelName}, sigma1_{modelName})".format(
            modelName=self.modelName))
        g2 = ws.factory("Gaussian::g2_{modelName}(x, mean2_{modelName}, sigma2_{modelName})".format(
            modelName=self.modelName))
        self.gaussians = R.RooArgList(g1, g2)
        self.fractions = R.RooArgList(ws.var("coef_{modelName}".format(
            modelName=self.modelName)))
        doubleGaus = R.RooAddPdf(self.modelName, self.modelName,
            self.gaussians, self.fractions, R.kTRUE)
        getattr(ws, "import")(doubleGaus, R.RooFit.RecycleConflictNodes())
        return ws.pdf(self.modelName)

    def buildWithParameterMatrix(self, ws, massPoints, pmatrix, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
        mean1s = pmatrix[0]
        sigma1s = pmatrix[1]
        mean2s = pmatrix[2]
        sigma2s = pmatrix[3]
        coefs = pmatrix[4]

        mean1sArray = array.array("f", mean1s)
        sigma1sArray = array.array("f", sigma1s)
        mean2sArray = array.array("f", mean2s)
        sigma2sArray = array.array("f", sigma2s)
        coefsArray = array.array("f", coefs)
        massPointsArray = array.array("f", massPoints)
        
        mean1sSpline = R.RooSpline1D("mean1_{modelName}".format(modelName=self.modelName),
            "mean1_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(mean1s), massPointsArray, mean1sArray)
        sigma1sSpline = R.RooSpline1D("sigma1_{modelName}".format(modelName=self.modelName),
            "sigma1_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(sigma1s), massPointsArray, sigma1sArray)
        mean2sSpline = R.RooSpline1D("mean2_{modelName}".format(modelName=self.modelName),
            "mean2_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(mean2s), massPointsArray, mean2sArray)
        sigma2sSpline = R.RooSpline1D("sigma2_{modelName}".format(modelName=self.modelName),
            "sigma2_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(sigma2s), massPointsArray, sigma2sArray)
        coefsSpline = R.RooSpline1D("coef_{modelName}".format(modelName=self.modelName),
            "coef_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(coefs), massPointsArray, coefsArray)
        getattr(ws, "import")(mean1sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(sigma1sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(mean2sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(sigma2sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(coefsSpline, R.RooFit.RecycleConflictNodes())
        return self.build(ws)

    def setNormalization(self, ws, massPoints, norms, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
        massPointsArray = array.array("f", massPoints)
        normsArray = array.array("f", norms)
        normsSpline = R.RooSpline1D("{modelName}_norm".format(modelName=self.modelName),
            "{modelName}_norm".format(modelName=self.modelName),
            ws.var("MH"), len(massPoints), massPointsArray, normsArray)
        getattr(ws, "import")(normsSpline, R.RooFit.RecycleConflictNodes())

    def setInitialValuesFromTH1(self, th1, **wargs):
        self.initialValues = {
            "mean1" : th1.GetMean(), "mean1min" : th1.GetMean() - 2*th1.GetRMS(),
            "mean1max" : th1.GetMean() + 2*th1.GetRMS(),
            "sigma1" : th1.GetRMS(), "sigma1min" : 0,
            "sigma1max" : 2*th1.GetRMS(),
            "mean2" : th1.GetMean(), "mean2min" : th1.GetMean() - 2*th1.GetRMS(),
            "mean2max" : th1.GetMean() + 2*th1.GetRMS(),
            "sigma2" : th1.GetRMS(), "sigma2min" : 0,
            "sigma2max" : 2*th1.GetRMS(),
            "coef" : 0.8, "coefmin" : 0, "coefmax" : 1
        }

    def getParameterValuesAsList(self, ws, **args):
        return \
            [
                ws.var("mean1_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("sigma1_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("mean2_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("sigma2_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("coef_{modelName}".format(modelName=self.modelName)).getVal()
            ]

    def setInitialValuesFromModel(self, model, ws, **wargs):
        massDifference = wargs["massDifference"]
        # print self.initialValues
        
        mean1 = ws.var("mean1_{modelName}".format(modelName=model.modelName)).getVal()+massDifference
        sigma1 = ws.var("sigma1_{modelName}".format(modelName=model.modelName)).getVal()
        mean2 = ws.var("mean2_{modelName}".format(modelName=model.modelName)).getVal()+massDifference
        sigma2 = ws.var("sigma2_{modelName}".format(modelName=model.modelName)).getVal()
        coef = ws.var("coef_{modelName}".format(modelName=model.modelName)).getVal()
        self.initialValues["mean1"] = mean1 
        self.initialValues["sigma1"] = sigma1
        self.initialValues["mean2"] = mean2
        self.initialValues["sigma2"] = sigma2
        self.initialValues["coef"] = coef
        # print self.initialValues

    def createParameters(self, ws, **wargs):
        # gaus vars
        # print self.initialValues
        ws.factory("mean1_{modelName}[{mean1}, {mean1min}, {mean1max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("sigma1_{modelName}[{sigma1}, {sigma1min}, {sigma1max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.Print("v")
        # print "mean1_{modelName}".format(modelName=self.modelName)
        # print ws.var("mean1_{modelName}".format(modelName=self.modelName))
        # print ws.var("sigma1_{modelName}".format(modelName=self.modelName))
        ws.var("mean1_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
        ws.var("sigma1_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
        ws.factory("mean2_{modelName}[{mean2}, {mean2min}, {mean2max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("sigma2_{modelName}[{sigma2}, {sigma2min}, {sigma2max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.var("mean2_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
        ws.var("sigma2_{modelName}".format(modelName=self.modelName)).setUnit("GeV")

        # fraction
        ws.factory("coef_{modelName}[{coef}, {coefmin}, {coefmax}]".format(
            modelName=self.modelName, **self.initialValues
        ))

    def extractParameters(self, ws, fitws, **wargs):
        pass

    def setParameters(self, ws, **wargs):
        ws.var("mean1_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("sigma1_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("mean2_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("sigma2_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("coef_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)

class TripleGaus(Model):
    def __init__(self, initialValues=None, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
        # print "-"*90 + "\n"
        # print "-"*90 + "\n"
        # print "building finalmodel"
        g1 = ws.factory("Gaussian::g1_{modelName}(x, mean1_{modelName}, sigma1_{modelName})".format(
            modelName=self.modelName))
        g2 = ws.factory("Gaussian::g2_{modelName}(x, mean2_{modelName}, sigma2_{modelName})".format(
            modelName=self.modelName))
        g3 = ws.factory("Gaussian::g3_{modelName}(x, mean3_{modelName}, sigma3_{modelName})".format(
            modelName=self.modelName))
        self.gaussians = R.RooArgList(g1, g2, g3)
        if "Spline" in wargs:
            self.fractions = R.RooArgList(ws.function("coef1_{modelName}".format(
                modelName=self.modelName)), ws.function("coef2_{modelName}".format(
                modelName=self.modelName)))
        else:
            self.fractions = R.RooArgList(ws.var("coef1_{modelName}".format(
                modelName=self.modelName)), ws.var("coef2_{modelName}".format(
                modelName=self.modelName)))
        # print self.fractions.getSize()
        # print self.gaussians.getSize()
        tripleGaus = R.RooAddPdf(self.modelName, self.modelName,
            self.gaussians, self.fractions, R.kTRUE)
        getattr(ws, "import")(tripleGaus, R.RooFit.RecycleConflictNodes())
        return ws.pdf(self.modelName)
    
    def setInitialValuesFromTH1(self, th1, **wargs):
        self.initialValues = {
            "mean1" : th1.GetMean(), "mean1min" : th1.GetMean() - 0.2*th1.GetRMS(),
            "mean1max" : th1.GetMean() + 0.2*th1.GetRMS(),
            "sigma1" : 0.6*th1.GetRMS(), "sigma1min" : 0.2*th1.GetRMS(),
            "sigma1max" : 1.2*th1.GetRMS(),
            "mean2" : th1.GetMean(), "mean2min" : th1.GetMean() - 0.4*th1.GetRMS(),
            "mean2max" : th1.GetMean() + 0.4*th1.GetRMS(),
            "sigma2" : 1.0*th1.GetRMS(), "sigma2min" : 0.4*th1.GetRMS(),
            "sigma2max" : 1.8*th1.GetRMS(),
            "mean3" : th1.GetMean(), "mean3min" : th1.GetMean() - 2.4*th1.GetRMS(),
            "mean3max" : th1.GetMean() + 0.8*th1.GetRMS(),
            "sigma3" : 2.4*th1.GetRMS(), "sigma3min" : 1.2*th1.GetRMS(),
            "sigma3max" : 4.8*th1.GetRMS(),
            "coef1" : 0.7, "coef1min" : 0.5, "coef1max" : 1,
            "coef2" : 0.6, "coef2min" : 0.0, "coef2max" : 1
        }
        # print self.initialValues 
    
    def buildWithParameterMatrix(self, ws, massPoints, pmatrix, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
        mean1s = pmatrix[0]
        sigma1s = pmatrix[1]
        mean2s = pmatrix[2]
        sigma2s = pmatrix[3]
        mean3s = pmatrix[4]
        sigma3s = pmatrix[5]
        coef1s = pmatrix[6]
        coef2s = pmatrix[7]

        mean1sArray = array.array("f", mean1s)
        sigma1sArray = array.array("f", sigma1s)
        mean2sArray = array.array("f", mean2s)
        sigma2sArray = array.array("f", sigma2s)
        mean3sArray = array.array("f", mean3s)
        sigma3sArray = array.array("f", sigma3s)
        coef1sArray = array.array("f", coef1s)
        coef2sArray = array.array("f", coef2s)
        massPointsArray = array.array("f", massPoints)

        # print pmatrix
        # print massPoints
        
        mean1sSpline = R.RooSpline1D("mean1_{modelName}".format(modelName=self.modelName),
            "mean1_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(mean1s), massPointsArray, mean1sArray)
        sigma1sSpline = R.RooSpline1D("sigma1_{modelName}".format(modelName=self.modelName),
            "sigma1_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(sigma1s), massPointsArray, sigma1sArray)
        mean2sSpline = R.RooSpline1D("mean2_{modelName}".format(modelName=self.modelName),
            "mean2_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(mean2s), massPointsArray, mean2sArray)
        sigma2sSpline = R.RooSpline1D("sigma2_{modelName}".format(modelName=self.modelName),
            "sigma2_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(sigma2s), massPointsArray, sigma2sArray)
        mean3sSpline = R.RooSpline1D("mean3_{modelName}".format(modelName=self.modelName),
            "mean3_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(mean3s), massPointsArray, mean3sArray)
        sigma3sSpline = R.RooSpline1D("sigma3_{modelName}".format(modelName=self.modelName),
            "sigma3_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(sigma3s), massPointsArray, sigma3sArray)
        coef1sSpline = R.RooSpline1D("coef1_{modelName}".format(modelName=self.modelName),
            "coef1_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(coef1s), massPointsArray, coef1sArray)
        coef2sSpline = R.RooSpline1D("coef2_{modelName}".format(modelName=self.modelName),
            "coef2_{modelName}".format(modelName=self.modelName),
            ws.var("MH"), len(coef2s), massPointsArray, coef2sArray)
        getattr(ws, "import")(mean1sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(sigma1sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(mean2sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(sigma2sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(mean3sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(sigma3sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(coef1sSpline, R.RooFit.RecycleConflictNodes())
        getattr(ws, "import")(coef2sSpline, R.RooFit.RecycleConflictNodes())
        return self.build(ws, Spline=True)
    
    def setNormalization(self, ws, massPoints, norms, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
        massPointsArray = array.array("f", massPoints)
        normsArray = array.array("f", norms)
        normsSpline = R.RooSpline1D("{modelName}_norm".format(modelName=self.modelName),
            "{modelName}_norm".format(modelName=self.modelName),
            ws.var("MH"), len(massPoints), massPointsArray, normsArray)
        getattr(ws, "import")(normsSpline, R.RooFit.RecycleConflictNodes())
    
    def getParameterValuesAsList(self, ws, **args):
        return \
            [
                ws.var("mean1_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("sigma1_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("mean2_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("sigma2_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("mean3_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("sigma3_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("coef1_{modelName}".format(modelName=self.modelName)).getVal(),
                ws.var("coef2_{modelName}".format(modelName=self.modelName)).getVal()
            ]

    
    def setInitialValuesFromModel(self, model, ws, **wargs):
        massDifference = wargs["massDifference"]
        self.initialValues["mean1"] = ws.var("mean1_{modelName}".format(modelName=model.modelName)).getVal()+massDifference
        self.initialValues["sigma1"] = ws.var("sigma1_{modelName}".format(modelName=model.modelName)).getVal()
        self.initialValues["mean2"] = ws.var("mean2_{modelName}".format(modelName=model.modelName)).getVal()+massDifference
        self.initialValues["sigma2"] = ws.var("sigma2_{modelName}".format(modelName=model.modelName)).getVal()
        self.initialValues["mean3"] = ws.var("mean3_{modelName}".format(modelName=model.modelName)).getVal()+massDifference
        self.initialValues["sigma3"] = ws.var("sigma3_{modelName}".format(modelName=model.modelName)).getVal()
        self.initialValues["coef1"] = ws.var("coef1_{modelName}".format(modelName=model.modelName)).getVal()
        self.initialValues["coef2"] = ws.var("coef2_{modelName}".format(modelName=model.modelName)).getVal()

    def createParameters(self, ws, **wargs):
        # gaus vars
        ws.factory("mean1_{modelName}[{mean1}, {mean1min}, {mean1max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("sigma1_{modelName}[{sigma1}, {sigma1min}, {sigma1max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.var("mean1_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
        ws.var("sigma1_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
        ws.factory("mean2_{modelName}[{mean2}, {mean2min}, {mean2max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("sigma2_{modelName}[{sigma2}, {sigma2min}, {sigma2max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.var("mean2_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
        ws.var("sigma2_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
        ws.factory("mean3_{modelName}[{mean3}, {mean3min}, {mean3max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("sigma3_{modelName}[{sigma3}, {sigma3min}, {sigma3max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.var("mean3_{modelName}".format(modelName=self.modelName)).setUnit("GeV")
        ws.var("sigma3_{modelName}".format(modelName=self.modelName)).setUnit("GeV")

        # fraction
        ws.factory("coef1_{modelName}[{coef1}, {coef1min}, {coef1max}]".format(
            modelName=self.modelName, **self.initialValues
        ))
        ws.factory("coef2_{modelName}[{coef2}, {coef2min}, {coef2max}]".format(
            modelName=self.modelName, **self.initialValues
        ))
    
    def extractParameters(self, ws, fitws, **wargs):
        pass

    def setParameters(self, ws, **wargs):
        ws.var("mean1_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("sigma1_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("mean2_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("sigma2_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("mean3_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("sigma3_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("coef1_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)
        ws.var("coef2_{modelName}".format(modelName=self.modelName)).setConstant(kTRUE)

class ExpGaus(Model):
    def __init__(self, initialValues, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
        ws.factory('expr::f_{modelName}("-(a1_{modelName}*(x/100)+a2_{modelName}*(x/100)^2)",a1_{modelName},a2_{modelName},x)'.format(modelName=self.modelName))
        ws.factory('Exponential::{modelName}(f_{modelName}, 1)'.format(
            modelName=self.modelName))
        return ws.pdf(self.modelName)

    def extractParameters(self, ws, fitws, **wargs):
        pass

    def createParameters(self, ws, **wargs):
        ws.factory('a1_{modelName}[ {a1}, {a1min}, {a1max}]'.format(
            modelName=self.modelName, **self.initialValues))
        ws.factory('a2_{modelName}[ {a2}, {a2min}, {a2max}]'.format(
            modelName=self.modelName, **self.initialValues))

class BWZ(Model):
    def __init__(self, initialValues, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
        ws.factory("EXPR::{modelName}('exp(x*expParam_{modelName})*(zwidth_{modelName})/(pow(x-zmass_{modelName}, 2) + 0.25*pow(zwidth_{modelName}, 2))', x, zmass_{modelName}, zwidth_{modelName}, expParam_{modelName})".format(modelName=self.modelName))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        ws.factory("zwidth_{modelName}[{zwidth}, {zwidthmin}, {zwidthmax}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("zmass_{modelName}[{zmass}, {zmassmin}, {zmassmax}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expParam_{modelName}[{expParam}, {expParammin}, {expParammax}]".format(modelName=self.modelName, **self.initialValues))
        ws.var("zwidth_{modelName}".format(modelName=self.modelName)).setConstant(R.kTRUE)
        ws.var("zmass_{modelName}".format(modelName=self.modelName)).setConstant(R.kTRUE)


class BWZRedux(Model):  ## With power term ("a1") floating

    def __init__(self, initialValues, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)
    
    def build(self, ws, **wargs):
        ws.factory("expr::f_{modelName}('(a2sq_{modelName}*(x/100)-a3sq_{modelName}*(x/100)^2)', x, a2sq_{modelName}, a3sq_{modelName})".format(modelName=self.modelName))
        ws.factory("EXPR::{modelName}('exp(f_{modelName})/(pow(x-91.2, a1sq_{modelName}) + pow(2.5/2, a1sq_{modelName}))', x, a1sq_{modelName}, f_{modelName})".format(modelName=self.modelName))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        ws.factory("a1_{modelName}[{a1}, {a1min}, {a1max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a1sq_{modelName}('a1_{modelName}*a1_{modelName}', a1_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a2_{modelName}[{a2}, {a2min}, {a2max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a2sq_{modelName}('a2_{modelName}*a2_{modelName}', a2_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a3_{modelName}[{a3}, {a3min}, {a3max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a3sq_{modelName}('a3_{modelName}*a3_{modelName}', a3_{modelName})".format(
            modelName=self.modelName))

    def extractParameters(self, ws, fitws, **wargs):
        pass


class BWZReduxFixed(Model):  ## With power term ("a1") fixed to 2
    def __init__(self, initialValues, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)
    
    def build(self, ws, **wargs):
        ws.factory("expr::f_{modelName}('(a2sq_{modelName}*(x/100)-a3sq_{modelName}*(x/100)^2)', x, a2sq_{modelName}, a3sq_{modelName})".format(modelName=self.modelName))
        ws.factory("EXPR::{modelName}('exp(f_{modelName})/(pow(x-91.2, a1sq_{modelName}) + pow(2.5/2, a1sq_{modelName}))', x, a1sq_{modelName}, f_{modelName})".format(modelName=self.modelName))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        ws.factory("a2_{modelName}[{a2}, {a2min}, {a2max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a2sq_{modelName}('a2_{modelName}*a2_{modelName}', a2_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a3_{modelName}[{a3}, {a3min}, {a3max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a3sq_{modelName}('a3_{modelName}*a3_{modelName}', a3_{modelName})".format(
            modelName=self.modelName))

    def extractParameters(self, ws, fitws, **wargs):
        pass


class BWZReduxTimesLine(Model):  ## Multiplying by constant slope term (hardcoded for 110 - 150 GeV).  Manual hack - fix??? - AWB 13.07.17
    def __init__(self, initialValues, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)
    
    def build(self, ws, **wargs):
        ws.factory("expr::f_{modelName}('(a2sq_{modelName}*(x/100)-a3sq_{modelName}*(x/100)^2)', x, a2sq_{modelName}, a3sq_{modelName})".format(modelName=self.modelName))
        ws.factory("expr::g_{modelName}('(1+sin(a4_{modelName})*((x-110)/40))', x, a4_{modelName})".format(modelName=self.modelName))
        ws.factory("EXPR::{modelName}('exp(f_{modelName})*g_{modelName}/(pow(x-91.2, a1sq_{modelName}) + pow(2.5/2, a1sq_{modelName}))', x, a1sq_{modelName}, f_{modelName}, g_{modelName})".format(modelName=self.modelName))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        ws.factory("a1_{modelName}[{a1}, {a1min}, {a1max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a1sq_{modelName}('a1_{modelName}*a1_{modelName}', a1_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a2_{modelName}[{a2}, {a2min}, {a2max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a2sq_{modelName}('a2_{modelName}*a2_{modelName}', a2_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a3_{modelName}[{a3}, {a3min}, {a3max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a3sq_{modelName}('a3_{modelName}*a3_{modelName}', a3_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a4_{modelName}[{a4}, {a4min}, {a4max}]".format(
            modelName=self.modelName, **self.initialValues))

    def extractParameters(self, ws, fitws, **wargs):
        pass


class BWZReduxPlusLine(Model):  ## Add constant plus slope term (hardcoded for 110 - 150 GeV).  Manual hack - fix??? - AWB 13.07.17
    def __init__(self, initialValues, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)
    
    def build(self, ws, **wargs):
        ws.factory("expr::f_{modelName}('(a2sq_{modelName}*(x/100)-a3sq_{modelName}*(x/100)^2)', x, a2sq_{modelName}, a3sq_{modelName})".format(modelName=self.modelName))
        ws.factory("expr::g_{modelName}('(a5sq_{modelName}*(1+sin(a4_{modelName})*((x-130)/20)))', x, a4_{modelName}, a5sq_{modelName})".format(modelName=self.modelName))
        ws.factory("EXPR::{modelName}('(g_{modelName} + exp(f_{modelName})/(pow(x-91.2, a1sq_{modelName}) + pow(2.5/2, a1sq_{modelName})))', x, a1sq_{modelName}, f_{modelName}, g_{modelName})".format(modelName=self.modelName))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        ws.factory("a1_{modelName}[{a1}, {a1min}, {a1max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a1sq_{modelName}('a1_{modelName}*a1_{modelName}', a1_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a2_{modelName}[{a2}, {a2min}, {a2max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a2sq_{modelName}('a2_{modelName}*a2_{modelName}', a2_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a3_{modelName}[{a3}, {a3min}, {a3max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a3sq_{modelName}('a3_{modelName}*a3_{modelName}', a3_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a4_{modelName}[{a4}, {a4min}, {a4max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("a5_{modelName}[{a5}, {a5min}, {a5max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a5sq_{modelName}('a5_{modelName}*a5_{modelName}', a5_{modelName})".format(
            modelName=self.modelName))

    def extractParameters(self, ws, fitws, **wargs):
        pass



class BWZReduxTimesPlusLine(Model):  ## Add constant plus slope term (hardcoded for 110 - 150 GeV).  Manual hack - fix??? - AWB 13.07.17
    def __init__(self, initialValues, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)
    
    def build(self, ws, **wargs):
        ws.factory("expr::f_{modelName}('(a2sq_{modelName}*(x/100)-a3sq_{modelName}*(x/100)^2)', x, a2sq_{modelName}, a3sq_{modelName})".format(modelName=self.modelName))
        ws.factory("expr::g_{modelName}('(a5sq_{modelName}*(1+sin(a4_{modelName})*((x-130)/20)))', x, a4_{modelName}, a5sq_{modelName})".format(modelName=self.modelName))
        ws.factory("expr::h_{modelName}('(1+sin(a6_{modelName})*((x-110)/40))', x, a6_{modelName})".format(modelName=self.modelName))
        ws.factory("EXPR::{modelName}('(g_{modelName} + exp(f_{modelName})*h_{modelName}/(pow(x-91.2, a1sq_{modelName}) + pow(2.5/2, a1sq_{modelName})))', x, a1sq_{modelName}, f_{modelName}, g_{modelName}, h_{modelName})".format(modelName=self.modelName))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        ws.factory("a1_{modelName}[{a1}, {a1min}, {a1max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a1sq_{modelName}('a1_{modelName}*a1_{modelName}', a1_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a2_{modelName}[{a2}, {a2min}, {a2max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a2sq_{modelName}('a2_{modelName}*a2_{modelName}', a2_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a3_{modelName}[{a3}, {a3min}, {a3max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a3sq_{modelName}('a3_{modelName}*a3_{modelName}', a3_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a4_{modelName}[{a4}, {a4min}, {a4max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("a5_{modelName}[{a5}, {a5min}, {a5max}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("expr::a5sq_{modelName}('a5_{modelName}*a5_{modelName}', a5_{modelName})".format(
            modelName=self.modelName))
        ws.factory("a6_{modelName}[{a6}, {a6min}, {a6max}]".format(
            modelName=self.modelName, **self.initialValues))

    def extractParameters(self, ws, fitws, **wargs):
        pass


class BWZGamma(Model):
    def __init__(self, initialValues, **wargs):
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
        ws.factory("EXPR::photonExp_{modelName}('exp(x*expParam_{modelName})*pow(x, -2)', x, expParam_{modelName})".format(modelName=self.modelName))
        ws.factory("EXPR::bwExp_{modelName}('exp(x*expParam_{modelName})*zwidth_{modelName}/(pow(x-zmass_{modelName}, 2) + 0.25*pow(zwidth_{modelName},2))', x, zmass_{modelName}, zwidth_{modelName}, expParam_{modelName})".format(modelName=self.modelName))
        ws.factory("SUM::{modelName}(fraction_{modelName}*bwExp_{modelName}, photonExp_{modelName})".format(modelName=self.modelName))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        ws.factory('zwidth_{modelName}[{zwidth},{zwidthmin},{zwidthmax}]'.format(modelName=self.modelName, **self.initialValues))
        ws.factory('zmass_{modelName}[{zmass},{zmassmin}, {zmassmax}]'.format(modelName=self.modelName, **self.initialValues))
        ws.factory("expParam_{modelName}[{expParam}, {expParammin}, {expParammax}]".format(modelName=self.modelName, **self.initialValues))
        ws.factory("fraction_{modelName}[{fraction}, {fractionmin}, {fractionmax}]".format(modelName=self.modelName, **self.initialValues))

        ws.var("zwidth_{modelName}".format(modelName=self.modelName)).setConstant(R.kTRUE)
        ws.var("zmass_{modelName}".format(modelName=self.modelName)).setConstant(R.kTRUE)

    def extractParameters(self, ws, fitws, **wargs):
        pass

class BernsteinFast(Model):
    def __init__(self, initialValues, **wargs):
        self.degree = wargs["degree"]
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
        # print self.parameters
        bern = R.RooBernsteinFast(self.degree)(self.modelName, self.modelName,
            ws.var("x"), self.parameters)
        getattr(ws, "import")(bern, R.RooFit.RecycleConflictNodes())
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        self.parameters = R.RooArgList()
        for deg in range(1, self.degree+1):
            ws.factory(("b%d_{modelName}[{b%d}, {b%dmin}, {b%dmax}]" % (
                deg, deg, deg, deg)).format(modelName=self.modelName, **self.initialValues))
            ws.factory(("expr::bsq%d_{modelName}('b%d_{modelName}*b%d_{modelName}', b%d_{modelName})" % (
                deg, deg, deg, deg)).format(modelName=self.modelName))
            self.parameters.add(ws.function("bsq{order}_{modelName}".format(
                order=deg, modelName=self.modelName)))

    def getNDF(self):
        return self.degree

class ModBernsteinFast(Model):
    def __init__(self, initialValues, **wargs):
        self.degree = wargs["degree"]
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
        # print self.parameters

        # bernstein part
        bern = R.RooBernsteinFast(self.degree)("bern_"+self.modelName, 
            "bern_"+self.modelName, ws.var("x"), self.parameters)
        getattr(ws, "import")(bern, R.RooFit.RecycleConflictNodes())
        
        # RooPower part
        exp = R.RooPower("exp_"+self.modelName, "exp",
            ws.var("x"), ws.var("tau_{modelName}".format(modelName=self.modelName)))
        getattr(ws, "import")(exp, R.RooFit.RecycleConflictNodes())

        # add them up
        functions = R.RooArgList(exp, bern)
        fractions = R.RooArgList(ws.var("fraction_{modelName}".format(
            modelName=self.modelName)))
        modbern = R.RooAddPdf(self.modelName, self.modelName,
            functions, fractions, True)

        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        self.parameters = R.RooArgList()
        ws.factory("tau_{modelName}[{tau}, {taumin}, {taumax}]".format(
            modelName=self.modelName, **self.initialValues))
        ws.factory("fraction_{modelName}[{fraction}, {fractionmin}, {fractionmax}]".format(modelName=self.modelName, **self.initialValues))
        for deg in range(1, self.degree+1):
            ws.factory(("b%d_{modelName}[{b%d}, {b%dmin}, {b%dmax}]" % (
                deg, deg, deg, deg)).format(modelName=self.modelName, **self.initialValues))
            ws.factory(("expr::bsq%d_{modelName}('b%d_{modelName}*b%d_{modelName}', b%d_{modelName})" % (
                deg, deg, deg, deg)).format(modelName=self.modelName))
            self.parameters.add(ws.function("bsq{order}_{modelName}".format(
                order=deg, modelName=self.modelName)))

    def getNDF(self):
        return self.degree + 2

class DYBernsteinFast(Model):
    def __init__(self, initialValues, **wargs):
        self.degree = wargs["degree"]
        self.dy = wargs["dy"]
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

        # bernstein part
        bern = R.RooBernsteinFast(self.degree)("bern_"+self.modelName, "bern"+self.modelName,
            ws.var("x"), self.parameters)
        getattr(ws, "import")(bern, R.RooFit.RecycleConflictNodes())
        
        # dy histo part
        # TODO: Hardcoded certain parts for now.  Manual hack - fix??? - AWB 13.07.17
        fdy = R.TFile(self.dy.pathToFile)
        hdy = fdy.Get(wargs["category"] + "/" + "DiMuonMass")
        rdy = aux.buildRooHist(ws, hdy)
        # 2 is the interpolation type
        histPdf = R.RooHistPdf("dy_"+self.modelName, "dy_"+self.modelName,
            ws.var("x"),  rdy, 2)
        getattr(ws, "import")(histPdf, R.RooFit.RecycleConflictNodes())

        # add the bern and dy parts
        functions = R.RooArgList(histPdf, bern)
        fractions = R.RooArgList(ws.var("fraction_{modelName}".format(
            modelName=self.modelName)))
        dybern = R.RooAddPdf(self.modelName, self.modelName,
                functions, fractions, 0)
        getattr(ws, "import")(dybern, R.RooFit.RecycleConflictNodes())

        return ws.pdf(self.modelName)
        
    def createParameters(self, ws, **wargs):
        self.parameters = R.RooArgList()
        ws.factory("fraction_{modelName}[{fraction}, {fractionmin}, {fractionmax}]".format(modelName=self.modelName, **self.initialValues))
        for deg in range(1, self.degree+1):
            ws.factory(("b%d_{modelName}[{b%d}, {b%dmin}, {b%dmax}]" % (
                deg, deg, deg, deg)).format(modelName=self.modelName, **self.initialValues))
            ws.factory(("expr::bsq%d_{modelName}('b%d_{modelName}*b%d_{modelName}', b%d_{modelName})" % (
                deg, deg, deg, deg)).format(modelName=self.modelName))
            self.parameters.add(ws.function("bsq{order}_{modelName}".format(
                order=deg, modelName=self.modelName)))

class Bernstein(Model):
    def __init__(self, initialValues, **wargs):
        self.degree = wargs["degree"]
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
        ws.factory('Bernstein::{modelName}(x, {paramList})'.format(
            modelName=self.modelName,
            paramList=("{" + ",".join("b{deg}_{modelName}".format(deg=i, 
                modelName=self.modelName) for i in range(1, self.degree+1)) + "}")))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        for deg in range(1, self.degree+1):
            ws.factory(("b%d_{modelName}[{b%d}, {b%dmin}, {b%dmax}]" % (deg, deg,
                deg, deg)).format(modelName=self.modelName,
                **self.initialValues))

class SumExponentials(Model):
    def __init__(self, initialValues, **wargs):
        self.degree = wargs["degree"]
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
        exps = R.RooArgList()
        for i in range(1, self.degree+1):
            ws.factory("Exponential::exp{degree}_{modelName}(x, alphasq{degree}_{modelName})".format(degree=i, modelName=self.modelName))
            exps.add(ws.pdf("exp{degree}_{modelName}".format(degree=i, 
                modelName=self.modelName)))
        
        expSum = R.RooAddPdf(self.modelName, self.modelName,
            exps, self.fractions, True)
        getattr(ws, "import")(expSum, R.RooFit.RecycleConflictNodes())
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        self.fractions = R.RooArgList()
        for i in range(1, self.degree+1):
            ws.factory(("alpha%d_{modelName}[{alpha%d}, {alpha%dmin}, {alpha%dmax}]" %
                (i, i, i, i)).format(modelName=self.modelName, **self.initialValues))
            ws.factory(("expr::alphasq%d_{modelName}('(-0.000000001 - alpha%d_{modelName}*alpha%d_{modelName})', alpha%d_{modelName})" %
                (i, i, i, i)).format(modelName=self.modelName, **self.initialValues))
            if i<self.degree:
                ws.factory(("fraction%d_{modelName}[{fraction%d}, {fraction%dmin}, {fraction%dmax}]" % (i,i,i,i)).format(modelName=self.modelName, **self.initialValues))
                self.fractions.add(ws.var("fraction{degree}_{modelName}".format(degree=i,
                    modelName=self.modelName)))

    def getNDF(self):
        return self.degree*2-1



class SumPoly(Model):  ## Hardcoded for 110 - 150 GeV).  Manual hack - fix??? - AWB 13.07.17
    def __init__(self, initialValues, **wargs):
        self.degree = wargs["degree"]
        Model.__init__(self, initialValues, **wargs)

    def initialize(self, modelName, *kargs, **wargs):
        Model.initialize(self, modelName, *kargs, **wargs)

    def build(self, ws, **wargs):
	formula = ""
	parameters = "x"
        for i in range(self.degree):
	    formula += "alphasq{degree}_{modelName}*pow((150-x)/40, {degree})".format(degree=i, modelName=self.modelName)
	    parameters += ",alphasq{degree}_{modelName}".format(degree=i, modelName=self.modelName)	    
	    if i<self.degree-1:
	        formula += "+"
       
	ws.factory("EXPR::{modelName}('{formula}', {parameters})".format(
	    modelName=self.modelName, formula=formula, parameters=parameters)) 
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        for i in range(self.degree):
            ws.factory(("alpha%d_{modelName}[{alpha%d}, {alpha%dmin}, {alpha%dmax}]" %
                (i, i, i, i)).format(modelName=self.modelName, **self.initialValues))
            ws.factory(("expr::alphasq%d_{modelName}('alpha%d_{modelName}*alpha%d_{modelName}', alpha%d_{modelName})" %
                (i, i, i, i)).format(modelName=self.modelName))

    def getNDF(self):
        return self.degree







class PowerLaw(Model):
    def __init__(self, initialValues, **wargs):
        self.degree = wargs["degree"]
        Model.__init__(self, initialValues, **wargs)

    def build(self, ws, **wargs):
        formula = ""
        parameters = "x"
        if self.degree==1:
            formula = "pow(x, alpha1_{modelName})".format(modelName=self.modelName)
            parameters += ",alpha1_{modelName}".format(modelName=self.modelName)
        else:
            for i in range(1, self.degree+1):
                parameters += ",alpha{degree}_{modelName}".format(
                    degree=i, modelName=self.modelName)
                if i<self.degree:
                    parameters += ",fraction{degree}_{modelName}".format(
                    degree=i, modelName=self.modelName)
                for j in range(1, i):
                    formula += "(1-fraction{degree}_{modelName})*".format(
                        degree=j, modelName=self.modelName)
                if i<self.degree:
                    formula += "fraction{degree}_{modelName}*pow(x, alpha{degree}_{modelName}) + ".format(degree=i, modelName=self.modelName)
                else:
                    formula += "pow(x, alpha{degree}_{modelName})".format(degree=i, modelName=self.modelName)

        # print formula + "\n"
        # print parameters + "\n"
        ws.factory("EXPR::{modelName}('{formula}', {parameters})".format(
            modelName=self.modelName, formula=formula, parameters=parameters))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        for i in range(1, self.degree+1):
            if i<self.degree:
                ws.factory(("fraction%d_{modelName}[{fraction%d}, {fraction%dmin}, {fraction%dmax}]" % (i,i,i,i)).format(modelName=self.modelName, **self.initialValues))
            ws.factory(("alpha%d_{modelName}[{alpha%d}, {alpha%dmin}, {alpha%dmax}]" % (
                i,i,i,i)).format(modelName=self.modelName, **self.initialValues))
            
    def getNDF(self):
        return self.degree*2-1

class LaurentSeriesRecursive(Model):
    def __init__(self, initialValues, **wargs):
        self.degree = wargs["degree"]
        self.exponents = wargs["exponents"]
        Model.__init__(self, initialValues, **wargs)

    def build(self, ws, **wargs):
        formula = ""
        parameters = "x"
        if self.degree==1:
            formula = "pow(x, alpha1_{modelName})".format(modelName=self.modelName)
            parameters += ",alpha1_{modelName}".format(modelName=self.modelName)
        else:
            for i in range(1, self.degree+1):
                parameters += ",alpha{degree}_{modelName}".format(
                    degree=i, modelName=self.modelName)
                if i<self.degree:
                    parameters += ",fraction{degree}_{modelName}".format(
                    degree=i, modelName=self.modelName)
                for j in range(1, i):
                    formula += "(1-fraction{degree}_{modelName})*".format(
                        degree=j, modelName=self.modelName)
                if i<self.degree:
                    formula += "fraction{degree}_{modelName}*pow(x, alpha{degree}_{modelName}) + ".format(degree=i, modelName=self.modelName)
                else:
                    formula += "pow(x, alpha{degree}_{modelName})".format(degree=i, modelName=self.modelName)

        # print formula + "\n"
        # print parameters + "\n"
        ws.factory("EXPR::{modelName}('{formula}', {parameters})".format(
            modelName=self.modelName, formula=formula, parameters=parameters))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        for i in range(1, self.degree+1):
            if i<self.degree:
                ws.factory(("fraction%d_{modelName}[{fraction%d}, {fraction%dmin}, {fraction%dmax}]" % (i,i,i,i)).format(modelName=self.modelName, **self.initialValues))
            
    def getNDF(self):
        return self.degree*2-1

class LaurentSeries(Model):
    def __init__(self, initialValues, **wargs):
        self.degree = wargs["degree"]
        self.exponents = wargs["exponents"]
        Model.__init__(self, initialValues, **wargs)
        #self.exponents = [-4, -3, -5, -2, -6, -1, -7, 0, -8, 1, -9]

    def build(self, ws, **wargs):
        R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
        
        powers = R.RooArgList()
        for i in range(1, self.degree+1):
            c = R.RooFit.RooConst(self.exponents[i-1])
            power = R.RooPower("power{degree}_{modelName}".format(degree=i, 
                modelName=self.modelName), "power{degree}_{modelName}".format(
                degree=i, modelName=self.modelName), ws.var("x"), 
                c)
            powers.add(power)
            getattr(ws, "import")(power, R.RooFit.RecycleConflictNodes())
        ws.Print("v")
        laur = R.RooAddPdf(self.modelName, self.modelName,
            powers, self.fractions, True)
        getattr(ws, "import")(laur, R.RooFit.RecycleConflictNodes())

        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        self.fractions = R.RooArgList()
        for i in range(1, self.degree):
            ws.factory(("fraction%d_{modelName}[{fraction%d}, {fraction%dmin}, {fraction%dmax}]"% (i,i,i,i)).format(modelName=self.modelName, **self.initialValues))
            self.fractions.add(ws.var("fraction{degree}_{modelName}".format(degree=i,
                modelName=self.modelName)))

    def getNDF(self):
        return self.degree-1

class LogPolynomial(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.degree = wargs["degree"]

    def build(self, ws, **wargs):
        pass

    def createParameters(self, ws, **wargs):
        pass

class Polynomial(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "bmodelPolynomial_%s" % self.wargs["category"]
        self.modelId += "_%d" % self.wargs["degree"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]
        lParameters = ",".join("p%d_%s" % (i, category) for i in range(1, degree+1))
        # print lParameters
        ws.factory('Polynomial::%s(x, {%s})' % (self.modelName, lParameters))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]
        ndata = wargs["ndata"]
        for deg in range(1, degree+1):
            ws.factory("p{deg}_{category}[10, -10000000, 10000000]".format(category=category,
                deg=deg))
        if "noNorm" in wargs: return
        else: ws.factory("%s_norm[%f, %f, %f]" % (self.modelName, ndata, ndata/2,
            ndata*2))
