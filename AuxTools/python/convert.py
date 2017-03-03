
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
CM.mkdir(out_path)

## Conversion between UF and Iowa label format ("UF" : "Iowa")
signalPPConversion = {
    "_gg" : "GluGlu_HToMuMu_M125_13TeV_powheg_pythia8",
    "_VBF" : "VBF_HToMuMu_M125_13TeV_powheg_pythia8",
    "_ZH" : "ZH_HToMuMu_M125_13TeV_powheg_pythia8",
    "_WH_pos" : "WPlusH_HToMuMu_M125_13TeV_powheg_pythia8",
    "_WH_neg" : "WMinusH_HToMuMu_M125_13TeV_powheg_pythia8"
}


def determineCategory(ccc):
    if len(ccc)==1:
        if ccc[0]=="ALL":
            category = "NoCats"
        else:
            category = "UNKNOWN"
            raise
    elif len(ccc)==2:
        if ccc[0]=="01":
            category = "01Jets"
        elif ccc[0]=="2":
            category = "2Jets"
        else:
            category = "UNKNOWN"
            raise
    elif len(ccc)==3:
        if ccc[0]=="01":
            if ccc[2]=="Loose":
                category = "01JetsLoose"
            elif ccc[2]=="Tight":
                category = "01JetsTight"
            else:
                category = "UNKNOWN"
                raise
        elif ccc[0]=="2":
            if ccc[2]=="Loose":
                category = "2JetsLoose"
            elif ccc[2]=="Tight":
                category = "2JetsTight"
            else:
                category = "UNKNOWN"
                raise
        else:
            category = "UNKNOWN"
            raise
    elif len(ccc)==4:
        if ccc[0]=="01":
            category = ccc[0]+ccc[1]+"s"+ccc[2]+ccc[3]
        elif ccc[0]=="2":
            if ccc[2]=="GGF":
                category = "ggFTight"
            elif ccc[2]=="VBF":
                if ccc[3]=="Tight":
                    category = "VBFTight"
                elif ccc[3]=="Loose":
                    category = "ggFLoose"
            else:
                category = "UNKNOWN"
                raise
    else:
        category = "UNKNOWN"
        raise

    return category

#
# Signals
#
for key in signalsDir.GetListOfKeys():
    hist = key.ReadObj()
    name = hist.GetName()
    first = name.split("H2Mu")[0]
    second = name.split("H2Mu")[1]
    fullpp = signalPPConversion[second]

    ccc = first.split("_")[1:-1]
    if len(ccc)==1:
        if ccc[0]=="ALL":
            category = "NoCats"
        else:
            category = "UNKNOWN"
            raise
    elif len(ccc)==2:
        if ccc[0]=="01":
            category = "01Jets"
        elif ccc[0]=="2":
            category = "2Jets"
        else:
            category = "UNKNOWN"
            raise
    elif len(ccc)==3:
        if ccc[0]=="01":
            if ccc[2]=="Loose":
                category = "01JetsLoose"
            elif ccc[2]=="Tight":
                category = "01JetsTight"
            else:
                category = "UNKNOWN"
                raise
    elif len(ccc)==4:
        if ccc[0]=="01":
            category = ccc[0]+ccc[1]+"s"+ccc[2]+ccc[3]
        elif ccc[0]=="2":
            if ccc[2]=="GGF":
                category = "ggFTight"
            elif ccc[2]=="VBF":
                if ccc[3]=="Tight":
                    category = "VBFTight"
                elif ccc[3]=="Loose":
                    category = "ggFLoose"
            else:
                category = "UNKNOWN"
    else:
        category = "UNKNOWN"
        raise
    if fullpp in mapPP2ListOfCats:
        mapPP2ListOfCats[fullpp].append((category, hist))
    else:
        mapPP2ListOfCats[fullpp] = [(category,hist)]
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
    hist = key.ReadObj()
    name = hist.GetName()
    run = name[-4:]
    rest = name[:-5].split("_")[1:]
    category = determineCategory(rest)
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
