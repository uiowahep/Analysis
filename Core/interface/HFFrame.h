#ifndef Analysis_Core_HFFrame_h
#define Analysis_Core_HFFrame_h

#include <vector>

namespace analysis
{
	namespace core
	{
		class HFFrame
		{
			public:
				HFFrame() {}
				HFFrame(uint32_t id): _id(id)
				{}
				virtual ~HFFrame() {}

				//	public members
				uint32_t	_id;
				int			_adc[10];
				double		nominal_fC[10];
		};

		typedef std::vector<analysis::core::HFFrame> HFDigis;
	}
}

#endif
