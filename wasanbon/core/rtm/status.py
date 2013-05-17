#!/usr/bin/env python
import os, sys
import wasanbon

def is_cpprtm_installed():
    #if platform.system() == 'Linux':
    #elif platform.system() == 'Windows':
    #elif platform.system() == 'Darwin':
    #else:
    #  print 'Unknown System (%s)' % platform.system()
    #  return None
    if sys.platform == 'darwin':
        file = 'version.txt'
        path = '/usr/local/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        path = '/usr/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
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
        return False

    return ('RTM_ROOT' in os.environ.keys())


def is_pyrtm_installed():
    try:
        import OpenRTM_aist
        return True
    except ImportError, e:
        return False
    pass

def is_javartm_installed():
    return os.path.isfile(os.path.join(wasanbon.setting['common']['path']['RTM_ROOT_JAVA'], wasanbon.setting['common']['file']['RTM_JAR']))


