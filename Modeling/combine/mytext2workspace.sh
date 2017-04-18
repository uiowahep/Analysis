#!/bin/bash

MYHOME=$1
CMSSWDIR=$2

# cd to cmssw and source envs
cd $CMSSWDIR
eval `scram runtime -sh`

# convert all of the datacards
cd $MYHOME
DATACARDS=`ls *$3.txt`
for d in $DATACARDS
do
    cmd="text2workspace.py $d"
    echo $cmd
    eval $cmd
    echo
done
