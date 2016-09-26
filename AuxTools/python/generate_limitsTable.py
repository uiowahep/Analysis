import ROOT as R
import os, sys, glob, json
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
py.sign_in('username', 'api_key')

def skipCategories(d):
    newd = {}
    for key in d.keys():
        nkey = key
#        if "Jets" in key:
#            nkey = nkey.replace("Jets", "J")
#        if "Jet" in key:
#            nkey = nkey.replace("Jet", "J")
#        if "Tight" in key:
#            nkey = nkey.replace("Tight", "T") 
#        if "Loose" in key:
#            nkey = nkey.replace("Loose", "L")
        if "Combination" in key:
  #          nkey = nkey.replace("Combination", "C")
            newd[nkey] = d[key]

    return newd

def main():
    template_limits = "/Users/vk/software/Analysis/files/limits_higsscombined_results/v0p6_20160824_1100/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22"
    analytic_limits = "/Users/vk/software/Analysis/files/limits_higsscombined_results/v0p5_20160824_1100/76X__Cert_271036-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T__Mu22"
    template_pattern = "explimits__templates*.json"
    analytic_pattern = "explimits__analytic*.json"

    alldata = {"templates": {}, "analytic" : {}}
    for pu in ["68", "69", "70", "71", "71p3", "72"]:
        files_template = glob.glob(os.path.join(template_limits, pu, template_pattern))
        files_analytic = glob.glob(os.path.join(analytic_limits, pu, analytic_pattern))
        print files_template
        print files_analytic
        alldata["analytic"][pu] = {}; alldata["templates"][pu] = {}
        for f in files_template:
            print "Processing Template file %s" % f
            s = f[:-5].split("/")[-1].split("__")
            mass = s[-1]
            alldata["templates"][pu] = skipCategories(json.load(open(f)))
        for f in files_analytic:
            s = f.split("/")[-1][:-5].split("__")
            bmodel = s[3]
            smode = s[4]
            smodel = s[5]
            if not smodel in alldata["analytic"][pu].keys(): 
                alldata["analytic"][pu][smodel] = {}
                alldata["analytic"][pu][smodel][smode] = skipCategories(json.load(open(f)))
            else:
                alldata["analytic"][pu][smodel][smode] = skipCategories(json.load(open(f)))
    print "-"*40
    print alldata
    generate_Table(alldata=alldata)

def generate_Table(**wargs):
    d = wargs["alldata"]
    data = []
    categories = None
    for t in d.keys():
        if t=="analytic":
            for pu in d[t].keys():
                for smodel in d[t][pu].keys():
                    for smode in d[t][pu][smodel].keys():
                        d[t][pu][smodel][smode]["PU"] = pu
                        d[t][pu][smodel][smode]["SMODE"] = smode
                        d[t][pu][smodel][smode]["SMODEL"] = smodel
                        data.append(d[t][pu][smodel][smode])
        else:
            for pu in d[t].keys():
                d[t][pu]["PU"] = pu
                data.append(d[t][pu])


    import tabulate
    table_latex = tabulate.tabulate(data, headers="keys", tablefmt="latex", floatfmt=".2f")
    f = open("test.tex", "w")
    f.write(table_latex)
    table_plain = tabulate.tabulate(data, headers="keys", tablefmt="fancy_grid", floatfmt=".2f")
    print table_plain

if __name__=="__main__":
    main()
