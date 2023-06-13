import CRABClient
from CRABClient.UserUtilities import config, getLumiListInValidFiles
#from FWCore.DataStructs.LumiList import LumiList
from FWCore.PythonUtilities.LumiList import LumiList

config = config()

# General
config.General.workArea = '/afs/cern.ch/user/r/rlopezru/private/DisplacedCollection_FW/CMSSW_13_2_0_pre1/src/DisplacedMuons-FrameWork/Ntuplizer/test/Cosmics_2022_ReReco'
config.General.requestName = 'CosmicsAnalysis_Run2022C_10Dec22_MiniAOD-Ntuples_CMSSW_13_2_0_pre1'
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
config.Data.inputDataset = '/NoBPTX/rlopezru-Cosmics_2022C_10Dec2022_CMSSW_13_2_0_pre1_MiniAOD_x-cf97a87bb8142e73806e929ae8e4f01b/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/user/rlopezru/Samples/'
config.Data.publication = False
config.Data.outputDatasetTag = 'CosmicsAnalysis_Run2022C_10Dec2022_MiniAOD-Ntuples_CMSSW_13_2_0_pre1'

# Site
config.Site.storageSite = 'T3_CH_CERNBOX'
