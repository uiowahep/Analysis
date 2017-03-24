import AuxTools.python.UF_AMC_settings as SET
from itertools import izip

varNames = ["DiMuonMass"]

#
# Run 1 Categories list
#

## Full list of categories
run1Categories = SET.out_category_names

## list of categories to make datacards and workspaces for
run1CategoriesForCombination = SET.out_category_names

## sets of combined limits to produce
#clist = SET.out_category_names[:]
#combinationsRun1 = dict(izip(SET.out_category_names, clist))
#combinationsRun1["Combination"] = run1CategoriesForCombination

combinationsRun1 = {
    "Combination" : run1CategoriesForCombination
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
