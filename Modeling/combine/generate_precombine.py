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
parser.add_argument("--massPoints", type=int, nargs="+",
    help="Mass Points for which to probe/run combine")
parser.add_argument("--categoriesToSkip", type=str, nargs="*",
    default=[],
    help="Categories that should be skipped")
parser.add_argument("--signalModel", type=str,
    default="SingleGaus", help="Name of the Signal Model to be used")
parser.add_argument("--extraCombineOptions", type=str,
    default="", help="Additional Options to be passed directly to combine")
parser.add_argument("--inDirName", type=str,
    default="test", help="Directory name that has been created in .../datacardsworkspaces/$jobLabel/ in which all the datacards/workspaces reside. The idea is that you might regenerate the workspaces with different bin width or mass range or changing the background envelope and keep track of these changes up to Combine Step")
parser.add_argument("--outDirName", type=str,
    default="test", help="Directory Name that will be created in the .../combineoutput/$jobLabel/ folder where all the results will go to. Directory Name that will be created in the .../combinesubmissions/$joblabel/ folder where all the launchers will go to.")
parser.add_argument("--splitLevel", type=int,
    default=10, help="Split Level for when we create launchers to submit for batch processing")
parser.add_argument("--nToys", type=int,
    default=100, help="Number of Toys whenever this is needed")
parser.add_argument("--queue", type=str,
    default="1nh", help="Lxplus Batch Queue")

args = parser.parse_args()

def split(cmds, splitLevel=10):
    """
    Split a given list of Commands into Jobs according to the Split Level
    """
    import definitions as defs
    ntotal = len(cmds)/splitLevel + 1
    jobs = []
    for i in range(ntotal):
        start = i*splitLevel
        finish = (i+1)*splitLevel
#        finish = (i+1)*splitLevel if (i+1)*splitLevel<=len(cmds) else len(cmds)
        job = defs.Job(str(i), cmds[start:finish])
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

def createLaunchers(cmds, submitDir, label):
    """
    Create Launchers
    """
    jobs = split(cmds, args.splitLevel)
    batchSubmitFile = open(os.path.join(submitDir, 
        "submit_{label}.sh".format(label=label)), "w")
    for job in jobs:
        launcherFile = os.path.join(submitDir, "launcher_{label}_{name}.sh".format(name=job.name, label=label))
        launchFile = open(os.path.join(submitDir, "launcher_{label}_{name}.sh".format(
            name=job.name, label=label)), "w")
        writeHeader(launchFile)
        launchFile.write("\n")
        launchFile.write(job.toString())
        launchFile.write("\n")
        launchFile.close()
        logFile = os.path.join(submitDir, "log_{label}_{name}.txt".format(name=job.name,
            label=label))
        errorFile = os.path.join(submitDir, "error_{label}_{name}.txt".format(
            name=job.name, label=label))
        forBatch = "bsub -q {queue} -o {logFile} -e {errorFile} {launcherFile}\n".format(
            logFile=logFile, errorFile=errorFile, launcherFile=launcherFile, 
            queue=args.queue)
        batchSubmitFile.write(forBatch)
        os.system("chmod 755 " + launcherFile)
    batchSubmitFile.close()
    os.system("chmod 755 " + os.path.join(submitDir, "submit_{label}.sh".format(label=label)))

