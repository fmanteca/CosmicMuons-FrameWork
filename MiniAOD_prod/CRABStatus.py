import os
import argparse

parser = argparse.ArgumentParser(description='Get CRAB status from directory.')
parser.add_argument('--dir', dest='directory', default='crab_projects', help='Directory to iterate (def:crab_projects)')
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

    def getTotal(self):
        return self.finished+self.failed+self.running+self.idle+self.unsubmitted+self.toRetry+self.transferring

    def add(self, tempFile):
        # get number of jobs
        njobs = int(os.popen(f"cat {tempFile} | grep 'Jobs status:'").read().split(' ')[-1].split('/')[-1][:-2])
        self.total += njobs
        for key in self.status:
            cmd_ = f"cat {tempFile} | grep 'Extended Job Status' -A{njobs+2} | grep '{key}' | wc -l"
            count = int(os.popen(cmd_).read())
            self.status[key] += count
            print(f"{key:12}: {count}")

    def print(self):
        print(40*'-')
        for key in self.status:
            print(f'>> {key:12}: {self.status[key]}')
        print(f'>> TOTAL       : {self.total}')
        print(40*'-')



if __name__=='__main__':
    CS = CRABSummary()
    directory = args.directory
    for subdir in os.listdir(directory):
        cmd = f'crab status -d {directory}/{subdir} --long > .temp.txt'
        print(cmd)
        os.system(cmd)
        CS.add('.temp.txt')
    CS.print()
    os.system('rm .temp.txt')
