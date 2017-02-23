#!/usr/bin/python

class Uncertainty:
    def __init__(self, name, uncType, valuesMap, exceptions=None): 
        self.name = name
        self.uncType = uncType
        self.valuesMap = valuesMap
        #
        #   exceptions come in the form of:
        #   {"category":Uncertainty}
        #   the idea is that if there is an exception for that category,
        #   you explicitly list it.
        #   otherwise this uncertainty is applied to all categories
        #
        self.exceptions = exceptions

def buildNameTypeVector(uncs):
    names = []; types = []
    for unc in uncs:
        names.append(unc.name)
        types.append(unc.uncType)
    return names,types

# list all the uncertainties
uncertainties_vR1 = [
    Uncertainty("Lumi", "lnN",
        {"GluGlu" : 1.062, "VBF" : 1.062, "WMinusH" : 1.062, "WPlusH" : 1.062, "ZH" : 1.062}),
    Uncertainty("PU", "lnN",
        {"GluGlu" : 1.052, "VBF" : 1.052, "WMinusH" : 1.052, "WPlusH" : 1.052, "ZH" : 1.052}),

    #
    # HLT
    #
    Uncertainty("SingleIsoMu", "lnN",
        {"GluGlu" : 1.05, "VBF" : 1.05, "WMinusH" : 1.05, "WPlusH" : 1.05, "ZH" : 1.05}),
    Uncertainty("MomentumScale", "lnN",
        {"GluGlu" : 1.002, "VBF" : 1.002, "WMinusH" : 1.002, "WPlusH" : 1.002, "ZH" : 1.002}),
    Uncertainty("MomentumResolution", "lnN",
        {"GluGlu" : 1.02, "VBF" : 1.02, "WMinusH" : 1.02, "WPlusH" : 1.02, "ZH" : 1.02}),
    Uncertainty("MuonIDIso", "lnN",
        {"GluGlu" : 1.02, "VBF" : 1.02, "WMinusH" : 1.02, "WPlusH" : 1.02, "ZH" : 1.02}),
    Uncertainty("ElectronIDIso", "lnN",
        {"GluGlu" : 1.02, "VBF" : 1.02, "WMinusH" : 1.02, "WPlusH" : 1.02, "ZH" : 1.02}),

    #
    # b-tag
    #
#    Uncertainty("bTagging", "lnN", 
#        {"GluGlu" : 1.03, "VBF" : 1.03, "WMinusH" : 1.03, "WPlusH" : 1.03, "ZH" : 1.03}),

    #
    # For Jets
    # 
    Uncertainty("JetPUID", "lnN",
        {"GluGlu" : 1.04, "VBF" : 1.04, "WMinusH" : 1.04, "WPlusH" : 1.04, "ZH" : 1.04}),
    Uncertainty("JetJEC", "lnN",
        {"GluGlu" : 1.08, "VBF" : 1.08, "WMinusH" : 1.08, "WPlusH" : 1.08, "ZH" : 1.08}),
    Uncertainty("JetJER", "lnN",
        {"GluGlu" : 1.03, "VBF" : 1.03, "WMinusH" : 1.03, "WPlusH" : 1.03, "ZH" : 1.03}),
    Uncertainty("MCStats", "lnN",
        {"GluGlu" : 1.02, "VBF" : 1.02, "WMinusH" : 1.02, "WPlusH" : 1.02, "ZH" : 1.02}),
    #
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV2014
    #
    Uncertainty("PDF", "lnN",
        {"GluGlu" : 1.071, "VBF" : 1.032, "WMinusH" : 1.022, "WPlusH" : 1.022, "ZH" : 1.022}),
    Uncertainty("ScaleVariation", "lnN",
        {"GluGlu" : 1.075, "VBF" : 1.007, "WMinusH" : 1.01, "WPlusH" : 1.01, "ZH" : 1.038}),

    # 
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR2014
    #
    Uncertainty("BFHmumu", "lnN",
        {"GluGlu" : 1.06, "VBF" : 1.06, "WMinusH" : 1.06, "WPlusH" : 1.06, "ZH" : 1.06}),
]

uncertainties_vR2 = uncertainties_vR1[:]
uncertainties_vR2.extend([
    Uncertainty("bTagging", "lnN", 
        {"GluGlu" : 1.03, "VBF" : 1.03, "WMinusH" : 1.03, "WPlusH" : 1.03, "ZH" : 1.03}),
])
