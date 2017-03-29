
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
    "ggFLoose", "01JetsTightBB", "01JetsTightBO",
    "01JetsTightBE", "01JetsTightOO", "01JetsTightOE", "01JetsTightEE",
    "01JetsLooseBB", "01JetsLooseBO", "01JetsLooseBE",
    "01JetsLooseOO", "01JetsLooseOE", "01JetsLooseEE", 
]

run1CategoriesForCombination = [
    "VBFTight", "ggFTight",
    "ggFLoose", "01JetsTightBB", "01JetsTightBO",
    "01JetsTightBE", "01JetsTightOO", "01JetsTightOE", "01JetsTightEE",
    "01JetsLooseBB", "01JetsLooseBO", "01JetsLooseBE",
    "01JetsLooseOO", "01JetsLooseOE", "01JetsLooseEE", 
]

combinationsRun1 = {
    "2JetsComb" : ["VBFTight", "ggFLoose", "ggFTight"],
    "01JetsComb" : ["01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
        "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO",
        "01JetsTightBB", "01JetsTightBE", "01JetsTightBO",
        "01JetsTightEE", "01JetsTightOE", "01JetsTightOO"],
    "Combination" : run1CategoriesForCombination,
    "2JetsggF" : ["ggFLoose", "ggFTight"],
    "01JetsTightBarrel" : ["01JetsTightBB", "01JetsTightBO", "01JetsTightBE"],
    "01JetsTightOther" : ["01JetsTightOO", "01JetsTightOE", "01JetsTightEE"],
    "01JetsLoose" : ["01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
        "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO"],
}
combinationsRun1["CombNoVBFTight"] = combinationsRun1["2JetsggF"] + combinationsRun1["01JetsComb"]

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
