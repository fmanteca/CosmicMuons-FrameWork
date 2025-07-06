import FWCore.ParameterSet.Config as cms

muonNtupleProducer = cms.EDAnalyzer("MuonNtupleProducer",
    muons = cms.InputTag("muons"),
    cosmicMuons = cms.InputTag("cosmicMuons")
)
