#!/usr/bin/python

class Dataset(object):
    def __init__(self, *kargs, **wargs):
        """
        name - dataset name as in CMS DAS
        label - shorthand name for this DataSet
        isData - if this is a data or MC
        """
        if len(kargs)>0: 
            Dataset.startup(self, kargs[0])
            return

        object.__init__(self)
        self.name = wargs["name"]
        self.isData = wargs["isData"]
        if 'label' not in wargs.keys():
            self.label = self.name[1:].replace("/", "__")
        else:
            self.label = wargs["label"]
        if "uflabel" not in wargs.keys():
            self.uflabel = ""
        else:
            self.uflabel = wargs["uflabel"]
        if "ufPlotLabel" not in wargs.keys():
            self.ufPlotLabel = ""
        else:
            self.ufPlotLabel = wargs["ufPlotLabel"]
        if "plotLabel" not in wargs.keys():
            self.plotLabel = ""
        else:
            self.plotLabel = wargs["plotLabel"]
        self.year = wargs["year"]
        self.globaltag = wargs["globaltag"]
        if 'test_file' not in wargs.keys():
            self.test_file = self.label+".files"
        else:
            self.test_file = wargs["test_file"]

    def startup(self, other):
        object.__init__(self)
        self.name = other.name
        self.label = other.label
        self.isData = other.isData
        self.year = other.year
        self.test_file = other.test_file
        self.globaltag = other.globaltag
        self.uflabel = other.uflabel
        self.ufPlotLabel = other.ufPlotLabel
        self.plotLabel = other.plotLabel

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = "-"*80 + "\n" +\
            "Dataset:" + "\n" +\
            ">>> name="+self.name+"\n" +\
            ">>> label="+self.label+"\n" +\
            ">>> isData="+str(self.isData)+"\n" +\
            ">>> year="+str(self.year)+"\n"+\
            ">>> globaltag="+str(self.globaltag)+"\n"+\
            ">>> test_file="+str(self.test_file)+"\n"+\
            "-"*80 +\
            "\n"
        return s

class MCDataset(Dataset):
    def __init__(self, *kargs, **wargs):
        if len(kargs)>0: 
            MCDataset.startup(self, kargs[0])
            return

        Dataset.__init__(self, **wargs)
        if "isSignal" not in wargs.keys():
            self.isSignal = None
        else:
            self.isSignal = wargs["isSignal"]
        if "initial_cmssw" not in wargs.keys():
            self.initial_cmssw = None
        else:
            self.initial_cmssw = wargs["initial_cmssw"]

        if "cross_section" not in wargs.keys():
            self.cross_section = None
        else:
            self.cross_section = wargs["cross_section"]

    def __str__(self):
        s = "-"*80 + "\n" +\
            "MCDataset:" + "\n" +\
            ">>> name="+self.name+"\n" +\
            ">>> label="+self.label+"\n" +\
            ">>> isData="+str(self.isData)+"\n" +\
            ">>> year="+str(self.year)+"\n"+\
            ">>> test_file="+str(self.test_file)+"\n"+\
            ">>> isSignal="+str(self.isSignal)+"\n"+\
            ">>> initial_cmssw="+str(self.initial_cmssw)+"\n"+\
            "-"*80 +\
            "\n"
        return s
    def __repr__(self):
        return self.__str__()

    def startup(self, other):
        Dataset.__init__(self, other)
        if hasattr(other, "isSignal"):
            self.isSignal = other.isSignal
        else:
            self.isSignal = None
        if hasattr(other, "initial_cmssw"):
            self.initial_cmssw = other.initial_cmssw
        else:
            self.initial_cmssw = None
        if hasattr(other, "cross_section"):
            self.cross_section=other.cross_section
        else:
            self.cross_section=None

    def buildProcessName(self):
        return self.name.split("/")[1].split("_")[0]

