#!/usr/bin/python

import os, sys, time, pickle, datetime, optparse

def main():
    print "-"*80
    print (" "*40)+"SET UP"+(" "*40)
    print "-"*80

    #   set some system vars
    batchSubmission = False
    atCern = False
    executable = "./process_Higgs"
    shouldGenPUMC = 1
    filelistdir = "."
    resultsdir = "."
    pileupdir = "."
    version = "v0"
    resultsdir+= "/"+version
    rootpath = "/store/user/vkhriste/higgs_ntuples"
    aux = "Mu22"
    shouldCreateFileList = False
    if not os.path.exists(resultsdir):
        os.system("mkdir %s" % resultsdir)

    #   do the Framework imports
    if "ANALYSISHOME" not in os.environ.keys():
        raise NameError("Can not find ANALYSISHOME env var")
    sys.path.append(os.environ["ANALYSISHOME"])
    sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "NtupleProcessing/python"))
    import NtupleProcessing.python.Samples as S
    import NtupleProcessing.python.Dataset as DS

    #
    #   generate all the Ntuple objects that are ready to be processed
    #
    data_datasets = S.datadatasets
    mc_datasets = S.mcdatasets
    jsonfiles = S.jsonfiles
    jsontag = "2016_Prompt_20100"
    jsonfile = jsonfiles[jsontag]
    data_ntuples = []
    mc_ntuples = []
    cmssw = "80X"
    storage = "EOS"
    for k in data_datasets:
        if data_datasets[k].year!=2016: continue
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
        ntuple = DS.Ntuple(mc_datasets[k],
            json = None,
            cmssw = mc_datasets[k].initial_cmssw,
            storage=storage,
            rootpath = os.path.join(rootpath, "mc"),
            timestamp=None,
            aux=aux
        )
    ntuples = []
    ntuples.extend(data_ntuples).extend(mc_ntuples)

    #
    #   Generate all the Results objects that are to be produced
    #   
    results = []
    for ntuple in ntuples:
        filelist_as_list = SdiscoverFileList(ntuple)
        filelist = os.path.join(filelistdir,S.buildFileListName(ntuple))
        if shouldCreateFileList:
            f = open(file, "w")
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
    for result in results:
        input_filelist = filelistdir+"/";
        print resulti
        output = S.buildResultOutputPathName(result)
        output = os.path.join(resultsdir, output)
        if not result.isData:
            (puMCfilename, puDATAfilename) = S.buildPUfilenames(result)
            puMCfilename = os.path.join(pileupdir, puMCfilename)
            puDATAfilename = os.path.join(pileupdir, puDATAfilename)

        if batchSubmission:
            pass
        else:
            cmd = ("{executable} --input={input} --output={output} --isMC={isMC} "+
                "--genPUMC={genPUMC} --puMCfilename={puMCfilename} "+
                "--puDATAfilename={puDATAfilename}").format(executable=executable,
                input=input_filelist, output=output, isMC=0 if result.isData else 1,
                genPUMC=0 if result.isData else shouldGenPUMC, 
                puMCfilename="" if result.isData else puMCfilename,
                puDATAfilename="" if result.isData else puDATAfilename)
            joblist.append(cmd)
    for cmd in joblist:
        print cmd

if __name__=="__main__":
    main()
