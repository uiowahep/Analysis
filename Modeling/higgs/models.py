"""
All the Model Declaration/Definitions used are provided below
"""

from ROOT import *
import sys, os

#
# Build Models
#
def buildModel_SingleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    category=wargs["category"]
    ws.factory("Gaussian::smodel{processName}(x, m{processName}_mass_{category}, m{processName}_width_{category})".format(processName=processName, category=category))
    return ws.pdf("smodel%s" % processName)

def buildModel_DoubleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    category=wargs["category"]
    ws.factory("Gaussian::smodel{processName}_g1_{category}(x, m{processName}_g1_mass_{category}, m{processName}_g1_width_{category})".format(
        processName=processName, category=category))
    ws.factory("Gaussian::smodel{processName}_g2_{category}(x, m{processName}_g2_mass_{category}, m{processName}_g2_width_{category})".format(
        processName=processName, category=category))
    ws.factory("SUM::smodel{processName}(smodel{processName}_coef_{category}*smodel{processName}_g1_{category}, smodel{processName}_g2_{category})".format(
        processName=processName, category=category))
    return ws.pdf("smodel%s" % processName)

def buildModel_ExpGaus(ws, *kargs, **wargs):
    category = wargs["category"]
    ws.factory('expr::f("-(a1_{category}*(x/100)+a2_{category}*(x/100)^2)",a1_{category},a2_{category},x)'.format(category=category))
    ws.factory('Exponential::bmodel(f, 1)')
    return ws.pdf('bmodel')


#
# Create the Parameters for Models
#
def createParameters_SingleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    category=wargs["category"]
    ws.factory("m{processName}_mass_{category}[125, {massmin}, {massmax}]".format(
        processName=processName,
        category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
    ws.factory("m{processName}_width_{category}[1.0, 0.1, 10]".format(
        processName=processName, category=category))

def createParameters_DoubleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    category=wargs["category"]
    ws.factory("m{processName}_g1_mass_{category}[125, {massmin}, {massmax}]".format(
        processName=processName,
        category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
    ws.factory("m{processName}_g2_mass_{category}[125, {massmin}, {massmax}]".format(
        processName=processName,
        category=category, massmin=wargs["massmin"], massmax=wargs["massmax"]))
    ws.factory("m{processName}_g1_width_{category}[1.0, 0.1, 10]".format(
        processName=processName,
        category=category))
    ws.factory("m{processName}_g2_width_{category}[1.0, 0.1, 10]".format(
        processName=processName,
        category=category))
    ws.factory("smodel{processName}_coef_{category}[0.1, 0.0001, 1.0]".format(
        processName=processName,
        category=category))

def createParameters_ExpGaus(ws, *kargs, **wargs):
    ndata = wargs["ndata"]
    category=wargs["category"]
    ws.factory('a1_%s[ 5.0, -1000, 1000]' % category)
    ws.factory('a2_%s[ 5.0, -1000, 1000]' % category)
    ws.factory("bmodel_norm[%f, %f, %f]" % (ndata, ndata/2, ndata*2))


#
# Set Parameters Fixed
#
def setParameters_SingleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    norm = wargs["norm"]
    category=wargs["category"]
    ws.factory("smodel%s_norm[%f, 0.0, 1000]" % (processName, norm))
    ws.var("smodel%s_norm" % processName).setConstant(kTRUE)
    ws.var("m%s_mass_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("m%s_width_%s" % (processName, category)).setConstant(kTRUE)

def setParameters_DoubleGaus(ws, *kargs, **wargs):
    processName = wargs["processName"]
    norm = wargs["norm"]
    category=wargs["category"]
    ws.factory("smodel%s_norm[%f, 0.0, 1000]" % (processName, norm))
    ws.var("smodel%s_norm" % processName).setConstant(kTRUE)
    ws.var("m%s_g1_mass_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("m%s_g2_mass_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("m%s_g1_width_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("m%s_g2_width_%s" % (processName, category)).setConstant(kTRUE)
    ws.var("smodel%s_coef_%s" % (processName, category)).setConstant(kTRUE)

#
# Initialize the Mass Variable
#
def createVariables_Mass(ws, *kargs, **wargs):
    massmin = wargs["massmin"]
    massmax = wargs["massmax"]
    ws.factory("x[125.0, %f, %f]" % (massmin, massmax))
    ws.var("x").SetTitle("m_{#mu#mu}")
    ws.var("x").setUnit("GeV")
