from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'REQUESTNAME'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'cfgname'
config.JobType.allowUndistributedCMSSW=True
#config.JobType.outputFiles = ['outputfile.root']

config.Data.inputDataset = 's.name'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.lumiMask = 'JSONFILE'
config.Data.unitsPerJob = JOBUNITS 
config.Data.outLFNDirBase = 'ROOTPATH'
config.Data.publication = False
config.Data.outputDatasetTag = 'DATASETTAGNAME'
config.Data.outputPrimaryDataset = "PRIMARYDATASETNAME"

config.Site.storageSite = 'T2_CH_CERN'
