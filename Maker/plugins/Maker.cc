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
#include "UserCode/Maker/interface/DigiUnit.h"

//	ROOT includes
#include "TTree.h"
#include "TDirectory.h"

//
// class declaration
//

using namespace analysis::core;
using namespace analysis::maker;
class Maker : public edm::EDAnalyzer {
   public:
      explicit Maker(const edm::ParameterSet&);
      ~Maker();

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
	  std::vector<EventUnit*>					_units;
	  int										_verbosity;
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
Maker::Maker(const edm::ParameterSet& ps)
{
	//	Initialize the TFileService and create the Directoies + Events Tree
	edm::Service<TFileService> fs;
	TFileDirectory evsDir		= fs->mkdir("Events");
	_tree = evsDir.make<TTree>("Events", "Events");

	//	init some plugin parameters
	_verbosity = ps.getUntrackedParameter<int>("verbosity");

	//	Initialize the EventUnits you need
	_units.push_back(new DigiUnit("Digis", _tree));

	for (unsigned int i=0; i<_units.size(); i++)
		_units[i]->setbranch();
}


Maker::~Maker()
{
}


//
// member functions
//

// ------------ method called for each event  ------------
void
Maker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	using namespace edm;

	//	Process and Fill
	for (unsigned int i=0; i<_units.size(); i++)
		_units[i]->process(iEvent, iSetup);
	_tree->Fill();
	//	Clear
	for (unsigned int i=0; i<_units.size(); i++)
		_units[i]->clear();
}


// ------------ method called once each job just before starting event loop  ------------
void 
Maker::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
Maker::endJob() 
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
Maker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(Maker);
