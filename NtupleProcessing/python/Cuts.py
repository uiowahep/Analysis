"""
List of Cut variables
"""

cut_ranges = {
    "muonPt" : [x for x in range(0, 50)],
    "muonEta" : [float(x)*0.01 for x in range(100, 310, 10)]
}

cuts = {
    "muonMatchedPt" : 22.,
    "muonMatchedEta" : 2.4,
    "muonPt" : 10.,
    "muonEta" : 2.4,
    "muonIso" : 0.1,
    "leadJetPt" : 40.,
    "subleadJetPt" : 30.,
    "metPt" : 40.,
    "dijetMass_VBFTight" : 650.,
    "dijetdEta_VBFTight" : 3.5,
    "dijetMass_ggFTight" : 250,
    "dimuonPt_ggFTight" : 50,
    "dimuonPt_01JetsTight" : 10,
}

import copy
def buildCutList():
    l = []
    c = copy.copy(cuts)

def buildCutValue(cut):
    cut = float(cut)
    name = "%.1f" % cut
    return name.replace(".", "p")

def buildcmdString(ccuts):
    s = ""
    for k in ccuts.keys():
        s+="  --{%s}=%.1f" % (k, ccuts[k])
    return s

def buildFolderName(ccuts):
    name = "muonMatchedPt{muonMatchedPt}__muonMatchedEta{muonMatchedEta}__muonPt{muonPt}__muonEta{muonEta}__muonIso{muonIso}__leadJetPt{leadJetPt}__subleadJetPt{subleadJetPt}__metPt{metPt}__dijetMass_VBFTight{dijetMass_VBFTight}__dijetdEta_VBFTight{dijetdEta_VBFTight}__dijetMass_ggFTight{dijetMass_ggFTight}__dimuonPt_ggFTight{dimuonPt_ggFTight}__dimuonPt_01JetsTight{dimuonPt_01JetsTight}".format(**ccuts)
    return name

if __name__=="__main__":
    s = buildFolderName(cuts)
    print s
    print len(s)
    print buildcmdString(cuts)
