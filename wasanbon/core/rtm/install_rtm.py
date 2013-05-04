#!/usr/bin/env python
import os, sys
import subprocess
#import zipfile
from wasanbon.core import *
from wasanbon.core.management import *
from wasanbon.core.rtm.status import *

import shutil

def install_rtm():
    print 'Installing OpenRTM on %s' % sys.platform
    print '-C++ version:'
    if is_cpprtm_installed():
        print """Your system have RTM_ROOT environemntal variable.
        You've installed OpenRTM C++ version."""
    else:
        install_cpprtm()

    print '-Python version:'
    if is_pyrtm_installed():
        print """Your system have OpenRTM_aist package in PYTHONPATH.
        You've installed OpenRTM Python version."""
    else:
        install_pyrtm()
    
    print '-Java version:'
    if is_javartm_installed():
        print """Your system have OpenRTM_aist java file.
        You've installed OpenRTM Python version."""
    else:
        install_javartm()
    pass

def install_cpprtm():
    if sys.platform == 'darwin':
        install_cpprtm_osx()

def install_pyrtm():
    if sys.platform == 'darwin':
        install_pyrtm_osx()

"""
def install_rtm_win():
        if not os.path.isfile(cpp_win_package[1]):
            print '-Downloading OpenRTM-aist C++'
            urllib.urlretrieve(cpp_win_package[0], cpp_win_package[1])
        print '-Installing OpenRTM-aist C++'
        cmd = ('msiexec', '/i', os.path.join(os.getcwd(), cpp_win_package[1]))
        subprocess.call(cmd)

    if is_pyrtm_installed():
    else:
        if not os.path.isfile(py_win_package[1]):
            print '-Downloading OpenRTM-aist Python'
            urllib.urlretrieve(py_win_package[0], py_win_package[1])
        print '-Installing OpenRTM-aist Python'
        cmd = ('msiexec', '/i', os.path.join(os.getcwd(), py_win_package[1]))
        subprocess.call(cmd)
        
    install_rtm_java()
    pass
"""    

def install_cpprtm_osx():
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    download_and_install(setting['darwin']['packages']['c++'])
    pass

def install_pyrtm_osx():
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    rtm_home = setting['common']['path']['RTM_HOME']
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
    old_dir = os.getcwd()
    os.chdir(rtm_temp)
    cmd = [os.path.join(y['svn_path'], 'svn'), 'co', setting['common']['svn']['python']]
    ret = subprocess.check_output(cmd)
    os.chdir(old_dir)


def install_rtm_linux():
    print '-Installing OpenRTM-aist in Linux'
    p = platform.dist()
    for cmd in linux_package[p[0]]['common']:
        print '-Launching command = ' + str(cmd)
        subprocess.call(cmd)
    for pac in linux_package[p[0]][p[2]]:
        cmd = linux_package[p[0]]['install-cmd'] + tuple([pac])
        print '-Installing with command = ' + str(cmd)
        subprocess.call(cmd)
    install_rtm_java()
    pass

def install_javartm():
    # Download RTM Java Version 
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    rtm_root_java = setting['common']['path']['RTM_ROOT_JAVA']
    if not os.path.isdir(rtm_root_java):
        os.makedirs(rtm_root_java)

    download_and_unpack(setting['common']['packages']['java'], rtm_temp)
    for root, dirs, files in os.walk(os.path.join(rtm_temp, 'OpenRTM-aist')):
        for file in files:
            if file.endswith('.jar'):
                shutil.copyfile(os.path.join(root, file),os.path.join(rtm_root_java, file))

    pass

