label=limits_test_multipdf_26_7_17
jobLabel=limits_test_multipdf_26_7_2017

cd Modeling/higgs2/
python generate.py --mode UF_AMC --outDirName $label --what datacardsTripleGaus --withSystematics
cd -
cd Modeling/combine/
python generate_precombine.py --mode UF_AMC --what combineCards --inDirName $label --signalModel TripleGaus
python generate_precombine.py --mode UF_AMC --what text2workspace --inDirName $label --signalModel TripleGaus

# --categoriesToSkip cat0

python generate_precombine.py --mode UF_AMC --what categories --inDirName $label --outDirName ${jobLabel} --method Asymptotic --massPoints 120 125 130 --signalModel TripleGaus --splitLevel 1 --queue 8nh
python generate_precombine.py --mode UF_AMC --what combinations --inDirName $label --outDirName ${jobLabel} --method Asymptotic --massPoints 120 125 130 --signalModel TripleGaus --splitLevel 1 --queue 8nh
cd -
cd /afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/limits_and_bias/combinesubmissions/AMC/${jobLabel}/
./submit_categories_Asymptotic_TripleGaus.sh  ## Submit limits for categories to the queue
./submit_combinations_Asymptotic_TripleGaus.sh  ## Submit limits for combinations to the queue
cd -
