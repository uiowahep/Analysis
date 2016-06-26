from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 's.name'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'cfgname'
config.JobType.allowUndistributedCMSSW=True
#config.JobType.outputFiles = ['outputfile.root']

config.Data.inputDataset = 's.dir'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.lumiMask = 's.jsonfiles[1]'
config.Data.unitsPerJob = 100
config.Data.outLFNDirBase = '/store/user/vkhriste/ntuples'
config.Data.publication = False
config.Data.outputDatasetTag = 's.name'

config.Site.storageSite = 'T2_CH_CERN'
