#!/usr/bin/python

import sys, os

## Can add more categories, combinations of categories later - AWB 23.02.17
categories = ["01JetsTightBB"]
combinations = {}

## Nominal, hard-coded cross section ... doesn't really need to be an option - AWB 23.02.17
cross_sections = ["69"]

## Datacard output location, and arbitrary version tag? - AWB 23.02.17
## Something in here is unfortunately buggy
version = 'AWB_Feb23_test'
datacardsdir = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/datacards/%s' % version

def mkdir(pathdir):
    if os.path.exists(pathdir):
        return
    else:
        os.system("mkdir %s" % pathdir)

## Not sure what all these do.  cmsswdir is where you "cmsenv" for Higgs Combine tool. - AWB 23.02.17
## Something in here is unfortunately buggy
bindir    = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/submission'
limitsdir = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/output'
cmsswdir  = "/afs/cern.ch/user/a/abrinke1/CMSSW_7_4_7/src"
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
