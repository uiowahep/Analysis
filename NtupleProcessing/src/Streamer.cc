#ifdef STANDALONE

#include "Streamer.h"

namespace analysis
{
	namespace processing
	{
		void Streamer::chainup(std::string const& inputname, 
			std::string const& tpathname)
		{
			_inputname = inputname;
			_tpathname = tpathname;
			_chain = new TChain(_tpathname.c_str());
			chainup();
		}

		void Streamer::chainup()
		{
			std::cout << "### Chaining all the data files" << std::endl;
			std::ifstream input(_inputname);
			for (std::string line; std::getline(input, line); )
			{
				_chain->Add(TString(line.c_str()));
			}

			std::cout << "### Total Entries=" << _chain->GetEntries() 
				<< std::endl;
		}
	}
}

#endif
