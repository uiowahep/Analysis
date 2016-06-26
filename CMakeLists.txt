#
# build everything with cmake
#

# min version for cmake
cmake_minimum_required(VERSION 2.8)

#	project name
project (Analysis)

message (SOURCE DIRECTORY = ${PROJECT_SOURCE_DIR})
message (BUILD DIRECTORY = ${PROJECT_BINARY_DIR})

#
#	Compiler flags
#
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

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
#	find and add ROOT
#
set (CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/config)
find_package(ROOT)
include_directories("${ROOT_INCLUDE_DIR}")

#
#	add ROOT to the eet of libraries to link against
#
set (EXTRA_LIBS ${EXTRA_LIBS} ${ROOT_LIBRARIES})

#
#	add the includes to the search path
#
include_directories ("${PROJECT_SOURCE_DIR}/Core/interface")

#
#	Since we do not build any .a static libs, we have to compile against them
#
file (GLOB headers ${PROJECT_SOURCE_DIR}/Core/interface/*.h)

#
#	add all the executables
#
add_executable(test_dimuon 
	${PROJECT_SOURCE_DIR}/NtupleProcessing/test/test_dimuon.cc ${headers}
)
add_executable(test_qie10
	${PROJECT_SOURCE_DIR}/NtupleProcessing/test/test_qie10.cc ${headers}
)

#
#	Link against whatever
#
target_link_libraries (test_dimuon ${EXTRA_LIBS})
target_link_libraries (test_qie10 ${EXTRA_LIBS})
