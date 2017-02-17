
#
# all the standard variable names
#
varNames = [
    "DiJetMass", "DiJetdeta", "DiMuonpt", "DiMuonMass",
    "DiMuoneta", "DiMuondphi", "Muonpt", "Muoneta", "Muonphi"
]

#
# Run 1 Categories list
#
run1Categories = [
    "NoCats", "2Jets", "01Jets", "VBFTight", "ggFTight",
    "ggFLoose", "01JetsTight", "01JetsTightBB", "01JetsTightBO",
    "01JetsTightBE", "01JetsTightOO", "01JetsTightOE", "01JetsTightEE",
    "01JetsLoose", "01JetsLooseBB", "01JetsLooseBO", "01JetsLooseBE",
    "01JetsLooseOO", "01JetsLooseOE", "01JetsLooseEE"
]

#
# Run 2 Categories list
#
run2Categories = run1Categories[:]
run2Categories.extend(
    [
        "1bJets", "1bJets4l", "1bJets4l2Mu2e", "1bJets4l3Mu1e", "1bJets4l4Mu",
        "1bJets3l", "1bJets2l", "0bJets", "0bJets4l", "0bJets4l2Mu1e", "0bJets4l3Mu0e",
        "0bJets4l3Mu1e", "0bJets4l4Mu0e", "0bJets4l2Mu2e", 
    ]
)
varNames = ["DiJetMass", "DiJetdeta", "DiMuonpt", "DiMuonMass",
    "DiMuoneta", "DiMuondphi", "Muonpt", "Muoneta", "Muonphi"]

allVariablesRun1 = []
dimuonMassVariablesRun1 = []
for v in varNames:
    for c in run1Categories:
        mymin = -0.999; mymax = -0.999
        if c!="NoCats" and v=="DiMuonMass":
            mymin = 110; mymax = 160
        allVariablesRun1.append(
            {
                "name":v, "min":mymin, "max":mymax,
                "category":c, "fullpath": "%s/%s" % (c, v)
            }
        )
        if v=="DiMuonMass":
            dimuonMassVariablesRun1.append(
                {
                    "name":v, "min":mymin, "max":mymax,
                    "category":c, "fullpath": "%s/%s" % (c, v)
                }
            )
allVariablesRun2 = []
dimuonMassVariablesRun2 = []
for v in varNames:
    for c in run2Categories:
        mymin = -0.999; mymax = -0.999
        if c!="NoCats" and v=="DiMuonMass":
            mymin = 110; mymax = 160
        allVariablesRun2.append(
            {
                "name":v, "min":mymin, "max":mymax,
                "category":c, "fullpath": "%s/%s" % (c, v)
            }
        )
        if v=="DiMuonMass":
            dimuonMassVariablesRun2.append(
                {
                    "name":v, "min":mymin, "max":mymax,
                    "category":c, "fullpath": "%s/%s" % (c, v)
                }
            )
