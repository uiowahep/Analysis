#include "UserCode/Core/interface/Candidate.h"
#include "UserCode/Core/interface/RecHit.h"
#include "UserCode/Core/interface/CaloTower.h"
#include "UserCode/Core/interface/Digi.h"
#include "DataFormats/Common/interface/Wrapper.h"

namespace
{
	struct dictionary
	{
		std::vector<analysis::core::Candidate>		dummy1;
		std::vector<analysis::core::Digi>	dummy8;
		std::vector<analysis::core::Digi10>	dummy9;
		analysis::core::DetId				dummy10;
	};
}
