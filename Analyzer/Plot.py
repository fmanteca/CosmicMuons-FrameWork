import ROOT as r
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()

class Plot:

    def __init__(self, name):
        self.name = name

    def addHist(self, h1):

    def addHist(self, hTotal, hPassed):
        hEff = r.TEfficiency(hPassed, hTotal)
        vEffHists.append(hEff)

    def makeEfficiencyPlot(self):
        c = r.TCanvas(self.name, self.name)



    def makeVarPlot(self):
