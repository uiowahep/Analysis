cd /afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/limit_and_bias_framework/CMSSW_8_0_26_patch2/src/ViktorAnalysis
dir=`pwd`
cd /afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/combine/CMSSW_7_4_7/src
eval `scramv1 runtime -sh`
cd $dir
source $PWD/config/env.sh
