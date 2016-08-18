import os

#
#   initialize the path to shelve file
#
if "ANALYSISRESOURCESHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISRESOURCESHOME env var")

analysisHome = os.environ["ANALYSISRESOURCESHOME"]
pathToShelve = os.path.join(analysisHome,"resources")
shelve_filename = os.path.join(pathToShelve,"SamplesInformation")
