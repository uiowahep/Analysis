#
# build everything with cmake
#

# min version for cmake
cmake_minimum_required(VERSION 2.8.0)

#	project name
project (Analysis)

message (SOURCE DIRECTORY = ${PROJECT_SOURCE_DIR})
message (BUILD DIRECTORY = ${PROJECT_BINARY_DIR})

#
#	Compiler flags and some definitions
#
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
add_definitions(-DSTANDALONE=1)

#
#	project's versions and some other env vars to pass
#
set (Analysis_VERSION_MAJOR 1)
set (Analysis_VERSION_MINOR 0)
configure_file(
	"${PROJECT_SOURCE_DIR}/config/config.h.in"
	"${PROJECT_BINARY_DIR}/config/config.h"
)

#
#	add the config.h to the search include path and enable
#
include_directories("${PROJECT_BINARY_DIR}/config")
option (STANDALONE
	"Compile and build in standalone mode without CMSSW" ON
)

#
#	Find BOOST
#
find_package(Boost COMPONENTS program_options system REQUIRED )
include_directories("${Boost_INCLUDE_DIRS}")
set (EXTRA_LIBS ${EXTRA_LIBS} ${Boost_LIBRARIES})
add_definitions(${})

#	
#	find and add ROOT
#
set (CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/config)
find_package(ROOT REQUIRED COMPONENTS RHTTP)
include_directories("${ROOT_INCLUDE_DIR}")
add_definitions(${ROOT_CXX_FLAGS})

#
#	add ROOT to the eet of libraries to link against
#
set (EXTRA_LIBS ${EXTRA_LIBS} ${ROOT_LIBRARIES})

#
#	add the includes to the search path
#
include_directories ("${PROJECT_SOURCE_DIR}/Core/interface")
include_directories ("${PROJECT_SOURCE_DIR}/NtupleProcessing/interface")
include_directories ("${PROJECT_SOURCE_DIR}/AuxTools/interface")
include_directories ("${PROJECT_SOURCE_DIR}/Drivers/interface")

#
#	Generate ROOT Dictionary and Shared Lib
#
ROOT_GENERATE_DICTIONARY(G__Core 
	${PROJECT_SOURCE_DIR}/Core/interface/Object.h
	${PROJECT_SOURCE_DIR}/Core/interface/Track.h
	${PROJECT_SOURCE_DIR}/Core/interface/Muon.h
	${PROJECT_SOURCE_DIR}/Core/interface/GenJet.h
	${PROJECT_SOURCE_DIR}/Core/interface/Jet.h
	${PROJECT_SOURCE_DIR}/Core/interface/GenParticle.h
	${PROJECT_SOURCE_DIR}/Core/interface/MET.h
	${PROJECT_SOURCE_DIR}/Core/interface/Vertex.h
	${PROJECT_SOURCE_DIR}/Core/interface/Event.h
    ${PROJECT_SOURCE_DIR}/Core/interface/QIE8Frame.h
	${PROJECT_SOURCE_DIR}/Core/interface/MetaHiggs.h
	${PROJECT_SOURCE_DIR}/Core/interface/QIE10Frame.h
    ${PROJECT_SOURCE_DIR}/Core/interface/Electron.h
    ${PROJECT_SOURCE_DIR}/Core/interface/Tau.h
	LINKDEF ${PROJECT_SOURCE_DIR}/config/LinkDef.h
	OPTIONS -DSTANDALONE=1
)
add_library(AnalysisCore SHARED G__Core.cxx)
target_link_libraries(AnalysisCore ${ROOT_LIBRARIES})
set (EXTRA_LIBS ${EXTRA_LIBS} AnalysisCore)

#
#	Add Ntuple Processing as shared lib but compiled as a ROOT dictionary
#
ROOT_GENERATE_DICTIONARY(G__NtupleProcessing
	${PROJECT_SOURCE_DIR}/NtupleProcessing/interface/Streamer.h
	LINKDEF ${PROJECT_SOURCE_DIR}/config/LinkDef.h
	OPTIONS -DSTANDALONE=1
)
add_library(AnalysisNtupleProcessing SHARED 
	${PROJECT_SOURCE_DIR}/NtupleProcessing/src/Streamer.cc 
	G__NtupleProcessing.cxx
)
target_link_libraries(AnalysisNtupleProcessing ${ROOT_LIBRARIES})
set (EXTRA_LIBS ${EXTRA_LIBS} AnalysisNtupleProcessing)

#
#	Add the headers to compile against
#
file (GLOB HEADERS ${PROJECT_SOURCE_DIR}/AuxTools/interface/*.h)
file (GLOB HEADERS1 ${PROJECT_SOURCE_DIR}/Drivers/interface/*.h)
set (HEADERS ${HEADERS} ${HEADERS1})

#
#	add all the executables and link against ROOT
#
file (GLOB MAIN_FILES1 ${PROJECT_SOURCE_DIR}/Drivers/test/*.cc)
file (GLOB MAIN_FILES2 ${PROJECT_SOURCE_DIR}/Drivers/bin/*.cc)
foreach (MAIN_FILE ${MAIN_FILES1})
	string(REPLACE ".cc" "" EXECUTABLE_NAME ${MAIN_FILE})
	string(REPLACE "${PROJECT_SOURCE_DIR}/Drivers/test/" "" 
		EXECUTABLE_NAME ${EXECUTABLE_NAME}
	)
	message("Adding Executable: ${EXECUTABLE_NAME}")
	#	add_executable(${EXECUTABLE_NAME} ${MAIN_FILE} ${SOURCES} ${HEADERS})
	add_executable(${EXECUTABLE_NAME} ${MAIN_FILE} ${HEADERS})
	target_link_libraries (${EXECUTABLE_NAME} ${EXTRA_LIBS})
endforeach(MAIN_FILE)
foreach (MAIN_FILE ${MAIN_FILES2})
	string(REPLACE ".cc" "" EXECUTABLE_NAME ${MAIN_FILE})
	string(REPLACE "${PROJECT_SOURCE_DIR}/Drivers/bin/" "" 
		EXECUTABLE_NAME ${EXECUTABLE_NAME}
	)
	message("Adding Executable: ${EXECUTABLE_NAME}")
	#add_executable(${EXECUTABLE_NAME} ${MAIN_FILE} ${SOURCES} ${HEADERS})
	add_executable(${EXECUTABLE_NAME} ${MAIN_FILE} ${HEADERS})
	target_link_libraries (${EXECUTABLE_NAME} ${EXTRA_LIBS})
endforeach(MAIN_FILE)

#
#	copy whatever you need
#	For Python Processing - copy python folders as well with purely python stuff
#
file (GLOB ALL_SCRIPTS ${PROJECT_SOURCE_DIR}/scripts/*.*)
file (GLOB ALL_CONFIG ${PROJECT_SOURCE_DIR}/config/*.*)
file (GLOB ALL_RESOURCES ${PROJECT_SOURCE_DIR}/resources/*.*)
file (COPY ${ALL_SCRIPTS} DESTINATION ${PROJECT_BINARY_DIR}/scripts)
file (COPY ${ALL_CONFIG} DESTINATION ${PROJECT_BINARY_DIR}/config)
file (COPY ${ALL_RESOURCES} DESTINATION ${PROJECT_BINARY_DIR}/resources)
file (COPY ${PROJECT_SOURCE_DIR}/AuxTools/python DESTINATION ${PROJECT_BINARY_DIR}/AuxTools)
file (COPY ${PROJECT_SOURCE_DIR}/NtupleProcessing/python DESTINATION ${PROJECT_BINARY_DIR}/NtupleProcessing)
