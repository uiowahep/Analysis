import ROOT as R
import sys

def genPU():
    if (len(sys.argv)<3):
        print "Usage: python2.7 genPU.py <input.files> out.root"
        sys.exit(1)
    inputFileName = sys.argv[1]
    outFileName = sys.argv[2]

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
