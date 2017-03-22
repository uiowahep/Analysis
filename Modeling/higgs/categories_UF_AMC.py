
#
# all the standard variable names
#

# varNames = [
#     "DiJetMass", "DiJetdeta", "DiMuonpt", "DiMuonMass",
#     "DiMuoneta", "DiMuondphi", "Muonpt", "Muoneta", "Muonphi"
# ]
varNames = ["DiMuonMass"]

#
# Run 1 Categories list
#

# ## Small test sample
# run1Categories = ["01JetsTightBB", "01JetsLooseBB", "01JetsTightEE"]
# run1CategoriesForCombination = run1Categories
# combinationsRun1 = { "Combination" : run1CategoriesForCombination }


## Full list of categories
run1Categories = [
    # "NoCats", "2Jets", "01Jets", "VBFTight", "ggFTight",
    "VBFTight", "ggFTight", "ggFLoose", 
    "01JetsTightBB", "01JetsTightBO", "01JetsTightBE", 
    "01JetsTightOO", "01JetsTightOE", "01JetsTightEE",
    "01JetsLooseBB", "01JetsLooseBO", "01JetsLooseBE",
    "01JetsLooseOO", "01JetsLooseOE", "01JetsLooseEE"
    ]

run1CategoriesForCombination = [
    "VBFTight", "ggFTight", "ggFLoose", 
    "01JetsTightBB", "01JetsTightBO", "01JetsTightBE", 
    "01JetsTightOO", "01JetsTightOE", "01JetsTightEE",
    "01JetsLooseBB", "01JetsLooseBO", "01JetsLooseBE",
    "01JetsLooseOO", "01JetsLooseOE", "01JetsLooseEE",
    ]

combinationsRun1 = {
    "2JetsComb"  : ["VBFTight", "ggFLoose", "ggFTight"],
    "01JetsTightCentral" : ["01JetsTightBB", "01JetsTightBO", "01JetsTightOO"],
    "01JetsTightForward" : ["01JetsTightBE", "01JetsTightOE", "01JetsTightEE"],
    "01JetsLoose" : ["01JetsLooseBB", "01JetsLooseBE", "01JetsLooseBO",
                     "01JetsLooseEE", "01JetsLooseOE", "01JetsLooseOO"],
    "Combination" : run1CategoriesForCombination,
    }


#
# Run 2 Categories list
#
run2Categories = run1Categories[:]


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
