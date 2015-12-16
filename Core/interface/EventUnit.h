#ifndef EventUnit_h
#define EventUnit_h

/**
 *	file:
 *	Author:
 *	Description:
 */

//	ROOT
#include "TTree.h"

//	user
#include "UserCode/Core/interface/Candidate.h"

using namespace std;

namespace analysis
{
	namespace core
	{
		class EventUnit : public Object
		{
			public:
				EventUnit() :
					Object(), _tree(NULL)
				{}
				EventUnit(string name, TTree* tree, int v=0, 
					bool supwarn=false) :
					Object(name, v, supwarn), _tree(tree)
				{}
				virtual ~EventUnit() {}

				virtual void setbranch() {}
				virtual void clear() {}
				virtual void process(edm::Event cosnt&,
					edm::EventSetup const&) {}

			protected:
				TTree		*_tree;
		};
	}
}

#endif
