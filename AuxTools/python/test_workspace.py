
import sys
from ROOT import *
filename = sys.argv[1]
wsname = sys.argv[2]
f = TFile(filename)
w = f.Get(wsname)
w.Print("v")