class Ntuple(MCDataset):
    """
    Data/MC Ntuple - the output of CMSSW Ntuple Making
    Location of Ntuples:
    rootpath<storagebased>/DATA.jsontag/label/timestamp/counter/files.root
    rootpath<storagebased>/MC.cmssw/label/timestamp/counter/files.root
    """
    def __init__(self, *kargs, **wargs):
        if len(kargs)>0: 
            Ntuple.startup(self, kargs[0], **wargs)
            return

        MCDataset.__init__(self, **wargs)
        self.json = wargs["json"]
        self.cmssw = wargs["cmssw"]

        self.timestamp = wargs["timestamp"]
        self.storage = wargs["storage"]
        self.rootpath = wargs["rootpath"]

        if "aux" not in wargs.keys():
            self.aux=None
        else:
            self.aux = wargs["aux"]

    def __str__(self):
        s = "-"*80 + "\n" +\
            "Ntuple:" + "\n" +\
            ">>> name="+self.name+"\n" +\
            ">>> label="+self.label+"\n" +\
            ">>> isData="+str(self.isData)+"\n" +\
            ">>> year="+str(self.year)+"\n"+\
            ">>> test_file="+str(self.test_file)+"\n"+\
            ">>> isSignal="+str(self.isSignal)+"\n"+\
            ">>> initial_cmssw="+str(self.initial_cmssw)+"\n"+\
            ">>> globaltag="+str(self.globaltag)+"\n"+\
            ">>> json="+str(self.json)+"\n"+\
            ">>> cmssw="+str(self.cmssw)+"\n"+\
            ">>> timestamp="+str(self.timestamp)+"\n"+\
            ">>> storage="+str(self.storage)+"\n"+\
            ">>> rootpath="+str(self.rootpath)+"\n"+\
            "-"*80 +\
            "\n"
        return s
    
    def __repr__(self):
        return self.__str__()

    def startup(self, otherds, **wargs):
        MCDataset.__init__(self, otherds)
        self.json = wargs["json"]
        self.cmssw = wargs["cmssw"]

        self.timestamp = wargs["timestamp"]
        self.storage = wargs["storage"]
        self.rootpath = wargs["rootpath"]
        if "aux" not in wargs.keys():
            self.aux=None
        else:
            self.aux = wargs["aux"]

class DataResult(Ntuple):
    """
    Data Result of Data Ntuple Processing
    """
    def __init__(self, *kargs, **wargs):
        if len(kargs)>0: 
            DataResult.startup(self, kargs[0], **wargs)
            return
        Ntuple.__init__(self, **wargs)
        self.filelist = wargs["filelist"]

    def startup(self, other, **wargs):
        Ntuple.__init__(self, other,
            json = other.json,
            cmssw = other.cmssw,
            timestamp = other.timestamp,
            storage=other.storage,
            rootpath=other.rootpath,
            aux=other.aux
        )
        self.filelist = wargs["filelist"]

class JsonFile(object):
    """
    Represents our Json files
    """
    def __init__(self, **wargs):
        object.__init__(self)
        self.filename = wargs["filename"]
        self.intlumi = wargs["intlumi"]
        self.url = None
        if "url" in wargs:
            self.url = wargs["url"]

    def __str__(self):
        s = "-"*80 + "\n" +\
            "JsonFile:" + "\n" +\
            ">>> filename="+str(self.filename)+"\n"+\
            ">>> intlumi="+str(self.intlumi)+"\n"+\
            ">>> url="+str(self.url)+"\n"+\
            "-"*80 +\
            "\n"
        return s

    def __repr__(self):
        return self.__str__()

class MCResult(DataResult):
    """
    MC Result of MC Ntuple Processing
    """
    def __init__(self, *kargs, **wargs):
        if len(kargs)>0: 
            MCResult.startup(self, kargs[0], **wargs)
            return
        DataResult.__init__(self, **wargs)
        self.pileupdata = wargs["pileupdata"]
    def startup(self, other, **wargs):
        DataResult.__init__(self, other, **wargs)
        self.pileupdata = wargs["pileupdata"]

class PileUp(object):
    """
    """
    def __init__(self, **wargs):
        object.__init__(self)
        self.cross_section = wargs["cross_section"]
        self.datajson = wargs["datajson"]

    def __str__(self):
        s = "-"*80 + "\n" + \
            "PileUp: " + "\n" + \
            ">>> cross_section="+self.cross_section + "\n" + \
            ">>> datajson="+self.datajson + "\n" + \
            "-"*80 + \
            "\n"
        return s
    def __repr__(self):
        return self.__str__()

if __name__=="__main__":
    ds = Dataset(name="/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD",
        isData=True, globaltag = "gt",
        year=2015, test_file="/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD")
    ntuple = Ntuple(ds, globaltag="test", cmssw="test", json="test", timestamp="",
        storage="test", rootpath="test")
    print ds
    print "/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD".replace("/", ".")[1:]
    print ntuple
