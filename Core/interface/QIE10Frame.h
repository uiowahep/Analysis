#ifndef Analysis_Core_QIE10Frame_h
#define Analysis_Core_QIE10Frame_h

#include <vector>

namespace analysis
{
	namespace core
	{
		class QIE10Frame
		{
			public:
				QIE10Frame() {}
				QIE10Frame(uint32_t id): _id(id)
				{}
				virtual ~QIE10Frame() {}

				//	public members
				uint32_t _id;
		};
	}
}

#endif
