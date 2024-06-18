# This will create IMPORTED targets for DLIO_PROFILER. The executables will be
# DLIO_PROFILER::<exe-name>-bin (e.g., DLIO_PROFILER::dlio_profiler-bin) and the library will
# be DLIO_PROFILER::dlio_profiler.

include("${CMAKE_CURRENT_LIST_DIR}/DLIO_PROFILERConfigVersion.cmake")

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/modules")
list(APPEND CMAKE_MODULE_PATH "")

#include(GNUInstallDirs)
include(ExternalProject)
include(DLIO_PROFILERCMakeUtilities)
include(CMakePackageConfigHelpers)


set(DLIO_PROFILER_VERSION ${PACKAGE_VERSION})

# Record compiler information
set(DLIO_PROFILER_C_COMPILER "/usr/bin/cc")
set(DLIO_PROFILER_CXX_COMPILER "/usr/bin/c++")

set(DLIO_PROFILER_C_FLAGS " -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wno-deprecated-declarations")
set(DLIO_PROFILER_CXX_FLAGS " -fPIC -Wall -Wextra -pedantic -Wno-unused-parameter -Wnon-virtual-dtor -Wno-deprecated-declarations")

set(DLIO_PROFILER_C_STANDARD "11")
set(DLIO_PROFILER_CXX_STANDARD "17")

set(CMAKE_C_STANDARD_REQUIRED TRUE)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# Record the various flags and switches accumlated in DLIO_PROFILER
set(DLIO_PROFILER_GNU_LINUX )
set(DLIO_PROFILER_HAS_STD_FILESYSTEM TRUE)
set(DLIO_PROFILER_HAS_STD_FSTREAM_FD TRUE)

# Setup dependencies




# Now actually import the DLIO_PROFILER target
set(_TMP_INCLUDE_DIRS "")
foreach (_DIR ${_TMP_INCLUDE_DIRS})
  set_and_check(_INCLUDE_DIR "${_DIR}")
  list(APPEND DLIO_PROFILER_INCLUDE_DIRS "${_INCLUDE_DIR}")
endforeach (_DIR "${_TMP_INCLUDE_DIRS}")

set(_TMP_LIBRARY_DIRS "")
foreach (_DIR ${_TMP_LIBRARY_DIRS})
  set_and_check(_LIBRARY_DIR "${_DIR}")
  list(APPEND DLIO_PROFILER_LIBRARY_DIRS "${_LIBRARY_DIR}")
endforeach (_DIR ${_TMP_LIBRARY_DIRS})

if (NOT TARGET DLIO_PROFILER::dlio_profiler)
  include(${CMAKE_CURRENT_LIST_DIR}/DLIO_PROFILERTargets.cmake)
endif (NOT TARGET DLIO_PROFILER::dlio_profiler)

check_required_components(DLIO_PROFILER)

set(DLIO_PROFILER_LIBRARIES DLIO_PROFILER::dlio_profiler)
