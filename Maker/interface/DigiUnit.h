#ifndef Analysis_Maker_DigiUnit_h
#define Analysis_Maker_DigiUnit_h

/**
 *	file:
 *	Author:
 *	Description:
 */

//	user
#include "Analysis/Core/interface/EventUnit.h"

//	CMSSW
#include "DataFormats/interface/HcalDigi/interface/QIE10DataFrame.h"

namespace analysis
{
	using namespace core
	namespace maker
	{
		typedef std::vector<QIE10DataFrame> Digis;
		class DigiUnit : public EventUnit
		{
			public:
				DigiUnit(): EventUnit()
				{}
				DigiUnit(string name, TTree* tree) :
					EventUnit(name, tree)
				{}
				virtual ~DigiUnit() {}

				virtual void setbranch()
				{
					_tree->SetBranchAddress(_name.str(),
						(Digis*)&_digis);
				}
				virtual void clear()
				{
					_digis.clear();
				}
				virtual void process()
				{
					std::cout << "Processing..." << std::endl;
				}

				//	public
				Digis	_digis;
		};
	}
}

#endif
