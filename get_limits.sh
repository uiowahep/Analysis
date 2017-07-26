label=limits_test_comb_split_c7_c8_24_7_17
jobLabel=limits_test_comb_split_c7_c8_24_7_2017comb

cd Modeling/combine
python generate_postcombine.py --mode UF_AMC --what plotLimits --workspacesDirName $label --outDirName $jobLabel --massPoints 120 125 130 --signalModel TripleGaus
cd -
