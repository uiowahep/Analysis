#ifndef Analysis_Core_Track_h
#define Analysis_Core_Track_h

#ifndef STANDALONE
#include "Analysis/Core/interface/Object.h"
#else
#include "Object.h"
#endif

namespace analysis
{
	namespace core
	{
		class Track : public Object
		{
			public:
				Track() : Object() {}

				virtual void reset()
				{
					_charge = 0;
					_pt = 0;
					_pterr = 0;
					_eta = 0;
					_phi = 0;
				}
				virtual ~Track() {}

				int _charge;
				float _pt;
				float _pterr;
				float _eta;
				float _phi;

#ifdef STANDALONE
				ClassDef(Track, 1)
#endif
		};

		typedef std::vector<analysis::core::Track> Tracks;
	}
}

#ifdef STANDALONE
		ClassImp(analysis::core::Track)
#endif

#endif
