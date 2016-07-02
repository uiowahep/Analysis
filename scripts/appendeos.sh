#!/bin/bash

filename=$1
dir=root://eoscms.cern.ch//eos/cms/store/user/vkhriste/ntuples2/SingleMuon/singleMuon_RunC25nsOct_MINIAOD_JSON1/160701_142617/0000

lines=`cat $filename`
echo $lines

rm $filename
for l in $lines; do
	echo $l
	echo $dir/$l >> $filename
done
