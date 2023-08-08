import CRABClient
from CRABClient.UserUtilities import config, getLumiListInValidFiles
#from FWCore.DataStructs.LumiList import LumiList
from FWCore.PythonUtilities.LumiList import LumiList

config = config()

# General
config.General.workArea = '/afs/cern.ch/user/r/rlopezru/private/DisplacedCollection_FW/CMSSW_13_2_0_pre1/src/DisplacedMuons-FrameWork/MiniAOD_prod/Run3DDM/crab_projects/'
config.General.requestName = ##REQUESTNAME##
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.instance = 'prod'

# JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = ##PSETNAME##
config.JobType.maxMemoryMB = 3000
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores = 2

# Data
config.Data.inputDataset = ##INPUTDATASET##
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1 # splitting to get ~500 output files
config.Data.outLFNDirBase = '/store/user/rlopezru/Samples/DDM_2022/' # modify accordingly
config.Data.publication = True
config.Data.outputDatasetTag = ##OUTPUTDATASET##

# Site
config.Site.storageSite = 'T2_ES_IFCA'
