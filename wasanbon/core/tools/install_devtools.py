#!/usr/bin/env python

import sys
from wasanbon.core import *
from wasanbon.core.management import *
from wasanbon.core.template import *



def check_and_install():
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    fin = open(rtm_home, 'r')
    y = yaml.load(fin)
    
    if len(y['cmake_path']) == 0:
        install_cmake()
    
    if len(y['git_path']) == 0:
        install_git()

    if len(y['doxygen_path']) == 0:
        install_doxygen()

def install_cmake():
    if sys.platform == 'darwin':
        install_cmake_osx()
    elif sys.platform == 'win32':
        install_cmake_win32()
    elif sys.platform == 'linux2':
        install_cmake_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_git():
    if sys.platform == 'darwin':
        install_git_osx()
    elif sys.platform == 'win32':
        install_git_win32()
    elif sys.platform == 'linux2':
        install_git_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_doxygen():
    if sys.platform == 'darwin':
        install_doxygen_osx()
    elif sys.platform == 'win32':
        install_doxygen_win32()
    elif sys.platform == 'linux2':
        install_doxygen_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass


def install_cmake_osx():
    setting = load_settings()
    download_and_install(setting['darwin']['packages']['cmake'])
    pass


def install_git_osx():
    pass

def install_doxygen_osx():
    pass
