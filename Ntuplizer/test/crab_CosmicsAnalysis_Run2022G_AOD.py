import CRABClient
from CRABClient.UserUtilities import config, getLumiListInValidFiles
#from FWCore.DataStructs.LumiList import LumiList
from FWCore.PythonUtilities.LumiList import LumiList

config = config()

# General
config.General.workArea = '/eos/user/r/rlopezru/crab_projects'
config.General.requestName = 'CosmicsAnalysis_Run2022G_AOD-Ntuples'
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.instance = 'prod'

# JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'Cosmics_runNtuplizer_AOD_cfg.py'
config.JobType.maxMemoryMB = 4000
config.JobType.allowUndistributedCMSSW = True
config.JobType.outputFiles = ['Cosmics_AOD-Ntuples.root']

# Data
config.Data.inputDataset = '/NoBPTX/Run2022G-PromptReco-v1/AOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
#config.Data.unitsPerJob = 100 # splitting to get ~500 output files
config.Data.outLFNDirBase = '/store/user/rlopezru/Samples/' # modify accordingly
config.Data.publication = False
config.Data.outputDatasetTag = 'CosmicsAnalysis_Run2022G_AOD-Ntuples'

# Site
config.Site.storageSite = 'T2_ES_IFCA'
