#!/usr/bin/env python

import os
from config.config import configure

options = """
Usage:
  ./setup.py [options] [<builddir>]
  ./setup.py (-h | --help)

Options:
  --fc=<FC>               Fortran compiler [default: gfortran].
  --cc=<CC>               C compiler [default: gcc].
  --cxx=<CXX>             C++ compiler [default: g++].
  --omp                   Enable OpenMP (sets -DENABLE_OMP=ON).
  --mpi                   Enable MPI (sets -DENABLE_MPI=ON).
  --coverage              Enable code coverage (sets -DENABLE_CODE_COVERAGE=ON).
  --mkl=<MKL>             Pass MKL flag to the compiler and linker (sequential, parallel, or cluster).
  --blas=<BLAS>           Specify BLAS library (auto, builtin, none, or full path) [default: auto].
  --lapack=<LAPACK>       Specify LAPACK library (auto, builtin, none, or full path) [default: auto].
  --explicit-libs=<LIBS>  Explicit linker specification for extra libraries; passed directly to the linker.
  --type=<TYPE>           Set the CMake build type (debug, release, relwithdeb, profile) [default: release].
  --show                  Show CMake command and exit. Do not write any files.
  <builddir>              Build directory.
  -h --help               Show this screen.
"""

root_directory = os.path.dirname(os.path.realpath(__file__))

configure(options, root_directory)
