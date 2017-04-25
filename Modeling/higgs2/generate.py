"""
"""
import ROOT as R
R.gROOT.SetBatch(R.kTRUE)

import generatingFunctions as funcs
import aux
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--what", type=str, default="distributions", 
    help="number identifies the function to run")
parser.add_argument('-v', '--verbose', action='store_true', default=False, 
    help='Verbose debugging output')
parser.add_argument('-m', '--mode', type=str, default='Iowa', 
    help='Run in Iowa, UF_AWB, or UF_AMC mode')
parser.add_argument("--outDirName", type=str,
    default="test", help="Directory Name that will be created in the .../{distributions | signalfits | etc}/$jobLabel/ - all of the plots/datacards/workspaces will be created inside of that folder")
parser.add_argument('--unblind', action='store_true', default=False, help='True will be blinding mass region. For limits observed limit values will not be plotted')
parser.add_argument("--logY", action="store_true", default=False,
    help="Will force all the plots on the logY scale")

args = parser.parse_args()

if args.mode == "Iowa":
    import Configuration.higgs.Iowa_settings as settings
    from Configuration.higgs.Iowa_settings import *
elif args.mode == "UF_AWB":
    import Configuration.higgs.UF_AWB_settings as settings
    from Configuration.higgs.UF_AWB_settings import *
elif args.mode == "UF_AMC":
    import Configuration.higgs.UF_AMC_settings as settings
    from Configuration.higgs.UF_AMC_settings import *

def backgroundFits():
    pathToDir = os.path.join(backgroundfitsDir, args.outDirName)
    aux.mkdir(pathToDir)
    for category in categoriesToUse:
        for modelGroup in backgroundModelGroups:
            ws = R.RooWorkspace("higgs")
            aux.buildMassVariable(ws, **diMuonMass125)
            modelsToUse = modelGroup.models
            counter = 0;
            for m in modelsToUse:
                m.color = colors[counter]
                counter+=1
            funcs.backgroundFits(
                (category, diMuonMass125), ws, data, modelsToUse,
                settings,
                pathToDir=pathToDir,groupName=modelGroup.name)

def ftest():
    pathToDir = os.path.join(ftestDir, args.outDirName)
    aux.mkdir(pathToDir)
    fTestResults = {}
    for category in categoriesToUse:
        fTestResults[category] = {}
        for modelGroup in orderedModelGroups:
            ws = R.RooWorkspace("higgs")
            aux.buildMassVariable(ws, **diMuonMass125)
            counter = 0;
            for m in modelGroup.models:
                m.color = colors[counter]
                counter+=1
            modelToBeUsed, values = funcs.ftestPerFamily(
                (category, diMuonMass125), ws, data, modelGroup,
                settings, pathToDir=pathToDir)
            fTestResults[category][modelGroup.name] = values
    funcs.plotFTestResults(fTestResults, pathToDir=pathToDir)

