import FWCore.ParameterSet.Config as cms

process = cms.Process("MuonNtuple")

# Load standard sequences
process.load("FWCore.MessageService.MessageLogger_cfi")

# Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:b82466a3-ec0f-473e-98c6-e9ba273d0a92.root'
    )
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)  
)

#output
process.TFileService = cms.Service("TFileService", fileName=cms.string("ntuples.root"))

# Analyzer
process.load("CosmicMuons-FrameWork.Ntuplizer.muonNtupleProducer_cfi")  
process.p = cms.Path(process.muonNtupleProducer)
