#!/bin/bash

CMSSWDIR=$1
MYHOME=$2

# cd to cmssw and source envs
cd $CMSSWDIR
eval `scram runtime -sh`

# run the combination
# note that we cd into the folder with datacards, so that the form of the 
# shapes section is the same w.r.t. normal datacards (without absolute paths!)
cd $MYHOME
cmd="combineCards.py $3 > $4"
echo 
echo $cmd
eval $cmd 
