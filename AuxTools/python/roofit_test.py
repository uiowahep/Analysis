import ROOT as R

mes = R.RooRealVar("mes", "m_{ES} (GeV)", 5.20, 5.30)

sigmean = R.RooRealVar("sigmean", "sigmean", 5.28, 5.20, 5.30)
sigwidth = R.RooRealVar("sigwidth", "sigwidth", 0.0027, 0.001, 1.)
gauss = R.RooGaussian("gauss", "gauss", mes, sigmean, sigwidth)

argpar = R.RooRealVar("argpar", "argpar", -20., -100, -1)
argus = R.RooArgusBG("argus", "argus", mes, R.RooFit.RooConst(5.291), argpar)

nsig = R.RooRealVar("nsig", "nsig", 200, 0, 10000)
nbkg = R.RooRealVar("nbkg", "nbkg", 800, 0, 10000)
pdfsum = R.RooAddPdf("pdfsum", "pdfsum", R.RooArgList(gauss, argus), 
    R.RooArgList(nsig, nbkg))

data = pdfsum.generate(R.RooArgSet(mes), 2000)
pdfsum.fitTo(data, R.RooFit.Extended())

mesframe = mes.frame()
data.plotOn(mesframe)
pdfsum.plotOn(mesframe)
#pdfsum.plotOn(mesframe, R.RooFit.Components(argus), R.RooFit.LineStyle(R.kDashed))
mesframe.Draw()
