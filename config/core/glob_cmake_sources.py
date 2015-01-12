
# Copyright (c) 2015 by Radovan Bast and Jonas Juselius
# see https://github.com/cmake-en-papillote/cmake-en-papillote/blob/master/LICENSE

#-------------------------------------------------------------------------------

import sys
import glob
import os

#-------------------------------------------------------------------------------

def main():

    directory_to_glob_in = sys.argv[1]

    l = glob.glob(os.path.join(directory_to_glob_in, '*.cmake'))

    for f in l:
        base = os.path.basename(f)
        print('include(%s)' % os.path.splitext(base)[0])

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
