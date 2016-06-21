// -*- C++ -*-
//
// 
/**\class ForwardStage1 ForwardStage1.cc FSQAnalysis/ForwardStage1/plugins/ForwardStage1.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Viktor Khristenko
//         Created:  Thu, 25 Jun 2015 15:55:22 GMT
//
//


// system include files
#include <memory>

// user include files
#include "Analysis/NtupleMaking/interface/CommonHeaders.h"
#include "Analysis/Core/interface/QIE10Frame.h"

//	ROOT includes
#include "TTree.h"
#include "TDirectory.h"

//
// class declaration
//

using namespace analysis::core;
class QIE10Maker : public edm::EDAnalyzer {
   public:
      explicit QIE10Maker(const edm::ParameterSet&);
      ~QIE10Maker();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
	  TTree										*_tree;
	  int										_verbosity;
	  QIE10Digis								_digis;
	  edm::EDGetTokenT<QIE10DigiCollection>		_tokQIE10;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
QIE10Maker::QIE10Maker(const edm::ParameterSet& ps)
{
	//	Initialize the TFileService and create the Directoies + Events Tree
	edm::Service<TFileService> fs;
	TFileDirectory evsDir		= fs->mkdir("QIE10Maker");
	_tree = evsDir.make<TTree>("Events", "Events");
	_tree->Branch("QIE10Maker", "QIE10Maker", (QIE10Digis*)&_digis);

	//	init some plugin parameters
	_verbosity = ps.getUntrackedParameter<int>("verbosity");
	
	//	consume the token
	_tokQIE10 = consumes<QIE10DigiCollection>(edm::InputTag("hcalDigis"));
}

QIE10Maker::~QIE10Maker()
{
}


//
// member functions
//

// ------------ method called for each event  ------------
void
QIE10Maker::analyze(const edm::Event& e, const edm::EventSetup& es)
{
	using namespace edm;

	std::cout << "Processing" << std::endl;
	edm::Handle<QIE10DigiCollection> cqie10;
	if (!e.getByToken(_tokQIE10, cqie10))
		return;

	for (uint32_t i=0; i<cqie10->size(); i++)
	{
		QIE10DataFrame frame = static_cast<QIE10DataFrame>((*cqie10)[i]); 
		QIE10Frame df(HcalDetId(frame.detid()));
		for (int j=0; j<frame.samples(); j++)
		{
			df._adc[j] = frame[j].adc();
			df._ltdc[j] = frame[j].le_tdc();
		}
		_digis.push_back(df);
	}

	_tree->Fill();
	_digis.clear();
}


// ------------ method called once each job just before starting event loop  ------------
void 
QIE10Maker::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
QIE10Maker::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
ForwardStage1::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
ForwardStage1::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
ForwardStage1::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
ForwardStage1::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
QIE10Maker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(QIE10Maker);
