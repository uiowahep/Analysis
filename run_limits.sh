label=test_28_9_2017
jobLabel=test_28_9_2017
hdir=$PWD

#///////////////////////////////////////////////////////////////////////////////////////////
################ FIT SIG AND BKG AND MAKE DATACARDS ########################################
cd Modeling/higgs2/
python generate.py --mode UF_AMC --outDirName $label --what datacardsTripleGaus --withSystematics

#///////////////////////////////////////////////////////////////////////////////////////////
################ GRID AND COPY IMAGES TO CHECK SIG AND BKG FITS ###########################

cd /afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/limits_and_bias/backgroundfitswithroomultipdf/AMC/$label
rm *grid*.png
montage -tile 3x4 -geometry +2+2 backgroundFits__*__bkgModels.png bkg-grid.png
cp *grid* $hdir/imgs/


cd /afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/limits_and_bias/signalfitinterpolationswithspline/AMC/$label
rm *grid*.png

montage -tile 3x4 -geometry +2+2 signalFit__*125*GluGlu*.png GluGlu-125-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*125*VBF*.png VBF-125-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*125*ZH*.png ZH-125-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*125*WPlusH*.png WplusH-125-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*125*WMinusH*.png WMinusH-125-grid.png

montage -tile 3x4 -geometry +2+2 signalFit__*120*GluGlu*.png GluGlu-120-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*120*VBF*.png VBF-120-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*120*ZH*.png ZH-120-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*120*WPlusH*.png WplusH-120-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*120*WMinusH*.png WMinusH-120-grid.png

montage -tile 3x4 -geometry +2+2 signalFit__*130*GluGlu*.png GluGlu-130-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*130*VBF*.png VBF-130-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*130*ZH*.png ZH-130-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*130*WPlusH*.png WplusH-130-grid.png
montage -tile 3x4 -geometry +2+2 signalFit__*130*WMinusH*.png WMinusH-130-grid.png

montage -tile 3x4 -geometry +2+2 signalFitInterpolation*GluGlu*.png GluGlu-igrid.png
montage -tile 3x4 -geometry +2+2 signalFitInterpolation*VBF*.png VBF-igrid.png
montage -tile 3x4 -geometry +2+2 signalFitInterpolation*ZH*.png ZH-igrid.png
montage -tile 3x4 -geometry +2+2 signalFitInterpolation*WPlusH*.png WplusH-igrid.png
montage -tile 3x4 -geometry +2+2 signalFitInterpolation*WMinusH*.png WMinusH-igrid.png

cp *grid* $hdir/imgs/
cd $hdir

cd /afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/limits_and_bias/ftest/AMC/$label/
rm *grid*.png
montage -tile 3x4 -geometry +2+2 ftest*.png ftest-grid.png
cp *grid* $hdir/imgs/
cd $hdir

#///////////////////////////////////////////////////////////////////////////////////////////
################ COMBINE DATACARDS #########################################################

cd Modeling/combine/
python generate_precombine.py --mode UF_AMC --what combineCards --inDirName $label --signalModel TripleGaus
python generate_precombine.py --mode UF_AMC --what text2workspace --inDirName $label --signalModel TripleGaus
#
## --categoriesToSkip cat0
#

#///////////////////////////////////////////////////////////////////////////////////////////
################ SUBMIT JOBS FOR LIMITS ####################################################

#python generate_precombine.py --mode UF_AMC --what categories --inDirName $label --outDirName ${jobLabel} --method Asymptotic --massPoints 120 125 130 --signalModel TripleGaus --splitLevel 1 --queue 8nh
#python generate_precombine.py --mode UF_AMC --what combinations --inDirName $label --outDirName ${jobLabel} --method Asymptotic --massPoints 120 125 130 --signalModel TripleGaus --splitLevel 1 --queue 8nh
#cd -
#cd /afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/limits_and_bias/combinesubmissions/AMC/${jobLabel}/
#./submit_categories_Asymptotic_TripleGaus.sh  ## Submit limits for categories to the queue
#./submit_combinations_Asymptotic_TripleGaus.sh  ## Submit limits for combinations to the queue
#cd -
