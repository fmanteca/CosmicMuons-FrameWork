import os

toFill =  {"requestname": "'HTo2LongLivedTo2mu2jets_MH-{0}_MFF-{1}_CTau-{2}mm_TuneCP5_13p6TeV_pythia8_AOD-MiniAOD'",
           "psetname":    "'HTo2LongLivedTo2mu2jets_TuneCP5_13p6TeV_pythia8_PAT.py'",
           "input":       "'/HTo2LongLivedTo2mu2jets_MH-{0}_MFF-{1}_CTau-{2}mm_TuneCP5_13p6TeV_pythia8/Run3Summer22EEDRPremix-124X_mcRun3_2022_realistic_postEE_v1-v2/AODSIM'",
           "output":      "'HTo2LongLivedTo2mu2jets_MH-{0}_MFF-{1}_CTau-{2}mm_TuneCP5_13p6TeV_pythia8_CMSSW_13_2_0_MiniAOD'"}

# [DoubleMuon/Muon, ERA, PromptReco/ReReco, VERSION, ERAS for cfg file]
samples = {"1000_150_1000":[1000,150,1000],
           "1000_150_100": [1000,150,100],
           "1000_150_10":  [1000,150,10],
           "1000_20_200":  [1000,20,200],
           "1000_20_20":   [1000,20,20],
           "1000_20_2":    [1000,20,2],
           "1000_350_3500":[1000,350,3500],
           "1000_350_350": [1000,350,350],
           "1000_350_35":  [1000,350,35],
           "1000_50_400":  [1000,50,400],
           "1000_50_40":   [1000,50,40],
           "1000_50_4":    [1000,50,4],
           "125_20_1300":  [125,20,1300],
           "125_20_130":   [125,20,130],
           "125_20_13":    [125,20,13],
           "125_50_5000":  [125,50,5000],
           "125_50_500":   [125,50,500],
           "125_50_50":    [125,50,50],
           "200_20_700":   [200,20,700],
           "200_20_70":    [200,20,70],
           "200_20_7":     [200,20,7],
           "200_50_2000":  [200,50,2000],
           "200_50_200":   [200,50,200],
           "200_50_20":    [200,50,20],
           "400_150_4000": [400,150,4000],
           "400_150_400":  [400,150,400],
           "400_150_40":   [400,150,40],
           "400_50_800":   [400,50,800],
           "400_50_80":    [400,50,80],
           "400_50_8":     [400,50,8],
           "400_20_400":   [400,20,400],
           "400_20_40":    [400,20,40],
           "400_20_4":     [400,20,4]}
           


template = "crab_template.py"

if __name__=='__main__':
    for key in samples:
        print(f"crab_HTo2LongLivedTo2mu2jets_{key}.py")
        requestname   = toFill["requestname"].format(*samples[key])
        psetname      = toFill["psetname"].format(*samples[key])
        inputdataset  = toFill["input"].format(*samples[key])
        outputdataset = toFill["output"].format(*samples[key])
        #print(requestname)
        #print(psetname)
        #print(inputdataset)
        #print(outputdataset)
        with open(template, "rt") as inFile:
            toWrite = inFile.read()
            toWrite = toWrite.replace('##REQUESTNAME##',   requestname)
            toWrite = toWrite.replace('##PSETNAME##',      psetname)
            toWrite = toWrite.replace('##INPUTDATASET##',  inputdataset)
            toWrite = toWrite.replace('##OUTPUTDATASET##', outputdataset)
            print(40*'#')
            print(toWrite)
            print(40*'#')
        with open(f"crab_HTo2LongLivedTo2mu2jets_{key}.py", "wt") as outFile:
            outFile.write(toWrite)
        os.system(f'crab submit -c crab_HTo2LongLivedTo2mu2jets_{key}.py')
