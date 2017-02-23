#!/usr/bin/python

#
# NOTE: Explanation of what the assumptions are and should be customized 
# - datacardsDir - root directory for datacards
# - workspacesDir - root directory of your workspaces
# - combineOutDir - root directory of combine outputs. Combined datacards will sit here!
# - submissionDir - root directory where launchers to submit to cern's bash will sit
# - cmsswDir - cmssw whose envs will be used to run combine
# - typesetting - I run both templates and analytic functions
# - smode - Signal Mode, previously used to do Combine or Separate (combining all signals together up front or leaving their contributions separately - separately is the preferred option!)
# - mass - mass that will go in, this is just a label for a datacard
# - version/pathModifier: datacards folder (if you generated those) will look the following:
#   datacardsDir/version/pathModifier/PUreweight/datacard1.txt....
#   The idea was to preserve exactly which json/cmssw/ntuple generation used for this whole process
#

import sys, os
from Modeling.higgs.categories import *
from Modeling.higgs.aux import *

#    "0bJets4lCombination" : ["0bJets4l2Mu1e", "0bJets4l3Mu1e",
#        "0bJets4l2Mu2e", "0bJets4l3Mu0e", "0bJets4l4Mu0e"],
#    "1bJetsCombination" : ["1bJets4l2Mu2e", "1bJets4l3Mu1e", "1bJets4l4Mu",
#        "1bJets3l", "1bJets2l"]
#}
#combinations["TotalCombinationNoVBFTight"] = combinations["2JetCombinationNoVBFTight"] + combinations["01JetCombination"] + combinations["0bJets4lCombination"] + combinations["1bJetsCombination"]
#combinations["012JetCombination"] = combinations["2JetCombination"]+combinations["01JetCombination"]

pus = ["69"]
version = "vR1_20170217_1742__TTJets_DiLept_TuneCUETP8M1_13TeV-" + \
    "madgraphMLM-pythia8__allBkg"
datacardsDir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/datacards"
workspacesDir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/workspaces"
combineOutDir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/combineOutDir"
pathModifier = "80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__Mu24"

fullDatacardsDir = os.path.join(datacardsDir,
    version, pathModifier)
fullCombineOutDir = os.path.join(combineOutDir,
    version)
mkdir(fullCombineOutDir)
fullCombineOutDir = os.path.join(fullCombineOutDir, pathModifier)
mkdir(fullCombineOutDir)

submissionsDir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/combineSubmissions"
cmsswDir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_7_4_9/src"
submitFromDir = os.path.join(submissionsDir, version)
mkdir(submitFromDir)

typesetting = "analytic"
smode = "Separate"
mass = 125
joblist = []

submitFromDir = os.path.join(submitFromDir, "%s__%s" % (typesetting, smode))
mkdir(submitFromDir)

#
# explicitly list the category for combination and combinations themselves!
#
categories = run1CategoriesForCombination
combinations = combinationsRun1

#
# At this point configuration part is finished!
#
def main():
    if typesetting == "templates":
        generate_template()
    else:
        generate_analytic()

def generate_template():
    for pu in pus:
        path_to_limits = limitsdir+"/%s"%pu
        mkdir(path_to_limits)
        os.chdir(path_to_limits)
        generate_combination = True
        generate_separate = True
        print os.environ["PWD"]
        print path_to_limits 
        if generate_separate:
            for c in categories:
                path_to_datacard = "%s/%s/datacard__%s__%s__%s.txt" % (datacardsdir,
                    pu, typesetting, c, mass)
                outname_modifier = "%s__%s__%s" % (typesetting, c,
                    mass)
                os.system("combine -M Asymptotic -m 125 -n %s %s" % (outname_modifier, 
                    path_to_datacard))
#                os.system("combine -M MaxLikelihoodFit -m 125 -n %s %s" % (outname_modifier, 
#                    path_to_datacard))


        #   combination
        if not generate_combination: continue
        for comb in combinations:
            list_datacards = ""
            combdatacardname = "datacard__%s__%s__%s.txt" % (
                typesetting, comb, mass)
            outname_modifier = "%s__%s__%s" % (typesetting, comb,
                mass)
            for cat in combinations[comb]:
                path_to_datacard = "%s/%s/datacard__%s__%s__%s.txt" % (datacardsdir,
                    pu, typesetting, cat, mass)
                list_datacards += "  {name}={path_to_datacard}".format(
                    name=("bin"+cat), path_to_datacard=path_to_datacard)
            #   create a datacard with all the categories/channels
            print "list_datacards combined = %s" % list_datacards
            print "combdatacardname = %s" % combdatacardname
            cmd = "combineCards.py %s > %s" % (list_datacards, combdatacardname)
            joblist.append(cmd)
            #   compute limits
            cmd = "combine -M Asymptotic -m 125 -n %s %s" % (
                outname_modifier, combdatacardname)
            joblist.append(cmd)
            #   do the simultaneous fits
#            os.system("combine -M MaxLikelihoodFit -m 125 -n %s %s" % (
#                outname_modifier, combdatacardname))

