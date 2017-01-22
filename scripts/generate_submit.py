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

    #   set the variables
    bindir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/bin/build-8"
    executable = os.path.join(bindir, "process_HiggsAnalysis_Run1Categorization")
    batchSubmission = True
    storage = "EOS"
    cmsswdir = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis/CMSSW_8_0_25/src/Analysis"
    dirToUse = "/afs/cern.ch/work/v/vkhriste/Projects/HiggsAnalysis"
    analysisHome = os.environ["ANALYSISHOME"]
    filelistdir = os.path.join(dirToUse, "filelists")
    resultsdir = os.path.join(dirToUse, "results")
    pileupdir = os.path.join(dirToUse, "pileup_moriond2017")
    mcera = "mcMoriond2017"
    import datetime
    version = "vR1_"+datetime.datetime.now().strftime("%Y%m%d_%H%M")
    dirToLaunchFrom = os.path.join(bindir, "submission"+"__"+version)
    if not os.path.exists(dirToLaunchFrom):
        os.system("mkdir %s" % dirToLaunchFrom)

    resultsdir+= "/"+version
    queue = '8nh'
    rootpath = "/store/user/vkhriste/higgs_ntuples"
    aux = "Mu24"
    shouldCreateFileList = True
    shouldCreateLaunchers = True
    shouldCreateSubmitter = True
    if not os.path.exists(resultsdir):
        os.system("mkdir %s" % resultsdir)

    #
    # specify which datasets to skip - not to process
    #
    #datasetsToSkip = ["/SingleMuon/Run2016H-PromptReco-v1/MINIAOD"]
    datasetsToSkip = ["/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM"]

    #
    # select the json to use
    #
    print "-"*80
    print (" "*40)+"SET UP Ntuples"+(" "*40)
    print "-"*80
    data_datasets = S.rerecoSep232016_datasets
    mc_datasets = S.mcMoriond2017datasets
    jsonfiles = S.jsonfiles
    jsontag = "2016_ReReco_36460"
    jsonfile = jsonfiles[jsontag]
    data_ntuples = []
    mc_ntuples = []
    cmssw = "80X"

    #
    # generate the description of what is being done
    #
    descFile = open(os.path.join(dirToLaunchFrom, "description.desc"), "w")
    desc = """
    Submitting Run 1 like Categorization/Analysis.
    1) For 36fb^-1 for json file {jsonfile} ReReco
    2) {mcera} is the mcera being used
    3) {executable} is the executable used
    4) No systematics - just analysis and categorization
    5) Ouput version is {version}
    """.format(jsonfile=jsonfile, mcera=mcera, executable=executable, version=version)
    descFile.write(desc)
    descFile.close()

    #
    # select the ntuples to be processed
    #
    for k in data_datasets:
        #if data_datasets[k].year!=2016 or "PromptReco" not in data_datasets[k].name: continue
        shouldGenerate = True
        for ddd in datasetsToSkip:
            if ddd==data_datasets[k].name: 
                shouldGenerate=False
                break
        if not shouldGenerate: continue
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
        #if mc_datasets[k].initial_cmssw!="80X": continue
        ntuple = DS.Ntuple(mc_datasets[k],
            json = None,
            cmssw = mc_datasets[k].initial_cmssw,
            storage=storage,
            rootpath = os.path.join(rootpath, mcera),
            timestamp=None,
            aux=aux
        )
        mc_ntuples.append(ntuple)
    print data_ntuples
    print mc_ntuples
    ntuples = []
    ntuples.extend(data_ntuples)
#    ntuples.extend(mc_ntuples)

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
                if "Cert_271036-284044_13TeV_23Sep2016ReReco" not in ipu: continue
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
        print result
        output = S.buildResultOutputPathName(result)
        output = os.path.join(resultsdir, output)
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
                puDATAfilename=puDATAfilename)
        else:
            cmd = ("{executable} --input={input} --output={output} --isMC={isMC} "
                ).format(executable=executable,
                input=input_filelist, output=output, isMC=0)
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
