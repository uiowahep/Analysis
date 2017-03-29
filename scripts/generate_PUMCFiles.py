#!/usr/bin/python

import os, sys, time, pickle, datetime, optparse

def main():
    print "-"*80
    print (" "*40)+"SET UP"+(" "*40)
    print "-"*80
    
    import Configuration.higgs.Samples as S
    import Configuration.higgs.Dataset as DS
#    import Configuration.higgs.Samples as S
#    import Configuration.higgs.Dataset as DS

    #   set the variables
    executable = os.path.join(os.environ["ANALYSISHOME"], "process_HiggsAnalysis")
    batchSubmission = True
    storage = "EOS"
    cmsswsrcdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_8_0_25/src"
    cmsswdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_8_0_25/src/Analysis"
    dirToUse = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis"
    executable = os.path.join(dirToUse, "bin/build-29032017", "generate_PUMCFiles")
    analysisHome = os.environ["ANALYSISHOME"]
    shouldGenPUMC = 1
    filelistdir = os.path.join(dirToUse, "filelists")
    resultsdir = os.path.join(dirToUse, "results")
    pileupdir = os.path.join(dirToUse, "pileup_moriond2017")
    version = "v0"
    resultsdir+= "/"+version
    queue = '1nh'
    rootpath = "/store/user/vkhriste/higgs_ntuples"
    aux = "Mu24"
    libext = ".so"
    shouldCreateFileList = True
    shouldCreateLaunchers = True
    shouldCreateSubmitter = True
    mcera = "mcMoriond2017"
    nbins = 80

    #
    #   generate all the Ntuple objects that are ready to be processed
    #
    print "-"*80
    print (" "*40)+"SET UP Ntuples"+(" "*40)
    print "-"*80
    mc_datasets = S.mcMoriond2017datasets_1
    mc_ntuples = []
    cmssw = "80X"
    for k in mc_datasets:
        #   use only 2016 MC with 80X
    #    if mc_datasets[k].initial_cmssw!="80X": continue
        #   skip DY for now...
#        if "DYJetsToLL" in mc_datasets[k].name: continue

        ntuple = DS.Ntuple(mc_datasets[k],
            json = None,
            cmssw = mc_datasets[k].initial_cmssw,
            storage=storage,
            rootpath = os.path.join(rootpath, mcera),
            timestamp=None,
            aux=aux
        )
        mc_ntuples.append(ntuple)
    ntuples = []
    ntuples.extend(mc_ntuples)

    #
    #   Iterate thru all the mc ntuples and generate the pileup files
    #   
    results = []
    print "-"*80
    print (" "*40)+"SET UP Result Objects"+(" "*40)
    print "-"*80
    for ntuple in ntuples:
        print ntuple
        try:
            print "00000000000000"
            filelist_as_list = S.discoverFileList(ntuple)
            print filelist_as_list
            filelist = os.path.join(filelistdir,S.buildFileListName(ntuple))
        except Exception as exc:
            print exc
            continue
        print "Creating a file list"
        if shouldCreateFileList:
            f = open(filelist, "w")
            for x in filelist_as_list:
                f.write("%s\n" % x)
            f.close()

        outFileName = S.buildPUfilename(ntuple)
#        os.chdir(cmsswsrcdir)
#        os.system("eval `scramv1 runtime -sh")
        os.system("{executable} --input={input} --output={output} --bins={bins}".format(
            executable=executable, input=filelist, 
            output=os.path.join(pileupdir, outFileName),
            directory=cmsswsrcdir, bins=nbins))
        s = """
        R.gSystem.Load("../libAnalysisCore%s" % libext)
        R.gSystem.Load("../libAnalysisNtupleProcessing%s" % libext)
        s = R.analysis.processing.Streamer(filelist,
            "ntuplemaker_H2DiMuonMaker/Events")
        s.chainup()

        aux = R.analysis.core.EventAuxiliary()
        s._chain.SetBranchAddress("EventAuxiliary", aux)

        outFileName = S.buildMCPUfilename(ntuple)
        out = R.TFile(os.path.join(pileupdir, outFileName), "recreate")
        h = R.TH1D("pileup", "pileup", 50, 0, 50)
        numEvents = s._chain.GetEntries()
        for i in range(numEvents):
            s._chain.GetEntry(i)
            if i%10000==0:
                print "Processing Event %d / %d" % (i, numEvents)
            h.Fill(aux._nPU, aux._genWeight)
        out.Write()
        out.Close()
"""

if __name__=="__main__":
    main()
