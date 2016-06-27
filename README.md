# Analysis Framework compliant with CMSSW.

## Branches
- master - default, should not be used...
- 80X - to be used with CMSSW80X
- 74X - to be used with CMSSW74X
- 76X - to be used with CMSSW76X

## Instructions
### With CMSSW
To build a shared lib to be include with CMSSW release do the following 
commands. 
> Note, that is only neccessary to do for **ntuplemaking** stage.
```
cmsrel CMSSWXXX
cd CMSSWXXX/src
cmsenv
git clone https://github.com/uiowahep/Analysis
scram b -j 8
```
### Standalone
To use Analysis package outside of CMSSW do the commands below.
> Note, this is only neccessary to do for stages beyond **ntuplemaking**!
 - ntuplepreprocesssing - preprocess ntuples to engineer features for ML or ...
 - ntupleprocessing - process ntuples to generate various distributions or ...
```
git clone https://github.com/uiowahep/Analysis
mkdir build 
cd build
cmake ../Analysis
```

**Requirements**:
- cmake
- ROOT
