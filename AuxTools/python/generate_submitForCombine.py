#!/usr/bin/python

import sys, os

categories = ["VBFTight", "ggFLoose", "ggFTight",
    "01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
    "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO",
    "01JetsTightBB", "01JetsTightBE", "01JetsTightBO",
    "01JetsTightEE", "01JetsTightOE", "01JetsTightOO",

#    "1bJets4l2Mu2e", "1bJets4l3Mu1e", "1bJets4l4Mu",
#    "1bJets3l", "1bJets2l",
#    "0bJets4l2Mu1e", "0bJets4l3Mu0e", "0bJets4l3Mu1e", "0bJets4l4Mu0e", "0bJets4l2Mu2e"
]

combinations = {
    "2JetCombination" : ["VBFTight", "ggFLoose", "ggFTight"],
    "01JetCombination" : ["01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
        "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO",
        "01JetsTightBB", "01JetsTightBE", "01JetsTightBO",
        "01JetsTightEE", "01JetsTightOE", "01JetsTightOO"],
    "TotalCombination" : categories,
    "2JetsggF" : ["ggFLoose", "ggFTight"],
    "01JetsTightBarrel" : ["01JetsTightBB", "01JetsTightBO", "01JetsTightBE"],
    "01JetsTightOther" : ["01JetsTightOO", "01JetsTightOE", "01JetsTightEE"],
    "01JetsLoose" : ["01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
        "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO"],

#    "0bJets4lCombination" : ["0bJets4l2Mu1e", "0bJets4l3Mu1e",
#        "0bJets4l2Mu2e", "0bJets4l3Mu0e", "0bJets4l4Mu0e"],
#    "1bJetsCombination" : ["1bJets4l2Mu2e", "1bJets4l3Mu1e", "1bJets4l4Mu",
#        "1bJets3l", "1bJets2l"]
}
combinations["TotalCombinationNoVBFTight"] = combinations["2JetCombinationNoVBFTight"] + combinations["01JetCombination"]
#combinations["TotalCombinationNoVBFTight"] = combinations["2JetCombinationNoVBFTight"] + combinations["01JetCombination"] + combinations["0bJets4lCombination"] + combinations["1bJetsCombination"]
#combinations["012JetCombination"] = combinations["2JetCombination"]+combinations["01JetCombination"]

cross_sections = ["68", "69", "71","72", "69p2", "70", "71p3"]
#cross_sections = ["69"]
version = "vR1_20170122_1326__TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
datacardsdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/datacards/%s/80X__Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON__Mu24" % version

def mkdir(pathdir):
    if os.path.exists(pathdir):
        return
    else:
        os.system("mkdir %s" % pathdir)

bindir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/limits_submission"
limitsdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/limits/"
cmsswdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_7_4_9/src"
limitsdir+="/%s" % version
mkdir(limitsdir)
limitsdir = os.path.join(limitsdir, datacardsdir.split("/")[-1])
mkdir(limitsdir)

typesetting = "analytic"
#typesetting = "templates"
#smode = "Combined"
smode = "Separate"
mass = 125
joblist = []

dirToLaunchFrom = os.path.join(bindir, "submission"+"__"+version)
if not os.path.exists(dirToLaunchFrom):
    os.system("mkdir %s" % dirToLaunchFrom)
dirToLaunchFrom = os.path.join(dirToLaunchFrom, ("analytic__%s" % smode) if typesetting=="analytic" else "templates")
mkdir(dirToLaunchFrom)

#
# At this point configuration part is finished!
#
def main():
    if typesetting == "templates":
        generate_template()
    else:
        generate_analytic()

def generate_template():
    for pu in cross_sections:
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
        for pu in cross_sections:
            path_to_limits = limitsdir + "/%s" % pu
            mkdir(path_to_limits)
