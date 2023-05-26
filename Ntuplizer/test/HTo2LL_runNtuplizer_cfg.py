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
nEvents = -1
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(nEvents) )

# Read events
#inputdir = '/eos/user/r/rlopezru/Samples/HTo2LongLivedTo2mu2jets_MiniAOD/HTo2LongLivedTo2mu2jets_MH-400_MFF-150_CTau-4000mm_TuneCP5_13p6TeV_pythia8/HTo2LongLivedTo2mu2jets_MH-400_MFF-150_CTau-4000mm_TuneCP5_13p6TeV_pythia8/HTo2LongLivedTo2mu2jets_MH-400_MFF-150_CTau-4000mm_MiniAOD_CMSSW_13_1_0_pre2_nsegments2_review/230508_074147/0000/'
#listOfFiles = ['file:'+inputdir+'HTo2LongLivedTo2mu2jets_MiniAOD_CMSSW_12_4_11_patch3_nsegments2_'+str(i+1)+'.root' for i in range(8)]
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( 'file:HTo2LongLivedTo2mu2jets_MiniAOD_CMSSW_12_4_11_patch3_nsegments2_5.root' ),
    secondaryFileNames = cms.untracked.vstring(),
    skipEvents = cms.untracked.uint32(0)
  )
process.GlobalTag = GlobalTag(process.GlobalTag, '124X_mcRun3_2022_realistic_v12')

## Define the process to run 
## 
process.load("Analysis.DisplacedMuons-Ntuplizer.HTo2LL_ntuples_cfi")

process.p = cms.EndPath(process.ntuples)
