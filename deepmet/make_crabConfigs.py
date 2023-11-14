import getpass # native python libraries

### CRAB PARAMETERS ###
                                                            # default: get username from shell
userName = ''                                               # change username here if different
if userName == '':
    userName = getpass.getuser()

jobTag = 'Run3Summer22_NanoAODv12_fromMiniAODv4'            # crab job name suffix for all jobs
psetName = 'deepmet_Run3Summer22_NanoAODv12_NANO.py'        # input python config file
outLFNDirBase = '/store/user/{}/DeepMET/'.format(userName)  # directory for output files
storageSite = 'T3_US_CMU'                                   # note: make sure you can write to storageSite

### DATASETS ###

jobs = []   # jobs.append(['jobName', nEvents, 'dataset'])

jobs.append([
 'DYJetsToLL', 1200000,
'/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/Run3Summer22MiniAODv4-forPOG_130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
])
jobs.append([
 'TTto2L2Nu', 1200000,
'/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
])
jobs.append([
 'Zto2Nu-4Jets_HT-100to200', 200000,
'/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
])
jobs.append([
 'Zto2Nu-4Jets_HT-200to400', 200000,
'/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
])
jobs.append([
 'Zto2Nu-4Jets_HT-400to800', 200000,
'/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
])
jobs.append([
 'Zto2Nu-4Jets_HT-800to1500', 200000,
'/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
])
jobs.append([
 'Zto2Nu-4Jets_HT-1500to2500', 200000,
'/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
])
jobs.append([
 'Zto2Nu-4Jets_HT-2500', 200000,
'/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2/MINIAODSIM'
])

################################################################################

def main():

    outputNames = []

    for jobName, nEvents, dataset in jobs:
        requestName = '{}_{}'.format(jobName, jobTag)
        output = ''

        with open('template_crabConfig.py', 'r') as template:
            for line in template.readlines():
                newLine = line
                newLine = newLine.replace('__requestName__', requestName)
                newLine = newLine.replace('__psetName__', psetName)
                newLine = newLine.replace('__inputDataset__', dataset)
                newLine = newLine.replace('__nEvents__', str(nEvents))
                newLine = newLine.replace('__outLFNDirBase__', outLFNDirBase)
                newLine = newLine.replace('__storageSite__', storageSite)

                output += newLine

        outputName = 'crabConfig_{}.py'.format(jobName)
        outputNames.append(outputName)
        with open(outputName, 'w') as outputFile:
            outputFile.write(output)

        print("Wrote {}".format(outputName))            # spacing lines up filename with dataset name :)
        print("Runs on dataset {}\n".format(dataset))

    print('Crab outputs will be saved in directory {} at site {}'.format(outLFNDirBase, storageSite))

    with open('submit_all.sh', 'w') as submit_all:
        submit_all.write('#! /bin/bash\n\n')

        for name in outputNames:
            cmd = 'crab submit -c {}'.format(name)
            submit_all.write(cmd + '\n')

    print('submit_all.py updated')

if __name__ == '__main__':
    main()

