#ifndef Analysis_Core_GenJet_h
#define Analysis_Core_GenJet_h

#include "Analysis/Core/interface/Object.h"

namespace analysis
{
	namespace core
	{
		class GenJet : public Object
		{
			public:
				GenJet() : Object()
				{}
				virtual ~GenJet() {}

				float _px;
				float _py;
				float _pz;
				float _pt;
				float _eta;
				float _phi;
				float _mass;
				int _charge;
		};

		typedef std::vector<analysis::core::GenJet> GenJets;
	}
}

#endif
