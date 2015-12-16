#ifndef Candidate_h
#define Candidate_h

/**
 *	file:
 *	Author:
 *	Description:
 */

//	std
#include <vector>

// user
#ifdef CMSSW
	#include "UserCode/Core/inteface/Object.h"
#else
	#include "Core/interface/Object.h"
#endif

using namespace std;

namespace analysis
{
	namespace core
	{
		struct DetId
		{
			int _ieta;
			int _iphi;
			int _depth;
			int _raw;
		};

		class Candidate : public Object
		{
			public:
				Candidate() :
					Object()
				{}
				Candidate(string name, int v=0, bool supwarn=false):
					Object(name, v, supwarn)
				{}
				virtual ~Candidate() {}
			protected:
				DetId _id;
		};

		typedef vector<Candidate> Candidates;
	}
}

#endif
