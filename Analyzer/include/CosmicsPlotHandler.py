import math
import os
import ROOT as r
import numpy as np
from include.Debugger import Debugger
from include.utils import passIDSelection, angle
from include.DisplacedMuonFilter import DisplacedMuonFilter
from include.PlotHandler import PlotHandler
import include.cfg as cfg


# Config debugger
debug = Debugger(cfg.DEBUG)

class CosmicsPlotHandler(PlotHandler):

    def __init__(self, histfilename, cutsFilePath, sampleName):
   
        super().__init__(histfilename, cutsFilePath, sampleName)
        
        self.collections = ['dsa', 'dgl', 'dmu_dsa','dmu_dgl']

        ## MuonFilter object
        #self.mfilter = DisplacedMuonFilter(3.5, 3.5, 0)
        
        ## Define histograms
        self.h_nmuons = {}
        self.h_nmuons_down = {}
        self.h_nmuons_up = {}
        self.h_pt = {}
        self.h_pt_100 = {}
        self.h_eta = {}
        self.h_eta_down = {}
        self.h_eta_up = {}
        self.h_phi = {}
        self.h_dxy = {}
        self.h_dz = {}
        self.h_Nhits = {}
        self.h_NDThits = {}
        self.h_NCSChits = {}
        self.h_normalizedChi2 = {}
        self.h_numberOfMatches = {} 
        self.h_charge_pt = {}
        self.h_cosalpha = {}
        self.h_dPhi = {}
        self.h_dEta = {}
        self.h_eff_pt = {}
        self.h_eff_eta = {}
        self.h_eff_dxy = {}
        self.h_eff_dxy_cutdz = {}
        self.h_eff_dz = {}
        self.h_eff_dz_cutdxy = {}
        self.h_eff_2D = {}
        self.h_dxy_dz_2D = {}
        # -- Hists for probe muons
        self.h_pt_probe = {}
        self.h_pt_100_probe = {}
        self.h_eta_probe = {}
        self.h_phi_probe = {}
        self.h_dxy_probe = {}
        self.h_dz_probe = {}
        self.h_normalizedChi2_probe = {}
        self.h_Nhits_probe = {}
        self.h_NDThits_probe = {}
        self.h_NCSChits_probe = {}


        for collection in self.collections:
            self.h_nmuons[collection]          = r.TH1F("h_muons_{0}".format(collection),r";N_{#mu};N events",6,0,6) 
            self.h_nmuons_down[collection]     = r.TH1F("h_muons_down_{0}".format(collection),r";N_{#mu}(#phi<0);N events",6,0,6) 
            self.h_nmuons_up[collection]       = r.TH1F("h_muons_up_{0}".format(collection),r";N_{#mu}(#phi>0);N events",6,0,6) 
            self.h_pt[collection]              = r.TH1F("h_pt_{0}".format(collection),r";tag p_{T} (GeV);N events",100,0,200)
            self.h_pt_100[collection]          = r.TH1F("h_pt_100_{0}".format(collection),r";tag p_{T} (GeV);N events",100,0,100)
            self.h_eta[collection]             = r.TH1F("h_eta_{0}".format(collection),r";tag #eta;N events",100,-0.9,0.9)
            self.h_eta_down[collection]        = r.TH1F("h_eta_down_{0}".format(collection),r";#eta;N events",100,-0.9,0.9)
            self.h_eta_up[collection]          = r.TH1F("h_eta_up_{0}".format(collection),r";#eta;N events",100,-0.9,0.9)
            self.h_phi[collection]             = r.TH1F("h_phi_{0}".format(collection),r";tag #phi;N events",100,-3.2,3.2)
            self.h_dxy[collection]             = r.TH1F("h_dxy_{0}".format(collection),r";tag |d_{xy}| (cm);N events",100,0,800)
            self.h_dz[collection]              = r.TH1F("h_dz_{0}".format(collection),r";tag |d_{z}| (cm);N events",100,0,800)
            self.h_Nhits[collection]           = r.TH1F("h_Nhits_{0}".format(collection),r";tag nValidMuonHits;N events",100,0,50)
            self.h_NDThits[collection]         = r.TH1F("h_NDThits_{0}".format(collection),r";tag nValidMuonDTHits;N events",100,0,50)
            self.h_NCSChits[collection]        = r.TH1F("h_NCSChits_{0}".format(collection),r";tag nValidMuonCSCHits;N events",100,0,50)
            self.h_normalizedChi2[collection]  = r.TH1F("h_normalizedChi2_{0}".format(collection),r";tag #chi^{2}/ndof;N events",100,0,5)
            self.h_charge_pt[collection]       = r.TH1F("h_charge_pt_{0}".format(collection),r";Q/p_{T};N events",100,-0.1,0.1)
            self.h_cosalpha[collection]        = r.TH1F("h_cosalpha_{0}".format(collection),r";cos(#alpha);N events",100,-1,1)
            self.h_dPhi[collection]            = r.TH1F("h_dPhi_{0}".format(collection),r";|#Delta#phi|;N events",100,0,3.2)
            self.h_dEta[collection]            = r.TH1F("h_dEta_{0}".format(collection),r";#Delta#eta;N events",100,-2.4,2.4)
            self.h_eff_pt[collection]          = r.TEfficiency("h_eff_pt_{0}".format(collection), "Efficiency cosmic muons;tag p_{T} (GeV);Efficiency",    50,0,90)
            self.h_eff_eta[collection]         = r.TEfficiency("h_eff_eta_{0}".format(collection),"Efficiency cosmic muons;tag #eta;Efficiency",30,-1.2,1.2)
            self.h_eff_dxy[collection]         = r.TEfficiency("h_eff_dxy_{0}".format(collection),"Efficiency cosmic muons;tag |d_{0}| (cm);Efficiency", 50, 0, 200)
                                                               #np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70.]))
            self.h_eff_dxy_cutdz[collection]   = r.TEfficiency("h_eff_dxy_cutdz_{0}".format(collection),"Efficiency cosmic muons;tag |d_{0}| (cm);Efficiency", 50, 0, 200) 
                                                               #np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70.]))
            self.h_eff_dz[collection]          = r.TEfficiency("h_eff_dz_{0}".format(collection), "Efficiency cosmic muons;tag |d_{z}| (cm);Efficiency", 6, 
                                                               np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_eff_dz_cutdxy[collection]   = r.TEfficiency("h_eff_dz_cutdxy_{0}".format(collection),"Efficiency cosmic muons;tag |d_{z}| (cm);Efficiency", 6, 
                                                               np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_eff_2D[collection]          = r.TEfficiency("h_eff_2D_{0}".format(collection), "Efficiency cosmic muons;tag |d_{0}| (cm);tag |d_{z}| (cm);Efficiency",6,
                                                               np.array([0., 2., 5., 10., 30., 50., 70.]), 6,np.array([0., 8., 20., 40., 60., 90., 140.]))
            self.h_dxy_dz_2D[collection]       = r.TH2F("h_dxy_dz_2D_{0}".format(collection), "Displacement cosmic muons;|d_{0}| (cm);|d_{z}| (cm);N events",100,0,500,100,0,700)
            self.h_pt_probe[collection]              = r.TH1F("h_pt_probe{0}".format(collection),r";probe p_{T} (GeV);N events",100,0,200)
            self.h_pt_100_probe[collection]          = r.TH1F("h_pt_100_probe_{0}".format(collection),r";probe p_{T} (GeV);N events",100,0,100)
            self.h_eta_probe[collection]             = r.TH1F("h_eta_probe_{0}".format(collection),r";probe #eta;N events",100,-0.9,0.9)
            self.h_phi_probe[collection]             = r.TH1F("h_phi_probe_{0}".format(collection),r";probe #phi;N events",100,-3.2,3.2)
            self.h_dxy_probe[collection]             = r.TH1F("h_dxy_probe_{0}".format(collection),r";probe |d_{xy}| (cm);N events",100,0,800)
            self.h_dz_probe[collection]              = r.TH1F("h_dz_probe_{0}".format(collection),r";probe |d_{z}| (cm);N events",100,0,800)
            self.h_normalizedChi2_probe[collection]  = r.TH1F("h_normalizedChi2_probe_{0}".format(collection),r";probe #chi^{2}/ndof;N events",100,0,5)
            self.h_Nhits_probe[collection]           = r.TH1F("h_Nhits_probe_{0}".format(collection),r";probe nValidMuonHits;N events",100,0,50)
            self.h_NDThits_probe[collection]         = r.TH1F("h_NDThits_probe_{0}".format(collection),r";probe nValidMuonDTHits;N events",100,0,50)         
            self.h_NCSChits_probe[collection]        = r.TH1F("h_NCSChits_probe_{0}".format(collection),r";probe nValidMuonCSCHits;N events",100,0,50)

        ### Parse config file
        self.readCuts()
        

    def readCuts(self):
        super().readCuts()


    def fillVariableHistograms(self, ev, n, collection, tag=True):
        if tag:
            self.h_pt[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
            self.h_pt_100[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
            self.h_eta[collection].Fill(eval('ev.{0}_eta[n]'.format(collection)))
            self.h_phi[collection].Fill(eval('ev.{0}_phi[n]'.format(collection)))
            self.h_dxy[collection].Fill(eval('abs(ev.{0}_dxy[n])'.format(collection)))
            self.h_dz[collection].Fill(eval('abs(ev.{0}_dz[n])'.format(collection)))
            self.h_normalizedChi2[collection].Fill(eval('ev.{0}_normalizedChi2[n]'.format(collection)))
            self.h_Nhits[collection].Fill(eval('ev.{0}_nValidMuonHits[n]'.format(collection)))
            self.h_NDThits[collection].Fill(eval('ev.{0}_nValidMuonDTHits[n]'.format(collection)))
            self.h_NCSChits[collection].Fill(eval('ev.{0}_nValidMuonCSCHits[n]'.format(collection)))
        if not tag:
            self.h_pt_probe[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
            self.h_pt_100_probe[collection].Fill(eval('ev.{0}_pt[n]'.format(collection)))
            self.h_eta_probe[collection].Fill(eval('ev.{0}_eta[n]'.format(collection)))
            self.h_phi_probe[collection].Fill(eval('ev.{0}_phi[n]'.format(collection)))
            self.h_dxy_probe[collection].Fill(eval('abs(ev.{0}_dxy[n])'.format(collection)))
            self.h_dz_probe[collection].Fill(eval('abs(ev.{0}_dz[n])'.format(collection)))
            self.h_normalizedChi2_probe[collection].Fill(eval('ev.{0}_normalizedChi2[n]'.format(collection)))
            self.h_Nhits_probe[collection].Fill(eval('ev.{0}_nValidMuonHits[n]'.format(collection)))
            self.h_NDThits_probe[collection].Fill(eval('ev.{0}_nValidMuonDTHits[n]'.format(collection)))
            self.h_NCSChits_probe[collection].Fill(eval('ev.{0}_nValidMuonCSCHits[n]'.format(collection)))
        self.h_charge_pt[collection].Fill(eval('ev.{0}_charge[n]/ev.{0}_pt[n]'.format(collection)))
        self.h_dxy_dz_2D[collection].Fill(eval('abs(ev.{0}_dxy[n])'.format(collection)), eval('abs(ev.{0}_dz[n])'.format(collection))) 


    def fillDimuonVariableHistograms(self, ev, n, i, cos_alpha, collection):
        self.h_cosalpha[collection].Fill(cos_alpha)
        self.h_dPhi[collection].Fill(eval('abs(ev.{0}_phi[n]-ev.{0}_phi[i])'.format(collection)))
        self.h_dEta[collection].Fill(eval('ev.{0}_eta[n]-ev.{0}_eta[i]'.format(collection)))
        self.h_eta_down[collection].Fill(eval('ev.{0}_eta[n]'.format(collection)))
        self.h_eta_up[collection].Fill(eval('ev.{0}_eta[i]'.format(collection)))


    def fillEfficiencyHistograms(self, ev, n, collection, hasProbe=False):
        self.h_eff_pt[collection].Fill(hasProbe, eval('ev.{0}_pt[n]'.format(collection)))
        self.h_eff_eta[collection].Fill(hasProbe, eval('ev.{0}_eta[n]'.format(collection)))
        self.h_eff_dxy[collection].Fill(hasProbe, eval('abs(ev.{0}_dxy[n])'.format(collection)))
        if eval('abs(ev.{0}_dz[n])'.format(collection)) < 8: self.h_eff_dxy_cutdz[collection].Fill(hasProbe, eval('abs(ev.{0}_dxy[n])'.format(collection)))
        self.h_eff_dz[collection].Fill(hasProbe, eval('abs(ev.{0}_dz[n])'.format(collection)))
        if eval('abs(ev.{0}_dxy[n])'.format(collection)) < 2: self.h_eff_dz_cutdxy[collection].Fill(hasProbe, eval('abs(ev.{0}_dz[n])'.format(collection)))
        self.h_eff_2D[collection].Fill(hasProbe, eval('abs(ev.{0}_dxy[n])'.format(collection)), eval('abs(ev.{0}_dz[n])'.format(collection)))

    '''
    Perform an OR of the triggers
    '''
    def evalTriggers(self, ev):
        for t in self.triggers:
            if eval(t): return True
        return False 

    '''
    Check if a muon passes the defined cuts
    '''
    def evalCuts(self, ev, n, collection):
        for c in self.cuts[collection]:
            if not eval(c): return False
        return True


    def processEvent(self, ev):
        ## Check if events pass the trigger
        if not self.evalTriggers(ev): return
        '''
        # -------------------------------------------------------------------------------
        ## First, process tracks
        for collection in self.collections[0:2]:
            N = eval(f'ev.n{collection}')
            if N < 1: continue

            ## Count number of muons in each hemisphere
            n_up, n_down = 0,0
            for n in range(N):
                if eval(f'ev.{collection}_phi[n]') < 0: n_down += 1
                else: n_up += 1

            ## Loop over muons in event
            for n in range(N):
                ## Apply cuts
                if not self.evalCuts(ev, n, collection): continue
                
                self.h_nmuons[collection].Fill(eval('ev.n{0}'.format(collection)))
                self.h_nmuons_down[collection].Fill(n_down)
                self.h_nmuons_up[collection].Fill(n_up)

                ### Tag and probe
                passID = self.tagNprobeTracks(collection, ev, n, list(range(ntotal)))
        # -------------------------------------------------------------------------------
        '''

        # -------------------------------------------------------------------------------
        ## Get the ids of DSA and DGL
        ids = self.count_muons(ev)
        for collection in self.collections:
            # Get total muons in event
            if 'dmu' in collection:
                N = ev.ndmu
            else:
                N = eval(f'ev.n{collection}')
            if N < 1: continue

            ## Loop over muons in event
            for n in ids[collection]:
                ### Apply cuts
                if not self.evalCuts(ev, n, collection): continue

                ### Tag and probe
                passID = self.tagNprobe(collection, ev, n, ids[collection])
        # -------------------------------------------------------------------------------


    def tagNprobe(self, collection, ev, n, ids):
        ## Check if muon passes ID selection
        passID = passIDSelection(ev, n, collection)
        cos_alpha_temp = None
        if passID:
            debug.print("ID passed by muon {0}".format(n), "INFO")
            hasProbe, cos_alpha_temp, i = self.findProbe(ev, n, collection, ids)
            # Fill variable histograms
            self.fillVariableHistograms(ev, n, collection, tag=True)
            # Fill efficiency histograms
            self.fillEfficiencyHistograms(ev, n, collection, hasProbe)
            if hasProbe: self.fillDimuonVariableHistograms(ev, n, i, cos_alpha_temp, collection)
        return passID

    
    def findProbe(self, ev, n, col, ids):
        existsProbe = False
        cos_alpha = None
        phi_tag = eval(f'ev.{col}_phi[n]')
        eta_tag = eval(f'ev.{col}_eta[n]')
        theta_tag = 2 * np.arctan(np.exp(-eta_tag)) - np.pi/2    
    
        if 'dsa' in col:
            temp_probe = -1 # initialize probe
            for i in ids:
                if i == n: continue
                if eval(f'ev.{col}_nValidMuonDTHits[i] + ev.{col}_nValidMuonCSCHits[i] <= 12'): continue
                if eval(f'ev.{col}_pt[i] <= 3.5'): continue
                phi_temp   = eval(f'ev.{col}_phi[i]')
                eta_temp   = eval(f'ev.{col}_eta[i]')
                theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
                v_tag      = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
                v_temp     = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
                cos_alpha_temp = angle(v_tag, v_temp)
                cos_alpha      = cos_alpha_temp
                if cos_alpha < np.cos(2.1) :
                    if not existsProbe: 
                        existsProbe = True
                        temp_probe = i
                    elif existsProbe and eval(f'ev.{col}_pt[i]') > eval(f'ev.{col}_pt[temp_probe]'): 
                        temp_probe = i
    
        if 'dgl' in col:
            temp_probe = -1 # initialize probe
            for i in ids:
                if i == n: continue
                if eval(f'ev.{col}_pt[i] <= 20'): continue
                phi_temp = eval(f'ev.{col}_phi[i]')
                eta_temp = eval(f'ev.{col}_eta[i]')
                theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
                v_tag      = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
                v_temp     = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
                cos_alpha_temp = angle(v_tag, v_temp)
                cos_alpha      = cos_alpha_temp
                if cos_alpha < np.cos(2.8):
                    if not existsProbe: 
                        existsProbe = True
                        temp_probe = i
                    elif existsProbe and eval(f'ev.{col}_pt[i]') > eval(f'ev.{col}_pt[temp_probe]'): 
                        temp_probe = i
     
        if existsProbe: self.fillVariableHistograms(ev, temp_probe, col, tag=False)
        return existsProbe, cos_alpha, i

    '''
    def tagNprobeMuons(self, collection, ev, n, ids):
        ## Check if muon passes ID selection
        passID = passIDSelection(ev, n, collection)
        cos_alpha_temp = None
        if passID:
            debug.print("ID passed by muon {0}".format(n), "INFO")
            hasProbe, cos_alpha_temp, i = self.findProbeMuons(ev, n, collection, ids)
            # Fill variable histograms
            self.fillVariableHistograms(ev, n, collection, tag=True)
            # Fill efficiency histograms
            self.fillEfficiencyHistograms(ev, n, collection, hasProbe)
            if hasProbe: self.fillDimuonVariableHistograms(ev, n, i, cos_alpha_temp, collection)
        return passID


    def tagNprobeTracks(self, collection, ev, n, ntotal):
        ## Check if muon passes ID selection
        passID = passIDSelection(ev, n, collection)
        cos_alpha_temp = None
        if passID:
            debug.print("ID passed by muon {0}".format(n), "INFO")
            hasProbe, cos_alpha_temp, i = self.findProbeTracks(ev, n, collection, ntotal)
            # Fill variable histograms
            self.fillVariableHistograms(ev, n, collection, tag=True)
            # Fill efficiency histograms
            self.fillEfficiencyHistograms(ev, n, collection, hasProbe)
            if hasProbe: self.fillDimuonVariableHistograms(ev, n, i, cos_alpha_temp, collection)
        return passID


    '''
    #Given one muon (tag), loop through the other muons in the event to find a matching probe.
    '''
    def findProbeMuons(self, ev, n, col, ids):
        existsProbe = False
        cos_alpha = None
    
        if col=='dmu_dsa':
            phi_tag = ev.dmu_dsa_phi[n]
            eta_tag = ev.dmu_dsa_eta[n]
            theta_tag = 2 * np.arctan(np.exp(-eta_tag)) - np.pi/2    
            for i in ids:
                if i == n: continue
                if ev.dmu_dsa_nValidMuonDTHits[i]+ev.dmu_dsa_nValidMuonCSCHits[i] <= 12: continue
                if ev.dmu_dsa_pt[i] <= 3.5: continue
                phi_temp   = ev.dmu_dsa_phi[i]
                eta_temp   = ev.dmu_dsa_eta[i]
                theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
                v_tag      = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
                v_temp     = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
                cos_alpha_temp = angle(v_tag, v_temp)
                cos_alpha      = cos_alpha_temp
                if cos_alpha < np.cos(2.1) :
                    existsProbe = True
                    self.fillVariableHistograms(ev, i, col, tag=False)
                    break
    
        if col=='dmu_dgl':
            phi_tag = ev.dmu_dgl_phi[n]
            eta_tag = ev.dmu_dgl_eta[n]
            theta_tag = 2 * np.arctan(np.exp(-eta_tag)) - np.pi/2
            for i in ids:
                if i == n: continue
                if ev.dmu_dgl_pt[i] <= 20: continue
                phi_temp = ev.dmu_dgl_phi[i]
                eta_temp = ev.dmu_dgl_eta[i]
                theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
                v_tag      = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
                v_temp     = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
                cos_alpha_temp = angle(v_tag, v_temp)
                cos_alpha      = cos_alpha_temp
                if cos_alpha < np.cos(2.8):
                    existsProbe = True
                    self.fillVariableHistograms(ev, i, col, tag=False)
                    break
    
        return existsProbe, cos_alpha, i


    '''
    #Given one muon (tag), loop through the other muons in the event to find a matching probe.
    '''
    def findProbeTracks(self, ev, n, col, ntotal):
        existsProbe = False
        cos_alpha = None

        if col=='dsa':
            phi_tag = ev.dsa_phi[n]
            eta_tag = ev.dsa_eta[n]
            theta_tag = 2 * np.arctan(np.exp(-eta_tag)) - np.pi/2
            for i in range(ntotal):
                if i == n: continue
                if ev.dsa_nValidMuonDTHits[i]+ev.dsa_nValidMuonCSCHits[i] <= 12: continue
                if ev.dsa_pt[i] <= 3.5: continue
                phi_temp   = ev.dsa_phi[i]
                eta_temp   = ev.dsa_eta[i]
                theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
                v_tag = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
                v_temp = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
                cos_alpha_temp = angle(v_tag, v_temp)
                cos_alpha = cos_alpha_temp
                if cos_alpha < np.cos(2.1) :
                    existsProbe = True
                    self.fillVariableHistograms(ev, i, col, tag=False)
                    break

        if col=='dgl':
            phi_tag = ev.dgl_phi[n]
            eta_tag = ev.dgl_eta[n]
            theta_tag = 2 * np.arctan(np.exp(-eta_tag)) - np.pi/2

            for i in range(ntotal):
                if i == n: continue
                if ev.dgl_pt[i] <= 20: continue
                phi_temp   = ev.dgl_phi[i]
                eta_temp   = ev.dgl_eta[i]
                theta_temp = 2 * np.arctan(np.exp(-eta_temp)) - np.pi/2
                v_tag = [np.cos(theta_tag)*np.cos(phi_tag), np.cos(theta_tag)*np.sin(phi_tag), np.sin(theta_tag)]
                v_temp = [np.cos(theta_temp)*np.cos(phi_temp), np.cos(theta_temp)*np.sin(phi_temp), np.sin(theta_temp)]
                cos_alpha_temp = angle(v_tag, v_temp)
                cos_alpha = cos_alpha_temp
                if cos_alpha < np.cos(2.8):
                    existsProbe = True
                    self.fillVariableHistograms(ev, i, col, tag=False)
                    break

        return existsProbe, cos_alpha, i
    '''

    def count_muons(self, ev):
        return super().count_muons(ev)

    '''
    Function to apply DisplacedMuonFilter. It fills a histogram telling, in case of returning False,
    in which stage of the filter the muon was dropped.
    Args:
        - ev               : event
        - n                : id of muon in event
        - toApply = [x,x,x]: indicates with 1 and 0 if each stage of the filter is applied
    '''
    def passMuonFilter(self, ev, n, toApply=[1,1,1]):
        return super().passMuonFilter(ev, n, toApply)


    def write(self):
        super().write()
