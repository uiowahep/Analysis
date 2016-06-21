#include "DataFormats/HcalDigi/interface/HFDataFrame.h"
#include "DataFormats/HcalDigi/interface/HBHEDataFrame.h"
#include "DataFormats/HcalDigi/interface/HODataFrame.h"
#include "DataFormats/HcalDigi/interface/QIE10DataFrame.h"
#include "DataFormats/HcalDigi/interface/QIE11DataFrame.h"
#include "DataFormats/Common/interface/Wrapper.h"

namespace
{
	struct dictionary
	{
		std::vector<HFDataFrame> dumm0;
		std::vector<HBHEDataFrame> dumm1;
		std::vector<HODataFrame> dumm2;

		std::vector<QIE10DataFrame> dumm3;
		std::vector<QIE11DataFrame> dumm4;
	}
}
