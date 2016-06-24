#ifndef Analysis_Core_MET_h
#define Analysis_Core_MET_h

#include "Analysis/Core/interface/Object.h"

namespace analysis
{
	namespace core
	{
		class MET : public Object
		{
			public:
				MET() : Object()
				{}
				virtual ~MET() {}

				float _px;
				float _py;
				float _pt;
				float _phi;
				float _sumEt;
		};

		typedef std::vector<analysis::core::MET> METs;
	}
}

#endif
