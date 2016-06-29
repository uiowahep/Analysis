#ifndef Analysis_Core_GenJet_h
#define Analysis_Core_GenJet_h

#ifndef STANDALONE
#include "Analysis/Core/interface/Object.h"
#else
#include "Object.h"
#endif

namespace analysis
{
	namespace core
	{
		class GenJet : public Object
		{
			public:
				GenJet() : Object()
				{this->reset();}
				virtual ~GenJet() {}
				virtual void reset()
				{
					_px = 0;
					_py = 0;
					_pz = 0;
					_pt = 0;
					_eta = 0;
					_phi = 0;
					_mass = 0;
				}

				float _px;
				float _py;
				float _pz;
				float _pt;
				float _eta;
				float _phi;
				float _mass;

#ifdef STANDALONE
				ClassDef(GenJet, 1)
#endif
		};

		typedef std::vector<analysis::core::GenJet> GenJets;
	}
}

#ifdef STANDALONE
ClassImpUnique(analysis::core::GenJet, GenJet)
#endif

#endif
