#! /bin/bash

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
