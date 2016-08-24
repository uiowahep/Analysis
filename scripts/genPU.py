import ROOT as R
import sys

def genPU():
    if "ANALYSISHOME" not in os.environ.keys():
        raise NameError("Can not find ANALYSISHOME env var")
    sys.path.append(os.environ["ANALYSISHOME"])
    sys.path.append(os.path.join(os.environ["ANALYSISHOME"], "NtupleProcessing/python"))
    import NtupleProcessing.python.Samples as S
    import NtupleProcessing.python.Dataset as DS

    print "input = " + inputFileName
    print "output = " + outFileName

    R.gSystem.Load("../libAnalysisCore.dylib")
    R.gSystem.Load("../libAnalysisNtupleProcessing.dylib")

    s = R.analysis.processing.Streamer(inputFileName,
        "ntuplemaker_H2DiMuonMaker/Events")
    s.chainup()

    aux = R.analysis.core.EventAuxiliary()
    s._chain.SetBranchAddress("EventAuxiliary", aux)

    out = R.TFile(outFileName, "recreate")
    h = R.TH1D("pileup", "pileup", 50, 0, 50)

    numEvents = s._chain.GetEntries()
    for i in range(numEvents):
        s._chain.GetEntry(i)
        if i%10000==0:
            print "Processing Event %d / %d" % (i, numEvents)
        h.Fill(aux._nPU, aux._genWeight)

    out.Write()
    out.Close()

if __name__=="__main__":
    genPU()
