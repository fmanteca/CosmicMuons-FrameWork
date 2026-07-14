from CRABClient.UserUtilities import config
config = config()

config.section_("General")
config.General.transferLogs = True
config.General.requestName = 'Commissioning2025_RECO' 
config.General.workArea = 'crab_projects'


config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'CosmicPPreco_RAW2DIGI_RECO.py'
config.JobType.numCores = 2
config.JobType.maxMemoryMB = 5000
config.JobType.outputFiles = ['CosmicPPreco_RAW2DIGI_RECO.root']

config.section_("Data")
config.Data.splitting       = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputDatasetTag = 'Commissioning2025_RECO'
config.Data.outLFNDirBase = '/store/group/phys_muon/fernanpe/Cosmics2025/'
config.Data.publication = True
config.Data.inputDataset = '/Cosmics/Commissioning2025-v1/RAW'

config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'