def combinations():
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
    for combination in combinationsToUse:
        if combination in args.categoriesToSkip:
            continue
        datacard = os.path.join(datacardsworkspacesDir, args.inDirName, 
            "datacard__{category}__{signalModel}.root".format(category=combination, signalModel=args.signalModel))
        for massPoint in args.massPoints:
            # set the mass for splines
            physicsModelParametersToSet["MH"] = massPoint

            outputModifier = combination + "__" + \
                str(massPoint) + "__" + args.signalModel
            cmdToRun = "combine -M {method} -m {mass} -n {outputModifier} -d {datacard} --setPhysicsModelParameters {physicsModelParametersToSet} --freezeNuisances {nuisancesToFreeze}".format(method=args.method, mass=massPoint, outputModifier=outputModifier, datacard=datacard, physicsModelParametersToSet=map2string(physicsModelParametersToSet), nuisancesToFreeze=",".join(nuisancesToFreeze))
            cmd = defs.Command(combination, [cmdToRun])
            cmds.append(cmd)

    label = "%s_%s_%s" % ("combinations", args.method, args.signalModel)
    createLaunchers(cmds, submitDir, label)

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
        if names2RepsToUse[category] in args.categoriesToSkip:
            continue
        datacard = os.path.join(datacardsworkspacesDir, args.inDirName, 
            "datacard__{category}__{signalModel}.root".format(category=names2RepsToUse[category], signalModel=args.signalModel))
        for massPoint in args.massPoints:
            # set the mass for splines
            physicsModelParametersToSet["MH"] = massPoint

            outputModifier = names2RepsToUse[category] + "__" + \
                str(massPoint) + "__" + args.signalModel
            cmdToRun = "combine -M {method} -m {mass} -n {outputModifier} -d {datacard} --setPhysicsModelParameters {physicsModelParametersToSet} --freezeNuisances {nuisancesToFreeze}".format(method=args.method, mass=massPoint, outputModifier=outputModifier, datacard=datacard, physicsModelParametersToSet=map2string(physicsModelParametersToSet), nuisancesToFreeze=",".join(nuisancesToFreeze))
            cmd = defs.Command(category, [cmdToRun])
            cmds.append(cmd)
    
    label = "%s_%s_%s" % ("categories", args.method, args.signalModel)
    createLaunchers(cmds, submitDir, label)

