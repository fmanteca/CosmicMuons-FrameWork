# Cosmics Muons Ntupler

## Instructions for installing 

### Installing

    cmsrel CMSSW_15_0_5
    cd CMSSW_15_0_5/src
    cmsenv
    git clone git@github.com:fmanteca/CosmicMuons-FrameWork.git
    scram b -j 8

### Producing Ntuples
The framework will produce Ntuples from AOD. Everytime you make a change anywhere, for instance in 'plugins/MuonNtupleProducer.cc', do not forget to re-compile (run 'scram b -j 8' in 'CMSSW_15_0_5/src').

    cd CosmicMuons-FrameWork/Ntuplizer/test/
        
    # Find an input AOD file and use it on process.source in 'Cosmics_runNtuplizer_AOD_cfg.py':
    # Use DAS to get the paths: https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2F*Cosmics*%2FRun*2025*%2FAOD
    # One can either give the path of any of them, i.e., fileNames = cms.untracked.vstring('/store/data/Run2025A/Cosmics/AOD/PromptReco-v1/000/390/735/00000/004edc0a-7cb1-46e1-af6c-5f24246a0418.root')
    # or copy it in local 'xrdcp root://cms-xrd-global.cern.ch//store/data/Run2025A/Cosmics/AOD/PromptReco-v1/000/390/735/00000/004edc0a-7cb1-46e1-af6c-5f24246a0418.root ./'
    # and then point to it: 'fileNames = cms.untracked.vstring('file:004edc0a-7cb1-46e1-af6c-5f24246a0418.root')'. The latter option should be faster for testing porpuses.
    
    cmsRun Cosmics_runNtuplizer_AOD_cfg.py

### Submit jobs to crab
The following instructions will allow to submit jobs to the cluster for an entire dataset like '/Cosmics/Run2025A-PromptReco-v1/AOD'. The output ntuples will be stored in your '/eos/user/' area.

    source /cvmfs/cms.cern.ch/crab3/crab.sh
    cmsenv
    voms-proxy-init --voms cms --valid 168:00
    crab submit crab_CosmicsData_2025A_AOD.py
