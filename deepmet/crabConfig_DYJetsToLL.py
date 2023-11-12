import os
from CRABClient.UserUtilities import config
config = config()

import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

config.General.requestName = 'DYJetsToLL_Run3Summer22_NanoAODv11_fromMiniAODv3_' + timestamp
config.General.workArea = 'CrabJobs'
config.General.transferLogs = True
config.General.instance = 'prod'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'deepmet_Run3Summer22_NanoAODv11_NANO.py'
config.JobType.maxMemoryMB = 5000 
config.JobType.numCores = 4

config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/Run3Summer22MiniAODv3-forPOG_124X_mcRun3_2022_realistic_v12-v4/MINIAODSIM'
config.Data.splitting = 'Automatic'
config.Data.totalUnits = 1000000
config.Data.outLFNDirBase = '/store/user/alejands/DeepMET/' # make sure to enter *your* username

config.Site.storageSite = 'T3_US_CMU' # site where you have permission to write
