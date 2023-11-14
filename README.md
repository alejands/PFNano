# PFNano

This README focuses on the usage of PFNano as it pertains to DeepMET. The original README from cms-jet can be found [here](https://github.com/cms-jet/PFNano/tree/13_0_7_from124MiniAOD#readme).

This branch is for generating custom Run3 **NanoAODv12-like** (13_0_X) data with PF candidate information **using MiniAODv3** (12_4_X) data. For NanoAODv11 (only used in Run3Summer22/Run3Summer22EE), see the [12_6_0 branch](https://github.com/DeepMETv2/PFNano/tree/12_6_0).

**NOTE:** For the time being, we will try running **MiniAODv4** on this branch since there is no branch from cms-jet specifically for this data yet, though this may need to be rerun in the future.

From [cms-jet README](https://github.com/cms-jet/PFNano/tree/13_0_7_from124MiniAOD#readme):

> This branch runs with 2022 data (ReRecoCDE and PromptRecoFG), MC for Run3 (Run3Summer22 and Run3Summer22EE, nanoAODv11), in 13_0_X. This branch reruns Puppi v17, reclusters the AK8 Puppi and AK8 taggers, and then reruns the new AK4 taggers (new DeepJet, new ParticleNetAK4 and RobustParTAK4) available from 13_0_X.

> (Note: this branch runs on NanoAOD v11 data and MC in 13_0_X, to mimic the NanoAOD v12 condition)

NanoAODv12 is the recommended version for Run3. For the most up-to-date information, refer to the [XPOG recommendations](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc) (*NanoAODv12 documentation is incomplete at time of writing and this page shows the wrong `--era` label but correct recommendation. Correct is below in the appropriate section*) or the [NanoAOD twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookNanoAOD).

Our additions to the original code from cms-jet are found in the `PFNano/deepmet` folder. The only other minor modification is to `PFNano/python/pfnano_cff.py` to not include data relevant to the BTV group (who currently maintains the cms-jet code) that is not relevant for DeepMET training.

## Setup

```
cmsrel CMSSW_13_0_13
cd CMSSW_13_0_13/src
cmsenv
git cms-merge-topic colizz:dev-130X-addNegPNet # adding negative tag
git clone git@github.com:DeepMETv2/PFNano.git PhysicsTools/PFNano -b 13_0_7_from124MiniAOD
scram b -j 10
cd PhysicsTools/PFNano/deepmet
```

Assume that code is being run in the `PFNano/deepmet` directory unless otherwise specified.

## Creating your own python configuration file

The python configuration file used is already saved in `deepmet_Run3Summer22_NanoAODv12_NANO.py`. If you just want to run this configuration and submit crab jobs, you can skip to the next section.

The configuration file can be regenerated/edited using the script `run_cmsDriver.sh`. To regenerate the python configuration file, run

```
./run_cmsDriver.sh
```

The cmsDriver command can also be run directly (note: backslashes `\` are only for separating lines for legibility while still allowing you to copy-paste and run this command).

```
cmsDriver.py deepmet_Run3Summer22_NanoAODv12 \
--mc --eventcontent NANOAODSIM --datatier NANOAODSIM --step NANO \
--conditions 130X_mcRun3_2022_realistic_v5 \
--era Run3 \
--customise_commands="process.add_(cms.Service('InitRootHandlers', \
EnableIMT = cms.untracked.bool(False)));\
process.MessageLogger.cerr.FwkReport.reportEvery=1000;\
process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)" \
--nThreads 4 -n 10 \
--filein "/store/mc/Run3Summer22MiniAODv4/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/MINIAODSIM/forPOG_130X_mcRun3_2022_realistic_v5-v2/2520000/08252cf5-7cda-4c6d-b358-0db4779efc6f.root" \
--fileout file:out_deepmet.root \
--customise="PhysicsTools/PFNano/pfnano_cff.PFnano_customizeMC_allPF"  --no_exec
```

If you are editing this command (directly or in `run_cmsDriver.sh`), the most important parameters to get right are `--era` and `--conditions`. Be sure to check these when running on a new dataset. The values used above are the recommended values for NanoAODv12 production in 12_6_X for Run3Summer22/Run3Summer22EE.

`--era` can be found in the [XPOG documentation on private NanoAOD production](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Instructions/Private-production#production-with-latest-developments-from-the-integration-branch).

`--conditions` is the global tag (GT) and can be found by looking at the [cmsDriver recipes used by PdmV for Run3](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis#Recipes_for_Run3Summer22_and_Run).

The best way to be sure is checking on [McM](https://cms-pdmv-prod.web.cern.ch/mcm/) (if you're comfortable with it) for the data you're trying to recreate (ie. the NanoAOD dataset, not the MiniAOD dataset), and looking for the `--era` and `--conditions` parameters of the cmsDriver commands used for central production.

The PFNano modifications are added with the argument

`--customise="PhysicsTools/PFNano/pfnano_cff.PFnano_customizeMC_allPF"`.

The option `PFnano_customizeMC_allPF` in `pfnano_cff.py` saves all PF candidates to the output NanoAODs. The other options are not relevant to DeepMET, but more information on them can be found in the [cms-jet README](https://github.com/cms-jet/PFNano/tree/13_0_7_from124MiniAOD#local-usage).

### Verifying python configuration file

Before submitting a CRAB job, it's good practice to run the configuration file locally for a few events.

```
cmsRun deepmet_Run3Summer22_NanoAODv12_NANO.py
```

For example, check that the correct number of events is produced and the file is not empty.

```
edmFileUtil out_deepmet.root
# out_deepmet.root
# out_deepmet.root (1 runs, 1 lumis, 10 events, 3192362 bytes)
```

You could also check that the PF candidate information is being filled using a ROOT TBrowser.

You can also edit the number of events to run locally by changing `maxEvents` in this python file. The configuration provided is set to 10 events by default. The default value can also be set with the cmsDriver argument `-n`. Setting to `-1` runs over all events in the input file(s). Changing `maxEvents` has no effect on CRAB jobs.

## Submitting CRAB jobs

**IMPORTANT**: Be sure to edit these files to include _your_ username and a storage site that you can write to. You can check if you have site permissions by doing, for example,

```
crab checkwrite --site=T3_US_CMU
```

To submit the CRAB jobs for the `DYJetsToLL` and `TTto2L2Nu` datasets,

```
crab submit -c crabConfig_DYJetsToLL.py
```

```
crab submit -c crabConfig_TTto2L2Nu.py
```

If you wish to create your own CRAB jobs, check out these twikis on the [CRAB software](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCrab) and [CRAB configuration file](https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile).

## Monitoring CRAB jobs

Below are some examples of how to check the status of the CRAB jobs from above. (Your job names will be different. The CRAB configs provided add a timestamp to the end of the job name.)

```
# examples only
crab status -d CrabJobs/crab_DYJetsToLL_Run3Summer22_NanoAODv12_fromMiniAODv4_20231114-072438/
crab status -d CrabJobs/crab_TTto2L2Nu_Run3Summer22_NanoAODv12_fromMiniAODv4_20231114-072503/
```

I recommend going to the `https://monit-grafana.cern.ch/...` URL that shows up in the `crab status` output for a nice monitoring UI.

## Where to find CRAB job output files

Once the jobs are done, they will be published on CMSDAS. **They will not show up immediately,** even if says they are already published. If you don't see them or the dataset is empty, wait a couple of hours or until the next day before panicking.

The dataset name and link can be found in the output of `crab status`. For example,

```
Output dataset:                 /DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/alejands-crab_DYJetsToLL_Run3Summer22_NanoAODv12_fromMiniAODv4_20231114-072438-71e480a15f73d107b0f9ddbffc19595d/USER
Output dataset DAS URL:         https://cmsweb.cern.ch/das/request?input=%2FDYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8%2Falejands-crab_DYJetsToLL_Run3Summer22_NanoAODv12_fromMiniAODv4_20231114-072438-71e480a15f73d107b0f9ddbffc19595d%2FUSER&instance=prod%2Fphys03
```

[Link to CMSDAS example here](https://cmsweb.cern.ch/das/request?instance=prod/phys03&input=/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/alejands-crab_DYJetsToLL_Run3Summer22_NanoAODv12_fromMiniAODv4_20231114-072438-71e480a15f73d107b0f9ddbffc19595d/USER). If you're looking up the dataset by copying the name, be sure to change the dbs instance to `prod/phys03` above the search bar on CMSDAS.

To list the output files in the terminal using CMSSW,

```
dasgoclient --query="file dataset=/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/alejands-crab_DYJetsToLL_Run3Summer22_NanoAODv12_fromMiniAODv4_20231114-072438-71e480a15f73d107b0f9ddbffc19595d/USER instance=prod/phys03"
```

This can be useful for saving the list of generated files to a text file for future use. **Note**: the parameter `instance=prod/phys03` is needed to see private datasets from CRAB jobs.

 The files can be accessed over xrootd. For example,

```
# show basic file info such as number of events
edmFileUtil root://cmsxrootd.fnal.gov//store/user/alejands/DeepMET/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/crab_DYJetsToLL_Run3Summer22_NanoAODv12_fromMiniAODv4_20231114-072438/231114_132453/0000/out_deepmet_1.root
```

NOTE: `cmsxrootd.fnal.gov` is for LPC use. For LXPLUS, use `xrootd-cms.infn.it`. See also the [xrootd twiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookXrootdService).

