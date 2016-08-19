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
    pileupdir = ""
    version = "v0"
    commitUpdates = False
    resultsdir+= "/"+version
    if not os.path.exists(resultsdir):
        os.system("mkdir %s" % resultsdir)

    #   do the Framework imports
    if "ANALYSISHOME" not in os.environ.keys():
        raise NameError("Can not find ANALYSISHOME env var")
    sys.path.append(os.environ["ANALYSISHOME"])
    import config.datasets_configuration as dcfg
    sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "NtupleProcessing/python"))
    import NtupleProcessing.python.Samples as S
    import NtupleProcessing.python.Dataset as DS

    #   initialize the ntuples
    filename = S.filename
    f = open(filename, "r")
    ds = pickle.load(f); f.close()
    datantuples = ds["DataNtuples"]
    mcntuples = ds["MCNtuples"]
    pileups = ds["pileups"]

    #   select the ntuples to process
    results = []
    sets = mcntuples
    for k in sets:
        #   if we are running locally, but ntuple is at CERN skip it
        if sets[k].storage=="EOS" and not atCern:
            continue
        pathstring,x = S.discoverNtuples(sets[k])
        if sets[k].isData:
            filelistname = os.path.join(filelistdir, "filelist.%s.%s.files" %
                sets[k].label.split(".")[1], sets[k].json)
            results.append(DS.DataResult(sets[k], filelist=filelistname))
        else:
            filelistname = os.path.join(filelistdir, "filelist.%s.%s.files" %
                sets[k].label.split(".")[0], sets[k].cmssw)
            for pkey in pileups.keys():
                results.append(DS.MCResult(sets[k],
                    cross_section=pileups[pkey].cross_section,
                    pileupdatajson=pileups[pkey].datajson,
                    filelist=filelistname))
        f = open(filelistname, "w")
        for xx in x:
            name =""
            if sets[k].storage=="EOS":
                name = os.path.join("root://eoscms.cern.ch/",
                    pathstring, xx)
            else:
                name = os.path.join(pathstring, xx)
            f.write("%s\n" % name)

    #   construct the processing schema  
    print "-"*80
    print (" "*40)+"START"+(" "*40)
    print "-"*80
    joblist = []
    for result in results:
        input_filelist = filelistdir+"/";
        print result
        if result.isData:
            output = resultsdir + "/" + "result.%s.%s.root" % (
                result.label.split(".")[1], result.json[:-4])
        else:
            output = resultsdir+ "/" + "result.%s.%s.%s.%smb.root" % (
                result.label.split(".")[0], result.cmssw,
                result.pileupdatajson[:-4], result.cross_section)
        if not result.isData:
            puMCfilename = pileupdir+"/"+"pileup_%s_%s.root" % (
                result.label.split(".")[0], result.cmssw)
            puDATAfilename = pileupdir+"/"+"pileup_%s_%smb.root" % (
                result.pileupdatajson[:-4], result.cross_section)

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
