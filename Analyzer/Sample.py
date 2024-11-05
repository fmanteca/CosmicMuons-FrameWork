import os
import ROOT as r

class Sample:

    def __init__(self, name, location, isData=False, isMC=False, isSignal=False):
        self.name = name
        self.location = location
        self.isData = isData
        self.isMC = isMC
        self.isSignal = isSignal

    def getTChain(self, treeName):
        if type(treeName) != str:
            print("Error: tree name must be string.")
            return 0
        tChain = r.TChain(treeName)
        for _f in os.listdir(self.location):
            if not '.root' in _f: continue
            tChain.Add(f"{self.location}/{_f}")
        self.tChain = tChain
        return self.tChain
