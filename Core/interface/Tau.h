#ifndef Analysis_Core_Tau_h
#define Analysis_Core_Tau_h

#ifndef STANDALONE
#include "Analysis/Core/interface/Track.h"
#else
#include "Track.h"
#endif

namespace analysis
{
    namespace core
    {
        class Tau : public Track
        {
            public:
                Tau() : Track() {this->reset();}
                virtual ~Tau() {}
                virtual void reset()
                {
                    Track::reset();
                    _ids.clear();
                    _isPF = false;
                }

                std::vector<float> _ids;
                bool _isPF;

#ifdef STANDALONE
                ClassDef(Tau, 1)
#endif
        };

        typedef std::vector<analysis::core::Tau> Taus;
    }
}

#ifdef STANDALONE
ClassImpUnique(analysis::core::Tau, Tau)
#endif

#endif
