import ROOT as R
import sys, os

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--pathToFileJES", type=str, default="/", help="full path to the ROOT file with histos")
parser.add_argument("--pathToFileTHEORY", type=str, default="/", help="full path to the ROOT file with histos")
parser.add_argument("--pathToOutput", type=str, default="/", help="full path to the ROOT file with histos")
args = parser.parse_args()

def write2csv(out, *kargs):
    for systematics in kargs:
        for uncname in systematics:
            out.write("\n\n\n")
            for category in systematics[uncname]:
                out.write("\n")
                for pp in systematics[uncname][category]:
                    out.write("{uncname},{category},{pp},{down},{up}\n".format(
                        uncname = uncname,
                        category = category,
                        pp = pp,
                        down = "{0:.3f}".format(systematics[uncname][category][pp][0]),
                        up = "{0:.3f}".format(systematics[uncname][category][pp][1])))

def convertAndrea2csv():
    fjes = R.TFile(args.pathToFileJES)
    ftheory = R.TFile(args.pathToFileTHEORY)
    rootPath = "HmumuAnalysis/Vars"
    varName = "Mmm"
    categories = ["cat%d" % i for i in range(13)]
    signals = ["GluGlu", "VBF", "WPlusH", "WMinusH", "ZH"]
    mass = 125
    auxstring = "HToMuMu"
    uncertainties_JES = ["BTAGB", "BTAGL", "JER", "JES", "PU"]
    uncertainties_JES_cms = {"BTAGB" : "cms_eff_b", "BTAGL" : "cms_fake_b", 
        "JER" : "cms_res_j", "JES" : "cms_scale_j", "PU" : "cms_pu"}
    uncertainties_pdf = ["Pdf%d" % i for i in range(100)]
    uncertainties_scale = ["ScaleFDown", "ScaleFUp", "ScaleRDown", "ScaleRFDown", "ScaleRFUp", "ScaleRUp"]

    uncs = {}
    for unc in uncertainties_JES:
        uncs[uncertainties_JES_cms[unc]] = {}
        for category in categories:
            uncs[uncertainties_JES_cms[unc]][category] = {}
            for signal in signals:
                h = fjes.Get(rootPath + "/" + "Mmm_{category}_{signal}_{auxstring}_M{mass}".format(category=category, signal=signal, auxstring=auxstring, mass=mass))
                hup = fjes.Get(rootPath + "/" + "Mmm_{category}_{signal}_{auxstring}_M{mass}_{unc}Up".format(category=category, signal=signal, auxstring=auxstring, mass=mass, unc=unc))
                hdown = fjes.Get(rootPath + "/" + "Mmm_{category}_{signal}_{auxstring}_M{mass}_{unc}Down".format(category=category, signal=signal, auxstring=auxstring, mass=mass, unc=unc))
                left = hdown.Integral()/h.Integral()
                right = hup.Integral()/h.Integral()
                print left,right
                uncs[uncertainties_JES_cms[unc]][category][signal] = (left, right)

    print uncs

    uncspdf = {"cms_pdf" : {} }
    for category in categories:
        uncspdf["cms_pdf"][category] = {}
        for signal in signals:
            l = []
            for unc in uncertainties_pdf:
                hpdf = ftheory.Get(rootPath + "/" + "Mmm_{category}_{signal}_{auxstring}_M{mass}_{pdf}".format(category=category, signal=signal, auxstring=auxstring, mass=mass, pdf=unc))
                h = ftheory.Get(rootPath + "/" + "Mmm_{category}_{signal}_{auxstring}_M{mass}".format(category=category, signal=signal, auxstring=auxstring, mass=mass, pdf=unc))
                ratio = hpdf.Integral()/h.Integral()
                l.append(ratio)
            print max(l),min(l)
            uncspdf["cms_pdf"][category][signal] = (min(l), max(l))

    uncsscale = {"cms_scale" : {} }
    for category in categories:
        uncsscale["cms_scale"][category] = {}
        for signal in signals:
            l = []
            for unc in uncertainties_scale:
                hpdf = ftheory.Get(rootPath + "/" + "Mmm_{category}_{signal}_{auxstring}_M{mass}_{pdf}".format(category=category, signal=signal, auxstring=auxstring, mass=mass, pdf=unc))
                h = ftheory.Get(rootPath + "/" + "Mmm_{category}_{signal}_{auxstring}_M{mass}".format(category=category, signal=signal, auxstring=auxstring, mass=mass, pdf=unc))
                ratio = hpdf.Integral()/h.Integral()
                l.append(ratio)
            print max(l),min(l)
            uncsscale["cms_scale"][category][signal] = (min(l), max(l))

    f = open(args.pathToOutput, "w")
    write2csv(f, uncs, uncspdf, uncsscale)
    f.close()
            
def main():
    convertAndrea2csv()

if __name__=="__main__":
    main()
