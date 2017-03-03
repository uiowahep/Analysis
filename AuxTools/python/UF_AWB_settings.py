
###########################
###  General settings  ###
###########################
job_label = 'AWB_Mar03_test'
UF_era    = 'Moriond17_Feb08'
JSON      = 'Moriond17_Feb08.txt'
analytic  = True

#######################
###   Data to use   ###
#######################
cmssws  = ['80X']
pileups = ['69']

signals = [ 'GluGlu_HToMuMu_M125_13TeV_powheg_pythia8',
            'VBF_HToMuMu_M125_13TeV_powheg_pythia8',
            'WMinusH_HToMuMu_M125_13TeV_powheg_pythia8',
            'WPlusH_HToMuMu_M125_13TeV_powheg_pythia8',
            'ZH_HToMuMu_M125_13TeV_powheg_pythia8' ]

backgrounds = []


######################################################
###   Settings for AuxTools/python/convert_UF.py   ###
######################################################
orig_file    = '/afs/cern.ch/work/a/acarnes/public/h2mumu/rootfiles/validate_UNBLINDED_dimu_mass_PF_110_160_nolow_run1categories_36814.root'
orig_sig_dir = 'signal_histos'

############################################################################
###   Settings for Modeling/higgs/generate_signalFitsPlusWorkspaces.py   ###
############################################################################
in_hist_dir    = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/input_hists/%s/%s' % (UF_era, job_label) 
workspaces_dir = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/workspaces/%s/%s' % (UF_era, job_label)
sig_fits_dir   = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/sig_fits/%s/%s' % (UF_era, job_label)

scale_MC     = False
sig_models   = ["DoubleGaus"]
# bkg_models   = ["ExpGaus", "Polynomial", "Bernstein"]
bkg_models   = ["ExpGaus"]
sig_modes    = ["Separate"]
aux_params   = { "Polynomial" : {"degree" : 5},
                 "ExpGaus" : {},
                 "Bernstein" : {"degree": 5} }
sig_M = [125, 115, 135, 118, 130]

#####################################################################
###   Settings for Modeling/higgs/generate_bkgDataWorkspaces.py   ###
#####################################################################
bkg_fits_dir = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/bkg_fits/%s/%s' % (UF_era, job_label)
bkg_M = [ 91, 110, 160, 110, 160]

#############################################################
###   Settings for Modeling/higgs/generate_datacards.py   ###
#############################################################
datacards_dir = '/afs/cern.ch/work/a/abrinke1/public/H2Mu/Limits/datacards/%s/%s' % (UF_era, job_label)
