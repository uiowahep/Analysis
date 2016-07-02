#!/bin/bash

filename=$1
dirprefix=root://eoscms.cern.ch//eos/cms
dir=$2

lines=`cat $filename`
echo $lines

rm $filename
for l in $lines; do
	echo $l
	echo $dirprefix$dir/$l >> $filename
done
