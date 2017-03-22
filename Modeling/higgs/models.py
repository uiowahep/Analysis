"""
All the Model Declaration/Definitions used are provided below
"""

from ROOT import *
import sys, os

#
# Model
#
class Model(object):
    def __init__(self, **wargs):
        object.__init__(self)
        self.wargs = wargs
        self.modelId = self.__class__.__name__

    def build(self, ws, **wargs):
        return None

    def createParameters(self, ws, **wargs):
        pass

    def setParameters(self, ws, **wargs):
        pass

    def extractParameters(self, ws, fitws, **wargs):
        pass

    def __str__(self):
        return "Unknown Model"

    def __repr__(self):
        return self.__str__()

    def getModelName(self):
        return self.modelName

    def getModelId(self):
        return self.modelId

class SingleGaus(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "smodel{processName}_{category}".format(
            processName=self.wargs["processName"], category=self.wargs["category"])

    def __str__(self):
        return "Single Gaus Model"

    def build(self, ws, **wargs):
        processName = self.wargs["processName"]
        category = self.wargs["category"]
        ws.factory("Gaussian::smodel{processName}_{category}(x, m{processName}_mass_{category}, m{processName}_width_{category})".format(processName=processName, category=category))
        return ws.pdf("smodel%s_%s" % (processName, category))

    def createParameters(self, ws, **wargs):
        processName = self.wargs["processName"]
        category = self.wargs["category"]
        ws.factory("m{processName}_mass_{category}[125, {massmin}, {massmax}]".format(
            processName=processName,
            category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
        ws.factory("m{processName}_width_{category}[1.0, 0.1, 10]".format(
            processName=processName, category=category))
        ws.var("m{processName}_mass_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.var("m{processName}_width_{category}".format(
            processName=processName, category=category)).setUnit("GeV")
    
    def extractParameters(self, ws, fitws, **wargs):
        category = self.wargs["category"]
        processName = self.wargs["processName"]
        modifier = self.wargs["modifier"]
        const_parameters = fitws.constPars()
        lparameterNames = [
            "m{processName}_mass_{category}".format(category=category, 
                processName=processName),
            "m{processName}_width_{category}".format(category=category,
                processName=processName)
        ]
        # extract model parameters
        for pname in lparameterNames:
            getattr(ws, "import")(const_parameters.find(pname))
        # extract normalization
        normName = "shapeSig_smodel{processName}_{category}_{mod}{category}__norm".format(category=category, processName=processName, mod=modifier)
        getattr(ws, "import")(
            const_parameters.find(normName))
        self.norm = ws.var(normName)

    def setParameters(self, ws, **wargs):
        processName = self.wargs["processName"]
        norm = wargs["norm"]
        category = self.wargs["category"]
        ws.factory("smodel%s_%s_norm[%f, 0.0, 1000]" % (processName, category, norm))
        ws.var("smodel%s_%s_norm" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_mass_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_width_%s" % (processName, category)).setConstant(kTRUE)

class DoubleGaus(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "smodel{processName}_{category}".format(
            processName=self.wargs["processName"], category=self.wargs["category"])

    def build(self, ws, **wargs):
        processName = self.wargs["processName"]
        category = self.wargs["category"]
        ws.factory("Gaussian::smodel{processName}_g1_{category}(x, m{processName}_g1_mass_{category}, m{processName}_g1_width_{category})".format(
            processName=processName, category=category))
        ws.factory("Gaussian::smodel{processName}_g2_{category}(x, m{processName}_g2_mass_{category}, m{processName}_g2_width_{category})".format(
            processName=processName, category=category))
        ws.factory("SUM::smodel{processName}_{category}(smodel{processName}_coef_{category}*smodel{processName}_g1_{category}, smodel{processName}_g2_{category})".format(
            processName=processName, category=category))
        return ws.pdf("smodel%s_%s" % (processName, category))

    def createParameters(self, ws, **wargs):
        processName = self.wargs["processName"]
        category = self.wargs["category"]
        ws.factory("m{processName}_g1_mass_{category}[125, {massmin}, {massmax}]".format(
            processName=processName,
            category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
        ws.var("m{processName}_g1_mass_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("m{processName}_g2_mass_{category}[125, {massmin}, {massmax}]".format(
            processName=processName,
            category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
        ws.var("m{processName}_g2_mass_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("m{processName}_g1_width_{category}[1.0, 0.1, 10]".format(
            processName=processName,
            category=category))
        ws.var("m{processName}_g1_width_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("m{processName}_g2_width_{category}[1.0, 0.1, 10]".format(
            processName=processName,
            category=category))
        ws.var("m{processName}_g2_width_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("smodel{processName}_coef_{category}[0.1, 0.0001, 1.0]".format(
            processName=processName,
            category=category))
    
    def extractParameters(self, ws, fitws, **wargs):
        category = self.wargs["category"]
        processName = self.wargs["processName"]
        modifier = self.wargs["modifier"]
        const_parameters = fitws.constPars()
        lparameterNames = [
            "m{processName}_g1_mass_{category}".format(category=category, 
                processName=processName),
            "m{processName}_g1_width_{category}".format(category=category,
                processName=processName),
            "m{processName}_g2_mass_{category}".format(category=category, 
                processName=processName),
            "m{processName}_g2_width_{category}".format(category=category,
                processName=processName),
            "smodel{processName}_coef_{category}".format(category=category,
                processName=processName)
        ]
        # extract model parameters
        for pname in lparameterNames:
            getattr(ws, "import")(const_parameters.find(pname))
        # extract normalization
        normName = "shapeSig_smodel{processName}_{category}_{mod}{category}__norm".format(category=category, processName=processName, mod=modifier)
        getattr(ws, "import")(
            const_parameters.find(normName))
        self.norm = ws.var(normName)

    def setParameters(self, ws, **wargs):
        processName = self.wargs["processName"]
        norm = wargs["norm"]
        category = self.wargs["category"]
        ws.factory("smodel%s_%s_norm[%f, 0.0, 1000]" % (processName, category, norm))
        ws.var("smodel%s_%s_norm" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g1_mass_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g2_mass_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g1_width_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g2_width_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("smodel%s_coef_%s" % (processName, category)).setConstant(kTRUE)

class TripleGaus(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "smodel{processName}_{category}".format(
            processName=self.wargs["processName"], category=self.wargs["category"])

    def build(self, ws, **wargs):
        processName = self.wargs["processName"]
        category = self.wargs["category"]
        ws.factory("Gaussian::smodel{processName}_g1_{category}(x, m{processName}_g1_mass_{category}, m{processName}_g1_width_{category})".format(
            processName=processName, category=category))
        ws.factory("Gaussian::smodel{processName}_g2_{category}(x, m{processName}_g2_mass_{category}, m{processName}_g2_width_{category})".format(
            processName=processName, category=category))
        ws.factory("Gaussian::smodel{processName}_g3_{category}(x, m{processName}_g3_mass_{category}, m{processName}_g3_width_{category})".format(
            processName=processName, category=category))
        ws.factory("SUM::smodel{processName}_{category}(smodel{processName}_coef1_{category}*smodel{processName}_g1_{category}, smodel{processName}_coef2_{category}*smodel{processName}_g2_{category}, smodel{processName}_g3_{category})".format(
            processName=processName, category=category))
        return ws.pdf("smodel%s_%s" % (processName, category))

    def createParameters(self, ws, **wargs):
        processName = self.wargs["processName"]
        category = self.wargs["category"]
        ws.factory("m{processName}_g1_mass_{category}[125, {massmin}, {massmax}]".format(
            processName=processName,
            category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
        ws.var("m{processName}_g1_mass_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("m{processName}_g2_mass_{category}[125, {massmin}, {massmax}]".format(
            processName=processName,
            category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
        ws.var("m{processName}_g2_mass_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("m{processName}_g3_mass_{category}[125, {massmin}, {massmax}]".format(
            processName=processName,
            category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
        ws.var("m{processName}_g3_mass_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("m{processName}_g1_width_{category}[1.0, 0.1, 10]".format(
            processName=processName,
            category=category))
        ws.var("m{processName}_g1_width_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("m{processName}_g2_width_{category}[1.0, 0.1, 10]".format(
            processName=processName,
        category=category))
        ws.var("m{processName}_g2_width_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("m{processName}_g3_width_{category}[1.0, 0.1, 10]".format(
            processName=processName,
            category=category))
        ws.var("m{processName}_g3_width_{category}".format(
            processName=processName,
            category=category)).setUnit("GeV")
        ws.factory("smodel{processName}_coef1_{category}[0.1, 0.0001, 1.0]".format(
            processName=processName,
            category=category))
        ws.factory("smodel{processName}_coef2_{category}[0.1, 0.0001, 1.0]".format(
            processName=processName,
            category=category))
    
    def extractParameters(self, ws, fitws, **wargs):
        category = self.wargs["category"]
        processName = self.wargs["processName"]
        modifier = self.wargs["modifier"]
        const_parameters = fitws.constPars()
        lparameterNames = [
            "m{processName}_g1_mass_{category}".format(category=category, 
                processName=processName),
            "m{processName}_g1_width_{category}".format(category=category,
                processName=processName),
            "m{processName}_g2_mass_{category}".format(category=category, 
                processName=processName),
            "m{processName}_g2_width_{category}".format(category=category,
                processName=processName),
            "m{processName}_g3_mass_{category}".format(category=category, 
                processName=processName),
            "m{processName}_g3_width_{category}".format(category=category,
                processName=processName),
            "smodel{processName}_coef1_{category}".format(category=category,
                processName=processName),
            "smodel{processName}_coef2_{category}".format(category=category,
                processName=processName)
        ]
        # extract model parameters
        for pname in lparameterNames:
            getattr(ws, "import")(const_parameters.find(pname))
        # extract normalization
        normName = "shapeSig_smodel{processName}_{category}_{mod}{category}__norm".format(category=category, processName=processName, mod=modifier)
        getattr(ws, "import")(
            const_parameters.find(normName))
        self.norm = ws.var(normName)

    def setParameters(self, ws, **wargs):
        processName = self.wargs["processName"]
        norm = wargs["norm"]
        category = self.wargs["category"]
        ws.factory("smodel%s_%s_norm[%f, 0.0, 1000]" % (processName, category, norm))
        ws.var("smodel%s_%s_norm" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g1_mass_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g2_mass_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g3_mass_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g1_width_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g2_width_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("m%s_g3_width_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("smodel%s_coef1_%s" % (processName, category)).setConstant(kTRUE)
        ws.var("smodel%s_coef2_%s" % (processName, category)).setConstant(kTRUE)

class ExpGaus(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "bmodelExpGaus_%s" % self.wargs["category"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        ws.factory('expr::f("-(a1_{category}*(x/100)+a2_{category}*(x/100)^2)",a1_{category},a2_{category},x)'.format(category=category))
        ws.factory('Exponential::%s(f, 1)' % self.modelName)
        return ws.pdf(self.modelName)

    def extractParameters(self, ws, fitws, **wargs):
        category = self.wargs["category"]
        modifier = self.wargs["modifier"]
        float_parameters = fitws.floatParsFinal()
        lparameterNames = ["a1_{category}".format(category=category),
            "a2_{category}".format(category=category)]
        # extract model parameters
        for pname in lparameterNames:
            getattr(ws, "import")(float_parameters.find(pname))
        # extract normalization
        normName = "shapeBkg_{modelName}_{mod}{category}__norm".format(category=category, mod=modifier, modelName=self.modelName)
        getattr(ws, "import")(
            float_parameters.find(normName))
        self.norm = ws.var(normName)

    def createParameters(self, ws, **wargs):
        ndata = wargs["ndata"]
        category = self.wargs["category"]
        ws.factory('a1_%s[ 5.0, -1000, 1000]' % category)
        ws.factory('a2_%s[ 5.0, -1000, 1000]' % category)
        if "noNorm" in wargs: return
        else: ws.factory("%s_norm[%f, %f, %f]" % (self.modelName, 
            ndata, ndata/2, ndata*2))

class BWZRedux(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "bmodelBWZRedux_%s" % self.wargs["category"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        ws.factory("expr::bwzredux_f_{category}('(bwzredux_a2_{category}*(x/100)+bwzredux_a3_{category}*(x/100)^2)', x, bwzredux_a2_{category}, bwzredux_a3_{category})".format(
            category=category))
        ws.factory("EXPR::bmodelBWZRedux_{category}('exp(bwzredux_f_{category})*(2.5)/(pow(x-91.2, bwzredux_a1_{category}) + pow(2.5/2, bwzredux_a1_{category}))', x, bwzredux_a1_{category}, bwzredux_f_{category})".format(category=category))
        return ws.pdf("bmodelBWZRedux_%s" % category)

    def createParameters(self, ws, **wargs):
        ndata = wargs["ndata"]
        category = self.wargs["category"]
        ws.factory("bwzredux_a1_%s[1.39, 0.7, 2.1]" % category)
        ws.factory("bwzredux_a2_%s[0.47, 0.30, 0.62]" % category)
        ws.factory("bwzredux_a3_%s[-0.26, -0.40, -0.12]" % category)
        if "noNorm" in wargs: return
        else: ws.factory("%s_norm[%f, %f, %f]" % (self.modelName, 
            ndata, ndata/2, ndata*2))

    def extractParameters(self, ws, fitws, **wargs):
        pass

class BWZGamma(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "bmodelBWZGamma_%s" % self.wargs["category"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        ws.factory("EXPR::photonExp_{category}('exp(x*expParam_{category})*pow(x, -2)', x, expParam_{category})".format(category=category))
        ws.factory("EXPR::bwExp_{category}('exp(x*expParam_{category})*zwidth_{category}/(pow(x-zmass_{category}, 2) + 0.25*pow(zwidth_{category},2))', x, zmass_{category}, zwidth_{category}, expParam_{category})".format(category=category))
        ws.factory("SUM::bmodelBWZGamma_{category}(fraction_{category}*bwExp_{category}, photonExp_{category})".format(category=category))
        return ws.pdf("bmodelBWZGamma_%s" % category)

    def createParameters(self, ws, **wargs):
        ndata = wargs["ndata"]
        category = self.wargs["category"]
        ws.factory('zwidth_%s[2.5,0,30]' % category)
        ws.factory('zmass_%s[91.2, 90, 92]' % category)
        ws.factory("expParam_%s[-0.0053, -0.0073, -0.0033]" % category)
        ws.factory("fraction_%s[0.379, 0.2, 1]" % category)

        ws.var("zwidth_%s" % category).setConstant(kTRUE)
        ws.var("zmass_%s" % category).setConstant(kTRUE)
        if "noNorm" in wargs: return
        else: ws.factory("%s_norm[%f, %f, %f]" % (self.modelName, 
            ndata, ndata/2, ndata*2))

    def extractParameters(self, ws, fitws, **wargs):
        pass

class Bernstein(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "bmodelBernstein_%s" % self.wargs["category"]
        self.modelId += "_%d" % self.wargs["degree"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        ws.factory('Bernstein::%s(x, {%s})' % (self.modelName,
            ",".join("b%d_%s" % (i, category) for i in range(1, self.wargs["degree"]+1))))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]
        ndata = wargs["ndata"]
        for deg in range(1, degree+1):
            ws.factory("b{deg}_{category}[10, -1000, 1000]".format(category=category,
                deg=deg))
        if "noNorm" in wargs: return
        else: ws.factory("%s_norm[%f, %f, %f]" % (self.modelName, ndata, ndata/2,
            ndata*2))

class SumExponentials(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "bmodelSumExponentials_%s" % self.wargs["category"]
        self.modelId += "_%d" % self.wargs["degree"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]

        acc = []
        for i in range(degree):
            ws.factory("expr::exp_{i}_{category}('beta_{i}_{category}*exp(alpha_{i}_{category}*x)', x, alpha_{i}_{category}, beta_{i}_{category})".format(i=i+1, category=category))
            acc.append("exp_{i}_{category}".format(i=i+1, category=category))
        resultSum = "+".join(acc)
        resultComma = ",".join(acc)
        ws.factory("EXPR::bmodelSumExponentials_{category}('{resultSum}', {resultComma})".format(category=category, resultSum=resultSum, resultComma=resultComma))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]
        ndata = wargs["ndata"]

        for i in range(degree):
            ws.factory("beta_%d_%s[10, -1000000, 1000000]" % (i+1, category))
            ws.factory("alpha_%d_%s[1, -20, 20]" % (i+1, category))
        if "noNorm" in wargs: return
        else: ws.factory("%s_norm[%f, %f, %f]" % (self.modelName, ndata, ndata/2,
            ndata*2))

class SumPowers(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "bmodelSumPowers_%s" % self.wargs["category"]
        self.modelId += "_%d" % self.wargs["degree"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]
        
        acc = []
        for i in range(degree):
            ws.factory("expr::pol_{i}_{category}('b_{i}_{category}*pow(x, a_{i}_{category})', x, a_{i}_{category}, b_{i}_{category})".format(i=i+1, category=category))
            acc.append("pol_{i}_{category}".format(i=i+1, category=category))
        resultSum = "+".join(acc)
        resultComma = ",".join(acc)
        ws.factory("EXPR::bmodelSumPowers_{category}('{resultSum}', {resultComma})".format(category=category, resultSum=resultSum, resultComma=resultComma))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]
        ndata = wargs["ndata"]
        
        for i in range(degree):
            ws.factory("b_%d_%s[10, -100000000, 10000000]" % (i+1, category))
            ws.factory("a_%d_%s[1, -20, 20]" % (i+1, category))
        if "noNorm" in wargs: return
        else: ws.factory("%s_norm[%f, %f, %f]" % (self.modelName, ndata, ndata/2,
            ndata*2))

class LaurentSeries(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "bmodelLaurentSeries_%s" % self.wargs["category"]
        self.exponents = [-4, -3, -5, -2, -6, -1, -7, 0, -8, 1, -9]
        self.modelId += "_%d" % self.wargs["degree"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]
        
        acc = []
        for i in range(degree):
            ws.factory("expr::lpol_{i}_{category}('lcoeff_{i}_{category}*pow(x, {exponent})', x, lcoeff_{i}_{category})".format(i=i+1, category=category, exponent=self.exponents[i]))
            acc.append("lpol_{i}_{category}".format(i=i+1, category=category))
        resultSum = "+".join(acc)
        resultComma = ",".join(acc)
        ws.factory("EXPR::bmodelLaurentSeries_{category}('{resultSum}', {resultComma})".format(category=category, resultSum=resultSum, resultComma=resultComma))
        return ws.pdf(self.modelName)

    def createParameters(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]
        ndata = wargs["ndata"]
        
        for i in range(degree):
            ws.factory("lcoeff_%d_%s[10, -1000, 1000]" % (i+1, category))
        if "noNorm" in wargs: return
        else: ws.factory("%s_norm[%f, %f, %f]" % (self.modelName, ndata, ndata/2,
            ndata*2))

class Polynomial(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)
        self.modelName = "bmodelPolynomial_%s" % self.wargs["category"]
        self.modelId += "_%d" % self.wargs["degree"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        degree = self.wargs["degree"]
        lParameters = ",".join("p%d_%s" % (i, category) for i in range(1, degree+1))
        print lParameters
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

#
# Initialize the Mass Variable
#
def createVariables_Mass(ws, *kargs, **wargs):
    massmin = wargs["massmin"]
    massmax = wargs["massmax"]
    ws.factory("x[125.0, %f, %f]" % (massmin, massmax))
    ws.var("x").SetTitle("m_{#mu#mu}")
    ws.var("x").setUnit("GeV")
