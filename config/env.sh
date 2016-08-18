#!/bin/bash

#	for CMSSW use it's the CMSSW/src/Analysis
#	for STANDALONE use it's the build directory or for testing purposes repo
export ANALYSISHOME=`dirname ${BASH_SOURCE[0]}`/..
echo "ANALYSIS HOME is now at $ANALYSISHOME"

#	location of resources.
#	Always under the git version control
export ANALYSISRESOURCESHOME=$1
echo "ANALYSIS RESOURCES ar located at $ANALYSISRESOURCESHOME"
