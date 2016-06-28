#ifndef Analysis_Core_QIE10Frame_h
#define Analysis_Core_QIE10Frame_h

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
		class QIE10Frame : public Object
		{
			public:
				QIE10Frame() : Object() {}

				virtual void reset()
				{
					for (int i=0; i<10; i++)
					{
						_adc[i] = 0;
						_ltdc[i] = 0;
					}
					_iphi = 0;
					_ieta = 0;
					_depth = 0;
				}
				virtual ~QIE10Frame() {}

				//	public members
				int			_iphi;
				int			_ieta;
				int			_depth;
				int			_adc[10];
				int			_ltdc[10];
		
#ifdef STANDALONE
				ClassDef(QIE10Frame, 1)
#endif
		};

		typedef std::vector<analysis::core::QIE10Frame> QIE10Digis;
	}
}

#ifdef STANDALONE
ClassImpUnique(analysis::core::QIE10Frame, QIE10Frame)
#endif

#endif
