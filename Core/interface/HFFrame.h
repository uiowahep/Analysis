#ifndef Analysis_Core_HFFrame_h
#define Analysis_Core_HFFrame_h

#ifndef STANDALONE
#include "Analysis/Core/interface/Object.h"
#else
#include "Object.h"
#endif

#include <vector>

namespace analysis
{
	namespace core
	{
		class HFFrame : public Object
		{
			public:
				HFFrame() : Object() {}

				virtual void reset()				
				{
					for (int i=0; i<10; i++)
					{
						_adc[i] = 0;
						_nominal_fC[i] = 0;
					}
					_iphi = 0;
					_ieta = 0;
					_depth = 0;
				}
				virtual ~HFFrame() {}

				//	public members
				int			_iphi;
				int			_ieta;
				int			_depth;
				int			_adc[10];
				double		_nominal_fC[10];

#ifdef STANDALONE
				ClassDef(HFFrame, 1)
#endif
		};

		typedef std::vector<analysis::core::HFFrame> HFDigis;
	}
}

#ifdef STANDALONE
ClassImpUnique(analysis::core::HFFrame, HFFrame)
#endif

#endif
