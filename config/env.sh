#!/bin/bash

#	for CMSSW use it's the CMSSW/src/Analysis
#	for STANDALONE use it's the build directory or for testing purposes repo
export ANALYSISHOME=`dirname ${BASH_SOURCE[0]}`/..
export PYTHONPATH=$ANALYSISHOME:$PYTHONPATH
echo "ANALYSIS HOME is now at $ANALYSISHOME"
echo $PYTHONPATH
