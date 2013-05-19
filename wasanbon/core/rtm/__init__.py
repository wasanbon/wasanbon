import os, sys, shutil, subprocess

import wasanbon
from . import status
from . import install

rtm_root_hints = ['/usr/local/include/openrtm-1.1', '/usr/include/openrtm-1.1']

def get_status():
    ret = {'c++' : status.is_cpprtm_installed() ,
           'python' : status.is_pyrtm_installed() ,
           'java' : status.is_javartm_installed() }
    return ret

def get_rtm_root():
    if 'RTM_ROOT' in os.environ.keys():
        return os.environ['RTM_ROOT']
    else:
        for hint in rtm_root_hints:
            if os.path.isfile(os.path.join(hint, 'rtm', 'version.txt')):
                return hint
        return ""

def install_rtm(force=False):
    if sys.platform == 'linux2':
        srcsfile = '/etc/apt/sources.list.d/openrtm-aist.list'
        key1 = 'deb http://www.openrtm.org/pub/Linux/ubuntu/ precise main\n'
        key2 = 'deb http://www.openrtm.org/pub/Linux/ubuntu/ precise-unstable main'
        if os.path.isfile(srcsfile):
            flag1 = False
            flag2 = False
            file = open(srcsfile, 'r+w')
            for line in file:
                if line.strip() == key1:
                    flag1 = True
                if line.strip() == key2:
                    flag2 = True
                    
            if not flag1:
                file.write(key1)
            if not flag2:
                file.write(key2)
            file.close()
        else:
            file = open(srcsfile, 'w')
            file.write(key1)
            file.write(key2)
            file.close()

        subprocess.call(['apt-get', 'update'])

    install_cpprtm(force)
    install_pyrtm(force)
    install.install_javartm(force)
    pass

def install_cpprtm(arg=False):
    if status.is_cpprtm_installed() and not arg:
        print "Your system seems to have OpenRTM C++."
        return False

    if sys.platform == 'darwin':
        install.install_cpprtm_osx(arg)
    elif sys.platform == 'win32':
        install.install_cpprtm_win(arg)
    elif sys.platform == 'linux2':
        install.install_cpprtm_linux(arg)
    pass

def install_pyrtm(arg=False):
    if status.is_pyrtm_installed() and not arg:
        print "Your system has OpenRTM_aist package in PYTHONPATH."
        return False
    if sys.platform == 'darwin':
        install.install_pyrtm_osx(arg)
    elif sys.platform == 'win32':
        install.install_pyrtm_win(arg)
    elif sys.platform == 'linux2':
        install.install_pyrtm_linux(arg)
    pass

