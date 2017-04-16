#!/usr/bin/python

import argparse
import os, sys
import definitions as defs
from Configuration.higgs.Iowa_settings import *
from Modeling.higgs2.aux import mkdir

parser = argparse.ArgumentParser()
parser.add_argument("--what", type=str,
    default="categories", help="What you want to run: combineCards or combine for now")
parser.add_argument('--mode', type=str, 
    default='Iowa', help='Run in Iowa, UF_AWB, or UF_AMC mode')
parser.add_argument("--method", type=str,
    default="Asymptotic", help="Which Combine Method to Run")
parser.add_argument("--signalModel", type=str,
    default="SingleGaus", help="Name of the Signal Model to be used")
parser.add_argument("--extraCombineOptions", type=str,
    default="", help="Additional Options to be passed directly to combine")
parser.add_argument("--outDirName", type=str,
    default="test", help="Directory Name that will be created in the .../combineoutput/$jobLabel/ folder where all the results will go to. Directory Name that will be created in the .../combinesubmissions/$joblabel/ folder where all the launchers will go to.")
parser.add_argument("--splitLevel", type=int,
    default=10, help="Split Level for when we create launchers to submit for batch processing")

args = parser.parse_args()

def split(cmds, splitLevel=10):
    """
    Split a given list of Commands into Jobs according to the Split Level
    """
    import definitions as defs
    ntotal = len(cmds)/splitLevel
    jobs = []
    for i in range(ntotal):
        job = defs.Job(str(i), cmds[i*splitLevel:(i+1)*splitLevel])
        jobs.append(job)
    
    return jobs

def writeHeader(launcherFile):
    """
    adds a header to the output launcher script that does:
        cd to CMSSW_SRC directory
        initialize the vars
        cd back to the directory from which we are to run combine
    """
    runCombineFromDir = os.path.join(combineoutputDir, args.outDirName)
    launcherFile.write("cd {pathToCMSSW}\n".format(pathToCMSSW=cmsswDir))
    launcherFile.write("eval `scramv1 runtime -sh`\n")
    launcherFile.write("cd {runCombineFromDir}\n".format(
        runCombineFromDir=runCombineFromDir))


def categories():
    #
    # prepare the submission/output dirs
    #
    outDir = os.path.join(combineoutputDir, args.outDirName)
    mkdir(outDir)
    submitDir = os.path.join(combinesubmissionsDir, args.outDirName)
    mkdir(submitDir)

    #
    # Do each Category separately
    #
    import definitions as defs
    cmds = []
    for category in categoriesToUse:
        datacard = os.path.join(datacardsworkspacesDir, "datacard__{category}__{signalModel}.root".format(category=names2RepsToUse[category], signalModel=args.signalModel))
        for massPoint in massPointsToUse:
            # set the mass for splines
            physicsModelParametersToSet["MH"] = massPoint

            cmdToRun = "combine -M {method} -m {mass} -n {outputModifier} -d {datacard} --setPhysicsModelParameters {physicsModelParametersToSet} --freezeNuisances {nuisancesToFreeze}".format(method=args.method, mass=massPoint, outputModifier=names2RepsToUse[category]+"__"+str(massPoint), datacard=datacard, physicsModelParametersToSet=map2string(physicsModelParametersToSet), nuisancesToFreeze=",".join(nuisancesToFreeze))
            cmd = defs.Command(category, [cmdToRun])
            cmds.append(cmd)

    #
    # Create laucnhers
    #
    jobs = split(cmds, args.splitLevel)
    batchSubmitFile = open(os.path.join(submitDir, "submit.sh"), "w")
    for job in jobs:
        launcherFile = os.path.join(submitDir, "launcher_{name}.sh".format(name=job.name))
        launchFile = open(os.path.join(submitDir, "launcher_{name}.sh".format(
            name=job.name)), "w")
        writeHeader(launchFile)
        launchFile.write("\n")
        launchFile.write(job.toString())
        launchFile.write("\n")
        launchFile.close()
        logFile = os.path.join(submitDir, "log_{name}.txt".format(name=job.name))
        errorFile = os.path.join(submitDir, "error_{name}.txt".format(name=job.name))
        forBatch = "bsub -q 1nh -o {logFile} -e {errorFile} {launcherFile}\n".format(
            logFile=logFile, errorFile=errorFile, launcherFile=launcherFile)
        batchSubmitFile.write(forBatch)
    batchSubmitFile.close()

def combineCards():
    print "Hello"

def main():
    import sys
    what = getattr(sys.modules[__name__], args.what)
    what()

if __name__=="__main__":
    main()
