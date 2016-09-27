"""
Crab Config Generator.
- Retrieve the CMSSW Datasets that you need to be processed
- Create and Commit new Ntuples that will be generated with Crab
- Generate the crab cfg files to be submitted
"""
import os,sys, shelve, pickle

#   import the Analysis dependency
if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.environ["ANALYSISHOME"])

#   we must include the directory in which the module resides to make it work!
sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "NtupleProcessing/python"))

#   import whatever you need
import NtupleProcessing.python.Samples as Samples
import NtupleProcessing.python.Dataset as DS

#   get the datasets to be processed
data_datasets = Samples.datadatasets
mc_datasets = Samples.mcdatasets

#   get the json file to be used if needed
jsonfiles = Samples.jsonfiles
jsontag = "2016_Prompt_20100"
jsonfile = jsonfiles[jsontag]

#   select the datasets to be submitted for grid processing
datasets = []
sets_to_consider=mc_datasets
for k in sets_to_consider:
#    if sets_to_consider[k].year==2016:
    if sets_to_consider[k].initial_cmssw=="76X":
        datasets.append(sets_to_consider[k])
samples = []

#   create the Ntuple objects for all of the datasets
hlttype = "HLT"
for d in datasets:
    #globaltag = "76X_dataRun2_v15"
    cmssw = d.initial_cmssw
    storage = "EOS"
    rootpath = "/store/user/vkhriste/higgs_ntuples"
    if d.isData:
        rootpath+="/data"
    else:
        rootpath+="/mc"
    s = DS.Ntuple(d, 
#        json = jsonfile.filename,
        json = None,
        cmssw = cmssw,
        storage = storage,
        rootpath=rootpath,
        timestamp=None,
        aux="Mu22"
    )
    samples.append(s)

#   iterate/generate/commit and create config files
print "Generating Config Files..."
for s in samples:

    "Generating...."
    print "-"*80
    print s

    #   create a config filename
    cfgname = 'dimu_'
    cfgname += s.label.replace(".", "_")
    if s.isData:cfgname += str(jsontag)
    cfgname += '_for_crab.py'
    outfile = open(cfgname, 'w')
    
    #   open the cmssw config template to update
    file = open('templates/maker_h2dimuon_cfg_crabtemplate.py', 'r')
    for line in file:
        if 's.isData' in line: 
            line = line.replace('s.isData', str(s.isData))
        if 's.globaltag' in line: 
            line = line.replace('s.globaltag', '\"' + s.globaltag + '\"')
        if 'HLTTYPE' in line:
            line = line.replace('HLTTYPE', hlttype)
        outfile.write(line)
    
    # close the generated cmssw config file
    outfile.close()
    #   close the cmssw config template
    file.close()
    
    #   open the crab cfg template
    file = open('templates/crab_template.py', 'r')
    if s.isData: 
        #   and open the crab cfg to be generated
        outfile = open('crab_auto_submit_'+s.label.replace(".", "_")+
			'_'+jsontag+'.py', 'w')

    else:
        outfile = open('crab_auto_submit_'+s.label.replace(".", "_")+'.py', 'w')
    
    # read in the template and replace the parameters to make a
    # crab submission file that uses the above cmssw script
    for line in file:
        if 'psetName' in line: 
            line = line.replace('cfgname', cfgname)
        if s.isData and 'FileBased' in line: 
            line = line.replace('FileBased', 'LumiBased')
        if s.isData and 'config.Data.lumiMask' in line: 
            line = line.replace('#', '')
            line = line.replace('JSONFILE', "json/"+s.json)
        if "REQUESTNAME" in line:
                line = line.replace("REQUESTNAME", Samples.buildRequestName(s, jsontag))
        if 'DATASETTAGNAME' in line: 
            datasettag = Samples.buildDatasetTagName(s)
            line = line.replace('DATASETTAGNAME', datasettag)
        if 's.name' in line: 
            line = line.replace('s.name', s.name)
        if 'ROOTPATH' in line:
            line = line.replace("ROOTPATH", s.rootpath)
        if "JOBUNITS" in line:
            if s.isData:
                line = line.replace("JOBUNITS", "100")
            else:
                line = line.replace("JOBUNITS", "40")
        outfile.write(line)
    
    outfile.close()
    file.close()
