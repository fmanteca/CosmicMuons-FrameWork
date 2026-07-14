import CRABClient
from CRABClient.UserUtilities import config, getLumiListInValidFiles
from FWCore.PythonUtilities.LumiList import LumiList

config = config()

# General
config.General.workArea = 'crab_projects'
config.General.requestName = 'CosmicsData_2025v2-Ntuples'
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.instance = 'prod'

# JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'Cosmics_runNtuplizer_AOD_cfg.py'
config.JobType.maxMemoryMB = 3000
config.JobType.allowUndistributedCMSSW = True
config.JobType.outputFiles = ['ntuples.root']

# Data
config.Data.inputDataset = '/Cosmics/Commissioning2025-PromptReco-v2/AOD'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/group/phys_muon/fernanpe/Cosmics2025/'
config.Data.publication = False
config.Data.outputDatasetTag = 'CosmicsData_2025v2_Ntuples'

# Site
config.Site.storageSite = 'T2_CH_CERN'
