from Cut import Cut
from Variable import Variable
from Sample import Sample
import numpy as np

EOSPATH = '/eos/user/r/rlopezru/Samples'

cuts = {
    'NONE':      Cut('1', '', perEvent=False),
    'HLT':       Cut('HLT_L2Mu10_NoVertex_NoBPTX3BX', 
                     'NoBPTX3BX trigger', perEvent=True),
    'passTagID': Cut('{0}_passTagID', 
                     'pass tag ID', perEvent=False),
    'hasProbe':  Cut('({0}_passTagID)&&({0}_hasProbe)', 
                     'tag muon has probe', perEvent=False),
    'isDSA':     Cut('dmu_isDSA', 'is DSA muon', perEvent=False),
    'isDGL':     Cut('dmu_isDGL', 'is DGL muon', perEvent=False),
    'PHIGm2p1':       Cut('{0}_phi>-2.1', r'\phi > -2.1', perEvent=False),
    'PHILm0p8':       Cut('{0}_phi<-0.8', r'\phi < -0.8', perEvent=False),
    'ABSETAL0p7':     Cut('abs({0}_eta)<0.7', r'|\eta| < 0.7', perEvent=False),
    'PTG12p5':        Cut('{0}_pt>12.5', r'p_{T} > 12.5', perEvent=False),
    'RELPTERRL0p2':   Cut('{0}_ptError/{0}_pt<0.2', r'\Delta p_{T}/p_{T} < 0.2', perEvent=False),
    'DTHITSG30':      Cut('{0}_nValidMuonDTHits>30', r'DT hits > 30', perEvent=False),
    'nCHI2L2':        Cut('{0}_normalizedChi2<2', r'\chi^2/ndof < 2', perEvent=False),
    'DSATAGID':       Cut('({0}_phi>-2.1)&&({0}_phi<-0.8)&&(abs({0}_eta)<0.7)&&({0}_pt>12.5)&&({0}_ptError/{0}_pt<0.2)&&({0}_nValidMuonDTHits>30)&&({0}_normalizedChi2<2)', 'DSA Tag ID', perEvent=False),
}

variables = {
    'dz':   Variable('{0}_dz', r'd_{z}', 
                     6, vbins=np.array([0., 8., 20., 40., 60., 90., 140.]), units='cm', perMuon=True),
    'dxy':  Variable('{0}_dxy', r'd_{xy}', 
                     9, vbins=np.array([0., 2., 5., 10., 20., 30., 40., 50., 60., 70.]), units='cm', perMuon=True),
    'pt':   Variable('{0}_pt', r'p_{T}', 
                     100, xmin=0,     xmax=100,  units='GeV', perMuon=True),
    'phi':  Variable('{0}_phi', r'\phi', 
                     50,  xmin=-3.14, xmax=3.14, units='', perMuon=True),
    'eta':  Variable('{0}_eta', r'\eta', 
                     50,  xmin=-2.4,  xmax=2.4,  units='', perMuon=True),
    'cosAlpha':  Variable('{0}_cosAlpha', r'cos(\alpha)', 
                     50,  xmin=-1,    xmax=1,    units='', perMuon=True),
    'ndmu': Variable('ndmu', 'N(\mu)',
                     6, xmin=0, xmax=6),
}

samples = {
    'Cosmics2022C': Sample('Cosmics 2022 C', 
                           f'{EOSPATH}/NoBPTX/CosmicsAnalysis_Run2022C-10Dec2022-v1_MiniAOD-Ntuples/230810_163339/0000/', 
                           isData=True),
    'Cosmics2022C_CMSSW13': Sample('Cosmics 2022 C',
                                   f"{EOSPATH}/NoBPTX/CosmicsAnalysis_Run2022C_10Dec2022_MiniAOD-Ntuples_CMSSW_13_2_0_pre1/230613_142822/0000/",
                                   isData=True),
    'Cosmics2022C_27Jun23_AOD': Sample('Cosmics 2022 C (AOD)', f"{EOSPATH}/NoBPTX/CosmicsAnalysis_Run2022C-27Jun2023-v1_AOD-Ntuples/230815_104243/0000/", isData=True),
}

legendNames = {'dsa': 'reco::Track DSA', 'dmu_dsa': 'reco::Muon DSA',
               'dgl': 'reco::Track DGL', 'dmu_dgl': 'reco::Muon DGL'}
