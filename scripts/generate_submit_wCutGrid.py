#!/usr/bin/python

import os, sys, time, pickle, datetime, optparse

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
    import NtupleProcessing.python.Cuts as Cuts

    #   set the variables
    bindir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/bin/build-4"
    executable = os.path.join(bindir, "process_HiggsAnalysis_wCutsExtended_NoPairing_wNewCats")
    batchSubmission = True
    dirToLaunchFrom = os.path.join(bindir, "submission")
    if not os.path.exists(dirToLaunchFrom):
        os.system("mkdir %s" % dirToLaunchFrom)
    storage = "EOS"
    cmsswdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_8_0_20/src/Analysis"
    dirToUse = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis"
    analysisHome = os.environ["ANALYSISHOME"]
    shouldGenPUMC = 1
    filelistdir = os.path.join(dirToUse, "filelists")
    resultsdir = os.path.join(dirToUse, "results")
    pileupdir = os.path.join(dirToUse, "pileup")
    import datetime
    version = "v2_"+datetime.datetime.now().strftime("%Y%m%d_%H%M")
    resultsdir+= "/"+version
    queue = '1nh'
    rootpath = "/store/user/vkhriste/higgs_ntuples"
    aux = "Mu24"
    shouldCreateFileList = True
    shouldCreateLaunchers = True
    shouldCreateSubmitter = True
    if not os.path.exists(resultsdir):
        os.system("mkdir %s" % resultsdir)

    #
    #   generate all the Ntuple objects that are ready to be processed
    #
    print "-"*80
    print (" "*40)+"SET UP Ntuples"+(" "*40)
    print "-"*80
    data_datasets = S.datadatasets
    mc_datasets = S.mcdatasets
    jsonfiles = S.jsonfiles
    jsontag = "2016_Prompt_29530"
    jsonfile = jsonfiles[jsontag]
    data_ntuples = []
    mc_ntuples = []
    cmssw = "80X"
    for k in data_datasets:
        if data_datasets[k].year!=2016 or "PromptReco" not in data_datasets[k].name: continue
        if "Run2016H-PromptReco-v1" in data_datasets[k].name: continue
        ntuple = DS.Ntuple(data_datasets[k],
            json = jsonfile.filename,
            cmssw = cmssw,
            storage = storage,
            rootpath = os.path.join(rootpath, "data"),
            timestamp = None,
            aux = aux
        )
        data_ntuples.append(ntuple)
    for k in mc_datasets:
        if mc_datasets[k].initial_cmssw!="80X": continue
        ntuple = DS.Ntuple(mc_datasets[k],
            json = None,
            cmssw = mc_datasets[k].initial_cmssw,
            storage=storage,
            rootpath = os.path.join(rootpath, "mc"),
            timestamp=None,
            aux=aux
        )
        mc_ntuples.append(ntuple)
    print data_ntuples
    print mc_ntuples
    ntuples = []
    ntuples.extend(data_ntuples)
    ntuples.extend(mc_ntuples)

    #
    #   Generate all the Results objects that are to be produced
    #   
    results = []
    print "-"*80
    print (" "*40)+"SET UP Result Objects"+(" "*40)
    print "-"*80
    for ntuple in ntuples:
        try:
            filelist_as_list = S.discoverFileList(ntuple)
            print filelist_as_list
            filelist = os.path.join(filelistdir,S.buildFileListName(ntuple))
        except Exception as exc:
            continue
        if shouldCreateFileList:
            f = open(filelist, "w")
            for x in filelist_as_list:
                f.write("%s\n" % x)
            f.close()
        if ntuple.isData:
            result = DS.DataResult(ntuple,
                filelist = filelist
            )
            results.append(result)
        else:
            for ipu in S.pileups:
                if "Cert_271036-282037" not in ipu or S.pileups[ipu].cross_section!="69p2": continue
                pu = S.pileups[ipu]
                result = DS.MCResult(ntuple,
                    filelist=filelist,
                    pileupdata=pu
                )
                results.append(result)

    #   construct the processing schema  
    print "-"*80
    print (" "*40)+"START"+(" "*40)
    print "-"*80
    joblist = []
    cmdlist = []
    jobid = 0
    for result in results:
        input_filelist = result.filelist;
        outputfilename = S.buildResultOutputPathName(result)
        print result

        for cut_set in Cuts.generate_cutsets1():
            cutfolder = Cuts.buildFolderName(cut_set)
            cmdcutstr = Cuts.buildcmdString(cut_set)
            fullpath2cutfolder = os.path.join(resultsdir, cutfolder)
            if not os.path.exists(fullpath2cutfolder):
                os.system("mkdir %s" % fullpath2cutfolder)
            output = os.path.join(fullpath2cutfolder, outputfilename)
            if not result.isData:
                (puMCfilename, puDATAfilename) = S.buildPUfilenames(result)
                puMCfilename = os.path.join(pileupdir, puMCfilename)
                puDATAfilename = os.path.join(pileupdir, puDATAfilename)
                cmd = ("{executable} --input={input} --output={output} --isMC={isMC} "+
                    "--genPUMC={genPUMC} --puMC={puMCfilename} "+
                    "--puDATA={puDATAfilename}").format(executable=executable,
                    input=input_filelist, output=output, isMC=1,
                    genPUMC=0, 
                    puMCfilename=puMCfilename,
                    puDATAfilename=puDATAfilename) + cmdcutstr
            else:
                cmd = ("{executable} --input={input} --output={output} --isMC={isMC} "
                    ).format(executable=executable,
                    input=input_filelist, output=output, isMC=0) + cmdcutstr
            cmdlist.append(cmd)
            if batchSubmission:
                launchername = "launcher_%d.sh" % jobid
                if shouldCreateLaunchers:
                    launcher = open(os.path.join(dirToLaunchFrom, launchername), 
                        "w")
                    launcher.write("cd %s\n" % cmsswdir)
                    launcher.write("eval `scramv1 runtime -sh`\n")
                    launcher.write("source %s\n" % os.path.join(
                        os.environ["ANALYSISHOME"], "config", "env.sh"))
                    launcher.write("%s\n" % cmd)
                    launcher.close()
                    os.system("chmod 755 %s" % os.path.join(dirToLaunchFrom, launchername))
                joblist.append("bsub -q {queue} -o {logfile} -e {errorfile} {launcherscript}".format(queue=queue, logfile=os.path.join(dirToLaunchFrom, "log_%d.log" % (
            jobid)), errorfile=os.path.join(dirToLaunchFrom, "error_%d.log" % (
            jobid)), launcherscript=os.path.join(dirToLaunchFrom, "launcher_%d.sh" % jobid)))
            jobid+=1
    
    for cmd in cmdlist:
        print "-"*40
        print cmd
        print "-"*40

    if shouldCreateSubmitter:
        submittername = "submit.sh"
        sub = open(os.path.join(dirToLaunchFrom, submittername), "w")
    for cmd in joblist:
        print "-"*40
        print cmd
        print "-"*40
        if shouldCreateSubmitter:
            sub.write("%s\n" % cmd)
    if shouldCreateSubmitter:
        os.system("chmod 755 %s" % os.path.join(dirToLaunchFrom, submittername))
        sub.close()

if __name__=="__main__":
    main()
