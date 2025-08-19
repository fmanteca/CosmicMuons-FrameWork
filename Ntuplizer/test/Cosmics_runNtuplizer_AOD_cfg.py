import FWCore.ParameterSet.Config as cms

process = cms.Process("MuonNtuple")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("TrackingTools.Configuration.TrackingTools_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.GlobalTrackingGeometryESProducer = cms.ESProducer("GlobalTrackingGeometryESProducer")

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, "auto:run3_data_prompt", "")

# Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'file:f86d1c77-9a31-4930-83e0-043884f9df1c.root'
        #'file:6ddf0cc8-31e6-4714-b3de-f521348e9b7f.root'
        'file:14cbfe49-ca4a-4d65-aa56-d349ba6415a0.root', #RAW-RECO
    )
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)  
)

#output
process.TFileService = cms.Service("TFileService", fileName=cms.string("file:ntuples.root"))

# Analyzer
process.load("CosmicMuons-FrameWork.Ntuplizer.muonNtupleProducer_cfi")


process.muonNtupleProducer.ServiceParameters = cms.PSet(
    Propagators=cms.untracked.vstring(
        "SteppingHelixPropagatorAny",
        "SteppingHelixPropagatorAlong",
        "SteppingHelixPropagatorOpposite",
    ),
    RPCLayers=cms.bool(True),
)

process.p = cms.Path(process.muonNtupleProducer)
