#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/MuonDetId/interface/MuonSubdetId.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "RecoMuon/TrackingTools/interface/MuonServiceProxy.h"
#include "Geometry/CommonDetUnit/interface/GeomDetType.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/CSCGeometry/interface/CSCGeometry.h"
#include "Geometry/DTGeometry/interface/DTGeometry.h"
#include "Geometry/RPCGeometry/interface/RPCGeometry.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/CommonDetUnit/interface/GeomDetEnumerators.h"
#include "Geometry/CommonDetUnit/interface/GlobalTrackingGeometry.h"
#include "RecoMuon/DetLayers/interface/MuonDetLayerGeometry.h"
#include "RecoMuon/TransientTrackingRecHit/interface/MuonTransientTrackingRecHitBuilder.h"
#include "RecoMuon/TransientTrackingRecHit/interface/MuonTransientTrackingRecHit.h"
#include "RecoMuon/Records/interface/MuonRecoGeometryRecord.h"
#include "RecoMuon/GlobalTrackingTools/interface/StateSegmentMatcher.h"
#include "TTree.h"

class MuonServiceProxy;

class MuonNtupleProducer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit MuonNtupleProducer(const edm::ParameterSet&);
  ~MuonNtupleProducer() override = default;

private:
  void beginJob() override;
  void endJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  edm::EDGetTokenT<std::vector<reco::Muon>> muonsToken_;
  edm::EDGetTokenT<std::vector<reco::Track>> cosmicMuonsToken_;
  edm::EDGetTokenT<DTRecSegment4DCollection> dtSegmentsToken_;
  edm::EDGetTokenT<CSCSegmentCollection> cscSegmentsToken_;
  edm::EDGetTokenT<edm::TriggerResults> hltResultsToken_;
  edm::ESGetToken<MagneticField, IdealMagneticFieldRecord> magneticFieldToken_;
  edm::ParameterSet parameters;
  MuonServiceProxy *theService;
  // output definition
  TTree* tree_;
  TFile *file_;
  std::string output_filename;
  
  static const int MAX = 1000;

  // Event-level info
  unsigned int run_, lumi_, event_;
  int magnetOn_;

  // Reco muon variables
  int nMuons_;
  float muonPt_[MAX], muonEta_[MAX], muonPhi_[MAX];
  int muonCharge_[MAX];
  int muonValidMuonHits_[MAX], muonValidGlobalHits_[MAX], muonValidStandaloneHits_[MAX], muonMatchedStations_[MAX];
  int muonIsGlobal_[MAX], muonIsTracker_[MAX], muonIsStandalone_[MAX], muonIsPF_[MAX], muonIsRPC_[MAX];
  float muonDxy_[MAX], muonDz_[MAX];
  int muonSegmentsDT_[MAX], muonSegmentsCSC_[MAX], muonSegmentsRPC_[MAX];
  
  // Cosmic track variables
  int nCosmics_;
  float cosmicPt_[MAX], cosmicEta_[MAX], cosmicPhi_[MAX];
  int cosmicCharge_[MAX], cosmicValidHits_[MAX];

  // Segments
  int   nSeg_;
  int Seg_isDT_[MAX], Seg_isCSC_[MAX], Seg_DTstation_[MAX], Seg_CSCstation_[MAX], Seg_ndof_[MAX];
  float Seg_x_[MAX], Seg_y_[MAX], Seg_z_[MAX];
  float Seg_dirx_[MAX], Seg_diry_[MAX], Seg_dirz_[MAX];
  float Seg_chi2_[MAX];

};

MuonNtupleProducer::MuonNtupleProducer(const edm::ParameterSet& iConfig) {
  usesResource("TFileService");
  muonsToken_ = consumes<std::vector<reco::Muon>>(iConfig.getParameter<edm::InputTag>("muons"));
  cosmicMuonsToken_ = consumes<std::vector<reco::Track>>(iConfig.getParameter<edm::InputTag>("cosmicMuons"));
  dtSegmentsToken_ = consumes<DTRecSegment4DCollection>(iConfig.getParameter<edm::InputTag>("segmentsDt"));
  cscSegmentsToken_ = consumes<CSCSegmentCollection>(iConfig.getParameter<edm::InputTag>("segmentsCSC"));
  magneticFieldToken_ = esConsumes<MagneticField, IdealMagneticFieldRecord>();
  parameters = iConfig;
  edm::ParameterSet serviceParameters = iConfig.getParameter<edm::ParameterSet>("ServiceParameters");
  theService = new MuonServiceProxy(serviceParameters,consumesCollector(),MuonServiceProxy::UseEventSetupIn::Event );
}

