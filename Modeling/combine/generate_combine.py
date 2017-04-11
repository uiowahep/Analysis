#!/usr/bin/python

import argparse
import os, sys
from Configuration.higgs.Iowa_settings import *

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, 
    default='Iowa', help='Run in Iowa, UF_AWB, or UF_AMC mode')
parser.add_argument("--mass", type=str,
    default="125", help="Mass to use")
parser.add_argument("--method", type=str,
    default="Asymptotic", help="Which Combine Method to Run")

args = parser.parse_args()

#
# given names for categories and datacard names
# returns a cmd to combine those and produce a combined datacard
#
def combineCards((namesForCombination, datacardNames), combinedDatacard):
    cardsToCombine = ""
    counter = 0
    for cardName in namesForCombination:
        cardsToCombine += "  {name}={datacard}".format(
            name=cardName, datacard=datacardNames[counter]
        )
        counter += 1
    cmd = "combineCards.py {cardsToCombine} > {combinedDatacard}\n".format(
        cardsToCombine=cardsToCombine, combinedDatacard=combinedDatacard
    )
    return cmd

def asymptotic(mass, outputModifier, pathToDatacard, **wargs):
    cmd = "combine -M Asymptotic -m {mass} -n {outputModifier} -d {pathToDatacard} {asymOptions}\n".format(
        mass=mass, outputModifier=outputModifier, pathToDatacard=pathToDatacard,
        **wargs
    )
    return cmd

def maxlikefit(mass, outputModifier, pathToDatacard, **wargs):
    cmd = "combine -M MaxLikelihoodFit -m {mass} -n {outputModifier} {pathToDatacard}\n".format(mass=mass, outputModifier=outputModifier, pathToDatacard=pathToDatacard)
    return cmd

def generate_combineCards():
    jobList = []
    #
    # generate the combined datacards
    #
    for combName in categoryCombinationsToUse:
        for signalModel in signalModelNames:
            datacardNames=["datacard__{category}__{signalModelName}.txt".format(
                signalModelName=signalModelName, category=c)
                for c in categoryCombinationsToUse[combName]]
            pathToCombineCard = "datacard__{combName}__{signalModelName}.txt".format(
                signalModeLName=signalModelName, combName=combName)
            cmdCombineCards = combineCards(categoryCombinationsToUse[combName],
                datacardNames, pathToCombineCard)
            jobList.append(cmdCombineCards)
    for job in jobList:
        print job

def generate_asymptoticCombination():
    jobList = []
    #
    # generate a job per combination per signalModel per mass point
    # this is a combination of categories
    #
    for combName in categoryCombinationsToUse:
        for signalModel in signalModelNames:
            combineDatacard = "datacard__{combName}__{signalModelName}.txt".format(
                signalModeLName=signalModelName, combName=combName)
            for mass in massListToUse:
                cmd = asymptotic(mass, outputModifier, combine)

def generate_asymptotic():
    jobList = []
    #
    # generate a job per category per signalModel per mass point
    # no combination!
    #
    for category in categoriesToUse:
        for signalModelName in signalModelNames:
            outputModifier = "__{category}__{signalModelName}".format(
                category=category, singalModelName=signalModelName)
            datacardName = "datacard__{category}__{signalModelName}.txt".format(
                category=category, signalModelName=signalModelName)
            pathToDatacard = os.path.join(datacardsworkspacesDir, datacardName)
            for mass in massListToUse:
                cmd = asymptotic(mass, outputModifier, pathToDatacard)
                jobList.append(cmd)
    for job in jobList:
        print job

def generate_maxlikefit():
    pass

if __name__=="__main__":
    if args.method=="Asymptotic":
        generate_asymptotic()
    elif args.method=="MaxLikelihoodFit":
        generate_maxlikefit()
    elif args.method=="CombineCards":
        generate_combineCards()
