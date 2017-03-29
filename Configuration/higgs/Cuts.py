"""
List of Cut variables
"""

cuts = {
    "muonMatchedPt" : 24.,
    "muonMatchedEta" : 2.4,
    "leadmuonPt" : 10.,
    "subleadmuonPt" : 10.,
    "leadmuonEta" : 2.4,
    "subleadmuonEta" : 2.4,
    "leadmuonIso" : 0.1,
    "subleadmuonIso" : 0.1,
    "leadJetPt" : 40.,
    "subleadJetPt" : 30.,
    "metPt" : 40.,
    "dijetMass_VBFTight" : 650.,
    "dijetdEta_VBFTight" : 3.5,
    "dijetMass_ggFTight" : 250,
    "dimuonPt_ggFTight" : 50,
    "dimuonPt_01JetsTight" : 10,
}

def generate_cutsets():
    l = []
    for leadmuonPt in range(0, 50, 5):
        for subleadmuonPt in range(0, 50, 5):
            c = cuts.copy()
            c["leadmuonPt"] = leadmuonPt
            c["subleadmuonPt"] = subleadmuonPt
            l.append(c)  
    return l

def generate_cutsets1():
    l = []
    cutnames = {
        "leadmuonPt" : range(0, 100, 2), "subleadmuonPt" : range(0, 100, 2),
        "leadmuonIso" : [x*0.01 for x in range(6, 16, 2)],
        "subleadmuonIso" : [x*0.01 for x in range(6, 16, 2)],
        "leadmuonEta" : [x*0.1 for x in range(0, 30, 1)],
        "subleadmuonEta" : [x*0.1 for x in range(0, 30, 1)]
    }
    for key in cutnames.keys():
        for cut in cutnames[key]:
            c = cuts.copy()
            c[key] = cut
            l.append(c)
    return l


#cuts_shortcuts = {}
#counter = 0
#for key in cuts:
#    cuts_shortcuts[key] = "%dc" % counter
#    counter+=1

cuts_shortcuts = {
    "muonMatchedPt" : "mmp",
    "muonMatchedEta" : "mme",
    "leadmuonPt" : "lmp",
    "subleadmuonPt" : "slmp",
    "leadmuonEta" : "lme",
    "subleadmuonEta" : "slme",
    "leadmuonIso" : "lmi",
    "subleadmuonIso" : "slmi",
    "leadJetPt" : "ljp",
    "subleadJetPt" : "sljp",
    "metPt" : "mp",
    "dijetMass_VBFTight" : "djmv",
    "dijetdEta_VBFTight" : "djev",
    "dijetMass_ggFTight" : "djmg",
    "dimuonPt_ggFTight" : "dmpg",
    "dimuonPt_01JetsTight" : "dmp0j"
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
        s+="  --%s=%.1f" % (k, ccuts[k])
    return s

def buildFolderName(ccuts):
    name = ""
    for key in ccuts.keys():
        if name=="":
            name += "%s{%s}" % (cuts_shortcuts[key], key)
        else:
            name += "__%s{%s}" % (cuts_shortcuts[key], key)
    return name.format(**ccuts)
#    name = "muonMatchedPt{muonMatchedPt}__muonMatchedEta{muonMatchedEta}__muonPt{muonPt}__muonEta{muonEta}__muonIso{muonIso}__leadJetPt{leadJetPt}__subleadJetPt{subleadJetPt}__metPt{metPt}__dijetMass_VBFTight{dijetMass_VBFTight}__dijetdEta_VBFTight{dijetdEta_VBFTight}__dijetMass_ggFTight{dijetMass_ggFTight}__dimuonPt_ggFTight{dimuonPt_ggFTight}__dimuonPt_01JetsTight{dimuonPt_01JetsTight}".format(**ccuts)
    return name

if __name__=="__main__":
    s = buildFolderName(cuts)
    print s
    print len(s)
    print buildcmdString(cuts)
