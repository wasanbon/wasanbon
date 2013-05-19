#!/usr/bin/env python
import os, sys
import wasanbon

def is_cpprtm_installed():

    if sys.platform == 'darwin':
        file = 'version.txt'
        path = '/usr/local/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        path = '/usr/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        if ('RTM_ROOT' in os.environ.keys()):
            if os.path.isfile(os.environ['RTM_ROOT'], 'rtm', file):
                return True
        return False

    elif sys.platform == 'linux2':
        file = 'version.txt'
        path = '/usr/local/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        path = '/usr/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        if ('RTM_ROOT' in os.environ.keys()):
            if os.path.isfile(os.environ['RTM_ROOT'], 'rtm', file):
                return True
        return False

    elif sys.platform == 'win32':
        file = 'version.txt'
        path = 'C:\\Program Files (x86)\\OpenRTM-aist\\1.1\\rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        path = 'C:\\Program Files\\OpenRTM-aist\\1.1\\rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        if ('RTM_ROOT' in os.environ.keys()):
            if os.path.isfile(os.environ['RTM_ROOT'], 'rtm', file):
                return True
        return False

    return False


def is_pyrtm_installed():
    try:
        import OpenRTM_aist
        return True
    except ImportError, e:
        return False
    pass

def is_javartm_installed():
    return os.path.isfile(os.path.join(wasanbon.setting['common']['path']['RTM_ROOT_JAVA'], wasanbon.setting['common']['file']['RTM_JAR']))


