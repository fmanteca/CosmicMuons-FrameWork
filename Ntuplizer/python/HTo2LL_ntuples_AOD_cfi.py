import FWCore.ParameterSet.Config as cms

ntuples = cms.EDAnalyzer('ntuplizer',
    nameOfOutput = cms.string('HTo2LongLivedTo2mu2jets_Ntuples_CMSSW_12_4_11_patch3_nseg2_5.root'),
    isData                        = cms.bool(True),
    EventInfo                     = cms.InputTag("generator"),
    RunInfo                       = cms.InputTag("generator"),
    BeamSpot                      = cms.InputTag("offlineBeamSpot"),
    displacedGlobalCollection     = cms.InputTag("displacedGlobalMuons"),
    displacedStandAloneCollection = cms.InputTag("displacedStandAloneMuons"),
    displacedMuonCollection       = cms.InputTag("displacedMuons"),
    genParticleCollection         = cms.InputTag("prunedGenParticles"),
    PrimaryVertexCollection       = cms.InputTag("offlinePrimaryVertices"),

    #prescales  = cms.InputTag("patTrigger"),
    bits       = cms.InputTag("TriggerResults","","HLT"),
    #objects    = cms.InputTag("slimmedPatTrigger")
)
