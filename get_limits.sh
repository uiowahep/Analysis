label=limits_res_mass_sb1_16cat_16_8_2017
jobLabel=limits_job_res_mass_sb1_16cat_16_8_2017

cd Modeling/combine
python generate_postcombine.py --mode UF_AMC --what plotLimits --workspacesDirName $label --outDirName $jobLabel --massPoints 120 125 130 --signalModel TripleGaus
cd -
