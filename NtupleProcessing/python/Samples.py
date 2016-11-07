#!/usr/bin/python

import shelve, pickle
import Dataset as DS
import os,sys,subprocess
if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.environ["ANALYSISHOME"])

#
#   Specify the full list of CMSSW Datasets
#
datadatasets = {
    "/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "74X_dataRun2_v4"
    ),
    "/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "74X_dataRun2_reMiniAOD_v0"
    ),
    "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015D-PromptReco-v4/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "74X_dataRun2_Prompt_v4"
    ),
    "/SingleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "76X_dataRun2_v15"
    ),
    "/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD",
        isData=True,
        year=2015,
        globaltag = "76X_dataRun2_v15"
    ),

    #
    #   2016 Prompt
    #
#    "/SingleMuon/Run2016B-PromptReco-v1/MINIAOD" : DS.Dataset(
#        name="/SingleMuon/Run2016B-PromptReco-v1/MINIAOD",
#        isData=True,
#        year=2016,
#        globaltag = "80X_dataRun2_Prompt_v9"
#    ),
    "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016C-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016C-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016D-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016D-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016E-PromptReco-v2/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016E-PromptReco-v2/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016F-PromptReco-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016F-PromptReco-v1/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016G-PromptReco-v1/MINIAOD" : DS.Dataset(
        name="/SingleMuon/Run2016G-PromptReco-v1/MINIAOD",
        isData=True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016H-PromptReco-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016H-PromptReco-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016H-PromptReco-v2/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016H-PromptReco-v2/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),
    "/SingleMuon/Run2016H-PromptReco-v3/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016H-PromptReco-v3/MINIAOD",
        isData = True,
        year = 2016,
        globaltag = "80X_dataRun2_Prompt_v9"
    ),

    #
    #   2016 Re Reco
    #
    "/SingleMuon/Run2016B-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016B-23Sep2016-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v3"
    ),
    "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v3"
    ),
    "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v3"
    ),
    "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD" : DS.Dataset(
        name = "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD",
        isData = True,
        year=2016,
        globaltag = "80X_dataRun2_2016SeptRepro_v3"
    )
}

mcdatasets = {
        #
        #   Signal Datasets
        #
    "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" : DS.MCDataset(
        name="/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        isData=False,
        year=2015,
        isSignal=True,
        initial_cmssw = "74X",
        globaltag = "74X_mcRun2_asymptotic_v2",
        cross_section =  43.62*0.00022
    ),
    "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "76X",
        globaltag = "76X_mcRun2_asymptotic_v12",
        cross_section =  43.62*0.00022
    ),

    "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year=2016,
        isData=False,
        isSignal=True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 43.62*0.00022
    ),

    "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" : DS.MCDataset(
        name="/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "74X",
        globaltag = "74X_mcRun2_asymptotic_v2",
        cross_section = 3.727*0.00022
    ),
    "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=True,
        initial_cmssw = "76X",
        globaltag = "76X_mcRun2_asymptotic_v12",
        cross_section = 3.727*0.00022
    ),

    "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM" : DS.MCDataset(
        name = "/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM",
        year = 2016,
        isData=False,
        isSignal=True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 3.727*0.00022
    ),

    "/WMinusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WMinusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year=2016,
        isData=False,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 0.1
    ),

    "/WPlusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/WPlusH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year = 2016,
        isData=False,
        isSignal = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 0.1
    ),

    "/ZH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/ZH_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal  = True,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 0.1
    ),

    #
    #   Background Datasets
    #
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" : DS.MCDataset(
        name="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        year=2015,isData=False,
        isSignal=False,
        initial_cmssw = "74X",
        globaltag = "74X_mcRun2_asymptotic_v2",
        cross_section = 6025.2
    ),
    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=False,
        initial_cmssw = "76X",
        globaltag = "76X_mcRun2_asymptotic_v12",
        cross_section = 6025.2
    ),

    "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year = 2016,
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 6025.2
    ),

    "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM" : DS.MCDataset(
        name="/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=False,
        initial_cmssw="74X",
        globaltag = "74X_mcRun2_asymptotic_v2",
        cross_section = 831.76
    ),
    "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM" : DS.MCDataset(
        name="/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        year=2015,
        isData=False,
        isSignal=False,
        initial_cmssw="76X",
        globaltag = "76X_mcRun2_asymptotic_v12",
        cross_section = 831.76
    ),

    "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" : DS.MCDataset(
        name = "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        year = 2016, 
        isData = False,
        isSignal = False,
        initial_cmssw = "80X",
        globaltag = "80X_mcRun2_asymptotic_v14",
        cross_section = 831.76
    )
}

#
#   jsons
#
jsonfiles = {
    #   ReReco of 2015
    "2015_ReReco" : DS.JsonFile(
        filename="Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt",
        intlumi = 2318.
    ),

    #   Prompt of 2015
    "2015_Prompt" : DS.JsonFile(
        filename="Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt",
        intlumi = 2169.
    ),

    #   Prompt of 2016 up to the point where MC/Data Mismatch was not present
    "2016_Prompt_7648" : DS.JsonFile(
        filename="Cert_271036-276097_13TeV_PromptReco_Collisions16_JSON_NoL1T_v2.txt",
        intlumi = 7648.
    ),

    #   Prompt of 2016 - MC/Data Mismatch is present - Trigger inefficiency!???
    "2016_Prompt_12900" : DS.JsonFile(
        filename="Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt",
        intlumi = 12900.
    ),

    #   latest
    "2016_Prompt_16900" : DS.JsonFile(
        filename="Cert_271036-277148_13TeV_PromptReco_Collisions16_JSON.txt",
        intlumi = 16900.
    ),
    "2016_Prompt_20100" : DS.JsonFile(
        filename = "Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt",
        intlumi = 20100.
    ),
    "2016_Prompt_26400" : DS.JsonFile(
        filename = "Cert_271036-280385_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt",
        intlumi = 26400.
    ),
    "2016_Prompt_29530" : DS.JsonFile(
        filename = "Cert_271036-282037_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt",
        intlumi = 29530.
    ),
    "2016_Prompt_36150" : DS.JsonFile(
        filename = "Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt",
        intlumi = 36150.
    )
}

