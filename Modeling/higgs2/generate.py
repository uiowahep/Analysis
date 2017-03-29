"""
"""
import ROOT as R
R.gROOT.SetBatch(R.kTRUE)

import categories
from generatingFunctions import *
from Configuration.higgs.Iowa_settings import *
from categories import *
from common import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--number", type=int, default=0, help="number identifies the function to run")
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose debugging output')
parser.add_argument('-m', '--mode', type=str, default='Iowa', help='Run in Iowa, UF_AWB, or UF_AMC mode')
args = parser.parse_args()

def generate_backgroundFits():
    for category in run1Categories:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        modelsToUse = bersteinsPlusPhysModels
        counter = 0;
        for m in modelsToUse:
            m.color = colors[counter]
            counter+=1
        backgroundFits((category, diMuonMass125), ws, data, modelsToUse,
            pathToDir=backgroundfitsDir,groupName="bersteinsPlusPhysModels")

def generate_signalFits():
    for category in run1Categories:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        for modelToUse in [singleGaus, doubleGaus, tripleGaus]:
            modelToUse.color = R.kRed
            signalFit((category, diMuonMass125), ws, vbf, modelToUse, pathToDir=signalfitsDir)
            signalFit((category, diMuonMass125), ws, glu, modelToUse, pathToDir=signalfitsDir)
            signalFit((category, diMuonMass125), ws, wm, modelToUse, pathToDir=signalfitsDir)
            signalFit((category, diMuonMass125), ws, wp, modelToUse, pathToDir=signalfitsDir)
            signalFit((category, diMuonMass125), ws, zh, modelToUse, pathToDir=signalfitsDir)

def generate_distributions():
    logY = False
    for category in run1Categories:
        for vname in varNames:
            variable = {}
            variable["name"]=vname
            variable["min"]=-0.999
            variable["max"]=-0.999
            if category!="NoCats" and vname=="DiMuonMass":
                variable["min"] = 110
                variable["max"] = 160
            distributions((category, variable), data, [glu, vbf, wm, wp, zh],
                [wJetsToLNu, wwTo2L2Nu, wzTo3LNu, tt, dy], pathToDir=distributionsDir,
                logY=logY)

if __name__=="__main__":
    if args.number == 0:
        generate_distributions()
    elif args.number == 1:
        generate_signalFits()
    elif args.number == 2:
        generate_backgroundFits()