def generate_analytic():
    bmodel = "ExpGaus"
    smodels = ["SingleGaus", "DoubleGaus"]

    generate_combination=True
    generate_separate=True
    jobid = 0
    for smodel in smodels:
        for pu in pus:
            #
            # full path to our datacards
            #
            pathFullDatacardsDir = os.path.join(fullDatacardsDir, pu)
            mkdir (pathFullDatacardsDir)

            #
            # full path to output files
            #
            pathFullCombineOutDir = os.path.join(fullCombineOutDir, pu)
            mkdir(pathFullCombineOutDir)

            #
            # build launchers
            #
            launcherName = "launcher_%d.sh" % jobid
            launcher = open(os.path.join(submitFromDir, launcherName), "w")
            launcher.write("cd %s\n" % cmsswDir)
            launcher.write("eval `scramv1 runtime -sh`\n")
            launcher.write("cd %s\n" % pathFullCombineOutDir)

            #
            # iterate over all categories and generate per Category Combine launcher
            # 
            if generate_separate:
                for c in categories:
                    pathToDatacard = os.path.join(pathFullDatacardsDir,
                        "datacard__%s__%s__%s__%s__%s__%s.txt" % (typesetting,
                        c, mass, bmodel, smode, smodel)
                    )
                    outModifier = "%s__%s__%s__%s__%s__%s" % (typesetting, c,
                        mass, bmodel, smode, smodel)
                    cmd1 = "combine -M Asymptotic -m 125 -n %s %s" % (outModifier, 
                        pathToDatacard)
                    cmd2 = "combine -M MaxLikelihoodFit -m 125 -n %s %s" % (
                        outModifier, pathToDatacard)
                    launcher.write("%s\n%s\n" % (cmd1, cmd2))
            joblist.append("bsub -q 1nh -o {logfile} -e {errorfile} {launcherscript}".format(logfile=os.path.join(submitFromDir, "log_%d.log" % jobid), errorfile=os.path.join(submitFromDir, "error_%d.log" % jobid), launcherscript=os.path.join(submitFromDir, "launcher_%d.sh" % jobid)))
            os.system("chmod 755 %s" % os.path.join(submitFromDir, launcherName))
            launcher.close()
            jobid+=1

            #
            # Create launchers for combination
            #
            launcherName = "launcher_%d.sh" % jobid
            launcher = open(os.path.join(submitFromDir, launcherName), "w")
            launcher.write("cd %s\n" % cmsswDir)
            launcher.write("eval `scramv1 runtime -sh`\n")
            launcher.write("cd %s\n" % pathFullCombineOutDir)
        #   combination
            if not generate_combination: continue
            for comb in combinations:
                listDatacards = ""
                #
                # NOTE: Combined datacards will sit in the folder with results!
                #
                pathToCombinedDatacard = os.path.join(pathFullCombineOutDir,
                    "datacard__%s__%s__%s__%s__%s__%s.txt" % (
                    typesetting, comb, mass, bmodel, smode, smodel))
                outModifier = "%s__%s__%s__%s__%s__%s" % (typesetting, comb,
                    mass, bmodel, smode, smodel)
                for cat in combinations[comb]:
                    pathToDatacard = os.path.join(pathFullDatacardsDir,
                        "datacard__%s__%s__%s__%s__%s__%s.txt" % (
                        typesetting, cat, mass, bmodel, smode, smodel))
                    listDatacards += "  {name}={path_to_datacard}".format(
                        name=("bin"+cat), path_to_datacard=pathToDatacard)

                #   create a datacard with all the categories/channels
                print "list_datacards combined = %s" % listDatacards
                print "combdatacardname = %s" % pathToCombinedDatacard

                #
                # cmd1 - combine the datacards you need
                # 
                cmd1 = "combineCards.py %s > %s" % (listDatacards, pathToCombinedDatacard)

                #
                # cmd2 - compute limits
                #
                cmd2 = "combine -M Asymptotic -m 125 -n %s %s" % (
                    outModifier, pathToCombinedDatacard)

                #
                # cmd3 - do the simultaneous fits
                #
                cmd3 = "combine -M MaxLikelihoodFit -m 125 -n %s %s" % (
                    outModifier, pathToCombinedDatacard)
                launcher.write("%s\n%s\n%s\n" % (cmd1, cmd2, cmd3))
            
            #
            # appending to the list of jobs to submit
            #
            joblist.append("bsub -q 1nh -o {logfile} -e {errorfile} {launcherscript}".format(logfile=os.path.join(submitFromDir, "log_%d.log" % jobid), errorfile=os.path.join(submitFromDir, "error_%d.log" % jobid), launcherscript=os.path.join(submitFromDir, "launcher_%d.sh" % jobid)))
            os.system("chmod 755 %s" % os.path.join(submitFromDir, launcherName))
            launcher.close()
            jobid+=1
    submitterName = "submit.sh"
    sub = open(os.path.join(submitFromDir, submitterName), "w")
    for cmd in joblist:
        sub.write("%s\n" % cmd)
    os.system("chmod 755 %s" % os.path.join(submitFromDir, submitterName))
    sub.close()

if __name__=="__main__":
    main()
