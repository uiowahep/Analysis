from itertools import izip
import ROOT as R

###########################
###  General settings  ###
###########################
job_label = 'AMC_Mar14_test_v1'
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

# combined limit of ~2.21
#orig_filename = 'validate_UNBLINDED_dimu_mass_PF_110_160_nolow_categories1_36814_dyMG.root'

# combined limit of ~ 2.00
#orig_filename = 'validate_UNBLINDED_dimu_mass_PF_110_160_nolow_categories3_tree_nodes16_minbkg200_36814_dyMG.root'        # !!!
#orig_filename = 'validate_UNBLINDED_dimu_mass_PF_110_160_nolow_categories3_tree_nodes16_minbkg100_scale1_36814_dyMG.root' # !!!
#orig_filename = 'validate_UNBLINDED_dimu_mass_PF_110_160_nolow_categories3_tree_nodes16_minbkg50_scale1_36814_dyMG.root'  # !!!

# combined limit of ~ 2.03
#orig_filename = 'validate_UNBLINDED_dimu_mass_PF_110_160_nolow_categories3_tree_nodes16_minbkg500_36814_dyMG.root'        # !!!
#orig_filename = 'validate_UNBLINDED_dimu_mass_PF_110_160_nolow_categories3_tree_nodes16_minbkg500_scale1_36814_dyMG.root'
#orig_filename = 'validate_UNBLINDED_dimu_mass_PF_110_160_nolow_categories3_tree_nodes16_minbkg200_scale1_36814_dyMG.root'
#orig_filename = 'validate_UNBLINDED_dimu_mass_PF_110_160_nolow_categories3_tree_nodes16_minbkg100_36814_dyMG.root'
#orig_filename = 'validate_UNBLINDED_dimu_mass_PF_110_160_nolow_categories3_tree_nodes16_minbkg50_36814_dyMG.root'

orig_file    = '/afs/cern.ch/work/a/acarnes/public/h2mumu/rootfiles/%s' % orig_filename
orig_sig_dir = 'signal_histos'

#####################################################
###   Categories                                  ###
#####################################################

in_category_names = []
out_category_names = []

in_file = R.TFile(orig_file)
stacks_dir = in_file.GetDirectory("stacks")

i = 0
for key in stacks_dir.GetListOfKeys():
    name = key.GetName()
    name = name.replace("_stack", "")
    if name == "c_ALL" or name == "c_01_Jet" or name == "c_2_Jet" or name == "c_01_Jet_Tight" or name == "c_01_Jet_Loose": 
        continue
    if "T_" != name[0:2] and "tree" in orig_filename:
        continue
    if "tree" in orig_filename:
        out_category_names.append("c" + str(i))
        i+=1
    in_category_names.append(name)

if "tree" not in orig_filename: 
    out_category_names = in_category_names

in_to_out_category_map = dict(izip(in_category_names, out_category_names))

#print in_category_names
#print ""
#print out_category_names
#print ""
#print in_to_out_category_map

############################################################################
###   Settings for Modeling/higgs/generate_signalFitsPlusWorkspaces.py   ###
############################################################################
in_hist_dir    = '/afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/input_hists/%s/%s' % (UF_era, job_label) 
workspaces_dir = '/afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/workspaces_datacards/%s/%s' % (UF_era, job_label)
sig_fits_dir   = '/afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/sig_fits/%s/%s' % (UF_era, job_label)

scale_MC     = False
sig_models   = ["DoubleGaus"]
#sig_models   = ["SingleGaus", "DoubleGaus", "TripleGaus"]
sig_modes    = ["Separate"]
#sig_modes    = ["Combined"]

bkg_models = [
    {"name" : "BWZRedux", "aux" : {}} 
    #{"name" : "BWZGamma", "aux" : {}},
    #{"name" : "SumExponentials", "aux" : {"degree" : 1}},
    #{"name" : "SumExponentials", "aux" : {"degree" : 2}},
    #{"name" : "SumExponentials", "aux" : {"degree" : 3}},
    #{"name" : "SumExponentials", "aux" : {"degree" : 4}},
    #{"name" : "SumPowers", "aux" : {"degree" : 2}},
    #{"name" : "SumPowers", "aux" : {"degree" : 3}},
    #{"name" : "SumPowers", "aux" : {"degree" : 4}},
    #{"name" : "SumPowers", "aux" : {"degree" : 5}},
    #{"name" : "SumPowers", "aux" : {"degree" : 6}},
    #{"name" : "LaurentSeries", "aux" : {"degree" : 2}},
    #{"name" : "LaurentSeries", "aux" : {"degree" : 3}},
    #{"name" : "LaurentSeries", "aux" : {"degree" : 4}},
    #{"name" : "LaurentSeries", "aux" : {"degree" : 5}},
    #{"name" : "LaurentSeries", "aux" : {"degree" : 6}},
    #{"name" : "LaurentSeries", "aux" : {"degree" : 7}},

    #{"name" : "Polynomial", "aux" : {"degree" : 3}},
    #{"name" : "Polynomial", "aux" : {"degree" : 4}},
    #{"name" : "Polynomial", "aux" : {"degree" : 5}},
    #{"name" : "Polynomial", "aux" : {"degree" : 6}},
    #{"name" : "Polynomial", "aux" : {"degree" : 7}},
    #{"name" : "Polynomial", "aux" : {"degree" : 8}},
    #{"name" : "Polynomial", "aux" : {"degree" : 9}},
    #{"name" : "ExpGaus", "aux" : {}},
    #{"name" : "Bernstein", "aux" : {"degree" : 2}},
    #{"name" : "Bernstein", "aux" : {"degree" : 3}},
    #{"name" : "Bernstein", "aux" : {"degree" : 4}},
    #{"name" : "Bernstein", "aux" : {"degree" : 5}}
    #{"name" : "Bernstein", "aux" : {"degree" : 6}},
    #{"name" : "Bernstein", "aux" : {"degree" : 7}},
    #{"name" : "Bernstein", "aux" : {"degree" : 8}},
]


sig_M = [125, 110, 160, 112, 132]

#####################################################################
###   Settings for Modeling/higgs/generate_bkgDataWorkspaces.py   ###
#####################################################################
bkg_fits_dir = '/afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/bkg_fits/%s/%s' % (UF_era, job_label)
bkg_M = [ 91, 110, 160, 110, 160]

#############################################################
###   Settings for Modeling/higgs/generate_datacards.py   ###
#############################################################
#datacards_dir = '/afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/datacards/%s/%s' % (UF_era, job_label)
datacards_dir = workspaces_dir # workspaces and datacards needs to be in the same directory

#####################################################################
###   Settings for Modeling/Modeling/combine/generate_submit.py   ###
#####################################################################
combine_dir   = '/afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/combine_out/%s/%s' % (UF_era, job_label)
combine_sub   = '/afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/combine_sub/%s/%s' % (UF_era, job_label)
combine_cmssw = '/afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/combine/CMSSW_7_4_7/src'

##########################################################
###   Settings for Modeling/higgs/generate_limits.py   ###
##########################################################
limits_dir = '/afs/cern.ch/work/a/acarnes/public/h2mumu/limit_setting/out/limits/%s/%s' % (UF_era, job_label)