#            os.chdir(path_to_limits)
#            print os.environ["PWD"]
            print path_to_limits
            #   separate limits + fits

            launcherName = "launcher_%d.sh" % jobid
            launcher = open(os.path.join(dirToLaunchFrom, launcherName), "w")
            launcher.write("cd %s\n" %cmsswdir)
            launcher.write("eval `scramv1 runtime -sh`\n")
            launcher.write("cd %s\n" % path_to_limits)
            if generate_separate:
                for c in categories:
                    path_to_datacard = "%s/%s/datacard__%s__%s__%s__%s__%s__%s.txt" % (datacardsdir,
                        pu, typesetting, c, mass, bmodel, smode, smodel)
                    outname_modifier = "%s__%s__%s__%s__%s__%s" % (typesetting, c,
                        mass, bmodel, smode, smodel)
                    cmd1 = "combine -M Asymptotic -m 125 -n %s %s" % (outname_modifier, 
                        path_to_datacard)
                    cmd2 = "combine -M MaxLikelihoodFit -m 125 -n %s %s" % (
                        outname_modifier, path_to_datacard)
                    launcher.write("%s\n%s\n" % (cmd1, cmd2))
            joblist.append("bsub -q 1nh -o {logfile} -e {errorfile} {launcherscript}".format(logfile=os.path.join(dirToLaunchFrom, "log_%d.log" % jobid), errorfile=os.path.join(dirToLaunchFrom, "error_%d.log" % jobid), launcherscript=os.path.join(dirToLaunchFrom, "launcher_%d.sh" % jobid)))
            os.system("chmod 755 %s" % os.path.join(dirToLaunchFrom, launcherName))
            launcher.close()
            jobid+=1

            launcherName = "launcher_%d.sh" % jobid
            launcher = open(os.path.join(dirToLaunchFrom, launcherName), "w")
            launcher.write("cd %s\n" %cmsswdir)
            launcher.write("eval `scramv1 runtime -sh`\n")
            launcher.write("cd %s\n" % path_to_limits)
        #   combination
            if not generate_combination: continue
            for comb in combinations:
                list_datacards = ""
                combdatacardname = "datacard__%s__%s__%s__%s__%s__%s.txt" % (
                    typesetting, comb, mass, bmodel, smode, smodel)
                outname_modifier = "%s__%s__%s__%s__%s__%s" % (typesetting, comb,
                    mass, bmodel, smode, smodel)
                for cat in combinations[comb]:
                    path_to_datacard = "%s/%s/datacard__%s__%s__%s__%s__%s__%s.txt" % (datacardsdir,
                        pu, typesetting, cat, mass, bmodel, smode, smodel)
                    list_datacards += "  {name}={path_to_datacard}".format(
                        name=("bin"+cat), path_to_datacard=path_to_datacard)
                #   create a datacard with all the categories/channels
                print "list_datacards combined = %s" % list_datacards
                print "combdatacardname = %s" % combdatacardname
                cmd1 = "combineCards.py %s > %s" % (list_datacards, combdatacardname)
                #   compute limits
                cmd2 = "combine -M Asymptotic -m 125 -n %s %s" % (
                    outname_modifier, combdatacardname)
                #   do the simultaneous fits
                cmd3 = "combine -M MaxLikelihoodFit -m 125 -n %s %s" % (
                    outname_modifier, combdatacardname)
                launcher.write("%s\n%s\n%s\n" % (cmd1, cmd2, cmd3))
            joblist.append("bsub -q 1nh -o {logfile} -e {errorfile} {launcherscript}".format(logfile=os.path.join(dirToLaunchFrom, "log_%d.log" % jobid), errorfile=os.path.join(dirToLaunchFrom, "error_%d.log" % jobid), launcherscript=os.path.join(dirToLaunchFrom, "launcher_%d.sh" % jobid)))
            os.system("chmod 755 %s" % os.path.join(dirToLaunchFrom, launcherName))
            launcher.close()
            jobid+=1
    submitterName = "submit.sh"
    sub = open(os.path.join(dirToLaunchFrom, submitterName), "w")
    for cmd in joblist:
        sub.write("%s\n" % cmd)
    os.system("chmod 755 %s" % os.path.join(dirToLaunchFrom, submitterName))
    sub.close()

if __name__=="__main__":
    main()
