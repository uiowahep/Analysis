#ifndef Analysis_Core_QIE8Frame_h
#define Analysis_Core_QIE8Frame_h

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
		class QIE8Frame : public Object
		{
			public:
				QIE8Frame() : Object() {this->reset();}

				virtual void reset()				
				{
                    _adc.clear();
                    _nominal_fC.clear();
					_iphi = 0;
					_ieta = 0;
					_depth = 0;
				}
				virtual ~QIE8Frame() {}

				//	public members
				int			_iphi;
				int			_ieta;
				int			_depth;
                std::vector<int>			_adc;
                std::vector<double>		_nominal_fC;

#ifdef STANDALONE
				ClassDef(QIE8Frame, 1)
#endif
		};

		typedef std::vector<analysis::core::QIE8Frame> QIE8Digis;
	}
}

#ifdef STANDALONE
ClassImpUnique(analysis::core::QIE8Frame, QIE8Frame)
#endif

#endif
