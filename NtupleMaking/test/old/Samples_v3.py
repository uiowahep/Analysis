# root://xrootd-cms.infn.it/

#
#   Sample Representation
#   
class sample:
    def __init__(self, name="", dir="", files=[], numevents=0, globaltag="", jsonfiles=[], isData=False):
        self.name = name
        self.dir = dir     # DAS directory
        self.numevents = numevents
        self.files = files
        self.globaltag = globaltag
        self.jsonfiles = jsonfiles
        self.isData = isData

#
#   JSON files
#

# 25 ns
# The jsonfiles detail which luminosity sections during data taking were good
jsonlist25 = [
    'sample_file_lists/data/json/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_MuonPhys_v2.txt',
    'sample_file_lists/data/json/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt',
    'sample_file_lists/data/json/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_Silver_v2.txt',
    'sample_file_lists/data/json/Cert_271036-275125_13TeV_PromptReco_Collisions16_JSON.txt',
    'sample_file_lists/data/json/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt',
    'sample_file_lists/data/json/Cert_271036-276097_13TeV_PromptReco_Collisions16_JSON_NoL1T_v2.txt',
    "sample_file_lists/data/json/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt",
    "sample_file_lists/data/json/Cert_271036-277148_13TeV_PromptReco_Collisions16_JSON.txt"
] 

#
#   DATA Samples: Double Muon
#

doubleMuon = []

# 25 ns
doubleMuon_RunC25nsOct_MINIAOD = sample(
    name="doubleMuon_RunC25nsOct_MINIAOD", 
    dir="/DoubleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD", 
    files = open('sample_file_lists/data/doubleMuon_RunC25nsOct_MINIAOD.files').read().splitlines(),
    numevents=900626,
    globaltag = '74X_dataRun2_v4',
    jsonfiles = jsonlist25[:],
    isData = True
)

doubleMuon_RunDOct_v1_MINIAOD = sample(
    name="doubleMuon_RunDOct_v1_MINIAOD", 
    dir="/DoubleMuon/Run2015D-05Oct2015-v1/MINIAOD", 
    files = open('sample_file_lists/data/doubleMuon_RunDOct_v1_MINIAOD.files').read().splitlines(),
    numevents=19923262,
    globaltag = '74X_dataRun2_reMiniAOD_v0',
    jsonfiles = jsonlist25[:],
    isData = True
)

doubleMuon_RunDPrompt_v4_MINIAOD = sample(
    name="doubleMuon_RunDPrompt_v4_MINIAOD", 
    dir="/DoubleMuon/Run2015D-PromptReco-v4/MINIAOD", 
    files = open('sample_file_lists/data/doubleMuon_RunDPrompt_v4_MINIAOD.files').read().splitlines(),
    numevents=31538841,
    globaltag = '74X_dataRun2_Prompt_v4',
    jsonfiles = jsonlist25[:],
    isData = True
)

doubleMuon.append(doubleMuon_RunC25nsOct_MINIAOD)
doubleMuon.append(doubleMuon_RunDOct_v1_MINIAOD)
doubleMuon.append(doubleMuon_RunDPrompt_v4_MINIAOD)

#
#   DATA Samples: Single Muon
#   

singleMuon = []

# 25 ns
singleMuon_RunC25nsOct_MINIAOD = sample(
    name="singleMuon_RunC25nsOct_MINIAOD", 
    dir="/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD", 
    files = open('sample_file_lists/data/singleMuon_RunC25nsOct_MINIAOD.files').read().splitlines(),
    numevents=1341179,
    globaltag = '74X_dataRun2_v4',
    jsonfiles = jsonlist25[:],
    isData = True
)

singleMuon_RunDOct_v1_MINIAOD = sample(
    name="singleMuon_RunDOct_v1_MINIAOD", 
    dir="/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD", 
    files = open('sample_file_lists/data/singleMuon_RunDOct_v1_MINIAOD.files').read().splitlines(),
    numevents=31298328,
    globaltag = '74X_dataRun2_reMiniAOD_v0',
    jsonfiles = jsonlist25[:],
    isData = True
)

singleMuon_RunDPrompt_v4_MINIAOD = sample(
    name="singleMuon_RunDPrompt_v4_MINIAOD", 
    dir="/SingleMuon/Run2015D-PromptReco-v4/MINIAOD", 
    files = open('sample_file_lists/data/singleMuon_RunDPrompt_v4_MINIAOD.files').read().splitlines(),
    numevents=61066301,
    globaltag = '74X_dataRun2_Prompt_v4',
    jsonfiles = jsonlist25[:],
    isData = True
)

