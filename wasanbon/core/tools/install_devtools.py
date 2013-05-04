#!/usr/bin/env python

import sys
from wasanbon.core import *
from wasanbon.core.management import *
from wasanbon.core.template import *

def check_devtools():
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    
    fin = open(os.path.join(rtm_home, 'setting.yaml'), 'r')
    y = yaml.load(fin)
    
    flag = False
    if len(y['cmake_path']) == 0:
        print 'CMake can not be found.'
        flag = True
    
    if len(y['git_path']) == 0:
        print 'Git can not be found.'
        flag = True

    if len(y['doxygen_path']) == 0:
        print 'Doxygen can not be found'
        flag = True

    if len(y['jdk_path']) == 0:
        print 'JDK can not be found.'
        flag = True

    if len(y['svn_path']) == 0:
        print 'Subversion can not be found.'
        flag = True
        
    return not flag


def check_and_install_devtools():
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    
    fin = open(os.path.join(rtm_home, 'setting.yaml'), 'r')
    y = yaml.load(fin)
    
    if len(y['cmake_path']) == 0:
        install_cmake()
    
    if len(y['git_path']) == 0:
        install_git()

    if len(y['doxygen_path']) == 0:
        install_doxygen()

    if len(y['jdk_path']) == 0:
        install_jdk()

    if len(y['svn_path']) == 0:
        install_svn()

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

def install_jdk():
    if sys.platform == 'darwin':
        install_jdk_osx()
    elif sys.platform == 'win32':
        install_jdk_win32()
    elif sys.platform == 'linux2':
        install_jdk_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_svn():
    if sys.platform == 'darwin':
        install_svn_osx()
    elif sys.platform == 'win32':
        install_svn_win32()
    elif sys.platform == 'linux2':
        install_svn_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_cmake_osx():
    setting = load_settings()
    download_and_install(setting['darwin']['packages']['cmake'])
    pass

def install_git_osx():
    setting = load_settings()
    download_and_install(setting['darwin']['packages']['git'])
    pass

def install_doxygen_osx():
    setting = load_settings()
    download_and_install(setting['darwin']['packages']['doxygen'])
    pass

def install_jdk_osx():
    setting = load_settings()
    download_and_install(setting['darwin']['packages']['jdk'])

def install_svn_osx():
    print 'Install Xcode commandline tool. Xcode -> Preference -> Download'