#
#   list all the pileup files
#
pileups = {}
for k in jsonfiles.keys():
    jfilename = jsonfiles[k].filename
    for cs in ["68", "69", "69p2", "70", "71", "72", "71p3"]:
        s = "pileup__%s__%s" % (jfilename[:-4], cs)
        pileups[s] = DS.PileUp(
            cross_section=cs, datajson=jfilename
        )

#
#   Useful functions to build up the name
#
def buildDatasetTagName(ntuple):
    if ntuple.isData:
	s = "%s__%s" % (ntuple.label.split("__")[1],ntuple.json[:-4])
    else:
        s = "%s" % (ntuple.cmssw)
    if ntuple.aux!=None and ntuple.aux!="":
        s+="__%s" % ntuple.aux
    return s

def buildRequestName(ntuple, *kargs):
    if ntuple.isData:
        s = ntuple.label.split("__")[1]
        s += "__%s"%kargs[0]
    else:
        s = ntuple.label.split("__")[0].split("-")[0]+"__%s" % ntuple.initial_cmssw
    if ntuple.aux!=None and ntuple.aux!="":
        s+="__%s" % ntuple.aux
    return s

def isReReco(dataset):
	if dataset.year==2015:
		if "16Dec2015" in dataset.name:
			return True
		else:
			return False
	else:
		return False

def buildPUfilename(ntuple):
    if ntuple.isData:
        sdata = "pileup__%s__%smb.root" % (ntuple.pileupdata.datajson[:-4],
            ntuple.pileupdata.cross_section)
        return sdata
    else:
        smc = "pileup__%s__%s.root" % (ntuple.label.split("__")[0],
            ntuple.cmssw)
        return smc

def buildPUfilenames(result):
    sdata = "pileup__%s__%smb.root" % (result.pileupdata.datajson[:-4],
        result.pileupdata.cross_section)
    smc = "pileup__%s__%s.root" % (result.label.split("__")[0],
        result.cmssw)
    return (smc, sdata)

def eos_system(cmd, args):
    import subprocess
    proc = subprocess.Popen([cmd, args], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out

def buildTimeStamp(ntuple):
    fullpattern = os.path.join(ntuple.rootpath,
        ntuple.label.split("__")[0],
        buildDatasetTagName(ntuple), "*")
    print fullpattern
    cmd = "ls" if ntuple.storage=="local" else "eos"
    print cmd
    if ntuple.storage=="local":
        args = fullpattern
    else:
        args = "ls %s" % os.path.join("/eos/cms", fullpattern)
    print "%s %s" % (cmd, args)
    x = eos_system(cmd, args).split("\n")[0]
    print x
    return x

def discoverFileList(ntuple):
    fullpath= os.path.join(ntuple.rootpath,
        ntuple.label.split("__")[0],
        buildDatasetTagName(ntuple), buildTimeStamp(ntuple), "0000")
    fullpattern = os.path.join(fullpath, "*.root")
    cmd = "ls" if ntuple.storage=="local" else "eos"
    args = "-d %s" % fullpattern if ntuple.storage=="local" else "ls %s" % (
        os.path.join("/eos/cms", fullpattern))
    x = eos_system(cmd, args).split("\n")[:-1]
    if ntuple.storage=="EOS":
        xxx = []
        for f in x:
            fullpathname = os.path.join("root://eoscms.cern.ch//", "eos/cms")
            fullpathname = fullpathname+os.path.join(fullpath, f)
            xxx.append(fullpathname)
        return xxx
    return x

def buildFileListName(ntuple):
    if ntuple.isData:
        s = "filelist__%s__%s" % (ntuple.label.split("__")[1],
                ntuple.json[:-4])
    else:
        s = "filelist__%s__%s" % (ntuple.label.split("__")[0],
            ntuple.cmssw)
    if ntuple.aux!=None and ntuple.aux!="":
        s += "__%s" % ntuple.aux
    s+=".files"
    return s

def buildResultOutputPathName(result):
    s = "result"
    if result.isData:
        s+="__%s__%s" % (result.label.split("__")[1],
            result.json[:-4])
    else:
        s += "__%s__%s__%s__%smb" % (result.label.split("__")[0],
            result.cmssw, result.pileupdata.datajson[:-4], 
            result.pileupdata.cross_section)
    if result.aux!=None and result.aux!="":
        s += "__%s" % result.aux
    s += ".root"
    return s

def discoverNtuples(ntuple):
    prefix = ""
    if ntuple.storage=="EOS":
        prefix+="/eos/cms"
        tstamp = getTimeStamp(ntuple)
        ntuple.timestamp = tstamp
        pathstring = os.path.join(prefix, ntuple.rootpath, ntuple.name.split("/")[0],
            buildDatasetTagName(ntuple), tstamp, "0000")
        x = eos_system("eos", "ls %s/*.root" % pathstring).split("\n")
        return pathstring,x
    else:
        pathstring = os.path.join(prefix, ntuple.rootpath, ntuple.name.split("/")[0],
            buildDatasetTagName(ntuple))
        x = eos_system("eos", "ls %s/*.root" % pathstring).split("\n")
        return pathstring,x

def getFileList(ntuple):
    pass

if __name__=="__main__":
    pass
