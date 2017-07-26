label=bias_c7_c8_comb_split_study_25_7_2017
jobLabel=bias_scan_c7_c8_comb_split_study_25_7_2017
ntoys=4000
allShapes=0

#cd Modeling/higgs2/
#python generate.py --mode UF_AMC --outDirName $label --what datacardsTripleGaus
#cd -
cd Modeling/combine/
#python generate_precombine.py --mode UF_AMC --what combineCards --inDirName $label --signalModel TripleGaus
#python generate_precombine.py --mode UF_AMC --what text2workspace --inDirName $label --signalModel TripleGaus
python generate_precombine.py --mode UF_AMC --what biasScan --inDirName $label --outDirName $jobLabel --massPoints 125 --signalModel TripleGaus --splitLevel 1 --saveAllShapes $allShapes --nToys $ntoys --queue 8nh
cd /afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/limits_and_bias/combinesubmissions/AMC/$jobLabel/
./submit_biasScan_TripleGaus.sh  ## Submit to the queue
cd -
