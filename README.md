# Cosmics Muons Ntupler

## Instructions for installing 

### Installing

    cmsrel CMSSW_15_0_5
    cd CMSSW_15_0_5/src
    cmsenv
    git clone git@github.com:fmanteca/CosmicMuons-FrameWork.git
    scram b -j 8

### Producing Ntuples
The framework will produce Ntuples from AOD. Every time you make a change anywhere, for instance in 'plugins/MuonNtupleProducer.cc', do not forget to re-compile (run 'scram b -j 8' in 'CMSSW_15_0_5/src').

    cd CosmicMuons-FrameWork/Ntuplizer/test/
        
    # Find an input AOD file and use it on process.source in 'Cosmics_runNtuplizer_AOD_cfg.py':
    # Use DAS to get the paths: https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2F*Cosmics*%2FRun*2025*%2FAOD
    # One can either give the path of any of them, i.e., fileNames = cms.untracked.vstring('/store/data/Commissioning2025/Cosmics/AOD/PromptReco-v1/000/389/353/00000/896a0637-7186-4d8e-8af5-b11e22c90ea4.root')
    # or copy it in local 'xrdcp root://cms-xrd-global.cern.ch//store/data/Commissioning2025/Cosmics/AOD/PromptReco-v1/000/389/353/00000/896a0637-7186-4d8e-8af5-b11e22c90ea4.root ./'
    # and then point to it: 'fileNames = cms.untracked.vstring('file:896a0637-7186-4d8e-8af5-b11e22c90ea4.root')'. The latter option should be faster for testing purposes.
    
    cmsRun Cosmics_runNtuplizer_AOD_cfg.py

### Submit jobs to HTCondor

Before running the following commands, set your personal path in run.sh and select the input datasets and output path in prepare_files.py.

prepare_files.py will produce a txt file where each row will contain a pair input_file output_file. 

condor.sub will submit one job per row to the cluster, taking run.sh as the executable.

    cd condor
    voms-proxy-init --voms cms --hours 96  -out ${HOME}/.x509up_${UID};export X509_USER_PROXY=${HOME}/.x509up_${UID}
    python3 prepare_files.py
    condor_submit condor.sub

    
### OR Submit jobs to crab
The following instructions will allow to submit jobs to the cluster for an entire dataset like '/Cosmics/Run2025A-PromptReco-v1/AOD'. The output ntuples will be stored in your '/eos/user/' area.

    source /cvmfs/cms.cern.ch/crab3/crab.sh
    cmsenv
    voms-proxy-init --voms cms --valid 168:00
    crab submit crab_Commissioning2025.py

### Useful links:
* Muon reconstruction documentation: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuons
* Cosmic muon reconstruction documentation: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCosmicMuonReco
* reco::Muon class: https://github.com/cms-sw/cmssw/blob/master/DataFormats/MuonReco/interface/Muon.h
* Muon POG selections & definitions: https://github.com/cms-sw/cmssw/blob/master/DataFormats/MuonReco/src/MuonSelectors.cc
* OMS (used to get run numbers from CRUZET/CRAFT): https://cmsoms.cern.ch/cms/run_3_cruz/cruzet_2025?cms_run_sequence=GLOBAL-RUN
* Get the datasets containing a given run number in DAS: https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset+run%3D389767

### Event displays with Fireworks (accept miniAOD/AOD/RECO formats as input)

Use edmPickEvents.py to filter out events if needed (see https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookPickEvents).

Copy the output to a public /eos/cms/store/group/ path.

Insert path here: https://fireworks.cern.ch/cmsShowWeb/revetor.pl (starting with /store/)

Instructions for cosmic multi-muons:
* Add Collections -> type "leg" -> select "Muons muon1Leg"
* FilterDialog -> $Muons10_muons1Leg@.size()>10 
* 3D -> i -> Geometry -> show all