def biasScan():
    R.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

    #
    # prepare the submission/output dirs
    #
    outDir = os.path.join(combineoutputDir, args.outDirName)
    mkdir(outDir)
    submitDir = os.path.join(combinesubmissionsDir, args.outDirName)
    mkdir(submitDir)
    workspacesDir = os.path.join(datacardsworkspacesDir, args.inDirName)

    #
    # perform the scan
    #
    import definitions as defs
    cmds = []
    ourNuisances = nuisancesToFreeze
    for category in categoriesToUse:
        if names2RepsToUse[category] in args.categoriesToSkip:
            continue
        datacard = os.path.join(datacardsworkspacesDir, args.inDirName,
            "datacard__{category}__{signalModel}.root".format(
                category=names2RepsToUse[category], signalModel=args.signalModel))
        # add the current pdfindex to the list of nuisances to be frozen
        ourNuisances.append("pdfindex_{category}".format(
            category=names2RepsToUse[category]))

        # get the current workspace
        workspaceFileName = "workspace__{category}__{signalModel}.root".format(
            category=names2RepsToUse[category], signalModel=args.signalModel)
        currentWorkspaceFile = R.TFile(os.path.join(workspacesDir, workspaceFileName))
        higgsWorkspace = currentWorkspaceFile.Get("higgs")
        # get all the variables
        allVariables = higgsWorkspace.allVars().contentsString().split(",")
        # get the multipdf
        multipdf = higgsWorkspace.pdf("multipdf_{category}".format(
            category=names2RepsToUse[category]))
        for massPoint in args.massPoints:
            physicsModelParametersToSet["MH"] = massPoint
            # iterate thru all of the pdfs in our envelope
            for iref in range(multipdf.getNumPdfs()):
                # this is list of cmd strings that have to go as a single Command!
                cmdStrings = []
                # set the pdfindex_category to the iref
                physicsModelParametersToSet["pdfindex_{category}".format(
                    category=names2RepsToUse[category])] = iref
                
                outputModifierGenerateOnly = names2RepsToUse[category] + "__" + \
                    str(massPoint) + "__" + str(iref) + "__" + args.signalModel
                # generate the toys command
                cmdStrings.append("# GenerateOnly\n")
                cmdGenerateOnly = "combine -d {datacard} -n {outputModifier} -M GenerateOnly --setPhysicsModelParameters {physicsModelParametersToSet} --toysFrequentist -t {nToys} --expectSignal 1 --saveToys -m {mass} --freezeNuisances {nuisancesToFreeze}".format(
                    datacard=datacard, mass=massPoint, 
                    outputModifier=outputModifierGenerateOnly,
                    physicsModelParametersToSet=map2string(physicsModelParametersToSet),
                    nuisancesToFreeze=",".join(ourNuisances),
                    nToys = args.nToys)
                cmdStrings.append(cmdGenerateOnly)
                for ibkg in range(multipdf.getNumPdfs()):
                    currentPdfName = multipdf.getPdf(ibkg).GetName()
                    # retrieve the names of all other parameters
                    # that we have to fix. Given that we fit with ibkg
                    # parameters of other models must be frozen
                    # for the fit to be executed 100% correctly!!!
                    otherModelsParametersToFreeze = []
                    for var in allVariables:
                        for ipdf in range(multipdf.getNumPdfs()):
                            if ibkg==ipdf: continue
                            currentPdfName = multipdf.getPdf(ipdf).GetName()
                            if currentPdfName in var:
                                otherModelsParametersToFreeze.append(var)
                                break
                    # set the pdfindex_category to the model that
                    # we are going to fit our toy's reference with!
                    physicsModelParametersToSet["pdfindex_{category}".format(
                        category=names2RepsToUse[category])] = ibkg
                    outputModifier = names2RepsToUse[category] + "__" + \
                        str(massPoint) + "__" + str(iref) + "__" + str(ibkg) + \
                        "__" + args.signalModel
                    # perform the fit for that function
                    cmdStrings.append("# MaxLikelihoodFit\n")
                    cmdMaxLikelihoodFit = "combine -d {datacard} -M MaxLikelihoodFit  --setPhysicsModelParameters {physicsModelParametersToSet} --toysFile higgsCombine{outputModifierGenerateOnly}.GenerateOnly.mH{mass}.123456.root  -t {nToys} --rMin 0.1 --rMax 50 --freezeNuisances {nuisancesToFreeze} -m {mass} -n {outputModifier} --saveShapes --plots".format(datacard=datacard,
                        physicsModelParametersToSet=map2string(physicsModelParametersToSet),
                        outputModifierGenerateOnly=outputModifierGenerateOnly,
                        mass=massPoint, 
                        nuisancesToFreeze=",".join(ourNuisances +
                            otherModelsParametersToFreeze),
                        outputModifier=outputModifier,
                        nToys = args.nToys)
                    cmdStrings.append(cmdMaxLikelihoodFit)
                # create a single Command
                # We must not split Generation[iref] + Fit[iref, *]
                # this is exactly what we do - splitting on
                # iref!
                cmd = defs.Command(category, cmdStrings)
                cmds.append(cmd)
            # remove that pdfindex..... from the dictionary!
            del physicsModelParametersToSet["pdfindex_{category}".format(
                category=names2RepsToUse[category])]
#            cmd = defs.Command(category, cmdStrings)
#            cmds.append(cmd)
        # remove the current pdfindex from the list of nuisances to be frozen!
        ourNuisances.remove("pdfindex_{category}".format(
            category=names2RepsToUse[category]))

    label = "biasScan_{signalModel}".format(signalModel = args.signalModel)
    createLaunchers(cmds, submitDir, label)

def combineCards():
    datacardsDir = os.path.join(datacardsworkspacesDir, args.inDirName)
    for combination in combinationsToUse:
        combinedDatacard = "datacard__{combination}__{signalModel}.txt".format(
            combination=combination, signalModel=args.signalModel)
        lexploded = ["{label}=datacard__{category}__{signalModel}.txt".format(
            category=x, label=x, signalModel=args.signalModel) for x in combinationsToUse[combination]]
        os.system('./mycombineCards.sh {cmssw} {cardsDir} "{lexploded}" {combinedDatacard}'.format(cmssw = cmsswDir, cardsDir=datacardsDir, lexploded=" ".join(lexploded), combinedDatacard=combinedDatacard))


def text2workspace():
    datacardsDir = os.path.join(datacardsworkspacesDir, args.inDirName)
    os.system("./mytext2workspace.sh %s %s %s" % (datacardsDir,
        cmsswDir, args.signalModel))

def main():
    import sys
    what = getattr(sys.modules[__name__], args.what)
    what()

if __name__=="__main__":
    main()
