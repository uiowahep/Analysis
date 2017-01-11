#ifndef Analysis_Core_Root4jTestSet_h
#define Analysis_Core_Root4jTestSet_h

#include "TLorentzVector.h"
#include <string>
#include <bitset>

#ifndef STANDALONE
#include "Analysis/Core/interface/Object.h"
#else
#include "Object.h"
#endif

namespace analysis
{
	namespace core
	{
        class R4JBase
		{
			public:
				R4JBase() {this->reset();}

				virtual void reset()
                {
                    _aaa = 1;
                    _bbb = 2.;
                    _ccc = 3.;
                    _ddd = 'x';
                    _eee = false;
				}
				virtual ~R4JBase() {}
                    
                int _aaa;
                float _bbb;
                double _ccc;
                char _ddd;
                bool _eee;

#ifdef STANDALONE
				ClassDef(R4JBase, 1)
#endif
        };
        
        class DDD
		{
			public:
				DDD() {this->reset();}

				virtual void reset()
                {
                    q = 15;
				}
				virtual ~DDD() {}

                int q;

#ifdef STANDALONE
				ClassDef(DDD, 1)
#endif
        };

        class CCC : public DDD
		{
			public:
				CCC() : DDD() {this->reset();}

				virtual void reset()
                {
                    c1 = 333;
                    c2 = 111;
                    c3 = 222;
				}
				virtual ~CCC() {}
                
                int c1;
                int c2;
                int c3;

#ifdef STANDALONE
				ClassDef(CCC, 1)
#endif
        };

        class BBB : public R4JBase, public CCC
		{
			public:
				BBB(): R4JBase(), CCC() {this->reset();}

				virtual void reset()
                {
                    b1 = 333;
                    b2 = 111;
                    b3 = 222;
                    ccc.reset();
                    vBool.clear();
                    vBool.push_back(false);
                    vBool.push_back(false);
                    vBool.push_back(true);
                    vBool.push_back(true);

                    vCCC.clear();
                    CCC cc;
                    cc.c1 = 1111;
                    cc.c2 = 2222;
                    cc.c3 = 3333;
                    vCCC.push_back(cc);
                    vCCC.push_back(cc);
                    vCCC.push_back(cc);
                    vCCC.push_back(cc);
                    vCCC.push_back(cc);
				}
				virtual ~BBB() {}
                
                CCC ccc;
                std::bitset<256> bits;
                int b1;
                int b2;
                int b3;
                std::vector<CCC> vCCC;
                std::vector<bool> vBool;

#ifdef STANDALONE
				ClassDef(BBB, 1)
#endif
        };

        class AAA : public R4JBase
		{
			public:
				AAA() : R4JBase() {this->reset();}

				virtual void reset()
                {
                    b.reset();
                    a1 = 10;
                    a2 = 10101.5;
                    vb.clear();
                    
                    va3.clear();
                    ma4.clear();
                    vva5.clear();
                    mma6.clear();
				}
				virtual ~AAA() {}

                int a1;
                float a2;
                std::vector<BBB> vb;
                BBB b;
                
                std::vector<int> va3;
                std::map<int, int> ma4;
                std::vector<std::vector<int> > vva5;
                std::map<int, std::map<int, int> > mma6;

#ifdef STANDALONE
				ClassDef(AAA, 1)
#endif
        };

		class R4JSomeObject
		{
			public:
				R4JSomeObject() {this->reset();}

				virtual void reset()
                {
                    _a = 0;
                    _b = 0.;
                    _c = 0.;
                    _d = 'x';
                    _e = false;
				}
				virtual ~R4JSomeObject() {}
                    
                int _a;
                float _b;
                double _c;
                char _d;
                bool _e;

#ifdef STANDALONE
				ClassDef(R4JSomeObject, 1)
#endif
        };

		class R4JObject : public R4JBase
		{
			public:
				R4JObject(): R4JBase() {this->reset();}

				virtual void reset()
                {
                    _aa = 0;
                    _bb = 0.;
                    _cc = 0.;
                    _dd = 'x';
                    _ee = false;
                    _test.reset();
				}
				virtual ~R4JObject() {}

                R4JSomeObject _test;
//                TLorentzVector _v4;
                int _aa;
                float _bb;
                double _cc;
                char _dd;
                bool _ee;

#ifdef STANDALONE
				ClassDef(R4JObject, 1)
#endif
		};
		class SimpleComposite : public R4JObject
		{
			public:
				SimpleComposite() : R4JObject() {this->reset();}

				virtual void reset()
                {
                    _a = 0;
                    _b = 0.;
                    _c = 0.;
                    _d = 'x';
                    _e = false;

                    a.reset();
                    _va.clear();
                    _vb.clear();
                    _vva.clear();
                    _mma.clear();
				}
				virtual ~SimpleComposite() {}
                    
                int _a;
                float _b;
                double _c;
                char _d;
                bool _e;
                AAA a;
                std::vector<int> _va;
                std::vector<float> _vb;
                std::vector<std::vector<int> > _vva;
                std::map<int, std::map<int, int> > _mma;

#ifdef STANDALONE
				ClassDef(SimpleComposite, 1)
#endif
		};

        class NestedComposite : public R4JObject
        {
            public :
                NestedComposite(): R4JObject() {this->reset();}

                virtual void reset()
                {
                    _simpleComposite1.reset();
                    _simpleComposite2.reset();
                    _a = 0;
                    _b = 0;
                    _va.clear();
                    _vb.clear();
                }
                virtual ~NestedComposite() {}

                SimpleComposite _simpleComposite1;
                SimpleComposite _simpleComposite2;
                int _a;
                float _b;
                std::vector<int> _va;
                std::vector<float> _vb;

#ifdef STANDALONE
				ClassDef(NestedComposite, 1)
#endif

        };
        
        class AnotherNestedComposite : public R4JObject
        {
            public :
                AnotherNestedComposite(): R4JObject() {this->reset();}

                virtual void reset()
                {
                    _simpleComposite1.reset();
                    _simpleComposite2.reset();
                    _another.reset();
                    vBool.clear();
                    _x = 123;
                    _y = 456;
                    vAAA.clear();
                }
                virtual ~AnotherNestedComposite() {}

                SimpleComposite _simpleComposite1;
                SimpleComposite _simpleComposite2;
                NestedComposite _another;
                int _x;
                int _y;
                std::vector<AAA> vAAA;
                std::vector<bool> vBool;

#ifdef STANDALONE
				ClassDef(AnotherNestedComposite, 1)
#endif

        };

		typedef std::vector<analysis::core::SimpleComposite> SimpleComposites;
	}
}

//
//	IMPORTANT!!! ROOT uses __LINE__ to generate the unique id......
//	and since we are in a global namespace....
//
#ifdef STANDALONE
ClassImpUnique(analysis::core::R4JObject, R4JObject)
ClassImpUnique(analysis::core::R4JBase, R4JBase)
ClassImpUnique(analysis::core::AAA, AAA)
ClassImpUnique(analysis::core::DDD, DDD)
ClassImpUnique(analysis::core::R4JSomeObject, R4JSomeObject)
ClassImpUnique(analysis::core::SimpleComposite, SimpleComposite)
ClassImpUnique(analysis::core::NestedComposite, NestedComposite)
ClassImpUnique(analysis::core::AnotherNestedComposite, AnotherNestedComposite)
#endif

#endif
