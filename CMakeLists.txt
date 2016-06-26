#
# build everything with cmake
#

# min version for cmake
cmake_minimum_required(VERSION 2.8)

#	project name
project (Analysis)

#
#	project's versions TODO
#
#set (Analysis_VERSION_MAJOR 1)
#set (Analysis_VERSION_MINOR 0)
#configure_file(
#	"$(PROJECT_SOURCE_DIR)/Config.h.in"
#	"$(PROJECT_BINARY_DIR)/"
#)

#	
#	add ROOT include dir 
#
set (CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR/config})
find_package(ROOT)
include_directories("${ROOT_INCLUDE_DIR}")

#
#	find all the source you need
#
file (GLOB)

#
#	add all the executables
#

#
#	Link against whatever
#
target_link_libraries ()
