#ifndef Analysis_Core_Electron_h
#define Analysis_Core_Electron_h

#ifndef STANDALONE
#include "Analysis/Core/interface/Track.h"
#else
#include "Track.h"
#endif

namespace analysis
{
    namespace core
    {
        class Electron : public Track
        {
            public:
                Electron() : Track() {this->reset();}
                virtual ~Electron() {}
                virtual void reset()
                {
                    Track::reset();
                    _ids.clear();
                    _trackIso = 0;
                    _ecalIso = 0;
                    _hcalIso = 0;
                    _dz = 0;
                    _isPF = false;
                }

                std::vector<bool> _ids;
                float _trackIso;
                float _ecalIso;
                float _hcalIso;
                double _dz;
                bool _isPF;
                bool _convVeto;

#ifdef STANDALONE
                ClassDef(Electron, 1)
#endif
        };

        typedef std::vector<analysis::core::Electron> Electrons;
    }
}

#ifdef STANDALONE
ClassImpUnique(analysis::core::Electron, Electron)
#endif

#endif
