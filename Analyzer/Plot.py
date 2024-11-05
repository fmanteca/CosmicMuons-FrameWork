import ROOT as r
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()

legendNames = {'dsa': 'reco::Track DSA', 'dmu_dsa': 'reco::Muon DSA',
               'dgl': 'reco::Track DGL', 'dmu_dgl': 'reco::Muon DGL'}

class Plot:

    def __init__(self, name, plotdir):
        self.name = name
        self.plotdir = plotdir
        # Init canvas
        self.canvas = r.TCanvas(self.name, self.name)
        self.canvas.cd()
        # Create lists for histos
        self.vEffHists = []
        self.vVarHists = []
        self.legend = None

        self.CMSlatex = r.TLatex()
        self.CMSlatex.SetNDC();
        self.CMSlatex.SetTextAngle(0);
        self.CMSlatex.SetTextColor(r.kBlack);
        self.CMSlatex.SetTextFont(42);
        self.CMSlatex.SetTextAlign(31);
        self.CMSlatex.SetTextSize(0.04);


    def initLegend(self, x0=.60, y0=.32, x1=.85, y1=.40):
        # Create legend
        self.legend = r.TLegend(x0,y0,x1,y1)
        self.legend.SetFillStyle(0)
        self.legend.SetTextFont(42)
        self.legend.SetTextSize(0.025)
        self.legend.SetBorderSize(0)


    def addHist(self, *args, **kwargs):
        if len(args)==1: self.addVarHist(args[0], **kwargs)
        if len(args)==2: self.addEffHist(args[0], args[1], **kwargs)


    def addVarHist(self, h1, **kwargs):
        '''
        List of kwargs:
          - color
          - legend
        '''
        n = len(self.vVarHists)
        _hVar = r.TH1F(h1)
        _hVar.SetName(f"h{n}")
        _hVar.SetLineWidth(2)
        _hVar.SetMarkerStyle(20)
        if 'color' in kwargs:
            _hVar.SetLineColor(kwargs['color'])
        self.vVarHists.append(_hVar)
        if 'legend' in kwargs and self.legend is not None: 
            self.legend.AddEntry(_hVar, kwargs['legend'], 'l')


    def addEffHist(self, hTotal, hPassed, **kwargs):
        '''
        List of kwargs:
          - color
          - legend
        '''
        n = len(self.vEffHists)
        hPassed.SetMaximum(1.2)
        hPassed.SetMinimum(0)
        hTotal.SetMaximum(1.2)
        hTotal.SetMinimum(0)
        _hEff = r.TEfficiency(hPassed, hTotal)
        _hEff.SetLineWidth(1)
        _hEff.SetMarkerStyle(20)
        if 'color' in kwargs:
            _hEff.SetMarkerColor(kwargs[color])
        self.vEffHists.append(_hEff)
        if 'legend' in kwargs and self.legend is not None: 
            self.legend.AddEntry(_hEff, kwargs['legend'], 'p')
    

    def makeVarPlot(self, **kwargs):
        '''
        List of kwargs:
          - ylog
        '''
        if not self.vVarHists:
            print("Error: no histograms added.")
            return

        self.canvas.cd()

        maxYValue = max([_h.GetMaximum() for _h in self.vVarHists])
        self.vVarHists[0].SetMinimum(1)
        self.vVarHists[0].SetMaximum(1.2*maxYValue)
        if 'ylog' in kwargs:
            self.canvas.GetPad(0).SetLogy(kwargs['ylog'])
            if kwargs['ylog']: self.vVarHists[0].SetMaximum(100*maxYValue)

        # Draw histograms
        for i,_h in enumerate(self.vVarHists):
            if i==0: _h.Draw("HIST")
            else:    _h.Draw("HIST,SAME")

        self.legend.Draw()
        self.CMSlatex.DrawLatex(0.34, 0.93, "#bf{CMS} #it{Internal}")


    def makeEfficiencyPlot(self):
        if not self.vEffHists:
            print("Error: no efficiency histograms added.")
            return

        self.canvas.cd()

        for i,_h in enumerate(self.vEffHists):
            if i==0: _h.Draw("PA")
            else:    _h.Draw("P,SAME")
        self.legend.Draw()
        self.CMSlatex.DrawLatex(0.34, 0.93, "#bf{CMS} #it{Internal}")


    def save(self, formats=['png','pdf','C']):
        for _format in formats:
            self.canvas.SaveAs(f'{self.plotdir}/{self.name}.{_format}')
