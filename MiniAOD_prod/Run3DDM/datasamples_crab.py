toFill =  {"requestname": "'{0}MuonRun2022{1}-{2}-v{3}_RAW-MiniAOD'",
           "psetname":    "'Muon_{2}_{4}_PAT.py'",
           "input":       "'/{0}Muon/Run2022{1}-{2}-v{3}/AOD'",
           "output":      "'{0}Muon_Run2022{1}-CMSSW_13_2_0-v{3}_MiniAOD'"}

# [DoubleMuon/Muon, ERA, PromptReco/ReReco, VERSION, ERAS for cfg file]
samples = {"2022_DoubleMuonRun2022A-ReReco-v2":     ["Double", "A", "10Dec2022",  "2", "ABCD"],
           "2022_DoubleMuonRun2022B-ReReco-v2":     ["Double", "B", "10Dec2022",  "2", "ABCD"],
           "2022_DoubleMuonRun2022C-ReReco-v1":     ["Double", "C", "10Dec2022",  "1", "ABCD"],
           "2022_DoubleMuonRun2022C-ReReco-v2":     ["Double", "C", "10Dec2022",  "2", "ABCD"],
           "2022_DoubleMuonRun2022C-PromptReco-v1": ["Double", "C", "PromptReco", "1", "ABCD"],
           "2022_MuonRun2022C-ReReco-v1":           ["",       "C", "10Dec2022",  "1", "ABCD"],
           "2022_MuonRun2022D-ReReco-v1":           ["",       "D", "10Dec2022",  "1", "ABCD"],
           "2022_MuonRun2022E-ReReco-v2":           ["",       "E", "10Dec2022",  "2", "E"],
           "2022_MuonRun2022C-PromptReco-v1":       ["",       "C", "PromptReco", "1", "ABCD"],
           "2022_MuonRun2022D-PromptReco-v1":       ["",       "D", "PromptReco", "1", "ABCD"],
           "2022_MuonRun2022D-PromptReco-v2":       ["",       "D", "PromptReco", "2", "ABCD"],
           "2022_MuonRun2022E-PromptReco-v1":       ["",       "E", "PromptReco", "1", "EFG"],
           "2022_MuonRun2022F-PromptReco-v1":       ["",       "F", "PromptReco", "1", "EFG"],
           "2022_MuonRun2022G-PromptReco-v1":       ["",       "G", "PromptReco", "1", "EFG"]}

template = "crab_template.py"

if __name__=='__main__':
    for key in samples:
        print(key)
        print(f"crab_{key}.py")
        print(samples[key][4])
        requestname   = toFill["requestname"].format(*samples[key])
        psetname      = toFill["psetname"].format(*samples[key])
        inputdataset  = toFill["input"].format(*samples[key])
        outputdataset = toFill["output"].format(*samples[key])
        print(requestname)
        print(psetname)
        print(inputdataset)
        print(outputdataset)
        with open(template, "rt") as inFile:
            toWrite = inFile.read()
            toWrite = toWrite.replace('##REQUESTNAME##',   requestname)
            toWrite = toWrite.replace('##PSETNAME##',      psetname)
            toWrite = toWrite.replace('##INPUTDATASET##',  inputdataset)
            toWrite = toWrite.replace('##OUTPUTDATASET##', outputdataset)
            print(toWrite)
        with open(f"crab_{key}.py", "wt") as outFile:
            outFile.write(toWrite)
