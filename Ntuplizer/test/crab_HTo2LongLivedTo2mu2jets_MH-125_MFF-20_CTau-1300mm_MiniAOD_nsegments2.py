import CRABClient
from CRABClient.UserUtilities import config, getLumiListInValidFiles
#from FWCore.DataStructs.LumiList import LumiList
from FWCore.PythonUtilities.LumiList import LumiList

config = config()

# General
config.General.workArea = '/eos/user/r/rlopezru/crab_projects'
config.General.requestName = 'HTo2LongLivedTo2mu2jets_MH-125_MFF-20_CTau-1300mm_MiniAOD-Ntuples_nsegments2'
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.instance = 'prod'

# JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'HTo2LL_runNtuplizer_cfg.py'
config.JobType.maxMemoryMB = 3000
config.JobType.allowUndistributedCMSSW = True
config.JobType.outputFiles = ['HTo2LongLivedTo2mu2jets.root']

# Data
config.Data.inputDataset = '/HTo2LongLivedTo2mu2jets_MH-125_MFF-20_CTau-1300mm_TuneCP5_13p6TeV_pythia8/rlopezru-HTo2LongLivedTo2mu2jets_MH-125_MFF-20_CTau-1300mm_MiniAOD_CMSSW_12_4_11_patch3_AOD-MiniAOD_nsegments2-42ad603b91d99d3cc77a3641b840e853/USER' 
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 50 # splitting to get ~500 output files
config.Data.outLFNDirBase = '/store/user/rlopezru/Samples/HTo2LongLivedTo2mu2jets_Ntuples/'
config.Data.publication = False
config.Data.outputDatasetTag = 'HTo2LongLivedTo2mu2jets_MH-125_MFF-20_CTau-1300mm_MiniAOD-Ntuples_nsegments2'

# Site
config.Site.storageSite = 'T3_CH_CERNBOX'
