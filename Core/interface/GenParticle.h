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
				GenParticle() : Object() {}

				virtual void reset()
				{
					_mass = 0;
					_pt = 0;
					_eta = 0;
					_rapid = 0;
					_phi = 0;
				}
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
