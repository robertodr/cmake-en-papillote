
# Copyright (c) 2015 by Radovan Bast and Jonas Juselius
# see https://github.com/cmake-en-papillote/cmake-en-papillote/blob/master/LICENSE

#-------------------------------------------------------------------------------

function(guard_against_in_source in_source_dir in_binary_dir)
    if(${in_source_dir} STREQUAL ${in_binary_dir})
        message(FATAL_ERROR "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there.")
    endif()
endfunction()

function(guard_against_bad_build_types in_build_type)
    string(TOLOWER "${in_build_type}" cmake_build_type_tolower)
    string(TOUPPER "${in_build_type}" cmake_build_type_toupper)

    if(    NOT cmake_build_type_tolower STREQUAL "debug"
       AND NOT cmake_build_type_tolower STREQUAL "release"
       AND NOT cmake_build_type_tolower STREQUAL "relwithdebinfo")
        message(FATAL_ERROR "Unknown build type \"${in_build_type}\". Allowed values are Debug, Release, RelWithDebInfo (case-insensitive).")
    endif()
endfunction()
