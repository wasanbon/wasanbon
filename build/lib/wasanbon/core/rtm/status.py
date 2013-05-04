#!/usr/bin/env python

import wasanbon
import os, sys

from wasanbon.core.management import *

def is_cpprtm_installed():
    #if platform.system() == 'Linux':
    #elif platform.system() == 'Windows':
    #elif platform.system() == 'Darwin':
    #else:
    #  print 'Unknown System (%s)' % platform.system()
    #  return None
    return ('RTM_ROOT' in os.environ.keys())

def is_pyrtm_installed():
    try:
        import OpenRTM_aist
        return True
    except ImportError, e:
        return False
    pass

def is_javartm_installed():
    setting = load_settings()
    return os.path.isfile(os.path.join(setting['common']['path']['RTM_ROOT_JAVA'], setting['common']['file']['RTM_JAR']))

def get_status():
    ret = {'c++' : is_cpprtm_installed() ,
           'python' : is_pyrtm_installed() ,
           'java' : is_javartm_installed() }
    return ret

