#ifndef DigiUnit_h
#define DigiUnit_h

/**
 *	file:
 *	Author:
 *	Description:
 */

//	user
#include "UserCode/Core/interface/EventUnit.h"
#include "UserCode/Core/interface/Digi.h"

namespace analysis
{
	using namespace core
	namespace maker
	{
		class DigiUnit : public EventUnit
		{
			public:
				DigiUnit():
					EventUnit()
				{}
				DigiUnit(string name, TTree* tree, int v=0,
					bool supwarn=false) : 
					EventUnit(name, tree, v, supwarn)
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

				}

			protected:
				Digis	_digis;
		};
	}
}

#endif
