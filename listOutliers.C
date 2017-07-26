#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "RooFitResult.h"
#include "RooArgSet.h"
#include "<fstream>"


void listOutliers(TString infilename)
{
    TFile* f = new TFile(infilename);
    TTree* t = (TTree*) f->Get("tree_fit_sb");
    std::cout << t->GetName() << ", " << t->GetEntries() << std::endl;
    Double_t mu, muErr, muLoErr, muHiErr;

    TBranch* bmu = t->GetBranch("mu");
    TBranch* bmuErr = t->GetBranch("muErr");
    TBranch* bmuLoErr = t->GetBranch("muLoErr");
    TBranch* bmuHiErr = t->GetBranch("muHiErr");

    bmu->SetAddress(&mu);
    bmuErr->SetAddress(&muErr);
    bmuLoErr->SetAddress(&muLoErr);
    bmuHiErr->SetAddress(&muHiErr);

    //std::fstream appendfile;
    //appendfile.open("outliers.txt", std::fstream::in | std::fstream::out | std::fstream::app );

    RooFitResult* rfit_s = f->Get("fit_s");
    RooFitResult* rfit_b = f->Get("fit_b");
    RooArgSet* rnorm_fit_s = f->Get("norm_fit_s");
    RooArgSet* rnorm_fit_b = f->Get("norm_fit_b");

    for(int i=0; i<t->GetEntries(); i++)
    {
        t->GetEvent(i);
        if(TMath::Abs(muLoErr) > 20 || TMath::Abs(muHiErr) > 20) 
        {
            std::cout << "\n !!!! FAIL !!!! \n" << std::endl;
        }
        else
        {
            std::cout << "\n ++++ PASS ++++ \n" << std::endl;
        } 

        std::cout << Form("[ %s ] :: mu: %6.3f, muLoErr: %6.3f, muHiErr: %6.3f \n", infilename.Data(), mu, muLoErr, muHiErr) << std::endl;
        //appendfile << Form("[ %s ] :: mu: %6.3f, muLoErr: %6.3f, muHiErr: %6.3f", infilename.Data(), mu, muLoErr, muHiErr) << std::endl;

        std::cout << "fit_s \n" << std::endl;
        rfit_s->Print();
        std::cout << "fit_s verbose \n" << std::endl;
        rfit_s->Print("v");
        std::cout << "fit_s correlation M \n" << std::endl;
        rfit_s->correlationMatrix().Print();
        std::cout << "fit_s covariance M \n" << std::endl;
        rfit_s->covarianceMatrix().Print();

        //std::cout << "fit_b" << std::endl;
        //rfit_b->Print();
        
        
        break;
    }
    //appendfile.close();
} 
