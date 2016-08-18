"""
Crab Config Generator.
- Retrieve the CMSSW Datasets that you need to be processed
- Create and Commit new Ntuples that will be generated with Crab
- Generate the crab cfg files to be submitted
"""
import os,sys, shelve

#   import the Analysis dependency
if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.environ["ANALYSISHOME"])
import NtupleProcessing.Samples as Samples
import NtupleProcessing.Dataset as DS

#   get the datasets to be processed
filename=Samples.filename
ds = shelve.open(filename)
data_datasets = ds["DataDatasets"]
mc_datasets = ds["MCDatasets"]
datantuples = ds["DataNtuples"]
mcntuples = ds["MCNtuples"]

#   get the json file to be used if needed
jsonfiles = ds["jsonfiles"]
jsontag = "2016_Prompt_16900"
jsonfile = jsonfiles[jsontag]

#   Final list of samples to be crab-submitted
datasets = []
for k in data_datasets:
    if data_datasets[k].year==2016:
        datasets.append(data_datasets[k])
samples = []
for ds in datasets:
    globaltag = "80X_dataRun2_Prompt_v9"
    cmssw = "80X"
    storage = "EOS"
    rootpath = "/store/user/vkhriste/higgs_ntuples"
    if ds.isData:
        rootpath+="/data"
    else:
        rootpath+="/mc"
    s = Samples.Ntuple(ds, 
        globaltag=globaltag,
        json = jsonfile,
        cmssw = cmssw,
        storage = storage,
        rootpath=rootpath,
        timestamp=""
    )
    samples.append(s)

#   iterate/generate/commit and create config files
for s in samples:

    #   create a config filename
    cfgname = 'dimu_'
    cfgname += s.label
    if s.isData: cfgname += str(jsontag)
    cfgname += '_for_crab.py'
    outfile = open(cfgname, 'w')
    
    #   open the cmssw config template to update
    file = open('templates/maker_h2dimuon_cfg_crabtemplate.py', 'r')
    for line in file:
        if 's.isData' in line: 
            line = line.replace('s.isData', str(s.isData))
        if 's.name' in line: 
            line = line.replace('s.label', '\"' + s.label + '\"')
        if 's.globaltag' in line: 
            line = line.replace('s.globaltag', '\"' + s.globaltag + '\"')
        outfile.write(line)
    
    # close the generated cmssw config file
    outfile.close()
    #   close the cmssw config template
    file.close()
    
    #   open the crab cfg template
    file = open('templates/crab_template.py', 'r')
    if s.isData: 
        #   and open the crab cfg to be generated
        outfile = open('crab_auto_submit_'+s.name+'_'+jsontag+'.py', 'w')

    else:
        outfile = open('crab_auto_submit_'+s.name+'.py', 'w')
    
    # read in the template and replace the parameters to make a
    # crab submission file that uses the above cmssw script
    for line in file:
        if 'psetName' in line: 
            line = line.replace('cfgname', cfgname)
        if s.isData and 'FileBased' in line: 
            line = line.replace('FileBased', 'LumiBased')
        if s.isData and 'config.Data.lumiMask' in line: 
            line = line.replace('#', '')
            line = line.replace('JSONFILE', s.json)
        if "REQUESTNAME" in line:
            if s.isData:
                line = line.replace("REQUESTNAME", s.label.split(".")[1]+".%s" % jsontag)
            else:
                line = line.replace("REQUESTNAME", s.label.split(".")[i]+".%s" % s.initial_cmssw)
        if 'DATASETTAGNAME' in line: 
            datasettag = Samples.buildDatasetTagName(s)
            line = line.replace('DATASETTAGNAME', datasettag)
        if "PRIMARYDATASETNAME" in line:
            primaryname = Samples.buildPrimaryDatasetName(s)
            line = line.replace("PRIMARYDATASETNAME", primaryname)
        if 's.name' in line: 
            line = line.replace('s.name', s.name)
        if 'ROOTPATH' in line:
            line = line.replace("ROOTPATH", s.rootpath)
        if "JOBUNITS" in line:
            if s.isData:
                line = line.replace("JOBUNITS", "100")
            else:
                line = line.replace("JOBUNITS", "10")
        outfile.write(line)
    
    outfile.close()
    file.close()

for s in samples:
    if s.isData:
        datantuples[s.label+"."+jsontag] = s
    else:
        mcntuples[s.label.split(".")[0]+".%s"%s.cmssw]
datantuples = ds["DataNtuples"]
mcntuples = ds["MCNtuples"]
ds["DataNtuples"] = datantuples
ds["MCNtuples"] = mcntuples
