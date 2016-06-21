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
				HFFrame() 
				{
					for (int i=0; i<10; i++)
					{
						_adc[i] = 0;
						_nominal_fC[i] = 0;
					}
				}
				HFFrame(uint32_t id): _id(id)
				{}
				virtual ~HFFrame() {}

				//	public members
				uint32_t	_id;
				int			_adc[10];
				double		_nominal_fC[10];
		};

		typedef std::vector<analysis::core::HFFrame> HFDigis;
	}
}

#endif
