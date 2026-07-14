import ROOT
import sys

if len(sys.argv) != 3:
   print(" USAGE : %s <input file> <output file >"%(sys.argv[0]))
   sys.exit(1)

inFileName = sys.argv[1]
outFileName = sys.argv[2]

inFile = ROOT.TFile.Open(inFileName, "READ")
tree = inFile.Get("muonNtupleProducer/Events")

outFile = open(outFileName, "w")
 
for entryNum in range(0,tree.GetEntries()):
   tree.GetEntry(entryNum)
   
   nMuons = getattr(tree, "nMuons") #number of reco muons
   nGenMuons = getattr(tree, "nGenMuons") #number of gen muons

   # ---- get 4-vectors ---- #

   pt  = getattr(tree, "muonPt")
   eta = getattr(tree, "muonEta")
   phi = getattr(tree, "muonPhi")
   
   ptGen  = getattr(tree, "genMuonPt")
   etaGen = getattr(tree, "genMuonEta")
   phiGen = getattr(tree, "genMuonPhi")
   
   muonMass = 0.106 #Gev

   #loop over reconstructed muons
   vecMuons = []
   for i in range(nMuons):
       muon = ROOT.TLorentzVector() 
       muon.SetPtEtaPhiM(pt[i], eta[i], phi[i], muonMass)
       vecMuons.append(muon)

   #loop over generated muons
   vecGenMuons = []
   for i in range(nGenMuons): 
       genMuon = ROOT.TLorentzVector() 
       genMuon.SetPtEtaPhiM(ptGen[i], etaGen[i], phiGen[i], muonMass)
       vecGenMuons.append(genMuon)
    

   # ---- match muons ---- #
   matchedPairs = []
   matchedGenMuons = set()
   matchedRecoMuons = set()

   for genIdx, genMuon in enumerate(vecGenMuons):
       for muIdx, muon in enumerate(vecMuons):
          dR = genMuon.DeltaR(muon)
          if dR < 0.5:
             matchedPairs.append((genIdx, muIdx, dR))
             matchedGenMuons.add(genIdx)
             matchedRecoMuons.add(muIdx)
   
   #unmatched muons
   unmatchedGens = [genIdx for genIdx in range(len(vecGenMuons)) if genIdx not in matchedGenMuons]
   unmatchedRecos = [muIdx for muIdx in range(len(vecMuons)) if muIdx not in matchedRecoMuons]
   
   # ---- write in output file ---- #
   outFile.write(f"Event {entryNum}\n")
   outFile.write(f"  Matched pairs (gen, reco, dR): {matchedPairs}\n")
   outFile.write(f"  Unmatched gens: {unmatchedGens}\n")
   outFile.write(f"  Unmatched recos: {unmatchedRecos}\n")


outFile.close()
