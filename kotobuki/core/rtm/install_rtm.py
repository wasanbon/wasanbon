#!/usr/bin/env python

import os
import urllib
import platform
import subprocess
import zipfile

from install_settings import *

def install_rtm():
    if not os.path.isdir(rtm_dir):
        os.mkdir(rtm_dir)

    if platform.system() == 'Linux':
        install_rtm_linux()
    elif platform.system() == 'Windows':
        install_rtm_win()
    elif platform.system() == 'Darwin':
        install_rtm_darwin()
    else:
        print 'Unknown System (%s)' % platform.system()
        pass
    pass

def install_rtm_darwin():
    print 'Current Version does not available in Darwin'
    install_rtm_java()
    pass

def is_cpprtm_installed_in_win():
    return ('RTM_ROOT' in os.environ.keys())

def is_pyrtm_installed_in_win():
    try:
        import OpenRTM_aist
        return True
    except ImportError, e:
        return False
    pass

def install_rtm_win():
    print 'Installing OpenRTM on Windows'
    if is_cpprtm_installed_in_win():
        print """Your system have RTM_ROOT environemntal variable.
                May be you've installed OpenRTM C++ version."""
    else:
        if not os.path.isfile(cpp_win_package[1]):
            print '-Downloading OpenRTM-aist C++'
            urllib.urlretrieve(cpp_win_package[0], cpp_win_package[1])
        print '-Installing OpenRTM-aist C++'
        cmd = ('msiexec', '/i', os.path.join(os.getcwd(), cpp_win_package[1]))
        subprocess.call(cmd)

    if is_pyrtm_installed_in_win():
        print """Your system have OpenRTM_aist package in PYTHONPATH.
        May be you've installed OpenRTM Python version."""
    else:
        if not os.path.isfile(py_win_package[1]):
            print '-Downloading OpenRTM-aist Python'
            urllib.urlretrieve(py_win_package[0], py_win_package[1])
        print '-Installing OpenRTM-aist Python'
        cmd = ('msiexec', '/i', os.path.join(os.getcwd(), py_win_package[1]))
        subprocess.call(cmd)
        
    install_rtm_java()
    pass
    
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

def install_rtm_java():
    # Download RTM Java Version 
    if not os.path.isfile(java_package[1]):
        print '-Downloading OpenRTM-aist Java'
        urllib.urlretrieve(java_package[0], java_package[1])
    print '-Uncompressing OpenRTM-aist Java Package'
    zf = zipfile.ZipFile(java_package[1])
    for filename in zf.namelist():
        path= os.path.join(rtm_dir, filename.lstrip('OpenRTM-aist/'))
        directory, fname = os.path.split(path)
        if not os.path.isdir(directory) and len(directory)>0:
            os.makedirs(directory)
        if len(fname) > 0:
            if not os.path.isfile(path):
                f = file(path, 'wb')
                f.write(zf.read(filename))
                f.close()
    zf.close()
    pass

