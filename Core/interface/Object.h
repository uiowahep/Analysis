#ifndef Object_h
#define Object_h

/**
 *	file:
 *	Author:
 *	Description:
 */

#include <iostream>
#include <string>

using namespace std;

namespace analysis
{
	namespace core
	{
		class Object
		{
			public:
				Object() :
					_name(string("Object1"))
				{}
				Object(string name, int v=0, bool supwarn=false) :
					_name(name), _verbosity(v), _supwarn(supwarn)
				{}
				virtual ~Object() {}

				inline void log(string const& msg) const
				{
					if (_verbosity<=0)
						return;

					cout  << "%MSG" << endl
						<< "%MSG-LOG Analysis::" << _name << "::" << msg
						<< endl;
				}

				inline oid warn(string const& msg) const
				{
					if (_supwarn)
						return;

					cout << "%MSG" << endl
						<< "%MSG-WARN Analysis::" << _name << "::" << msg
						<< endl;
						
				}

			protected:
				string	_name;
				int		_verbosity;
				bool	_supwarn;
		};
	}
}

#endif


