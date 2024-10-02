#ifndef Analysis_Maker_CommonHeaders_h
#define Analysis_Maker_CommonHeaders_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h" 
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/stream/EDAnalyzer.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/View.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "CondFormats/RunInfo/interface/RunInfo.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"

#endif
