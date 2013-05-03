#!/usr/bin/env python

import sys, os

__path = os.path.join(os.path.dirname(__file__), "TPR_CORE_PATH")
if __path not in sys.path:
    sys.path.append(__path)
del __path


def import_module(name):
    __import__(name)
    return sys.modules[name]


def yes_no(msg):
    print '%s (y/n)' % msg
    while True:
        c = raw_input()
        if c[0] == 'y':
            return 'yes'
        else:
            return 'no'


from platform import *
from Application import *
from OptionParserEx import OptionParserEx
from loader import *
