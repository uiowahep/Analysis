import ROOT as R

x = R.RooRealVar("x", "x", -10, 10)
mean = R.RooRealVar("mean", "mean", 0, -10, 10)
sigma = R.RooRealVar("sigma", "sigma", 3, -10, 10)

gauss = R.RooGaussian("gauss", "gauss", x, mean, sigma)
xframe = x.frame()
gauss.plotOn(xframe)
xframe.Draw()
