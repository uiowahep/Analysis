import ROOT as R
import sys

from pyspark import SparkContext
from pyspark.mllib.linalg import Vectors

def genPU():
    inputFileName = sys.argv[1]

    print "input = " + inputFileName

    R.gSystem.Load("../libAnalysisCore.dylib")
    R.gSystem.Load("../libAnalysisNtupleProcessing.dylib")
    sc = SparkContext("local", "Test Spark")

    s = R.analysis.processing.Streamer(inputFileName,
        "ntuplemaker_H2DiMuonMaker/Events")
    s.chainup()

    aux = R.analysis.core.EventAuxiliary()
    muons1 = R.analysis.core.Muons()
    muons2 = R.analysis.core.Muons()
    jets = R.analysis.core.Jets()
    s._chain.SetBranchAddress("EventAuxiliary", aux)
    s._chain.SetBranchAddress("Muons1", muons1)
    s._chain.SetBranchAddress("Muons2", muons2)
    s._chain.SetBranchAddress("Jets", jets)

    numEvents = s._chain.GetEntries()
    for i in range(numEvents):
        s._chain.GetEntry(i)
        print "SiZE = %d" % muons.size()
        if i%10000==0:
            print "Processing Event %d / %d" % (i, numEvents)
#        h.Fill(aux._nPU, aux._genWeight)

if __name__=="__main__":
    genPU()
