import FWCore.ParameterSet.Config as cms
import os


process = cms.Process("demo")
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load('Configuration.StandardSequences.Services_cff')

# Debug printout and summary.
process.load("FWCore.MessageService.MessageLogger_cfi")

process.options = cms.untracked.PSet(
  wantSummary = cms.untracked.bool(True),
  # Set up multi-threaded run. Must be consistent with config.JobType.numCores in crab_cfg.py.
  #numberOfThreads=cms.untracked.uint32(8)
)

from Configuration.AlCa.GlobalTag import GlobalTag

# Select number of events to be processed
nEvents = 100
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(nEvents) )

# Read events
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( '/store/user/rlopezru/Samples/DDM_2022/HTo2LongLivedTo2mu2jets_MH-1000_MFF-350_CTau-3500mm_TuneCP5_13p6TeV_pythia8/HTo2LongLivedTo2mu2jets_MH-1000_MFF-350_CTau-3500mm_TuneCP5_13p6TeV_pythia8_CMSSW_13_2_0_MiniAOD/230620_095702/0000/step0_1.root' ),
    secondaryFileNames = cms.untracked.vstring(),
    skipEvents = cms.untracked.uint32(0)
  )

# Define global tag
gTag = '124X_mcRun3_2022_realistic_postEE_v1'
process.GlobalTag = GlobalTag(process.GlobalTag, gTag)

## Define the process to run 
## 
process.load("DisplacedMuons-FrameWork.Ntuplizer.HTo2LL_ntuples_MiniAOD_cfi")

process.p = cms.EndPath(process.ntuples)
