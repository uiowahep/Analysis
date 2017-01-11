#ifndef Analysis_Core_TestClass3_h
#define Analysis_Core_TestClass3_h

#ifndef STANDALONE
#include "Analysis/Core/interface/Object.h"
#else
#include "Object.h"
#endif

namespace analysis
{
	namespace core
	{
		class TestClass3 : public Object
		{
			public:
				TestClass3() : Object() {this->reset();}

				virtual void reset()
                {
                    _a3 = 0;
                    _b3 = 0.;
                    _c3 = 0.;
                    _d3 = 'x';
                    _e3 = false;
/*
                    for (int ii=0; ii<10; ii++)
                        for (int jj=0; jj<10; jj++)
                        {
                            _aa[ii][jj] = 0;
                            _bb[ii][jj] = 0;
                            _cc[ii][jj] = 0;
                            _dd[ii][jj] = 0;
                            _ee[ii][jj] = 0;
                        }

//                    _f = "abcdefgh";
                    _va.clear();
                    _vb.clear();
                    _vc.clear();
                    _vd.clear();
                    _vva.clear();
                    _vvb.clear();
                    _vvc.clear();
                    _vvd.clear();
                    */
				}
				virtual ~TestClass3() {}
                    
                int _a3;
                float _b3;
                double _c3;
                char _d3;
                bool _e3;

                /*
                int _aa[10][10];
                float _bb[10][10];
                double _cc[10][10];
                char _dd[10][10];
                bool _ee[10][10];

                std::vector<int> _va;
                std::vector<float> _vb;
                std::vector<double> _vc;
                std::vector<char> _vd;
                */
/*
                std::vector<std::vector<int> > _vva;
                std::vector<std::vector<float> > _vvb;
                std::vector<std::vector<double> > _vvc;
                std::vector<std::vector<char> > _vvd;
*/
#ifdef STANDALONE
				ClassDef(TestClass3, 1)
#endif
		};

		typedef std::vector<analysis::core::TestClass3> TestClass3s;
	}
}

//
//	IMPORTANT!!! ROOT uses __LINE__ to generate the unique id......
//	and since we are in a global namespace....
//
#ifdef STANDALONE
ClassImpUnique(analysis::core::TestClass3, TestClass3)
#endif

#endif
