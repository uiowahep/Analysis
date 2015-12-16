#ifndef Digi10_h
#define Digi10_h

/**
 *	file:
 *	Author:
 *	Description:
 */

//	user
#ifdef CMSSW 
	#include "UserCode/Core/interface/Digi.h"
#else
	#include "Core/interface/Digi.h"
#endif

using namespace std;

namespace analysis
{
	namespace core
	{
		class Digi10 : public Digi
		{
			public:
				Digi10():
					Digi()
				{}
				Digi10(string name, int v=0, bool supwarn=false) : 
					Digi(name, v, supwarn)
				{}
				virtual ~Digi10() {}

			protected:
				int			_tdc_le[NUMTS];
				int			_tdc_te[NUMTS];
		};

		typedef vector<Digi10> Digi10s;
	}
}

#endif
