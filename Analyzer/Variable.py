import os
import ROOT as r
import numpy as np

class Variable:

    def __init__(self, string, latex, nbins, xmin=None, xmax=None, vbins=None, units=None, perMuon=False):
        self.string     = string      # expression evaluated by root
        self.latex      = latex       # latex name of variable
        self.units      = units       # measurement unit of the variable
        self.perMuon    = perMuon     # if the quantity is plotted per muon

        self.nbins      = nbins
        self.xmin       = xmin
        self.xmax       = xmax
        self.vbins      = vbins
    
    def setHistParams(nbins, vbins):
        self.nbins = nbins
        self.vbins = vbins

    def setHistParams(nbins, xmin, xmax):
        self.nbins = nbins
        self.xmin  = xmin
        self.xmax  = xmax

    def __eq__(self, other):
        if not isinstance(other,Variable): return False
        return self.__string__ == other.__string__

    def title(self):
        if self.units: return self.latex+f' [{self.units}]' 
        else: return self.latex

    def getStr(self, *args):
        return self.string.format(*args)

# Test area
'''
if __name__=='__main__':
    var = Variable('string_{0}', 'latex')
    print(var.getROOTexpr('dsa'))
'''
