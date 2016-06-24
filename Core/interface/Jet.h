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
				Jet() : Object() {}

				virtual void reset()
				{
					_px = 0;
					_py = 0;
					_pz = 0;
					_pt = 0;
					_eta = 0;
					_phi = 0;
					_mass = 0;
					_charge = 0;
					_partonFlvour = 0;
					_chf = 0;
					_nhf = 0;
					_cef = 0;
					_nef = 0;
					_muf = 0;
					_hfhf = 0;
					_hfef = 0;
					_cm = 0;
					_chm = 0;
					_nhm = 0;
					_cem = 0;
					_nem = 0;
					_mum = 0;
					_hfhm = 0;
					_hfem = 0;
					_jecf = 0;
					_jecu = 0;
					_csv = 0;
				}
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
