#!/bin/sh

cd /eos/user/f/fernanpe/CMSSW_15_0_5/src/CosmicMuons-FrameWork/Ntuplizer/test/condor
cmsenv

cmsRun Cosmics_runNtuplizer_AOD_cfg.py input=$1 output=$2
