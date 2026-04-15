import FWCore.ParameterSet.Config as cms

muonNtupleProducer = cms.EDAnalyzer("MuonNtupleProducer",
    muons = cms.InputTag("muons1Leg"),
    # segmentsDt = cms.InputTag('dt4DSegments'),
    # segmentsCSC = cms.InputTag('cscSegments'),
)