void MuonNtupleProducer::beginJob() {
  
  // Output file definition
  output_filename = "ntuples.root";
  file_ = new TFile(output_filename.c_str(), "RECREATE");
  tree_ = new TTree("Events", "Flat muon ntuple");
  file_->cd();

  tree_->Branch("run", &run_, "run/i");
  tree_->Branch("lumi", &lumi_, "lumi/i");
  tree_->Branch("event", &event_, "event/i");
  tree_->Branch("magnetOn", &magnetOn_, "magnetOn/I");

  tree_->Branch("nMuons", &nMuons_, "nMuons/I");
  tree_->Branch("muonPt", muonPt_, "muonPt[nMuons]/F");
  tree_->Branch("muonEta", muonEta_, "muonEta[nMuons]/F");
  tree_->Branch("muonPhi", muonPhi_, "muonPhi[nMuons]/F");
  tree_->Branch("muonCharge", muonCharge_, "muonCharge[nMuons]/I");
  tree_->Branch("muonValidGlobalHits", muonValidGlobalHits_, "muonValidGlobalHits[nMuons]/I");
  tree_->Branch("muonValidStandaloneHits", muonValidStandaloneHits_, "muonValidStandaloneHits[nMuons]/I");
  tree_->Branch("muonMatchedStations", muonMatchedStations_, "muonMatchedStations[nMuons]/I");
  tree_->Branch("muonIsGlobal", muonIsGlobal_, "muonIsGlobal[nMuons]/I");
  tree_->Branch("muonIsTracker", muonIsTracker_, "muonIsTracker[nMuons]/I");
  tree_->Branch("muonIsStandalone", muonIsStandalone_, "muonIsStandalone[nMuons]/I");
  tree_->Branch("muonIsPF", muonIsPF_, "muonIsPF[nMuons]/I");
  tree_->Branch("muonIsRPC", muonIsRPC_, "muonIsRPC[nMuons]/I");
  tree_->Branch("muonDxy", muonDxy_, "muonDxy[nMuons]/F");
  tree_->Branch("muonDz", muonDz_, "muonDz[nMuons]/F");
  tree_->Branch("muonSegmentsDT", muonSegmentsDT_, "muonSegmentsDT[nMuons]/I");
  tree_->Branch("muonSegmentsCSC", muonSegmentsCSC_, "muonSegmentsCSC[nMuons]/I");
  tree_->Branch("muonSegmentsRPC", muonSegmentsRPC_, "muonSegmentsRPC[nMuons]/I");

  tree_->Branch("nCosmics", &nCosmics_, "nCosmics/I");
  tree_->Branch("cosmicPt", cosmicPt_, "cosmicPt[nCosmics]/F");
  tree_->Branch("cosmicEta", cosmicEta_, "cosmicEta[nCosmics]/F");
  tree_->Branch("cosmicPhi", cosmicPhi_, "cosmicPhi[nCosmics]/F");
  tree_->Branch("cosmicCharge", cosmicCharge_, "cosmicCharge[nCosmics]/I");
  tree_->Branch("cosmicValidHits", cosmicValidHits_, "cosmicValidHits[nCosmics]/I");

  tree_->Branch("nSeg", &nSeg_, "nSeg/I");
  tree_->Branch("Seg_isDT", Seg_isDT_, "Seg_isDT[nSeg]/I");
  tree_->Branch("Seg_DTstation", Seg_DTstation_, "Seg_DTstation[nSeg]/I");
  tree_->Branch("Seg_isCSC", Seg_isCSC_, "Seg_isCSC[nSeg]/I");
  tree_->Branch("Seg_CSCstation", Seg_CSCstation_, "Seg_CSCstation[nSeg]/I");
  tree_->Branch("Seg_ndof", Seg_ndof_, "Seg_ndof[nSeg]/I");
  tree_->Branch("Seg_x", Seg_x_, "Seg_x[nSeg]/F");
  tree_->Branch("Seg_y", Seg_y_, "Seg_y[nSeg]/F");
  tree_->Branch("Seg_z", Seg_z_, "Seg_z[nSeg]/F");
  tree_->Branch("Seg_dirx", Seg_dirx_, "Seg_dirx[nSeg]/F");
  tree_->Branch("Seg_diry", Seg_diry_, "Seg_diry[nSeg]/F");
  tree_->Branch("Seg_dirz", Seg_dirz_, "Seg_dirz[nSeg]/F");
  tree_->Branch("Seg_chi2", Seg_chi2_, "Seg_chi2[nSeg]/F");
}

