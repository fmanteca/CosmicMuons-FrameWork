import CRABClient
from CRABClient.UserUtilities import config, getLumiListInValidFiles
from FWCore.PythonUtilities.LumiList import LumiList

config = config()

# General
config.General.workArea = 'crab_projects'
config.General.requestName = 'CosmicsData_2025A_AOD-Ntuples'
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.instance = 'prod'

# JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'Cosmics_runNtuplizer_AOD_cfg.py'
config.JobType.maxMemoryMB = 4000
config.JobType.allowUndistributedCMSSW = True
config.JobType.outputFiles = ['ntuples.root']

# Data
config.Data.inputDataset = '/Cosmics/Run2025A-PromptReco-v1/AOD'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/user/fernanpe/Cosmics2025A/'
config.Data.publication = False
config.Data.outputDatasetTag = 'CosmicsData_2025A_Ntuples'

# Site
config.Site.storageSite = 'T3_CH_CERNBOX'
