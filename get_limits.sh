label=limits_test_multipdf_26_7_17
jobLabel=limits_test_multipdf_26_7_2017

cd Modeling/combine
python generate_postcombine.py --mode UF_AMC --what plotLimits --workspacesDirName $label --outDirName $jobLabel --massPoints 120 125 130 --signalModel TripleGaus
cd -
