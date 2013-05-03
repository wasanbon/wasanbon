#!/usr/bin/env python

import os, sys

def get_home_path():
    if sys.platform == 'darwin':
        return os.environ['HOME'] 
    return 'hoge'
