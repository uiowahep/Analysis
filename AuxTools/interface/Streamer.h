/*
 *	Author:
 *	Date:
 *	Description:
 */

#ifndef Analysis_AuxTools_Streamer_h
#define Analysis_AuxTools_Streamer_h

#ifdef STANDALONE

#include "TString.h"
#include "TChain.h"

#include <fstream>
#include <string>
#include <iostream>

namespace analysis
{
	namespace processing
	{
		class Streamer
		{
			public:
				Streamer() : _inputname(""), _tpathname(""), _chain(NULL)
				{}
				Streamer(std::string const& inputname, 
					std::string const& tpathname):
					_inputname(inputname), _tpathname(tpathname)
				{
					_chain = new TChain(_tpathname.c_str());
				}
				virtual ~Streamer() {}

				void chainup();
				void chainup(std::string const& inputname, 
					std::string const& tpathname);

				std::string			_inputname;
				std::string			_tpathname;
				TChain				*_chain;
		};
	}
}

#endif

#endif
