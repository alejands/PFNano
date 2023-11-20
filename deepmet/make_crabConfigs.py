#!/usr/bin/env python3
import sys,re   # Native python libraries

if len(sys.argv) != 3:
    print("Usage: ./make_crabConfigs.py <username> <storageSite>")
    sys.exit()

### CRAB PARAMETERS ###

username = sys.argv[1]                                      # LFN set to /store/user/<username>/deepmet
storageSite = sys.argv[2]                                   # make sure you can write to storageSite

jobTag = 'Run3Summer22_NanoAODv12_fromMiniAODv4'            # crab job name suffix for all jobs
psetName = 'deepmet_Run3Summer22_NanoAODv12_NANO.py'        # input python config file
outLFNDirBase = f'/store/user/{username}/DeepMET/'          # directory for output files

### JOB PARAMETERS ###
jobs = []   # list of dictionaries with job name, dataset, and nEvents

jobs.append({
'name':     'DYJetsToLL',
'dataset': '/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/Run3Summer22MiniAODv4-forPOG_130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM',
'nEvents': 1200000
})
jobs.append({
'name':     'TTto2L2Nu',
'dataset': '/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM',
'nEvents':  1200000
})
jobs.append({
'name':     'Zto2Nu-4Jets_HT-100to200',
'dataset': '/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM',
'nEvents':  200000
})
jobs.append({
'name':     'Zto2Nu-4Jets_HT-200to400',
'dataset': '/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM',
'nEvents': 200000
})
jobs.append({
'name':     'Zto2Nu-4Jets_HT-400to800',
'dataset': '/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM',
'nEvents': 200000
})
jobs.append({
'name':     'Zto2Nu-4Jets_HT-800to1500',
'dataset': '/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM',
'nEvents': 200000
})
jobs.append({
'name':     'Zto2Nu-4Jets_HT-1500to2500',
'dataset': '/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM',
'nEvents': 200000
})
jobs.append({
'name':     'Zto2Nu-4Jets_HT-2500',
'dataset': '/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM',
'nEvents': 200000
})

### MAIN ###

def main():

    checkIfValidSite(storageSite)
    checkIfValidDatasets(jobs)

    ## Write crab configs ##

    outputNames = []

    for job in jobs:
        jobName = job['name']
        dataset = job['dataset']
        nEvents = job['nEvents']

        outputName = f'crabConfig_{jobName}.py'
        outputNames.append(outputName)

        outputConfig = ''
        requestName = f'{jobName}_{jobTag}'

        with open('template_crabConfig.py', 'r') as template:
            for templateLine in template.readlines():
                outputLine = templateLine
                outputLine = outputLine.replace('__requestName__', requestName)
                outputLine = outputLine.replace('__psetName__', psetName)
                outputLine = outputLine.replace('__inputDataset__', dataset)
                outputLine = outputLine.replace('__nEvents__', str(nEvents))
                outputLine = outputLine.replace('__outLFNDirBase__', outLFNDirBase)
                outputLine = outputLine.replace('__storageSite__', storageSite)

                outputConfig += outputLine

        with open(outputName, 'w') as outputFile:
            outputFile.write(outputConfig)
        print(f'Wrote {outputName}')
    print(f'Crab outputs will be saved in directory {outLFNDirBase} at site {storageSite}')

    ## Update submit_all.sh ##

    with open('submit_all.sh', 'w') as submit_all:
        submit_all.write('#! /bin/bash\n\n')

        for name in outputNames:
            cmd = f'crab submit -c {name}'
            submit_all.write(f'{cmd}\n')

    print('submit_all.py updated')

### UTILITY FUNCTIONS ###

def checkIfValidSite(site_):
    if not re.search('^T[0-3]_[A-Z]{2}_[A-Z]+$',site_):
        print(f'Invalid site format: {site_}')
        sys.exit()

def checkIfValidDatasets(jobs_):
    for job in jobs_:
        dataset = job['dataset']
        if not re.search('\/(.+)\/(.+)\/(.+)', dataset):
            print(f'Invalid dataset format: {dataset}')
            print('Datasets must be of the format "/<PrimaryDataset>/<ProcessedDataset>/<DataTier>"')
            sys.exit()

if __name__ == '__main__':
    main()

