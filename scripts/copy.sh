#!/bin/bash

filename=$1
dest=$2

files=`cat $filename`
for f in $files; do
	xrdcp $f $dest
done
