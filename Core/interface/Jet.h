#ifndef Analysis_Core_Jet_h
#define Analysis_Core_Jet_h

#include "Analysis/Core/interface/Object.h"

namespace analysis
{
	namespace core
	{
		class Jet : public Object
		{
			public:
				Jet() : Object()
				{}
				virtual ~Jet() {}

				float _px;
				float _py;
				float _pz;
				float _pt;
				float _eta;
				float _phi;
				float _mass;
				float _charge;
				float _partonFlavour;

				float _chf;
				float _nhf;
				float _cef;
				float _nef;
				float _muf;
				float _hfhf;
				float _hfef;
				float _cm;
				float _chm;
				float _nhm;
				float _cem;
				float _nem;
				float _mum;
				float _hfhm;
				float _hfem;
				float _jecf;
				float _jecu;
				float _csv;
		};

		typedef std::vector<analysis::core::Jet> Jets;
	}
}

#endif
