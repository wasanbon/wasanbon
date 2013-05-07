import os, sys, shutil

import wasanbon
from . import status
from . import install
def get_status():
    ret = {'c++' : status.is_cpprtm_installed() ,
           'python' : status.is_pyrtm_installed() ,
           'java' : status.is_javartm_installed() }
    return ret

def install_rtm(force=False):
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
    pass

def install_pyrtm(arg=False):
    if status.is_pyrtm_installed() and not arg:
        print "Your system has OpenRTM_aist package in PYTHONPATH."
        return False
    if sys.platform == 'darwin':
        install.install_pyrtm_osx(arg)
    elif sys.platform == 'win32':
        install.install_cpprtm_win(arg)
    pass

