#ifndef Analysis_Core_GenParticle_h
#define Analysis_Core_GenParticle_h

#include "Analysis/Core/interface/Object.h"

namespace analysis
{
	namespace core
	{
		class GenParticle : public Object
		{
			public:
				GenParticle() : Object()
				{}
				virtual ~GenParticle() {}

				float _mass;
				float _pt;
				float _eta;
				float _rapid;
				float _phi;
		};

		typedef std::vector<analysis::core::GenParticle> GenParticles;
	}
}

#endif