singleMuon_Run2015C25nsReReco_16Dec_MINIAOD = sample(
    name="singleMuon_Run2015C25nsReReco_16Dec_MINIAOD",
    dir="/SingleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD",
    files=open('sample_file_lists/data/singleMuon_Run2015C25nsReReco_16Dec_MINIAOD.files').read().splitlines(),
    numevents=1341179,
    globaltag = '76X_dataRun2_v15',
    jsonfiles=jsonlist25[:],
    isData=True
)

singleMuon_Run2015DReReco_16Dec_MINIAOD = sample(
    name="singleMuon_Run2015DReReco_16Dec_MINIAOD",
    dir="/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD",
    files=open('sample_file_lists/data/singleMuon_Run2015DReReco_16Dec_MINIAOD.files').read().splitlines(),
    numevents=91999861,
    globaltag="76X_dataRun2_v15",
    jsonfiles=jsonlist25[:],
    isData=True
)

singleMuon_Run2016B_PromptReco_v2_MINIAOD = sample(
	name = 'singleMuon_Run2016B_PromptReco_v2_MINIAOD',
	dir = "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
	files = open('sample_file_lists/data/singleMuon_Run2016B_PromptReco_v2_MINIAOD.files').read().splitlines(),
	numevents = 143011542,
	globaltag = '80X_dataRun2_Prompt_v9',
	jsonfiles = jsonlist25[:],
	isData=True
)

#   seems like none of the runs from this set are included in the json!
singleMuon_Run2016B_PromptReco_v1_MINIAOD = sample(
    name="singleMuon_Run2016B_PromptReco_v1_MINIAOD",
    dir="/SingleMuon/Run2016B-PromptReco-v1/MINIAOD",
    files=open('sample_file_lists/data/singleMuon_Run2016B_PromptReco_v1_MINIAOD.files').read().splitlines(),
    numevents = 2816842,
    globaltag= '80X_dataRun2_Prompt_v9',
    jsonfiles = jsonlist25[:],
    isData=True
)

singleMuon_Run2016C_PromptReco_v2_MINIAOD = sample(
    name = "singleMuon_Run2016C_PromptReco_v2_MINIAOD",
    dir = "/SingleMuon/Run2016C-PromptReco-v2/MINIAOD",
    files = open('sample_file_lists/data/singleMuon_Run2016C_PromptReco_v2_MINIAOD.files').read().splitlines(),
    numevents = 68492270,
    globaltag = '80X_dataRun2_Prompt_v9',
    jsonfiles = jsonlist25[:],
    isData = True
)

singleMuon_Run2016D_PromptReco_v2_MINIAOD = sample(
    name = "singleMuon_Run2016D_PromptReco_v2_MINIAOD",
    dir = "/SingleMuon/Run2016D-PromptReco-v2/MINIAOD",
    files = open('sample_file_lists/data/singleMuon_Run2016D_PromptReco_v2_MINIAOD.files').read().splitlines(),
    numevents = 98175265,
    globaltag = "80X_dataRun2_Prompt_v9",
    jsonfiles = jsonlist25[:],
    isData = True
)

singleMuon_Run2016E_PromptReco_v2_MINIAOD = sample(
    name = "singleMuon_Run2016E_PromptReco_v2_MINIAOD",
    dir = "/SingleMuon/Run2016E-PromptReco-v2/MINIAOD",
    files = open("sample_file_lists/data/singleMuon_Run2016E_PromptReco_v2_MINIAOD.files").read().splitlines(),
    numevents = 1111,
    jsonfiles = jsonlist25[:],
    isData = True
)

singleMuon.append(singleMuon_RunC25nsOct_MINIAOD)
singleMuon.append(singleMuon_RunDOct_v1_MINIAOD)
singleMuon.append(singleMuon_RunDPrompt_v4_MINIAOD)

singleMuon2015ReReco = []
singleMuon2015ReReco.append(singleMuon_Run2015C25nsReReco_16Dec_MINIAOD)
singleMuon2015ReReco.append(singleMuon_Run2015DReReco_16Dec_MINIAOD)

singleMuon2016 = []
singleMuon2016.append(singleMuon_Run2016B_PromptReco_v2_MINIAOD)
singleMuon2016.append(singleMuon_Run2016C_PromptReco_v2_MINIAOD)
singleMuon2016.append(singleMuon_Run2016D_PromptReco_v2_MINIAOD)
singleMuon2016.append(singleMuon_Run2016E_PromptReco_v2_MINIAOD)

# ----------------------------
#   MC Samples: Signal
# ----------------------------
signal2015_74X = []
signal2015_76X = []
signal2016_80X = []

