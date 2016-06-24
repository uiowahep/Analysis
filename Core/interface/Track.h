#ifndef Analysis_Core_Track_h
#define Analysis_Core_Track_h

#include "Analysis/Core/interface/Object.h"

namespace analysis
{
	namespace core
	{
		class Track : public Object
		{
			public:
				Track() : Object()
				{}
				virtual ~Track() {}

				int _charge;
				float _pt;
				float _pterr;
				float _eta;
				float _phi;
		};

		std::vector<analysis::core::Track> Tracks;
	}
}

#endif
