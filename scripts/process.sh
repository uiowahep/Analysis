#!/bin/bash

runData=$1
runMC=$2

exec=../process_2016MCPrompt
filelistdir=$ANALYSIS/files/filelist
outputdir=$ANALYSIS/files/results/dimuon-v3
pileupdir=$ANALYSIS/files/pileup

#data_instances_to_process=("data2015Prompt data2015ReReco data2016Prompt_v1 data2016Prompt_v2")
data_instances_to_process=("data2015Prompt data2015ReReco data2016Prompt_v1")
mc_instances_to_process=(mc_dy_jetsToLL_74X mc_ttJets_74X mc_dy_jetsToLL_76X mc_ttJets_76X mc_gg_HToMuMu_74X mc_gg_HToMuMu_76X mc_vbf_HToMuMu_74X mc_vbf_HToMuMu_76X)

mc_pileup=(pileup_dy_jetsToLL_74X2015.root pileup_ttJets_74X2015.root pileup_dy_jetsToLL_76X2015.root pileup_ttJets_76X2015.root pileup_ggHtoMuMu_74X.root pileup_ggHtoMuMu_76X.root pileup_vbfHToMuMu_74X.root pileup_vbfHToMuMu_76X.root)

#data_pileup=("$pileupdir/pileup_data2015Prompt_69mb.root $pileupdir/pileup_data2015ReReco_69mb.root $pileupdir/pileup_data2016Prompt_71p3mb.root $pileupdir/pileup_data2016Prompt_v2_71p3mb.root")
data_pileup=("$pileupdir/pileup_data2015Prompt_69mb.root $pileupdir/pileup_data2015ReReco_69mb.root $pileupdir/pileup_data2016Prompt_71p3mb.root")
#data_pileup=`ls ${pileupdir}/pileup_data*${PUnum}mb.root`

#	create a dir with logs
logdir=../logs
label=_wCats
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
		outputfile=$outputdir/${idata}${label}.root
		echo ""
		echo "-----------------"
		echo ""
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
	for imc in `seq 0 7`;
	do
		mc=${mc_instances_to_process[$imc]}
		mcpu=${mc_pileup[$imc]}
		for idatapu in ${data_pileup};
		do
			desc=${idatapu%.root}
			desc=${desc##*/pileup_}
			logfile=$logdir/${mc}_${desc}.log
			inputfile=$filelistdir/$mc.files
			outputfile=$outputdir/${mc}_${desc}${label}.root

			echo ""
			echo "-----------------"
			echo ""
			echo "Launching Processing for $mc with PU $mcpu w.r.t. PU $idatapu"
			echo "Logs are saved here $logfile"
			echo "Outputs will be saved here $outputfile"
			echo "Processing Description here $desc"
			$exec --input=$inputfile --output=$outputfile --isMC=1 --puMC=$pileupdir/$mcpu --puDATA=$idatapu > $logfile &
		done
	done
fi
