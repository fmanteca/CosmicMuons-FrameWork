import ROOT as r
from array import array
from ROOT import TTree, TFile, TCut, TH1F, TH2F, TH3F, THStack, TCanvas, SetOwnership
import copy
import os
import __main__

'''
Class that contains everything to read and process a certain dataset
'''
class DTree:

    def __init__(self, name, label, location, tag, short_name = None, isData = False):
        self.name = name # May be a list
        if isinstance(self.name, list): self.short_name = short_name # Always string
        else: self.short_name = self.name
        self.label = label
        self.location = location # May be a list
        self.isData = isData
        self.tag = tag # esto se da por linea de comandos al correr fill.py

        # ---------------------------------------------------------------------------------------------------------
        # Get useful directories, paths and filenames
        self.WORKDIR = os.getcwd() + '/'
        # Condor templates
        self.condorSh_template =  open(self.WORKDIR+"templates/condor_template.sh","r").read()
        self.condorSub_template = open(self.WORKDIR+"templates/condor_template.sub","r").read()
        # Script for looping events
        self.scriptLoc = self.WORKDIR+"loopEvents.py"
        # Condor logs location
        self.condorDir = self.WORKDIR+"condor/"+self.tag+"/"
        if not os.path.exists(self.condorDir): os.makedirs(self.condorDir)
        # Declare histograms dir and list
        self.histsDir = "/eos/user/r/rlopezru/DisplacedMuons-Analyzer_out/Analyzer/temp_hists/"+self.tag+"/"
        if not os.path.exists(self.histsDir): os.makedirs(self.histsDir)
        # ----------------------------------------------------------------------------------------------------------
        
        self.dtpaths = []
        #self.dtfiles = []
        #self.dtrees  = []
        self.outHistFiles = []
        if not isinstance(self.location, list):
            for i,_file in enumerate(os.listdir(self.location)):
                if '.root' not in _file: continue
                #ftfile = TFile(location + _file)
                #ttree = ftfile.Get('Events')
                self.dtpaths.append(location + _file)
                #self.dtfiles.append(ftfile)
                #self.dtrees.append(ttree)
                outHistFilename = self.histsDir+'hists_{0}_{1}.root'.format(self.name, i)
                self.outHistFiles.append(outHistFilename) # have a register of the output files with the histograms
            #self.closeFiles()

        '''
        self.count = 0.
        if self.isData:
            for dtree in self.dtrees:
                self.count += dtree.GetEntries()
        '''
        self.printSample() 
        

    def getHistsDir(self):
        return self.histsDir

    def getMergedHistsFile(self):
        return self.targetFile

    def printSample(self):
        print(50*"-")
        print("Sample Name: ", self.name)
        print("Sample Location: ", self.location)
        print("Sample IsData: ", self.isData)
        #print("Event count: ", self.count)
        print(50*"-")

    def closeFiles(self):
        for _file in self.dtfiles:
            _file.Close()

    def process(self, outHistFile):
        return 

    def launchJobs(self, cutsFilename):
        self.cutsFilename = cutsFilename

        for i,path in enumerate(self.dtpaths):
            # aqui hay que llamar a loopevents.py
            command = "python3 {0} -o {1} -i {2} -c {3} --name {4}".format(self.scriptLoc,
                                                                                  self.outHistFiles[i],
                                                                                  path,
                                                                                  self.cutsFilename,
                                                                                  self.name)
            sh_filename = self.condorDir+"bash_{0}_{1}.sh".format(self.name, i)
            with open(sh_filename,"w") as f_sh:
                f_sh.write(self.condorSh_template.format(command))

        sub_filename = self.condorDir+"condor_{0}.sub".format(self.name)
        with open(sub_filename,"w") as f_sub:
            f_sub.write(self.condorSub_template.format(self.condorDir, self.name))
        os.system("condor_submit "+sub_filename+" --batch-name "+self.name)

    def loop(self, cutsFilename):
        self.cutsFilename = cutsFilename

        for i,path in enumerate(self.dtpaths[305:306]):
            print(' -> Processing file {0}'.format(path))
            command = "python3 {0} -o {1} -i {2} -c {3} --name {4}".format(self.scriptLoc,
                                                                                  self.outHistFiles[i],
                                                                                  path,
                                                                                  self.cutsFilename,
                                                                                  self.name)
            os.system(command)


    def merge(self, force=False):
        if not isinstance(self.name, list):
            self.targetFile = self.histsDir + 'merged_hists_{0}.root'.format(self.name)
            if os.path.exists(self.targetFile): 
                print('>> Merged file {0} already exists'.format(self.targetFile))
                if force:
                    print('    - Removing file {0}'.format(self.targetFile)) 
                    os.system('rm {0}'.format(self.targetFile))
                else: return
            print('>> Merging files with following details:')
            print('    - location: {0}'.format(self.histsDir))
            print('    - sample:   {0}'.format(self.name))
            command = 'hadd {0} '.format(self.targetFile)
            for _file in self.outHistFiles:
                if not os.path.exists(_file): continue
                command += '{0} '.format(_file)
        else:
            self.targetFile = self.histsDir + 'merged_hists_{0}.root'.format(self.short_name)
            if os.path.exists(self.targetFile):
                print('>> Merged file {0} already exists'.format(self.targetFile))
                if force:
                    print('    - Removing file {0}'.format(self.targetFile))
                    os.system('rm {0}'.format(self.targetFile))
                else: return
            # Check if individual merged files exist
            #for _name in self.name:
            #    if not os.path.exists(self.histsDir + 'merged_hists_{0}.root'.format(_name)):
            #        self.merge_(_name)
            print('>> Merging files with following details:')
            print('    - location: {0}'.format(self.histsDir))
            print('    - sample:   {0}'.format(self.name))
            command = 'hadd {0} '.format(self.targetFile)
            for i,_name in enumerate(self.name):
                command += '{0} '.format(self.histsDir+'merged_hists_{0}.root'.format(_name))
        os.system(command)
        print('>> Merging done')


    def merge_(self, name):
        targetFile = self.histsDir + 'merged_hists_{0}.root'.format(name)
        print('>> Merging files with following details:')
        print('    - location: {0}'.format(self.histsDir))
        print('    - sample:   {0}'.format(name))
        command = 'hadd {0} '.format(targetFile)
        for _file in self.outHistFiles:
            if not os.path.exists(_file): continue
            command += '{0} '.format(_file)
        os.system(command)
