import os
import argparse

parser = argparse.ArgumentParser(description='Get CRAB status from directory.')
parser.add_argument('--dir', dest='directory', default='crab_projects', help='Directory to iterate (def:crab_projects)')
parser.add_argument('--match', dest='matches', default='HTo2LongLived', help='Directory contains... (def:HTo2LongLived)')
args = parser.parse_args()

class CRABSummary:

    def __init__(self):
        self.status= {"finished":     0,
                      "failed":       0,
                      "running":      0,
                      "idle":         0,
                      "unsubmitted":  0,
                      "toRetry":      0,
                      "transferring": 0}
        self.total = 0
        self.datasets = []
        self.serverStatus = None
        self.tempFile = None

    def call(self, cmd, tempFile):
        os.system(f'{cmd} > {tempFile}')
        self.tempFile = tempFile

    def getServerStatus(self):
        self.serverStatus = os.popen(f"grep 'Status on the CRAB server:' {self.tempFile}").read()

    def getTotal(self):
        return self.finished+self.failed+self.running+self.idle+self.unsubmitted+self.toRetry+self.transferring

    def add(self):
        # get number of jobs
        njobs = int(os.popen(f"cat {self.tempFile} | grep 'Jobs status:'").read().split(' ')[-1].split('/')[-1][:-2])
        self.total += njobs
        for key in self.status:
            cmd_ = f"cat {self.tempFile} | grep 'Extended Job Status' -A{njobs+2} | grep '{key}' | wc -l"
            count = int(os.popen(cmd_).read())
            if count == 0: continue
            self.status[key] += count
            print(f"{key:12}: {count}")
        dataset = os.popen(f"grep 'Output dataset:' {self.tempFile}").read().split('	')[-1][:-1]
        if 'USER' in dataset: 
            print(f'Dataset: {dataset}')
            self.datasets.append(dataset)

    def print(self):
        print(40*'-')
        for key in self.status:
            print(f'>> {key:12}: {self.status[key]:6} ({self.status[key]/self.total*100:4.1f} %)')
        print(f'>> TOTAL       : {self.total:6}')
        print(40*'-')



if __name__=='__main__':
    CS = CRABSummary()
    directory = args.directory
    for subdir in os.listdir(directory):
        if not args.matches in subdir: continue
        cmd = f'crab status -d {directory}/{subdir} --long'
        print(cmd)
        CS.call(cmd, '.temp.txt')
        CS.getServerStatus()
        if 'SUBMITTED' in CS.serverStatus:
            CS.add()
        elif 'TAPERECALL' in CS.serverStatus:
            print('TAPERECALL')
        elif 'SUBMITFAILED' in CS.serverStatus:
            print('SUBMITFAILED')
    CS.print()
    os.system('rm .temp.txt')
