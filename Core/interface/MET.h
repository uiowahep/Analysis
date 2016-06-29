#ifndef Analysis_Core_MET_h
#define Analysis_Core_MET_h

#ifndef STANDALONE
#include "Analysis/Core/interface/Object.h"
#else
#include "Object.h"
#endif

namespace analysis
{
	namespace core
	{
		class MET : public Object
		{
			public:
				MET() : Object() {this->reset();}

				virtual void reset()
				{
					_px = 0;
					_py = 0;
					_pt = 0; 
					_phi = 0;
					_sumEt = 0;
				}
				virtual ~MET() {}

				float _px;
				float _py;
				float _pt;
				float _phi;
				float _sumEt;

#ifdef STANDALONE
				ClassDef(MET, 1)
#endif
		};

		typedef std::vector<analysis::core::MET> METs;
	}
}

//
//	Using the unique
//
#ifdef STANDALONE
ClassImpUnique(analysis::core::MET, MET)
#endif

#endif
