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
				Object(){}
				virtual ~Object() {}
		};

		typedef std::vector<analysis::core::Object> Objects;
	}
}

#endif