background2015_74X = []
background2015_76X = []
background2016_80X = []


# ----------------------------
# GG Fusion
# ----------------------------
gg_HToMuMu = sample( 
    name="gg_HToMuMu", 
    dir="/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM", 
    files = open('sample_file_lists/signal/gg_HToMuMu.files').read().splitlines(),
    numevents=250000,
    globaltag = '74X_mcRun2_asymptotic_v2'
)

gg_HToMuMu_76X2015 = sample(
    name="gg_HToMuMu_76X2015",
    dir="/GluGlu_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
    files=open('sample_file_lists/signal/gg_HToMuMu_76X2015.files').read().splitlines(),
    numevents = 250000,
    globaltag="76X_mcRun2_asymptotic_v12"
)

signal2015_74X.append(gg_HToMuMu)
signal2015_76X.append(gg_HToMuMu_76X2015)

# ----------------------------
# VBF
# ----------------------------
vbf_HToMuMu = sample(
    name="vbf_HToMuMu", 
    dir="/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
    files = open('sample_file_lists/signal/vbf_HToMuMu.files').read().splitlines(),
    numevents=249200,
    globaltag = '74X_mcRun2_asymptotic_v2'
)

vbf_HToMuMu_76X2015 = sample(
    name="vbf_HToMuMu_76X2015",
    dir="/VBF_HToMuMu_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
    files=open("sample_file_lists/signal/vbf_HToMuMu_76X2015.files").read().splitlines(),
    numevents=249200,
    globaltag='76X_mcRun2_asymptotic_v12'
)

signal2015_74X.append(vbf_HToMuMu)
signal2015_76X.append(vbf_HToMuMu_76X2015)

# ----------------------------
# W/Z to Higgs
# No 2015 production sample yet
# Old samples
# ----------------------------
wh_zh_HToMuMu_PU40bx50 = sample(
    name="wh_zh_HToMuMu_PU40bx50", 
    dir="/WH_ZH_HToMuMu_M-125_13TeV_pythia6/Spring14miniaod-141029_PU40bx50_PLS170_V6AN2-v1/MINIAODSIM",
                                #files = open('sample_file_lists/signal/vbf_HToMuMu_PU20bx25.files').read().splitlines(),
                                numevents=100000,
                                globaltag = 'PLS170_V6AN2')

wh_zh_HToMuMu_PU20bx25 = sample(name="wh_zh_HToMuMu_PU20bx25", 
                                dir="/WH_ZH_HToMuMu_M-125_13TeV_pythia6/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM",
                                #files = open('sample_file_lists/signal/vbf_HToMuMu_PU20bx25.files').read().splitlines(),
                                numevents=100000,
                                globaltag = 'POSTLS170_V5')

# ----------------------------
#   MC Samples: Background
# ----------------------------

# ----------------------------
# DY
# ----------------------------

dy_ZToMuMu_asympt25 = sample(
    name="dy_ZToMuMu_asympt25", 
    dir="/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
    files = open('sample_file_lists/bg/dy_ZToMuMu_asympt25.files').read().splitlines(),
    numevents=2848076,
    globaltag = 'MCRUN2_74_V9'
)

dy_jetsToLL = sample(
    name="dy_jetsToLL", 
    dir="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
    files = open('sample_file_lists/bg/dy_jetsToLL.files').read().splitlines(),
    numevents=28747969,
    globaltag = '74X_mcRun2_asymptotic_v2'
);

dy_jetsToLL_76X2015 = sample(
    name="dy_jetsToLL_76X2015",
    dir="/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
    files=open("sample_file_lists/bg/dy_jetsToLL_76X2015.files"),
    numevents=28751199,
    globaltag="76X_mcRun2_asymptotic_v12"
)

#background.append(dy_ZToMuMu_asympt25)
background2015_74X.append(dy_jetsToLL)
background2015_76X.append(dy_jetsToLL_76X2015)

# ----------------------------
# ttbar Jets
# ----------------------------
ttJets = sample(
    name="ttJets", 
    dir="/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM",
    files = open('sample_file_lists/bg/ttJets.files').read().splitlines(),
    numevents=42784971,
    globaltag = '74X_mcRun2_asymptotic_v2'
)

ttJets_76X2015 = sample(
    name="ttJets_76X2015",
    dir = "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
#    dir="/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
    files=open("sample_file_lists/bg/ttJets_76X2015.files").read().splitlines(),
    numevents = 6102376,
    globaltag="76X_mcRun2_asymptotic_v12"
)

