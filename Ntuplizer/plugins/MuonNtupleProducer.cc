#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/MuonDetId/interface/MuonSubdetId.h"
#include "TTree.h"

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
  edm::EDGetTokenT<edm::TriggerResults> hltResultsToken_;

  // output definition
  TTree* tree_;
  TFile *file_;
  std::string output_filename;
  
  static const int MAX = 1000;

  // Event-level info
  unsigned int run_, lumi_, event_;

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
};

MuonNtupleProducer::MuonNtupleProducer(const edm::ParameterSet& iConfig) {
  usesResource("TFileService");
  muonsToken_ = consumes<std::vector<reco::Muon>>(iConfig.getParameter<edm::InputTag>("muons"));
  cosmicMuonsToken_ = consumes<std::vector<reco::Track>>(iConfig.getParameter<edm::InputTag>("cosmicMuons"));
}

void MuonNtupleProducer::beginJob() {
  
  // Output file definition
  output_filename = "ntuples.root";
  file_ = new TFile(output_filename.c_str(), "RECREATE");
  // edm::Service<TFileService> fs;
  // TDirectory* oldDir = gDirectory;
  // fs->file().cd();
  tree_ = new TTree("Events", "Flat muon ntuple");
  file_->cd();
  //oldDir->cd();

  tree_->Branch("run", &run_, "run/i");
  tree_->Branch("lumi", &lumi_, "lumi/i");
  tree_->Branch("event", &event_, "event/i");

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
}

void MuonNtupleProducer::analyze(const edm::Event& iEvent, const edm::EventSetup&) {
  run_ = iEvent.id().run();
  lumi_ = iEvent.luminosityBlock();
  event_ = iEvent.id().event();

  nMuons_ = 0;
  nCosmics_ = 0;

  edm::Handle<std::vector<reco::Muon>> muons;
  iEvent.getByToken(muonsToken_, muons);
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

  tree_->Fill();
}

void MuonNtupleProducer::endJob() 
{
    file_->cd();
    tree_->Write();
    file_->Close();

}
DEFINE_FWK_MODULE(MuonNtupleProducer);
