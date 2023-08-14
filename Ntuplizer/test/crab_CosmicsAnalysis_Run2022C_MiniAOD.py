import CRABClient
from CRABClient.UserUtilities import config, getLumiListInValidFiles
#from FWCore.DataStructs.LumiList import LumiList
from FWCore.PythonUtilities.LumiList import LumiList

config = config()

# General
config.General.workArea = 'crab_projects'
config.General.requestName = 'CosmicsAnalysis_Run2022C-10Dec2022-v1_MiniAOD-Ntuples'
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.instance = 'prod'

# JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'Cosmics_runNtuplizer_MiniAOD_cfg.py'
config.JobType.maxMemoryMB = 4000
config.JobType.allowUndistributedCMSSW = True
config.JobType.outputFiles = ['ntuples.root']

# Data
config.Data.inputDataset = '/NoBPTX/Run2022C-10Dec2022-v1/MINIAOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/user/rlopezru/Samples/'
config.Data.publication = False
config.Data.outputDatasetTag = 'CosmicsAnalysis_Run2022C-10Dec2022-v1_MiniAOD-Ntuples'

# Site
config.Site.storageSite = 'T3_CH_CERNBOX'
