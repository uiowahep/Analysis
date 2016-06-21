#ifndef Analysis_Core_EventUnit_h
#define Analysis_Core_EventUnit_h

/**
 *	file:
 *	Author:
 *	Description:
 */

//	ROOT
#include "TTree.h"

//	user
#include "Analysis/Core/interface/Object.h"

using namespace std;

namespace analysis
{
	namespace core
	{
		class EventUnit : public Object
		{
			public:
				EventUnit() : Object(), _tree(NULL) {}
				EventUnit(string const& name, TTree* tree) :
					Object(name), _tree(tree)
				{}
				virtual ~EventUnit() {}

				virtual void setbranch() {}
				virtual void clear() {}
				virtual void process(edm::Event const&,
					edm::EventSetup const&) {}

				//	public members!
				TTree		*_tree;
		};
	}
}

#endif
