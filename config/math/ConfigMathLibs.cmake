
# Copyright (c) 2015 by Radovan Bast and Jonas Juselius
# see https://github.com/cmake-en-papillote/cmake-en-papillote/blob/master/LICENSE

#-------------------------------------------------------------------------------

# variables used:
#     - MATH_LIB_SEARCH_ORDER, example: set(MATH_LIB_SEARCH_ORDER MKL ESSL ATLAS ACML SYSTEM_NATIVE)
#     - ENABLE_BLAS
#     - ENABLE_LAPACK
#     - BLAS_FOUND
#     - LAPACK_FOUND
#     - BLAS_LANG
#     - LAPACK_LANG
#     - ENABLE_64BIT_INTEGERS

# variables set:
#     - MATH_LIBS
#     - BLAS_FOUND
#     - LAPACK_FOUND

#-------------------------------------------------------------------------------

foreach(_service BLAS LAPACK)
    if(NOT ${_service}_LANG)
        set(${_service}_LANG C)
    elseif(${_service}_LANG STREQUAL "C" OR ${_service}_LANG STREQUAL "CXX")
        set(${_service}_LANG C)
    elseif(NOT ${_service}_LANG STREQUAL "Fortran")
        message(FATAL_ERROR "Invalid ${_service} library linker language: ${${_service}_LANG}")
    endif()
endforeach()

include(MathLibsDefinitions)
include(MathLibsFunctions)

set(MATH_LIBS)

foreach(_service BLAS LAPACK)
    if(ENABLE_${_service} AND NOT ${_service}_FOUND)
        config_math_service(${_service})
        if(${_service}_FOUND)
            include_directories(${${_service}_INCLUDE_DIRS})
        endif()
    endif()
endforeach()
