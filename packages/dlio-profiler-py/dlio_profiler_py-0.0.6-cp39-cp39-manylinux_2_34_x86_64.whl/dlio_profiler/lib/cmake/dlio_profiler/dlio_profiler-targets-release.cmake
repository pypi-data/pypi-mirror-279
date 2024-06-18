#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "dlio_profiler" for configuration "Release"
set_property(TARGET dlio_profiler APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(dlio_profiler PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libdlio_profiler.so.2.0.1"
  IMPORTED_SONAME_RELEASE "libdlio_profiler.so.2.0.1"
  )

list(APPEND _cmake_import_check_targets dlio_profiler )
list(APPEND _cmake_import_check_files_for_dlio_profiler "${_IMPORT_PREFIX}/lib/libdlio_profiler.so.2.0.1" )

# Import target "dlio_profiler_preload" for configuration "Release"
set_property(TARGET dlio_profiler_preload APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(dlio_profiler_preload PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libdlio_profiler_preload.so"
  IMPORTED_SONAME_RELEASE "libdlio_profiler_preload.so"
  )

list(APPEND _cmake_import_check_targets dlio_profiler_preload )
list(APPEND _cmake_import_check_files_for_dlio_profiler_preload "${_IMPORT_PREFIX}/lib/libdlio_profiler_preload.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
