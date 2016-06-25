#ifndef Analysis_Core_DiMuon_h
#define Analysis_Core_DiMuon_h

#include "Analysis/Core/interface/Object.h"

namespace analysis
{
	namespace core
	{
		class DiMuon : public Object
		{
			public:
				DiMuon() : Object() {}

				virtual void DiMuon()
				{
					_mass = 0;
					_pt = 0;
					_eta = 0;
					_rapid = 0;
					_phi = 0;
				}
				virtual ~DiMuon() {}

				float _mass;
				float _pt;
				float _eta;
				float _rapid;
				float _phi;
		};

		typedef std::vector<analysis::core::DiMuon> DiMuons;
	}
}

#endif
