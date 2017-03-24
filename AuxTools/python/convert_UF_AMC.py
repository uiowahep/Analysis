
import subprocess, argparse
import ROOT as R
import AuxTools.python.common as CM

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose debugging output')
parser.add_argument('-m', '--mode', type=str, default='Iowa', help='Run in Iowa, UF_AWB, or UF_AMC mode')
args = parser.parse_args()

if (args.mode == 'Iowa'):
    import AuxTools.python.Iowa_settings as SET
if (args.mode == 'UF_AWB'):
    import AuxTools.python.UF_AWB_settings as SET
if (args.mode == 'UF_AMC'):
    import AuxTools.python.UF_AMC_settings as SET

in_file = R.TFile(SET.orig_file)
in_file.ls()
signalsDir = in_file.GetDirectory(SET.orig_sig_dir)
mapPP2ListOfCats = {} ## What is this? - AWB 23.02.17

out_path = SET.in_hist_dir
in_to_out_category_map = SET.in_to_out_category_map
CM.mkdir(out_path)

## Conversion between UF and Iowa label format ("UF" : "Iowa")
signalPPConversion = {
    "gg" : "GluGlu_HToMuMu_M125_13TeV_powheg_pythia8",
    "VBF" : "VBF_HToMuMu_M125_13TeV_powheg_pythia8",
    "ZH" : "ZH_HToMuMu_M125_13TeV_powheg_pythia8",
    "WH_pos" : "WPlusH_HToMuMu_M125_13TeV_powheg_pythia8",
    "WH_neg" : "WMinusH_HToMuMu_M125_13TeV_powheg_pythia8"
}


#print in_to_out_category_map
#
# Signals
#
for key in signalsDir.GetListOfKeys():
    out_category_name = 'UNKNOWN'
    hist = key.ReadObj()
    name = hist.GetName()
    in_category_name = name.split("_H2Mu_")[0]
    in_signal_name = name.split("_H2Mu_")[1]
    fullpp = signalPPConversion[in_signal_name]

    if in_category_name in in_to_out_category_map:
        out_category_name = in_to_out_category_map[in_category_name]
    else:
        continue

    if fullpp in mapPP2ListOfCats:
        mapPP2ListOfCats[fullpp].append((out_category_name, hist))
    else:
        mapPP2ListOfCats[fullpp] = [(out_category_name,hist)]

#    print "%s, %s, %s" % (in_category_name, out_category_name, in_signal_name)
if (args.verbose): print mapPP2ListOfCats

for pp in mapPP2ListOfCats:
    if 'UF' in args.mode:
        resultFile = R.TFile(out_path+"/%s.root" % pp, "RECREATE")
    else:
        cert = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON"
        resultFile = R.TFile(out_path+"/result__%s__80X__cert__69mb__Mu24.root" % (pp, cert), "RECREATE")
    print 'Created file %s.root' % pp
    for category,hist in mapPP2ListOfCats[pp]:
        resultFile.mkdir(category)
        resultFile.cd(category)
        hist.SetName("DiMuonMass")
        hist.Write()
        resultFile.cd("..")
    resultFile.Close()

#
# Data
# 
mapRun2ListOfCats = {}
dataDir = in_file.GetDirectory("data_histos")
for key in dataDir.GetListOfKeys():
    category = 'UNKNOWN'
    hist = key.ReadObj()
    name = hist.GetName()
    run = name[-4:]
    in_category = name[:-5]


    if in_category in in_to_out_category_map:
        category = in_to_out_category_map[in_category]
    else:
        continue

#    print "%s, %s" % (run, in_category)

    if (args.verbose): print category
    if run in mapRun2ListOfCats:
        mapRun2ListOfCats[run].append((category, hist))
    else:
        mapRun2ListOfCats[run] = [(category, hist)]

if (args.verbose): print mapRun2ListOfCats

if 'UF' in args.mode:
    hadd_str = 'hadd -f %s/MergedData.root' % out_path
else:
    cert = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON"
    hadd_str = 'hadd -f %s/result__merged__80X__%s__69mb__Mu24.root' % (out_path, cert)

for run in mapRun2ListOfCats:
    if 'UF' in args.mode:
        resultFile = R.TFile(out_path+"/%s.root" % run, "RECREATE")
    else:
        cert = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON"
        resultFile = R.TFile(out_path+"/result__%s__80X__%s__69mb__Mu24.root" % (pp, cert), "RECREATE")
    print 'Created data file %s.root' % run
    for category,hist in mapRun2ListOfCats[run]:
        resultFile.mkdir(category)
        resultFile.cd(category)
        hist.SetName("DiMuonMass")
        hist.Write()
        resultFile.cd("..")
    resultFile.Close()

    if 'UF' in args.mode:
        hadd_str +=' %s/%s.root' % (out_path, run)
    else:
        cert = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON"
        hadd_str += " %s/result__%s__80X__%s__69mb__Mu24.root" % (out_path, pp, cert)
        
if (args.verbose): print hadd_str
subprocess.call('%s' % hadd_str, shell=True)
