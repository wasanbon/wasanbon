#!/usr/bin/env python
import os, sys
import subprocess
#import zipfile
from wasanbon.core import *
from wasanbon.core.management import *
from wasanbon.core.rtm.status import *

import shutil

def install_rtm():
    install_cpprtm()
    install_pyrtm()
    install_javartm()
    pass

def install_cpprtm(arg=False):
    if is_cpprtm_installed() and not arg:
        print "Your system seems to have OpenRTM C++."
        return False
    if sys.platform == 'darwin':
        install_cpprtm_osx(arg)
    elif sys.platform == 'win32':
        install_cpprtm_win(arg)
    pass

def install_pyrtm(arg=False):
    if is_pyrtm_installed() and not arg:
        print "Your system has OpenRTM_aist package in PYTHONPATH."
        return False
    if sys.platform == 'darwin':
        install_pyrtm_osx(arg)
    elif sys.platform == 'win32':
        install_cpprtm_win(arg)
    pass

def install_javartm(arg=False):
    if is_javartm_installed() and not arg:
        print "Your system have OpenRTM_aist java file in RTM_HOME directory."
        return False
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    rtm_root_java = setting['common']['path']['RTM_ROOT_JAVA']
    if not os.path.isdir(rtm_root_java):
        os.makedirs(rtm_root_java)

    download_and_unpack(setting['common']['packages']['java'], rtm_temp, force=arg)
    for root, dirs, files in os.walk(os.path.join(rtm_temp, 'OpenRTM-aist')):
        for file in files:
            if file.endswith('.jar'):
                shutil.copyfile(os.path.join(root, file),os.path.join(rtm_root_java, file))
    pass

def install_cpprtm_win(force):
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    download_and_install(setting['win32']['packages']['c++'], force=force)

def install_pyrtm_win(force):
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    download_and_install(setting['win32']['packages']['python'], force=force)

def install_cpprtm_osx(force):
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    download_and_install(setting['darwin']['packages']['c++'], force=force)

    srcdir = '/usr/local/lib/python2.7/site-packages' 
    distdir = os.path.split(wasanbon.__path__[0])[0]
    for file in os.listdir(srcdir):
        filepath = os.path.join(srcdir, file)
        if os.path.isfile(filepath):
            shutil.copy2(os.path.join(srcdir, file), os.path.join(distdir, file))
        elif os.path.isdir(filepath):
            shutil.copytree(os.path.join(srcdir, file), os.path.join(distdir, file))
    pass

def install_pyrtm_osx(force):
    setting = load_settings()
    rtm_temp = setting['common']['path']['RTM_TEMP']
    rtm_home = setting['common']['path']['RTM_HOME']
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
    old_dir = os.getcwd()
    os.chdir(rtm_temp)
    cmd = [y['svn_path'], 'co', setting['common']['svn']['python']]
    ret = subprocess.call(cmd)
    os.chdir('OpenRTM-aist-Python')
    cmd = ['python', 'setup.py', 'build_core']
    ret = subprocess.call(cmd)
    cmd = ['python', 'setup.py', 'install']
    ret = subprocess.call(cmd)
    cmd = ['python', 'setup.py', 'install_example']
    ret = subprocess.call(cmd)
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

