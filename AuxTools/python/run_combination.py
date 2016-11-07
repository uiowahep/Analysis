#!/usr/bin/python

import sys, os

categories = ["VBFTight", "ggFLoose", "ggFTight",
    "01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
    "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO",
    "01JetsTightBB", "01JetsTightBE", "01JetsTightBO",
    "01JetsTightEE", "01JetsTightOE", "01JetsTightOO"
]

combinations = {
    "2JetCombination" : ["VBFTight", "ggFLoose", "ggFTight"],
    "01JetCombination" : ["01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
        "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO",
        "01JetsTightBB", "01JetsTightBE", "01JetsTightBO",
        "01JetsTightEE", "01JetsTightOE", "01JetsTightOO"],
        "TotalCombination" : categories,
    "2JetCombinationNoVBFTight" : ["ggFLoose", "ggFTight"],
}
combinations["TotalCombinationNoVBFTight"] = combinations["2JetCombinationNoVBFTight"] + combinations["01JetCombination"]

cross_sections = ["68", "69", "70", "71", "71p3", "72"]
version = "v0p6_20160824_1100"
datacardsdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_7_4_9/src/datacards/%s/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22" % version

def mkdir(pathdir):
    if os.path.exists(pathdir):
        return
    else:
        os.system("mkdir %s" % pathdir)

limitsdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_7_4_9/src/limits"
version = datacardsdir.split("/")[-2]
cmsswdir = datacardsdir.split("/")[-1]
limitsdir+="/%s" % version
mkdir(limitsdir)
limitsdir+="/%s" % cmsswdir
mkdir(limitsdir)
typesetting = "templates"
mass = 125

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
            os.system("combineCards.py %s > %s" % (list_datacards, combdatacardname))
            #   compute limits
            os.system("combine -M Asymptotic -m 125 -n %s %s" % (
                outname_modifier, combdatacardname))
            #   do the simultaneous fits
#            os.system("combine -M MaxLikelihoodFit -m 125 -n %s %s" % (
#                outname_modifier, combdatacardname))

def generate_analytic():
    bmodel = "ExpGaus"
    smodels = ["SingleGaus", "DoubleGaus"]
    generate_combination=True
    generate_separate=True
    smode = sys.argv[1]
    for smodel in smodels:
        for pu in cross_sections:
            path_to_limits = limitsdir + "/%s" % pu
            mkdir(path_to_limits)
            os.chdir(path_to_limits)
            print os.environ["PWD"]
            print path_to_limits
            #   separate limits + fits
            if generate_separate:
                for c in categories:
                    path_to_datacard = "%s/%s/datacard__%s__%s__%s__%s__%s__%s.txt" % (datacardsdir,
                        pu, typesetting, c, mass, bmodel, smode, smodel)
                    outname_modifier = "%s__%s__%s__%s__%s__%s" % (typesetting, c,
                        mass, bmodel, smode, smodel)
                    os.system("combine -M Asymptotic -m 125 -n %s %s" % (outname_modifier, 
                        path_to_datacard))
                    os.system("combine -M MaxLikelihoodFit -m 125 -n %s %s" % (outname_modifier, 
                        path_to_datacard))

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
                os.system("combineCards.py %s > %s" % (list_datacards, combdatacardname))
                #   compute limits
                os.system("combine -M Asymptotic -m 125 -n %s %s" % (
                    outname_modifier, combdatacardname))
                #   do the simultaneous fits
                os.system("combine -M MaxLikelihoodFit -m 125 -n %s %s" % (
                    outname_modifier, combdatacardname))

if __name__=="__main__":
    main()
