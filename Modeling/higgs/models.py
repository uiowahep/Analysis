"""
All the Model Declaration/Definitions used are provided below
"""

from ROOT import *
import sys, os

#
# Model
#
class Model:
    def __init__(self, **wargs):
        self.wargs = wargs

    def build(self, ws, **wargs):
        return None

    def createParameters(self, ws, **wargs):
        pass

    def setParameters(self, ws, **wargs):
        pass

    def __str__(self):
        return "Unknown Model"

    def __repr__(self):
        return self.__str__()

    def getModelName(self):
        return self.modelName

class SingleGaus(Model):
    def __init__(self, **wargs):
        Model.__init__(self, **wargs)

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

    def setParameters_TripleGaus(self, ws, **wargs):
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
        self.modelName = "bmodel_%s" % self.wargs["category"]

    def build(self, ws, **wargs):
        category = self.wargs["category"]
        ws.factory('expr::f("-(a1_{category}*(x/100)+a2_{category}*(x/100)^2)",a1_{category},a2_{category},x)'.format(category=category))
        ws.factory('Exponential::bmodel_%s(f, 1)' % category)
        return ws.pdf('bmodel_%s' % category)

    def createParameters(self, ws, **wargs):
        ndata = wargs["ndata"]
        category = self.wargs["category"]
        ws.factory('a1_%s[ 5.0, -1000, 1000]' % category)
        ws.factory('a2_%s[ 5.0, -1000, 1000]' % category)
        ws.factory("bmodel_%s_norm[%f, %f, %f]" % (category, ndata, ndata/2, ndata*2))

#
# Initialize the Mass Variable
#
def createVariables_Mass(ws, *kargs, **wargs):
    massmin = wargs["massmin"]
    massmax = wargs["massmax"]
    ws.factory("x[125.0, %f, %f]" % (massmin, massmax))
    ws.var("x").SetTitle("m_{#mu#mu}")
    ws.var("x").setUnit("GeV")