def datacardsTripleGaus():
    physGroupToUse = physGroupTest
    orderedGroupsToUse = orderedGroupsTest
    workspaceName = "higgs"
    signalSplinesDir = os.path.join(signalfitinterpolationswithsplineDir, args.outDirName)
    backgroundsDir = os.path.join(backgroundfitswithroomultipdfDir, args.outDirName)
    datacardsDir = os.path.join(datacardsworkspacesDir, args.outDirName)
    fffTestDir = os.path.join(ftestDir, args.outDirName)
    aux.mkdir(signalSplinesDir); aux.mkdir(backgroundsDir); aux.mkdir(datacardsDir)
    aux.mkdir(fffTestDir)
    fTestResults = {}
    for category in categoriesToUse:
        fTestResults[category] = {}
        workspaceFileName = "workspace__{category}__{signalModelId}.root".format(
            category=names2RepsToUse[category], signalModelId = tripleGaus120.modelId)
        ws = R.RooWorkspace(workspaceName)
        aux.buildMassVariable(ws, **diMuonMass125)
        aux.buildMH(ws, mhmin=120, mhmax=130)
        
        #
        # create the RooDataHist and import it into the Workspace here explicitly
        #
        fdata = R.TFile(data.pathToFile)

        hdata_name = category + "/DiMuonMass"
        if settings.useInputFileUF:
            hdata_name = "net_histos/"+category+"_Net_Data"

        hdata = fdata.Get(hdata_name)
        rdata = aux.buildRooHist(ws, hdata,
            "data_obs_{category}".format(category=names2RepsToUse[category]))
        getattr(ws, "import")(rdata, R.RooFit.RecycleConflictNodes())
        fdata.Close()
        
        #
        # Create the Signal Models
        #
        print "*"*80
        print "Generating Triple Gaus Splines"
        print "*"*80
        vbfmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, tripleGaus120, diMuonMass120),
                (vbf125, tripleGaus125, diMuonMass125),
                (vbf130, tripleGaus130, diMuonMass130),
            ], 
            settings,
            pathToDir=signalSplinesDir
        )
        glumodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, tripleGaus120, diMuonMass120),
                (glu125, tripleGaus125, diMuonMass125),
                (glu130, tripleGaus130, diMuonMass130),
            ],
            settings, 
            pathToDir=signalSplinesDir
        )
        wpmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, tripleGaus120, diMuonMass120),
                (wp125, tripleGaus125, diMuonMass125),
                (wp130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        wmmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, tripleGaus120, diMuonMass120),
                (wm125, tripleGaus125, diMuonMass125),
                (wm130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        zhmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, tripleGaus120, diMuonMass120),
                (zh125, tripleGaus125, diMuonMass125),
                (zh130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        
        #
        # Perform the F-Test and select the proper order of the 
        #
        selectedOrderedModels = []
        for modelGroup in orderedGroupsToUse:
            counter = 0;
            for m in modelGroup.models:
                m.color = colors[counter]
                counter+=1
            selectedModel, values = funcs.ftestPerFamily(
                (category, diMuonMass125), ws, data, modelGroup,
                settings, pathToDir=fffTestDir)
            if selectedModel is not None:
                selectedOrderedModels.append(selectedModel)
            fTestResults[category][modelGroup.name] = values

        #
        # Create the Background Model
        #
        totalModelGroup = ModelGroup("bkgModels",
            physGroupTest.models + selectedOrderedModels)
        counter = 0
        for model in totalModelGroup.models:
            model.color = colors[counter]
            counter += 1
        funcs.backgroundsWithRooMultiPdf((category, diMuonMass125), ws, data, 
            totalModelGroup.models, settings, pathToDir=backgroundsDir,
            groupName=totalModelGroup.name)

        #
        # Signal and Background Models are ready and are in the Workspace
        # create the datacard for this category
        #
        funcs.datacardAnalytic(category, ws, data, 
            [vbfmodel, glumodel, wpmodel, wmmodel, zhmodel], 
            ws.pdf("multipdf_{category}".format(category=names2RepsToUse[category])),
            settings,
            pathToDir=datacardsDir,
            workspaceFileName=workspaceFileName,
            workspaceName=workspaceName
        )

        #
        # save the Workspacee
        #
        ws.SaveAs(os.path.join(datacardsDir, workspaceFileName))

    #
    # plot all the F-test results
    #
    funcs.plotFTestResults(fTestResults, pathToDir=fffTestDir)

def datacardsDoubleGaus():
    physGroupToUse = physGroupTest
    orderedGroupsToUse = orderedGroupsTest
    workspaceName = "higgs"
    signalSplinesDir = os.path.join(signalfitinterpolationswithsplineDir, args.outDirName)
    backgroundsDir = os.path.join(backgroundfitswithroomultipdfDir, args.outDirName)
    datacardsDir = os.path.join(datacardsworkspacesDir, args.outDirName)
    fffTestDir = os.path.join(ftestDir, args.outDirName)
    aux.mkdir(signalSplinesDir); aux.mkdir(backgroundsDir); aux.mkdir(datacardsDir)
    aux.mkdir(fffTestDir)
    fTestResults = {}
    for category in categoriesToUse:
        fTestResults[category] = {}
        workspaceFileName = "workspace__{category}__{signalModelId}.root".format(
            category=names2RepsToUse[category], signalModelId = doubleGaus120.modelId)
        ws = R.RooWorkspace(workspaceName)
        aux.buildMassVariable(ws, **diMuonMass125)
        aux.buildMH(ws, mhmin=120, mhmax=130)
        
        #
        # create the RooDataHist and import it into the Workspace here explicitly
        #
        fdata = R.TFile(data.pathToFile)

        hdata_name = category + "/DiMuonMass"
        if settings.useInputFileUF:
            hdata_name = "net_histos/"+category+"_Net_Data"

        hdata = fdata.Get(hdata_name)
        rdata = aux.buildRooHist(ws, hdata,
            "data_obs_{category}".format(category=names2RepsToUse[category]))
        getattr(ws, "import")(rdata, R.RooFit.RecycleConflictNodes())
        fdata.Close()
        
        #
        # Create the Signal Models
        #
        print "*"*80
        print "Generating Double Gaus Splines"
        print "*"*80
        vbfmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, doubleGaus120, diMuonMass120),
                (vbf125, doubleGaus125, diMuonMass125),
                (vbf130, doubleGaus130, diMuonMass130),
            ],
            settings, 
            pathToDir=signalSplinesDir
        )
        glumodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, doubleGaus120, diMuonMass120),
                (glu125, doubleGaus125, diMuonMass125),
                (glu130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        wpmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, doubleGaus120, diMuonMass120),
                (wp125, doubleGaus125, diMuonMass125),
                (wp130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        wmmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, doubleGaus120, diMuonMass120),
                (wm125, doubleGaus125, diMuonMass125),
                (wm130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        zhmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, doubleGaus120, diMuonMass120),
                (zh125, doubleGaus125, diMuonMass125),
                (zh130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        
        #
        # Perform the F-Test and select the proper order of the 
        #
        selectedOrderedModels = []
        for modelGroup in orderedGroupsToUse:
            counter = 0;
            for m in modelGroup.models:
                m.color = colors[counter]
                counter+=1
            selectedModel, values = funcs.ftestPerFamily(
                (category, diMuonMass125), ws, data, modelGroup,
                settings, pathToDir=fffTestDir)
            if selectedModel is not None:
                selectedOrderedModels.append(selectedModel)
            fTestResults[category][modelGroup.name] = values

        #
        # Create the Background Model
        #
        totalModelGroup = ModelGroup("bkgModels",
            physGroupTest.models + selectedOrderedModels)
        counter = 0
        for model in totalModelGroup.models:
            model.color = colors[counter]
            counter += 1
        funcs.backgroundsWithRooMultiPdf((category, diMuonMass125), ws, data, 
            totalModelGroup.models, settings, pathToDir=backgroundsDir,
            groupName=totalModelGroup.name)

        #
        # Signal and Background Models are ready and are in the Workspace
        # create the datacard for this category
        #
        funcs.datacardAnalytic(category, ws, data, 
            [vbfmodel, glumodel, wpmodel, wmmodel, zhmodel], 
            ws.pdf("multipdf_{category}".format(category=names2RepsToUse[category])),
            settings,
            pathToDir=datacardsDir,
            workspaceFileName=workspaceFileName,
            workspaceName=workspaceName
        )

        #
        # save the Workspacee
        #
        ws.SaveAs(os.path.join(datacardsDir, workspaceFileName))

    #
    # plot all the F-test results
    #
    funcs.plotFTestResults(fTestResults, pathToDir=fffTestDir)

def datacardsSingleGaus():
    physGroupToUse = physGroupTest
    orderedGroupsToUse = orderedGroupsTest
    workspaceName = "higgs"
    signalSplinesDir = os.path.join(signalfitinterpolationswithsplineDir, args.outDirName)
    backgroundsDir = os.path.join(backgroundfitswithroomultipdfDir, args.outDirName)
    datacardsDir = os.path.join(datacardsworkspacesDir, args.outDirName)
    fffTestDir = os.path.join(ftestDir, args.outDirName)
    aux.mkdir(signalSplinesDir); aux.mkdir(backgroundsDir); aux.mkdir(datacardsDir)
    aux.mkdir(fffTestDir)
    fTestResults = {}
    for category in categoriesToUse:
        fTestResults[category] = {}
        workspaceFileName = "workspace__{category}__{signalModelId}.root".format(
            category=names2RepsToUse[category], signalModelId = singleGaus120.modelId)
        ws = R.RooWorkspace(workspaceName)
        aux.buildMassVariable(ws, **diMuonMass125)
        aux.buildMH(ws, mhmin=120, mhmax=130)

        #
        # create the RooDataHist and import it into the Workspace here explicitly
        #
        fdata = R.TFile(data.pathToFile)

        hdata_name = category + "/DiMuonMass"
        if settings.useInputFileUF:
            hdata_name = "net_histos/"+category+"_Net_Data"

        hdata = fdata.Get(hdata_name)
        rdata = aux.buildRooHist(ws, hdata,
            "data_obs_{category}".format(category=names2RepsToUse[category]))
        getattr(ws, "import")(rdata, R.RooFit.RecycleConflictNodes())
        fdata.Close()
        
        #
        # Create the Signal Models
        #
        print "*"*80
        print "Generating Single Gaus Splines"
        print "*"*80
        vbfmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, singleGaus120, diMuonMass120),
                (vbf125, singleGaus125, diMuonMass125),
                (vbf130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        glumodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, singleGaus120, diMuonMass120),
                (glu125, singleGaus125, diMuonMass125),
                (glu130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        wpmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, singleGaus120, diMuonMass120),
                (wp125, singleGaus125, diMuonMass125),
                (wp130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        wmmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, singleGaus120, diMuonMass120),
                (wm125, singleGaus125, diMuonMass125),
                (wm130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )
        zhmodel = funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, singleGaus120, diMuonMass120),
                (zh125, singleGaus125, diMuonMass125),
                (zh130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=signalSplinesDir
        )

        #
        # Perform the F-Test and select the proper order of the 
        #
        selectedOrderedModels = []
        for modelGroup in orderedGroupsToUse:
            counter = 0;
            for m in modelGroup.models:
                m.color = colors[counter]
                counter+=1
            selectedModel, values = funcs.ftestPerFamily(
                (category, diMuonMass125), ws, data, modelGroup,
                settings, pathToDir=fffTestDir)
            if selectedModel is not None:
                selectedOrderedModels.append(selectedModel)
            fTestResults[category][modelGroup.name] = values

        #
        # Create the Background Model
        #
        totalModelGroup = ModelGroup("bkgModels", 
            physGroupTest.models + selectedOrderedModels)
        counter = 0
        for model in totalModelGroup.models:
            model.color = colors[counter]
            counter += 1
        funcs.backgroundsWithRooMultiPdf((category, diMuonMass125), ws, data, 
            totalModelGroup.models, settings,
            pathToDir=backgroundsDir,
            groupName=totalModelGroup.name)

        #
        # Signal and Background Models are ready and are in the Workspace
        # create the datacard for this category
        #
        funcs.datacardAnalytic(category, ws, data, 
            [vbfmodel, glumodel, wpmodel, wmmodel, zhmodel], 
            ws.pdf("multipdf_{category}".format(category=names2RepsToUse[category])),
            settings,
            pathToDir=datacardsDir,
            workspaceFileName=workspaceFileName,
            workspaceName=workspaceName
        )

        #
        # save the Workspacee
        #
        print "*"*80
        print "*** Final RooWorkspace contents ***"
        print "*"*80
        ws.Print("v")
        ws.SaveAs(os.path.join(datacardsDir, workspaceFileName))

    #
    # plot all the F-Test Results
    #
    funcs.plotFTestResults(fTestResults, pathToDir=fffTestDir)

