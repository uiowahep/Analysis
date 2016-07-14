#!/bin/bash

pname=process_2016MCPrompt
lpids=`pgrep $pname`
echo $lpids
for ip in $lpids;
do
	kill -9 $ip
done
