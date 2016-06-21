#ifndef Analysis_Core_QIE10Frame_h
#define Analysis_Core_QIE10Frame_h

#include <vector>

namespace analysis
{
	namespace core
	{
		class QIE10Frame
		{
			public:
				QIE10Frame() 
				{
					for (int i=0; i<10; i++)
					{
						_adc[i] = 0;
						_ltdc[i] = 0;
					}
				}
				QIE10Frame(uint32_t id): _id(id)
				{
					for (int i=0; i<10; i++)
					{
						_adc[i] = 0;
						_ltdc[i] = 0;
					}
				}
				virtual ~QIE10Frame() {}

				//	public members
				uint32_t	_id;
				int			_adc[10];
				int			_ltdc[10];
//				int			_ttdc[10];
		};

		typedef std::vector<analysis::core::QIE10Frame> QIE10Digis;
	}
}

#endif