def backgroundsWithRooMultiPdf():
    modelGroupToUse = modelGroupForMultiPdf
    pathToDir = os.path.join(backgroundfitswithroomultipdfDir, args.outDirName)
    aux.mkdir(pathToDir)
    for category in categoriesToUse:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        counter = 0;
        for model in modelGroupToUse.models:
            model.color = colors[counter]
            counter += 1
        funcs.backgroundsWithRooMultiPdf((category, diMuonMass125), ws, data, 
            modelGroupToUse.models, settings, pathToDir=pathToDir,
            groupName=modelGroupToUse.name)

def signalFitInterpolations():
    pathToDir = os.path.join(singalfitinterpolationsDir, args.outDirName)
    aux.mkdir(pathToDir)
    for category in categoriesToUse:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        funcs.signalFitInterpolation(category, ws, 
            [
                (vbf120, singleGaus120, diMuonMass120),
                (vbf125, singleGaus125, diMuonMass125),
                (vbf130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )

def signalFitInterpolationsWithSpline():
    pathToDir = os.path.join(signalfitinterpolationswithsplineDir, args.outDirName)
    aux.mkdir(pathToDir)
    for category in categoriesToUse:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        aux.buildMH(ws, mhmin=120, mhmax=130)
        print "*"*80
        print "Generating Single Gaus Splines"
        print "*"*80
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, singleGaus120, diMuonMass120),
                (vbf125, singleGaus125, diMuonMass125),
                (vbf130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, singleGaus120, diMuonMass120),
                (glu125, singleGaus125, diMuonMass125),
                (glu130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, singleGaus120, diMuonMass120),
                (wp125, singleGaus125, diMuonMass125),
                (wp130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, singleGaus120, diMuonMass120),
                (wm125, singleGaus125, diMuonMass125),
                (wm130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, singleGaus120, diMuonMass120),
                (zh125, singleGaus125, diMuonMass125),
                (zh130, singleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        print "*"*80
        print "Generating Double Gaus Splines"
        print "*"*80
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, doubleGaus120, diMuonMass120),
                (vbf125, doubleGaus125, diMuonMass125),
                (vbf130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, doubleGaus120, diMuonMass120),
                (glu125, doubleGaus125, diMuonMass125),
                (glu130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, doubleGaus120, diMuonMass120),
                (wp125, doubleGaus125, diMuonMass125),
                (wp130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, doubleGaus120, diMuonMass120),
                (wm125, doubleGaus125, diMuonMass125),
                (wm130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, doubleGaus120, diMuonMass120),
                (zh125, doubleGaus125, diMuonMass125),
                (zh130, doubleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        print "*"*80
        print "Generating Triple Gaus Splines"
        print "*"*80
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (vbf120, tripleGaus120, diMuonMass120),
                (vbf125, tripleGaus125, diMuonMass125),
                (vbf130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (glu120, tripleGaus120, diMuonMass120),
                (glu125, tripleGaus125, diMuonMass125),
                (glu130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wp120, tripleGaus120, diMuonMass120),
                (wp125, tripleGaus125, diMuonMass125),
                (wp130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (wm120, tripleGaus120, diMuonMass120),
                (wm125, tripleGaus125, diMuonMass125),
                (wm130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )
        funcs.signalFitInterpolationWithSpline(category, ws, 
            [
                (zh120, tripleGaus120, diMuonMass120),
                (zh125, tripleGaus125, diMuonMass125),
                (zh130, tripleGaus130, diMuonMass130),
            ],
            settings,
            pathToDir=pathToDir
        )

def signalFits():
    pathToDir = os.path.join(signalfitsDir, args.outDirName)
    aux.mkdir(pathToDir)
    initialValuesFromTH1 = True
    for category in categoriesToUse:
        ws = R.RooWorkspace("higgs")
        aux.buildMassVariable(ws, **diMuonMass125)
        for modelToUse in [singleGaus125, doubleGaus125, tripleGaus125]:
            modelToUse.color = R.kRed
            funcs.signalFit((category, diMuonMass125), ws, vbf125, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass125), ws, glu125, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass125), ws, wm125, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass125), ws, wp125, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass125), ws, zh125, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
        aux.buildMassVariable(ws, **diMuonMass120)
        for modelToUse in [singleGaus120, doubleGaus120, tripleGaus120]:
            modelToUse.color = R.kRed
            funcs.signalFit((category, diMuonMass120), ws, vbf120, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass120), ws, glu120, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass120), ws, wm120, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass120), ws, wp120, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass120), ws, zh120, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
        aux.buildMassVariable(ws, **diMuonMass130)
        for modelToUse in [singleGaus130, doubleGaus130, tripleGaus130]:
            modelToUse.color = R.kRed
            funcs.signalFit((category, diMuonMass130), ws, vbf130, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass130), ws, glu130, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass130), ws, wm130, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass130), ws, wp130, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)
            funcs.signalFit((category, diMuonMass130), ws, zh130, modelToUse, settings, pathToDir=pathToDir, initialValuesFromTH1=initialValuesFromTH1)

def distributions():
    logY = args.logY
    pathToDir = os.path.join(distributionsDir, args.outDirName)
    aux.mkdir(pathToDir)
    for category in categoriesToUse:
        for vname in varNames:
            variable = {}
            variable["name"]=vname
            variable["min"]=-0.999
            variable["max"]=-0.999
            if category!="NoCats" and vname=="DiMuonMass":
                variable["min"] = 110
                variable["max"] = 160
            funcs.distributions((category, variable), data, 
                [glu125, vbf125, wm125, wp125, zh125],
                # [wJetsToLNu, wwTo2L2Nu, wzTo3LNu, tt, dy], settings,
                [], settings,
                pathToDir=pathToDir,
                logY=logY)

def main():
    import sys
    print args
    what = getattr(sys.modules[__name__], args.what)
    what()

if __name__=="__main__":
    main()
