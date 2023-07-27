# ------------------------------------------------------------------------- #
# Global Workflow
# ------------------------------------------------------------------------- #

# Check for minimim cmake requirement
cmake_minimum_required( VERSION 3.20 FATAL_ERROR )

project(global_workflow VERSION 1.0.0)

include(GNUInstallDirs)
enable_testing()

# Build type.
if(NOT CMAKE_BUILD_TYPE MATCHES "^(Debug|Release|RelWithDebInfo|MinSizeRel)$")
  message(STATUS "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE
      "Release"
      CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
                                               "MinSizeRel" "RelWithDebInfo")
endif()

option(BUILD_GFS_UTILS "Build GFS utilities" ON)
option(BUILD_UFS_UTILS "Build UFS utilities" OFF)  # TODO: Await PR in ufs-utils
option(BUILD_GSI_MONITOR "Build GSI monitoring utilities" ON)

add_subdirectory(sorc)
