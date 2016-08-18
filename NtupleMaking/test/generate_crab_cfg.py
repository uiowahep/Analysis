"""
Crab Config Generator.
- Retrieve the CMSSW Datasets that you need to be processed
- Create and Commit new Ntuples that will be generated with Crab
- Generate the crab cfg files to be submitted
"""
import os,sys, shelve

#   input options
commitUpdates = False

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

#   select the datasets to be submitted for grid processing
datasets = []
for k in data_datasets:
    if data_datasets[k].year==2016:
        datasets.append(data_datasets[k])
samples = []

#   create the Ntuple objects for all of the datasets
for d in datasets:
    globaltag = "80X_dataRun2_Prompt_v9"
    cmssw = "80X"
    storage = "EOS"
    rootpath = "/store/user/vkhriste/higgs_ntuples"
    if d.isData:
        rootpath+="/data"
    else:
        rootpath+="/mc"
    s = DS.Ntuple(d, 
        globaltag=globaltag,
        json = jsonfile.filename,
        cmssw = cmssw,
        storage = storage,
        rootpath=rootpath,
        timestamp=""
    )
    samples.append(s)

#   iterate/generate/commit and create config files
for s in samples:

    "Generating...."
    print "-"*80
    print s

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
        outfile = open('crab_auto_submit_'+s.label+'_'+jsontag+'.py', 'w')

    else:
        outfile = open('crab_auto_submit_'+s.label+'.py', 'w')
    
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

#   Commit all the Ntuples that you are going to generate
if commitUpdates:
    print "-"*80
    print "Commiting Updates"
    print "-"*80
    for s in samples:
        print s
        if s.isData:
            datantuples[s.label+"."+jsontag] = s
        else:
            mcntuples[s.label.split(".")[0]+".%s"%s.cmssw]
    datantuples = ds["DataNtuples"]
    mcntuples = ds["MCNtuples"]
    ds["DataNtuples"] = datantuples
    ds["MCNtuples"] = mcntuples
ds.close()
