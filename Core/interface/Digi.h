#ifndef Digi_h
#define Digi_h

/**
 *	file:
 *	Author:
 *	Description:
 */

//	user
#ifdef CMSSW 
	#include "UserCode/Core/interface/Candidate.h"
#else
	#include "Core/interface/Candidate.h"
#endif

using namespace std;

namespace analysis
{
	namespace core
	{
		#define NUMTS 10

		class Digi : public Candidate
		{
			public:
				Digi():
					Candidate()
				{}
				Digi(string name, int v=0, bool supwarn=false) : 
					Candidate(name, v, supwarn)
				{}
				virtual ~Digi() {}

			protected:
				DetId		_id;
				int			_adc[NUMTS];
				double		_fc[NUMTS];
		};

		typedef vector<Digi> Digis;
	}
}

#endif
