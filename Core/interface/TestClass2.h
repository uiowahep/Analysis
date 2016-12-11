#ifndef Analysis_Core_TestClass2_h
#define Analysis_Core_TestClass2_h

#ifndef STANDALONE
#include "Analysis/Core/interface/Object.h"
#else
#include "Object.h"
#endif

namespace analysis
{
	namespace core
	{
		class TestClass2 : public Object
		{
			public:
				TestClass2() : Object() {this->reset();}

				virtual void reset()
                {
                    _a = 0;
                    _b = 0.;
                    _c = 0.;
                    _d = 'x';
                    _e = false;
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
				virtual ~TestClass2() {}
                    
                int _a;
                float _b;
                double _c;
                char _d;
                bool _e;

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
				ClassDef(TestClass2, 1)
#endif
		};

		typedef std::vector<analysis::core::TestClass2> TestClass2s;
	}
}

//
//	IMPORTANT!!! ROOT uses __LINE__ to generate the unique id......
//	and since we are in a global namespace....
//
#ifdef STANDALONE
ClassImpUnique(analysis::core::TestClass2, TestClass2)
#endif

#endif
