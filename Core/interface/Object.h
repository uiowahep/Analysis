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
#include <vector>
#include <list>
#include <set>
#include <array>
#include <map>

using namespace std;

#ifdef STANDALONE
#include "TObject.h"
#endif

namespace analysis
{
	namespace core
	{
		class Object
		{
			public:
				Object(){this->reset();}
				virtual ~Object() {}

				virtual void reset() {}

#ifdef STANDALONE
				ClassDef(Object, 1)
#endif
		};

		typedef std::vector<analysis::core::Object> Objects;
	}
}

//
//	Unique!
//
#ifdef STANDALONE
ClassImpUnique(analysis::core::Object, Object)
#endif

#endif