void MuonNtupleProducer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  run_ = iEvent.id().run();
  lumi_ = iEvent.luminosityBlock();
  event_ = iEvent.id().event();
  theService->update(iSetup);
  magnetOn_ = 0; //by default assume magnet off
  
  try {
    const MagneticField& magneticField = iSetup.getData(magneticFieldToken_);
    float bField = magneticField.nominalValue();
    magnetOn_ = (bField > 0.1) ? 1 : 0;
  } catch (cms::Exception& e) {
    edm::LogWarning("MuonNtupleProducer") << "IdealMagneticFieldRecord not available, assuming magnetOff.";
  }
  
  nMuons_ = 0;
  nCosmics_ = 0;
  nSeg_ = 0;

  edm::Handle<std::vector<reco::Muon>> muons;
  iEvent.getByToken(muonsToken_, muons);
  edm::Handle<DTRecSegment4DCollection> dtSegments;
  iEvent.getByToken(dtSegmentsToken_, dtSegments);
  edm::Handle<CSCSegmentCollection> cscSegments;
  iEvent.getByToken(cscSegmentsToken_, cscSegments);
  
  for (const auto& mu : *muons) {
    if (nMuons_ >= MAX) break;
    muonPt_[nMuons_] = mu.pt();
    muonEta_[nMuons_] = mu.eta();
    muonPhi_[nMuons_] = mu.phi();
    muonCharge_[nMuons_] = mu.charge();
    muonValidGlobalHits_[nMuons_] = mu.globalTrack().isNonnull() ? mu.globalTrack()->hitPattern().numberOfValidMuonHits() : -1;
    muonValidStandaloneHits_[nMuons_] = mu.outerTrack().isNonnull() ? mu.outerTrack()->numberOfValidHits() : -1;
    muonMatchedStations_[nMuons_] = mu.numberOfMatchedStations();
    muonIsGlobal_[nMuons_] = mu.isGlobalMuon();
    muonIsTracker_[nMuons_] = mu.isTrackerMuon();
    muonIsStandalone_[nMuons_] = mu.isStandAloneMuon();
    muonIsPF_[nMuons_] = mu.isPFMuon();
    muonIsRPC_[nMuons_] = mu.isRPCMuon();
    muonDxy_[nMuons_] = mu.innerTrack().isNonnull() ? mu.innerTrack()->dxy() : -999.0;
    muonDz_[nMuons_] = mu.innerTrack().isNonnull() ? mu.innerTrack()->dz() : -999.0;

    muonSegmentsDT_[nMuons_] = 0;
    muonSegmentsCSC_[nMuons_] = 0;
    muonSegmentsRPC_[nMuons_] = 0;
    for (const auto& match : mu.matches()) {
      if (match.detector() == MuonSubdetId::DT) ++muonSegmentsDT_[nMuons_];
      else if (match.detector() == MuonSubdetId::CSC) ++muonSegmentsCSC_[nMuons_];
      else if (match.detector() == MuonSubdetId::RPC) ++muonSegmentsRPC_[nMuons_];
    }
    ++nMuons_;
  }

  edm::Handle<std::vector<reco::Track>> cosmics;
  iEvent.getByToken(cosmicMuonsToken_, cosmics);
  for (const auto& trk : *cosmics) {
    if (nCosmics_ >= MAX) break;
    cosmicPt_[nCosmics_] = trk.pt();
    cosmicEta_[nCosmics_] = trk.eta();
    cosmicPhi_[nCosmics_] = trk.phi();
    cosmicCharge_[nCosmics_] = trk.charge();
    cosmicValidHits_[nCosmics_] = trk.numberOfValidHits();
    ++nCosmics_;
  }


  std::map<const GeomDet*, std::vector<TrackingRecHit *> > DetAllSegmentsMap;
  std::map<const GeomDet*, std::vector<TrackingRecHit *> >::iterator it;
  // Loop over DT segments
  for (auto itSeg = dtSegments->begin(); itSeg != dtSegments->end(); itSeg++) {
    //Only valid segments & hasZ & hasPhi
    if(!itSeg->isValid() || !itSeg->hasPhi()) continue;
    DetId myDet = itSeg->geographicalId();
    const GeomDet *geomDet = theService->trackingGeometry()->idToDet(myDet);
    if(geomDet->geographicalId().subdetId()  == MuonSubdetId::DT){
      DTWireId id(geomDet->geographicalId().rawId());
      if(id.station() != 4 && !itSeg->hasZed()){continue;}
      if(id.station() != 4 && itSeg->dimension()!=4){continue;}
    }
    //Get the GeomDet associated to this DetId
    it = DetAllSegmentsMap.find(geomDet);
    if(it == DetAllSegmentsMap.end()) {
      //No -> we create a pair of GeomDet and vector of hits, and put the hit in the vector.
      std::vector<TrackingRecHit *> trhit;
      TrackingRecHit *rechitref = (TrackingRecHit *)&(*itSeg);
      trhit.push_back(rechitref);
      DetAllSegmentsMap.insert(std::pair<const GeomDet*, std::vector<TrackingRecHit *> > (geomDet, trhit));
    } else {
      //Yes -> we just put the hit in the corresponding hit vector.
      TrackingRecHit *rechitref = (TrackingRecHit *) &(*itSeg);
      it->second.push_back(rechitref);
    }
  }

  // Loop over CSC segments
  for (auto itSeg = cscSegments->begin(); itSeg != cscSegments->end(); itSeg++) {
    //Only valid segments     
    if(!itSeg->isValid()) continue;
    DetId myDet = itSeg->geographicalId();
    const GeomDet *geomDet = theService->trackingGeometry()->idToDet(myDet);
    //Get the GeomDet associated to this DetId
    it = DetAllSegmentsMap.find(geomDet);
    if(it == DetAllSegmentsMap.end()) {
      //No -> we create a pair of GeomDet and vector of hits, and put the hit in the vector.
      std::vector<TrackingRecHit *> trhit;
      TrackingRecHit *rechitref = (TrackingRecHit *)&(*itSeg);
      trhit.push_back(rechitref);
      DetAllSegmentsMap.insert(std::pair<const GeomDet*, std::vector<TrackingRecHit *> > (geomDet, trhit));
    } else {
      //Yes -> we just put the hit in the corresponding hit vector.
      TrackingRecHit *rechitref = (TrackingRecHit *) &(*itSeg);
      it->second.push_back(rechitref);
    }
  }


  for (auto it = DetAllSegmentsMap.begin(); it != DetAllSegmentsMap.end(); ++it) {
    const GeomDet* geom = it->first;
    const auto& segVec  = it->second;
    for (size_t i = 0; i < segVec.size(); ++i) {
      const auto* seg = segVec[i];
      LocalPoint  seg_lp  = seg->localPosition();
      GlobalPoint seg_gp  = geom->surface().toGlobal(seg_lp);
      if((*it).second.at(i)->geographicalId().subdetId() == MuonSubdetId::DT){
	DTWireId id((*it).second.at(i)->geographicalId().rawId());
	Seg_isDT_[nSeg_] =1;
	Seg_isCSC_[nSeg_] =0;
	Seg_DTstation_[nSeg_] =id.station();
	Seg_CSCstation_[nSeg_] =-9999;
	DTRecSegment4D *mySegment = dynamic_cast<DTRecSegment4D *>((*it).second.at(i));
	GlobalVector gv = it->first->surface().toGlobal(mySegment->localDirection());
	Seg_dirx_[nSeg_] =gv.x();
	Seg_diry_[nSeg_] =gv.y();
	Seg_dirz_[nSeg_] =gv.z();
	Seg_chi2_[nSeg_] =mySegment->chi2();
	Seg_ndof_[nSeg_] =mySegment->degreesOfFreedom();
      }else if((*it).second.at(i)->geographicalId().subdetId() == MuonSubdetId::CSC){
	CSCDetId id((*it).second.at(i)->geographicalId().rawId());
	Seg_isDT_[nSeg_] =0;
	Seg_isCSC_[nSeg_] =1;
	Seg_DTstation_[nSeg_] =-9999;
	Seg_CSCstation_[nSeg_] =id.station();
	CSCSegment *mySegment = dynamic_cast<CSCSegment *>((*it).second.at(i));
	GlobalVector gv = it->first->surface().toGlobal(mySegment->localDirection());
	Seg_dirx_[nSeg_] =gv.x();
	Seg_diry_[nSeg_] =gv.y();
	Seg_dirz_[nSeg_] =gv.z();
	Seg_chi2_[nSeg_] =mySegment->chi2();
	Seg_ndof_[nSeg_] =mySegment->degreesOfFreedom();
      }
      Seg_x_[nSeg_] =seg_gp.x(); 
      Seg_y_[nSeg_] =seg_gp.y(); 
      Seg_z_[nSeg_] =seg_gp.z();
      ++nSeg_;
    }
  }
  tree_->Fill();
}

void MuonNtupleProducer::endJob() 
{
    file_->cd();
    tree_->Write();
    file_->Close();

}
DEFINE_FWK_MODULE(MuonNtupleProducer);
