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
				Muon() : Track() {}

				virtual void reset()
				{
					_isTrk = 0;
					_isSA = 0;
					_isGlb = 0;
					_isTight = 0;
					_isMedium = 0;
					_isLoose = 0;

					_isPF = 0;

					_normCh2 = 0; 
					_d0BS = 0;
					_dzBS = 0;
					_d0PV = 0;
					_dzPV = 0;

					_nPLs = 0;
					_nTLs = 0;
					_nSLs = 0;

					_nvfrTrk = 0;
					_nvMuHits = 0;
					_nvPHits = 0;
					_nvTrkHits = 0;
					_nvSHits = 0;
					_nSegMts =0 ;
					_nMtsStations = 0;

					_trkIsoSumPt = 0;
					_trkIsoSumPtCorr = 0;

					_hIso = 0;
					_eIso = 0;
					_relCombIso = 0;
					Track::reset();
					_track.reset();
					_isHLTMatched.clear();
					_segmentCompatibility = 0;
					_combinedQChi2LocalPosition = 0;
					_combinedQTrkKink = 0;
				}
				virtual ~Muon() {}

				bool _isTrk;
				bool _isSA;
				bool _isGlb;
				bool _isTight;
				bool _isMedium;
				bool _isLoose;

				bool _isPF;

				int _normCh2;
				float _d0BS;
				float _dzBS;
				float _d0PV;
				float _dzPV;

				int _nPLs;
				int _nTLs;
				int _nSLs;

				float _vfrTrk;
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
				Track _track;

				float _segmentCompatibility;
				float _combinedQChi2LocalPosition;
				float _combinedQTrkKink;
				std::vector<bool> _isHLTMatched;
		};

		typedef std::vector<analysis::core::Muon> Muons;
	}
}

#endif
