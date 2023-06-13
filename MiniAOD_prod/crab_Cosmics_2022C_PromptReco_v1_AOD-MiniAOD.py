import CRABClient
from CRABClient.UserUtilities import config, getLumiListInValidFiles
#from FWCore.DataStructs.LumiList import LumiList
from FWCore.PythonUtilities.LumiList import LumiList

config = config()

# General
config.General.workArea = '/afs/cern.ch/user/r/rlopezru/private/DisplacedCollection_FW/CMSSW_13_2_0_pre1/src/DisplacedMuons-FrameWork/MiniAOD_prod/crab_projects/'
config.General.requestName = 'Cosmics_2022C_PromptReco_CMSSW_13_2_0_pre1_MiniAOD_2'
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.instance = 'prod'

# JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'Cosmics_PromptReco_C_PAT.py'
config.JobType.maxMemoryMB = 3000
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores = 2

# Data
config.Data.inputDataset = '/NoBPTX/Run2022C-PromptReco-v1/AOD'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1 # splitting to get ~500 output files
config.Data.outLFNDirBase = '/store/user/rlopezru/Samples/' # modify accordingly
config.Data.publication = True
config.Data.outputDatasetTag = 'Cosmics_2022C_PromptReco_CMSSW_13_2_0_pre1_MiniAOD'

# Site
config.Site.storageSite = 'T2_ES_IFCA'
