#include "Analysis/Core/interface/Object.h"
#include "Analysis/Core/interface/QIE10Frame.h"
#include "Analysis/Core/interface/QIE8Frame.h"
#include "Analysis/Core/interface/Event.h"
#include "Analysis/Core/interface/GenParticle.h"
#include "Analysis/Core/interface/Jet.h"
#include "Analysis/Core/interface/Muon.h"
#include "Analysis/Core/interface/Vertex.h"
#include "Analysis/Core/interface/GenJet.h"
#include "Analysis/Core/interface/MET.h"
#include "Analysis/Core/interface/Track.h"
#include "Analysis/Core/interface/Tau.h"
#include "Analysis/Core/interface/Electron.h"
#include "Analysis/Core/interface/MetaHiggs.h"
#include "DataFormats/Common/interface/Wrapper.h"

namespace
{
	struct dictionary
	{
		analysis::core::Objects dumm0;
		analysis::core::QIE10Digis dumm1;
		analysis::core::QIE8Digis dumm2;
		analysis::core::Events dumm3;
		analysis::core::GenParticles dumm4;
		analysis::core::Jets dumm5;
		analysis::core::Muons dumm6;
		analysis::core::Vertices dumm7;
		analysis::core::GenJets dumm8;
		analysis::core::METs dumm9;
		analysis::core::Tracks dumm10;
		analysis::dimuon::MetaHiggs dumm12;
		analysis::core::EventAuxiliaries dumm13;
        analysis::core::Taus dumm14;
        analysis::core::Electrons dumm15;
		analysis::dimuon::Auxiliary dumm16;
	};
}
