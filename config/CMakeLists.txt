
# Copyright (c) 2015 by Radovan Bast and Jonas Juselius
# see https://github.com/cmake-en-papillote/cmake-en-papillote/blob/master/LICENSE

#-------------------------------------------------------------------------------

# set minimum cmake version
cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

# do not rebuild if rules (compiler flags) change
set(CMAKE_SKIP_RULE_DEPENDENCY TRUE)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/config/core)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/config/math)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/compilers)

# python interpreter is required at many places during configuration and build
find_package(PythonInterp REQUIRED)

# determine program version from file, example: "14.1"
file(READ "${PROJECT_SOURCE_DIR}/VERSION" PROGRAM_VERSION)
string(STRIP "${PROGRAM_VERSION}" PROGRAM_VERSION)

# generated cmake files will be written to this path
file(MAKE_DIRECTORY ${PROJECT_BINARY_DIR}/generated_cmake)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_BINARY_DIR}/generated_cmake)

# on Cray configure with -D MPI_FOUND=1
option(ENABLE_MPI "Enable MPI parallelization" OFF)
if(ENABLE_MPI AND NOT MPI_FOUND)
    find_package(MPI)
    if(MPI_FOUND)
        set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} ${MPI_COMPILE_FLAGS}")
        include_directories(${MPI_INCLUDE_PATH})
    else()
        message(FATAL_ERROR "-- You asked for MPI, but CMake could not find any MPI installation, check $PATH")
    endif()
endif()

# collect cmake includes from local directories
foreach(_dir pre_build pre_link body post_build)
    if(IS_DIRECTORY ${PROJECT_SOURCE_DIR}/local/${_dir})
        set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PROJECT_SOURCE_DIR}/local/${_dir})
        exec_program(
            ${PYTHON_EXECUTABLE}
            ${PROJECT_SOURCE_DIR}/config/core
            ARGS glob_cmake_sources.py ${PROJECT_SOURCE_DIR}/local/${_dir} > ${PROJECT_BINARY_DIR}/generated_cmake/config_local_${_dir}.cmake
            OUTPUT_VARIABLE _discard # we don't care about the output
            )
    endif()
endforeach()

if(EXISTS ${PROJECT_BINARY_DIR}/generated_cmake/config_local_pre_build.cmake)
    include(config_local_pre_build)
endif()

# not sure these two should be here
option(ENABLE_64BIT_INTEGERS "Enable 64-bit integers" OFF)
option(ENABLE_CODE_COVERAGE "Enable code coverage" OFF)

# place where fortran modules reside
set(CMAKE_Fortran_MODULE_DIRECTORY ${PROJECT_BINARY_DIR}/modules)

# parse compiler flags
exec_program(
    ${PYTHON_EXECUTABLE}
    ${PROJECT_SOURCE_DIR}/config/core
    ARGS update_compiler_flags.py ${PROJECT_SOURCE_DIR}/compilers ${PROJECT_BINARY_DIR}/generated_cmake/compiler_flags.cmake 'Fortran C CXX'
    OUTPUT_VARIABLE _discard # we don't care about the output
    )
include(compiler_flags) # generated

# guards against in-source builds and bad build types
include(safe_guards)
guard_against_in_source(${PROJECT_SOURCE_DIR} ${PROJECT_BINARY_DIR})
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Debug")
endif()
guard_against_bad_build_types(${CMAKE_BUILD_TYPE})

# forward CPP directly to the code
set(CPP)
if(NOT "${CPP}" STREQUAL "")
    add_definitions(${CPP})
endif()

if(EXISTS ${PROJECT_BINARY_DIR}/generated_cmake/config_local_pre_link.cmake)
    include(config_local_pre_link)
endif()

if(EXISTS ${PROJECT_BINARY_DIR}/generated_cmake/config_local_body.cmake)
    include(config_local_body)
endif()

include(config_info)

if(EXISTS ${PROJECT_BINARY_DIR}/generated_cmake/config_local_post_build.cmake)
    include(config_local_post_build)
endif()
