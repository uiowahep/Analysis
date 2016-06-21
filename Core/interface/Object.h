#ifndef Analysis_Core_Object_h
#define Analysis_Core_Object_h

/**
 *	file:
 *	Author:
 *
 *	Description:	Common Base Class 
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
				Object() :	_name(string("Object1")) {}
				Object(std::string const& n) :
					_name(n)
				{}
				virtual ~Object() {}

				//	public members!
				string	_name;
		};
	}
}

#endif


