#!/bin/bash

runData=$1
runMC=$2

exec=../process_2016MCPrompt
filelistdir=$ANALYSIS/files/filelist
outputdir=$ANALYSIS/files/results/dimuon
pileupdir=$ANALYSIS/files/pileup

data_instances_to_process=("data2015Prompt data2015ReReco data2016Prompt")
mc_instances_to_process=(mc_dy_jetsToLL_74X mc_ttJets_74X mc_dy_jetsToLL_76X mc_ttJets_76X)

mc_pileup=(pileup_dy_jetsToLL_74X2015.root pileup_ttJets_74X2015.root pileup_dy_jetsToLL_76X2015.root pileup_ttJets_76X2015.root)

data_pileup=(pileup_data2015Prompt_69mb.root pileup_data2015ReReco_69mb.root pileup_data2016Prompt_71p3mb.root)

description=(data2015Prompt_69mb data2015ReReco_69mb data2016Prompt_71p3mb)

#	create a dir with logs
logdir=../logs
if [ ! -d $logdir ];
then
	mkdir $logdir
fi

if [ $runData -eq 1 ];
then
	#	process Data
	echo "-----------------"
	echo "Starting Data Processing"
	echo "-----------------"
	for idata in $data_instances_to_process;
	do
		logfile=$logdir/$idata.log
		inputfile=$filelistdir/$idata.files
		outputfile=$outputdir/$idata.root
		echo "Launching Processing $idata"
		echo "Logs are saved here $logfile"
		echo "Input file is $inputfile"
		echo "Output is saved here $outputfile"
		$exec --input=$inputfile --output=$outputfile --isMC=0 > $logfile &
	done
fi

#	process MC 74X and 76X
if [ $runMC -eq 1 ];
then
	echo "-----------------"
	echo "Starting MC Processing"
	echo "-----------------"
	for imc in `seq 0 3`;
	do
		mc=${mc_instances_to_process[$imc]}
		mcpu=${mc_pileup[$imc]}
		for idatapu in `seq 0 1 2`;
		do
			datapu=${data_pileup[$idatapu]}
			desc=${description[$idatapu]}
			logfile=$logdir/${mc}_${desc}.log
			inputfile=$filelistdir/$mc.files
			outputfile="$outputdir/${mc}_${desc}.root"
	
			echo "Launching Processing for $mc with PU $mcpu w.r.t. PU $datapu"
			echo "Logs are saved here $logfile"
			echo "Outputs will be saved here $outputfile"
			$exec --input=$inputfile --output=$outputfile --isMC=1 --puMC=$pileupdir/$mcpu --puDATA=$pileupdir/$datapu > $logfile &
		done
	done
fi
