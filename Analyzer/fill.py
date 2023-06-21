import ROOT as r
import os, json
from math import pi
import numpy as np
from argparse import ArgumentParser
import include.drawUtils as draw
from include.Launcher import Launcher
import include.cfg as cfg
from include.DTree import DTree

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

########################################## FUNCTIONS #############################################
def printConfig(args):
    print(bcolors.WARNING + 20*'#' + ' DISPLACED MUON ANALYZER ' + 20*'#')
    print(' >> -t / --tag:    {0}'.format(args.tag))
    print(' >> -c / --cuts:   {0}'.format(args.cuts_filename))
    print(' >> --no-run:      {0}'.format(not args.run))
    print(' >> -q / --condor: {0}'.format(args.condor))
    print(65*'#' + bcolors.ENDC)


#r.gStyle.SetLabelFont(42)
################################# GLOBAL VARIABLES DEFINITION ####################################

runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'
EOSPATH = '/eos/user/r/rlopezru/DisplacedMuons-Analyzer_out/Analyzer/'

# Read dat file
datFile = WORKPATH + 'dat/Samples_Summer23_Cosmics.json'
dat = json.load(open(datFile,'r'))

if __name__ == '__main__':

    r.gROOT.ProcessLine('.L ./include/tdrstyle.C')
    r.gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)
    print('EOSPATH: ' + EOSPATH)

    r.gStyle.SetPaintTextFormat("3.2f")
    parser = ArgumentParser()
    parser.add_argument('-c', '--cuts', dest='cuts_filename')
    parser.add_argument('-t', '--tag', dest='tag')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true')
    parser.add_argument('-q', '--queue', dest='condor', action= 'store_true')
    parser.add_argument('--no-run', dest='run', action= 'store_false')
    args = parser.parse_args()

    printConfig(args)
   
    run = args.run
    gTag = args.tag
    cuts_filename = WORKPATH + args.cuts_filename
 
    # Set debugging mode
    with open(WORKPATH+'include/cfg.py','w') as f:
        f.write('DEBUG = {0}'.format(args.debug))

    # Trees
    trees = []
    trees.append(DTree('Cosmics_2022B_MiniAOD_ReReco',    'Cosmics Run2022B MiniAOD',            dat['Cosmics_2022B']['MiniAOD_ReReco'],                  gTag, isData = True))
    trees.append(DTree('Cosmics_2022C_MiniAOD_ReReco',    'Cosmics Run2022C MiniAOD',            dat['Cosmics_2022C']['MiniAOD_ReReco'],                  gTag, isData = True))
    trees.append(DTree('Cosmics_2022D_MiniAOD_ReReco',    'Cosmics Run2022D MiniAOD',            dat['Cosmics_2022D']['MiniAOD_ReReco'],                  gTag, isData = True))    
    trees.append(DTree('Cosmics_2022E_MiniAOD_ReReco',    'Cosmics Run2022E MiniAOD',            dat['Cosmics_2022E']['MiniAOD_ReReco'],                  gTag, isData = True))    
    trees.append(DTree('Cosmics_2022F_MiniAOD',    'Cosmics Run2022F MiniAOD',            dat['Cosmics_2022F']['MiniAOD-Ntuples'],                  gTag, isData = True))    
    trees.append(DTree('Cosmics_2022G_MiniAOD',    'Cosmics Run2022G MiniAOD',            dat['Cosmics_2022G']['MiniAOD-Ntuples'],                  gTag, isData = True))    

    if run:
        # Empty condor folder
        if args.condor:
            os.system('rm {0}/condor/{1}/*'.format(WORKPATH, args.tag))

        # Launch jobs
        for dtree in trees:
            if args.condor:
                dtree.launchJobs(cuts_filename)
            else:
                dtree.loop(cuts_filename)
