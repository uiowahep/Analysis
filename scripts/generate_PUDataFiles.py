#!/usr/bin/python

import os, sys, time, pickle, datetime, optparse
import ROOT as R

def main():
    print "-"*80
    print (" "*40)+"SET UP"+(" "*40)
    print "-"*80

    #   do the Framework imports
    if "ANALYSISHOME" not in os.environ.keys():
        raise NameError("Can not find ANALYSISHOME env var")
    sys.path.append(os.environ["ANALYSISHOME"])
    sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "NtupleProcessing/python"))
    import NtupleProcessing.python.Samples as S
    import NtupleProcessing.python.Dataset as DS

    #   set the variables
    cmsswdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_8_0_12/src/Analysis"
    analysisHome = os.environ["ANALYSISHOME"]
    dirToUse = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis"
    filelistdir = os.path.join(dirToUse, "filelists")
    resultsdir = os.path.join(dirToUse, "results")
    pileupdir = os.path.join(dirToUse, "pileup")
    import datetime
    rootpath = "/store/user/vkhriste/higgs_ntuples"
    aux = "Mu22"
    libext = ".so"
    shouldCreateFileList = True
    shouldCreateLaunchers = True
    shouldCreateSubmitter = True

    #   generate the pile up files for data
    print "-"*80
    print (" "*40)+"SET UP Ntuples"+(" "*40)
    print "-"*80
    pileups = S.pileups
    joblist = []
    cross_section_conversions = {"68" : 68000, "69" : 69000, "69p2" : 69200,
        "70" : 70000, "71" : 71000, "72" : 72000, "71p3" : 71300}
    for ipu in pileups:
        if "Cert_271036-280385_13TeV_PromptReco_Collisions16" not in ipu: continue
        jsonfilepathname = os.path.join(cmsswdir, "NtupleMaking/test/json", 
            pileups[ipu].datajson)
        outputfile=os.path.join(pileupdir, ipu+"mb.root")
        if "Collisions15" in ipu:
            year = "15"
        else:
            year = "16"
        cross_section = cross_section_conversions[pileups[ipu].cross_section]
        cmd = "pileupCalc.py -i {jsonfile} --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions{year}/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec {cross_section} --maxPileupBin 50 --numPileupBins 50 {outputfile}".format(
            jsonfile=jsonfilepathname, year=year, 
            cross_section=cross_section,
            outputfile=outputfile)
        joblist.append(cmd)
    for cmd in joblist:
        print "-"*40
        print cmd
        os.system(cmd)

if __name__=="__main__":
    main()
