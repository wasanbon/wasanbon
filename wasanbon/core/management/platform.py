#!/usr/bin/env python

import os, sys

def get_home_path():
    if sys.platform == 'darwin':
        return os.environ['HOME'] 
    elif sys.platform == 'win32':
        return os.path.join(os.environ['HOMEDRIVE'] , os.environ['HOMEPATH'])
    return 'hoge'
