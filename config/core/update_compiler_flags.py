
# Copyright (c) 2015 by Radovan Bast and Jonas Juselius
# see https://github.com/cmake-en-papillote/cmake-en-papillote/blob/master/LICENSE

#-------------------------------------------------------------------------------

import sys
import ConfigParser
import glob
import os

#-------------------------------------------------------------------------------

def result_file_is_uptodate(config_path, result_file):
    if os.path.isfile(result_file):
        newest_stamp = 0.0
        for f in glob.glob(os.path.join(config_path, '*.cfg')):
            stamp = os.path.getmtime(f)
            if newest_stamp > stamp: newest_stamp = stamp
        result_stamp = os.path.getmtime(result_file)
        return result_stamp > newest_stamp
    else:
        return False

#-------------------------------------------------------------------------------

def read_flags(config_path):
    """
    get list of all vendors and read in flags
    """
    vendors = []
    flags = {}
    for f in glob.glob(os.path.join(config_path, '*.cfg')):
        config = ConfigParser.ConfigParser()
        config.read(f)
        base = os.path.basename(f)
        vendor = os.path.splitext(base)[0]
        vendors.append(vendor)
        for lang in config.sections():
            for keyword in ['always', 'release', 'debug', 'static', 'coverage', 'int64']:
                try:
                    flags[(vendor, lang, keyword)] = config.get(lang, keyword).replace('\n', ' ')
                except:
                    pass
    return vendors, flags

#-------------------------------------------------------------------------------

def generate_cmake_code(lang, vendors, flags):

    s = []

    s.append('\nif(NOT DEFINED CMAKE_%s_COMPILER_ID)' % lang)
    s.append('    message(FATAL_ERROR "CMAKE_%s_COMPILER_ID variable is not defined! (CMake Error)")' % lang)
    s.append('endif()')

    s.append('\nif(NOT CMAKE_%s_COMPILER_WORKS)' % lang)
    s.append('    message(FATAL_ERROR "CMAKE_%s_COMPILER_WORKS is false! (CMake Error)")' % lang)
    s.append('endif()')

    for vendor in vendors:
        s.append('\nif(CMAKE_%s_COMPILER_ID MATCHES %s)' % (lang, vendor))
        key = (vendor, lang, 'always')
        if key in flags:
            s.append('    set(CMAKE_%s_FLAGS "${CMAKE_%s_FLAGS} %s")' % (lang, lang, flags[key]))
        key = (vendor, lang, 'release')
        if key in flags:
            s.append('    set(CMAKE_%s_FLAGS_RELEASE "%s")' % (lang, flags[key]))
        key = (vendor, lang, 'debug')
        if key in flags:
            s.append('    set(CMAKE_%s_FLAGS_DEBUG "%s")' % (lang, flags[key]))
        key = (vendor, lang, 'static')
        if key in flags:
            s.append('    if(ENABLE_STATIC_LINKING)')
            s.append('        set(CMAKE_%s_FLAGS "${CMAKE_%s_FLAGS} %s")' % (lang, lang, flags[key]))
            s.append('    endif()')
        key = (vendor, lang, 'coverage')
        if key in flags:
            s.append('    if(ENABLE_CODE_COVERAGE)')
            s.append('        set(CMAKE_%s_FLAGS "${CMAKE_%s_FLAGS} %s")' % (lang, lang, flags[key]))
            s.append('    endif()')
        key = (vendor, lang, 'int64')
        if key in flags:
            s.append('    if(ENABLE_64BIT_INTEGERS)')
            s.append('        set(CMAKE_%s_FLAGS "${CMAKE_%s_FLAGS} %s")' % (lang, lang, flags[key]))
            s.append('    endif()')
        s.append('endif()')

    s.append('\nif(DEFINED EXTRA_%s_FLAGS)' % lang)
    s.append('    set(CMAKE_%s_FLAGS "${CMAKE_%s_FLAGS} ${EXTRA_%s_FLAGS}")' % (lang, lang, lang))
    s.append('endif()')

    return '\n'.join(s)

#-------------------------------------------------------------------------------

def main():

    # directory containing config files
    config_path = sys.argv[1]

    # generated cmake file
    result_file = sys.argv[2]

    # list of languages
    languages = sys.argv[3].split()

    if result_file_is_uptodate(config_path, result_file):
        sys.exit(0)

    vendors, flags = read_flags(config_path)

    with open(result_file, 'w') as f:
        f.write('# this file is generated - do not edit!\n')
        for lang in languages:
            f.write(generate_cmake_code(lang, vendors, flags))

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
