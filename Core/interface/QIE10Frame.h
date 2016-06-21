#ifndef Analysis_Core_QIE10Frame_h
#define Analysis_Core_QIE10Frame_h

#include <vector>

#include "DataFormats/HcalDetId/interface/HcalDetId.h"

namespace analysis
{
	namespace core
	{
		class QIE10Frame
		{
			public:
				QIE10Frame() {}
				QIE10Frame(HcalDetId const& id): _did(id)
				{}
				virtual ~QIE10Frame() {}

				//	public members
				HcalDetId	_did;
				int			_adc[10];
				int			_ltdc[10];
//				int			_ttdc[10];
		};

		typedef std::vector<analysis::core::QIE10Frame> QIE10Digis;
	}
}

#endif
