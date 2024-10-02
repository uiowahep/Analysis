/*
 *	Author:
 *	Date:
 *	Description:
 */

// system include files
#include <memory>

// user include files
#include "Analysis/NtupleMaking/interface/CommonHeaders.h"
#include "Analysis/Core/interface/QIE10Frame.h"
#include "Analysis/Core/interface/QIE8Frame.h"

//	ROOT includes
#include "TTree.h"
#include "TDirectory.h"

//
// class declaration
//

using namespace analysis::core;
class QIE10Maker : public edm::stream::EDAnalyzer {
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
	  QIE10Digis								_qie10digis;
	  QIE8Digis									_hfdigis;
      QIE8Digis                                 _hedigis;
      QIE8Digis                                 _hbdigis;
	  edm::EDGetTokenT<QIE10DigiCollection>		_tokQIE10;
	  edm::EDGetTokenT<HFDigiCollection>		_tokHF;
	  edm::EDGetTokenT<HBHEDigiCollection>		_tokHBHE;
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
	_tree =fs->make<TTree>("Events", "Events");
	_tree->Branch("QIE10Digis", "QIE10Digis", (QIE10Digis*)&_qie10digis);
	_tree->Branch("HFDigis", "HFDigis", (QIE8Digis*)&_hfdigis);
	_tree->Branch("HBDigis", "HBDigis", (QIE8Digis*)&_hbdigis);
	_tree->Branch("HEDigis", "HEDigis", (QIE8Digis*)&_hedigis);

	//	init some plugin parameters
	_verbosity = ps.getUntrackedParameter<int>("verbosity");
	
	//	consume the token
	_tokQIE10 = consumes<QIE10DigiCollection>(edm::InputTag("hcalDigis"));
	_tokHF = consumes<HFDigiCollection>(edm::InputTag("hcalDigis"));
    _tokHBHE = consumes<HBHEDigiCollection>(edm::InputTag("hcalDigis"));
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

	edm::Handle<QIE10DigiCollection> cqie10;
	edm::Handle<HFDigiCollection> chf;
	edm::Handle<HBHEDigiCollection> chbhe;
	if (!e.getByToken(_tokQIE10, cqie10))
		return;
	if (!e.getByToken(_tokHF, chf))
		return;
    if (!e.getByToken(_tokHBHE, chbhe))
        return;

	//	QIE10
	for (uint32_t i=0; i<cqie10->size(); i++)
	{
		QIE10DataFrame frame = static_cast<QIE10DataFrame>((*cqie10)[i]); 
		QIE10Frame df;
		HcalDetId did(frame.detid());
		df._iphi = did.iphi();
		df._ieta = did.ieta();
		df._depth = did.depth();
		for (int j=0; j<frame.samples(); j++)
		{
			df._adc.push_back(frame[j].adc());
			df._ltdc.push_back(frame[j].le_tdc());
		}
		_qie10digis.push_back(df);
	}

	//	HF Digis
	for (HFDigiCollection::const_iterator it=chf->begin(); it!=chf->end();
		++it)
	{
		HcalDetId did(it->id());
		QIE8Frame df;

		df._iphi = did.iphi();
		df._ieta = did.ieta();
		df._depth = did.depth();
		for (int i=0; i<it->size(); i++)
		{
			df._adc.push_back(it->sample(i).adc());
			df._nominal_fC.push_back(it->sample(i).nominal_fC());
		}

		_hfdigis.push_back(df);
	}

	for (HBHEDigiCollection::const_iterator it=chbhe->begin(); it!=chbhe->end();
		++it)
	{
		HcalDetId did(it->id());
		QIE8Frame df;

		df._iphi = did.iphi();
		df._ieta = did.ieta();
		df._depth = did.depth();
		for (int i=0; i<it->size(); i++)
		{
			df._adc.push_back(it->sample(i).adc());
			df._nominal_fC.push_back(it->sample(i).nominal_fC());
		}

        if (did.subdet()==1)
		    _hbdigis.push_back(df);
        else
            _hedigis.push_back(df);
	}

	//	fill and clear
	_tree->Fill();
	_qie10digis.clear();
	_hfdigis.clear();
	_hbdigis.clear();
	_hedigis.clear();
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
