#ifndef Analysis_Core_Vertex_h
#define Analysis_Core_Vertex_h

#include "Analysis/Core/interface/Object.h"

namespace analysis
{
	namespace core
	{
		class Vertex : public Object
		{
			public:
				Vertex() : Object()
				{}

				virtual ~Vertex() {}

				int _isValid;
				float _x;
				float _y;
				float _z;
				float _xerr;
				float _yerr;
				float _zerr;
				float _chi2;
				float _ndf;
				float _normChi2;
		};

		typedef std::vector<analysis::core::Vertex> Vertices;
	}
}

#endif