ttZToLLNuNu = sample(name="ttZToLLNuNu", 
                     dir="/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM",
                     files = open('sample_file_lists/bg/ttZToLLNuNu.files').read().splitlines(),
                     numevents=398000,
                     globaltag = '74X_mcRun2_asymptotic_v2')

background2015_74X.append(ttJets)
background2015_76X.append(ttJets_76X2015)

background2016_76X_ttjetsonly = []
background2016_76X_ttjetsonly.append(ttJets_76X2016)
#background.append(ttZToLLNuNu)

# DiBoson
# Haven't added all of the Diboson backgrounds. There are a ton of samples.
# 12.178 pb
WWTo2L2Nu = sample(name="WWTo2L2Nu", 
                   dir="/WWTo2L2Nu_13TeV-powheg/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
                   files = open('sample_file_lists/bg/WWTo2L2Nu.files').read().splitlines(),
                   numevents=1965200,
                   globaltag = '74X_mcRun2_asymptotic_v2')

# 5.595 pb
WZTo2L2Q = sample(name="WZTo2L2Q", 
                   dir="/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
                   files = open('sample_file_lists/bg/WZTo2L2Q.files').read().splitlines(),
                   numevents=31477411,
                   globaltag = '74X_mcRun2_asymptotic_v2')

# 4.42965 pb
WZTo3LNu = sample(name="WZTo3LNu", 
                   dir="/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
                   files = open('sample_file_lists/bg/WZTo3LNu.files').read().splitlines(),
                   numevents=1980800,
                   globaltag = '74X_mcRun2_asymptotic_v2')
# 3.22 pb
ZZTo2L2Q = sample(name="ZZTo2L2Q", 
                   dir="/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
                   files = open('sample_file_lists/bg/ZZTo2L2Q.files').read().splitlines(),
                   numevents=18790122,
                   globaltag = '74X_mcRun2_asymptotic_v2')

#background.append(WWTo2L2Nu)
#background.append(WZTo2L2Q)
#background.append(WZTo3LNu)
#background.append(ZZTo2L2Q)

# 1.256 pb
ZZTo4L = sample(name="ZZTo4L", 
                   dir="/ZZTo4L_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM",
                   files = open('sample_file_lists/bg/ZZTo4L.files').read().splitlines(),
                   numevents=6665004,
                   globaltag = '74X_mcRun2_asymptotic_v2')
# 0.564 pb
ZZTo2L2Nu = sample(name="ZZTo2L2Nu", 
                   dir="/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM",
                   files = open('sample_file_lists/bg/ZZTo2L2Nu.files').read().splitlines(),
                   numevents=8719200,
                   globaltag = '74X_mcRun2_asymptotic_v2')

#background.append(ZZTo4L)
#background.append(ZZTo2L2Nu)

# 0.003194 pb
GluGluToZZTo2mu2tau = sample(name="GluGluToZZTo2mu2tau", 
                   dir="/GluGluToZZTo2mu2tau_BackgroundOnly_13TeV_MCFM/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
                   files = open('sample_file_lists/bg/GluGluToZZTo2mu2tau.files').read().splitlines(),
                   numevents=650000,
                   globaltag = '74X_mcRun2_asymptotic_v2')

# 0.003194 pb
GluGluToZZTo2e2mu = sample(name="GluGluToZZTo2e2mu", 
                   dir="/GluGluToZZTo2e2mu_BackgroundOnly_13TeV_MCFM/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
                   files = open('sample_file_lists/bg/GluGluToZZTo2e2mu.files').read().splitlines(),
                   numevents= 648800,
                   globaltag = '74X_mcRun2_asymptotic_v2')

# 0.001586 pb
GluGluToZZTo4mu = sample(name="GluGluToZZTo4mu", 
                   dir="/GluGluToZZTo4mu_BackgroundOnly_13TeV_MCFM/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
                   files = open('sample_file_lists/bg/GluGluToZZTo4mu.files').read().splitlines(),
                   numevents= 339600,
                   globaltag = '74X_mcRun2_asymptotic_v2')

#background.append(GluGluToZZTo2mu2tau)
#background.append(GluGluToZZTo2e2mu)
#background.append(GluGluToZZTo4mu)


singleAndMC = []
singleAndMC.extend(singleMuon)
singleAndMC.extend(signal2015_74X)
singleAndMC.extend(background2015_74X)

MC2015_74X = []
MC2015_76X = []
MC2016_80X = []

MC2015_74X.extend(signal2015_74X)
MC2015_74X.extend(background2015_74X)

MC2015_76X.extend(signal2015_76X)
MC2015_76X.extend(background2015_76X)
