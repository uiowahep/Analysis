"""
Representation of a Datacard for Higgs Combination
"""
class Datacard:
    def __init__(self, signals, bkg, uncs):
        self.signals = signals
        self.bkg = self.bkg
        self.uncs = uncs

    def __str__(self):
        return self.generate()

    def __repr__(self):
        return self.generate()

    def generateUncertaintiesSection(self):
        pass
        
    def generateModelsSection(self):
        pass

    def generateHeaderSection(self):
        return """
        # Datacard
        imax 1
        jmax {jmax}
        kmax *
        {delimiter}
        shapes * * {rootFile} {workspace}:$PROCESS
        {delimiter}
        bin {category}
        observation -1
        {delimiter}
        """

if __name__=="__main__":
    d = Datacard()
    print d
