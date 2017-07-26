label=bias_c7_c8_comb_split_study_25_7_2017
jobLabel=bias_scan_c7_c8_comb_split_study_25_7_2017

python Modeling/combine/generate_postcombine.py --mode UF_AMC --what biasScan --workspacesDirName $label --outDirName $jobLabel --massPoints 125 --signalModel TripleGaus
