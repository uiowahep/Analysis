#ifndef Analysis_Core_Muon_h
#define Analysis_Core_Muon_h

#include "Analysis/Core/interface/Track.h"

namespace analysis
{
	namespace core
	{
		class Muon : public Track
		{
			public:
				Muon() : Track()
				{}
				virtual ~Muon() {}

				int _isTrk;
				int _isSA;
				int _isGlb;
				int _isTight;
				int _isMedium;
				int _isLoose;

				int _normCh2;
				float _d0BS;
				float _dzBS;
				float _d0PV;
				float _dzPV;

				int _nPLs;
				int _nTLs;
				int _nSLs;

				float _nvfrTrk;
				int _nvMuHits;
				int _nvPHits;
				int _nvTrkHits;
				int _nvSHits;
				int _nSegMts;
				int _nMtsStations;

				float _trkIsoSumPt;
				float _trkIsoSumPtCorr;

				float _hIso;
				float _eIso;
				float _relCombIso;
		};

		typedef std::vector<analysis::core::Muon> Muons;
	}
}

#endif
