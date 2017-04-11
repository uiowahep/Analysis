
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

#
# Category Representations
#
run1CatReps = ["cat%d" % i for i in range(len(run1Categories))]
run1Reps2Names = {}
run1Names2Reps = {}
for i in range(len(run1CatReps)):
    run1Reps2Names[run1CatReps[i]] = run1Categories[i]
    run1Names2Reps[run1Categories[i]] = run1CatReps[i]

#
# Combinations for Run1
# combinations are named already so that you can use them directly
# NOTE: run1CategoriesForCombination is used rather than run1Categories!
#
run1Combinations = {
    "comb2Jets" : [
        run1Names2Reps["VBFTight"], 
        run1Names2Reps["ggFLoose"], 
        run1Names2Reps["ggFTight"]],
    "comb01Jets" : [
        run1Names2Reps["01JetsLooseBB"], 
        run1Names2Reps["01JetsLooseBE"], 
        run1Names2Reps["01JetsLooseBO"],
        run1Names2Reps["01JetsLooseEE"], 
        run1Names2Reps["01JetsLooseOE"], 
        run1Names2Reps["01JetsLooseOO"],
        run1Names2Reps["01JetsTightBB"], 
        run1Names2Reps["01JetsTightBE"], 
        run1Names2Reps["01JetsTightBO"],
        run1Names2Reps["01JetsTightEE"], 
        run1Names2Reps["01JetsTightOE"], 
        run1Names2Reps["01JetsTightOO"]],
    "comb2JetsggF" : [
        run1Names2Reps["ggFLoose"], 
        run1Names2Reps["ggFTight"]],
    "comb01JetsTightB" : [
        run1Names2Reps["01JetsTightBB"], 
        run1Names2Reps["01JetsTightBO"], 
        run1Names2Reps["01JetsTightBE"]],
    "comb01JetsTightO" : [
        run1Names2Reps["01JetsTightOO"], 
        run1Names2Reps["01JetsTightOE"], 
        run1Names2Reps["01JetsTightEE"]],
    "comb01JetsLoose" : [
        run1Names2Reps["01JetsLooseBB"], 
        run1Names2Reps["01JetsLooseBE"], 
        run1Names2Reps["01JetsLooseBO"],
        run1Names2Reps["01JetsLooseEE"], 
        run1Names2Reps["01JetsLooseOE"], 
        run1Names2Reps["01JetsLooseOO"]],
}
run1Combinations["combTotal"] = run1Combinations["comb01Jets"] + run1Combinations["comb2Jets"]
run1Combinations["combNoVBFTight"] = run1Combinations["comb2JetsggF"] + run1Combinations["comb01Jets"]
