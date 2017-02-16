# Analysis Framework compliant with CMSSW.

## CMSSW Branches and Repos to merge in
```
1) for cut/mva based electron id
git cms-merge-topic ikrav:egm_id_80X_v2 

2) Optional???!!! I believe these guys have been merged
data files for mva based electron id
cd $CMSSW_BASE/external
cd slc6_amd64_gcc530/
git clone https://github.com/ikrav/RecoEgamma-ElectronIdentification.git data/RecoEgamma/ElectronIdentification/data
cd data/RecoEgamma/ElectronIdentification/data
git checkout egm_id_80X_v1
cd $CMSSW_BASE/src
```

## Instructions
### With CMSSW or Against CMSSW
To build a shared lib to be include with CMSSW release do the following 
commands. 

> Note, that is only neccessary to do for **ntuplemaking** stage.

```
cmsrel CMSSWXXX
cd CMSSWXXX/src
cmsenv
git clone https://github.com/uiowahep/Analysis
scram b -j 8
source $PWD/Analysis/config/env.sh - source with the full path!
```

### Standalone
To use Analysis package outside of CMSSW do the commands below.

> Note, this is only neccessary to do for stages beyond **ntuplemaking**!
> Note, that if you are working on lxplus and processing ntuples from lxplus, you don't have to clone again - reuse the same source **Analysis** directory.

```
git clone https://github.com/uiowahep/Analysis - optional!
mkdir build 
cd build
cmake ../Analysis or cmake /full/path/to/Analysis, where /full/path/to - is the full path to Analysis folder
source /full/path/to/Analysis/config/env.sh
```

**Requirements**:
- cmake
- ROOT
