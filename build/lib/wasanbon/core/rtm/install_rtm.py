#!/usr/bin/env python
import os
import urllib
import platform
import subprocess
import zipfile
from status_rtm import *
import kotobuki.core.management.import_tools as importer
settings = importer.import_setting()
packages = importer.import_packages()

def install_rtm():
    print 'Installing OpenRTM on %s' % platform.system()
    print '-C++ version:'
    if is_cpprtm_installed():
        print """Your system have RTM_ROOT environemntal variable.
                May be you've installed OpenRTM C++ version."""
    else:
        install_cpprtm()

    print '-Python version:'
    if is_pyrtm_installed():
        print """Your system have OpenRTM_aist package in PYTHONPATH.
        May be you've installed OpenRTM Python version."""
    else:
        install_pyrtm()
    
    print '-Java version:'
    if is_javartm_installed():
        print """Your system have OpenRTM_aist java file.
        May be you've installed OpenRTM Python version."""
    else:
        install_javartm()
    pass


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
    javadir = (settings.rtm['RTM_ROOT_JAVA'])
    if not os.path.isdir(javadir):
        os.makedirs(javadir)
        pass
    zipfilename = os.path.basename(packages.packages[platform.system()]['java'])
    tempdir = os.path.join(settings.rtm['RTM_ROOT'], 'temp')
    if not os.path.isdir(tempdir):
        os.makedirs(tempdir)
        pass
    tempfile = os.path.join(tempdir, zipfilename)
    if not os.path.isfile(tempfile):
        print '-Downloading OpenRTM-aist Java'
        urllib.urlretrieve(packages.packages[platform.system()]['java'], tempfile)
    print '-Uncompressing OpenRTM-aist Java Package'
    zf = zipfile.ZipFile(tempfile)
    for filename in zf.namelist():
        path= os.path.join(tempdir, filename.lstrip('OpenRTM-aist/'))
        print '#%s' % path
        directory, fname = os.path.split(path)
        if not os.path.isdir(directory) and len(directory)>0:
            os.makedirs(directory)
        if len(fname) > 0:
            if not os.path.isfile(path):
                f = file(path, 'wb')
                f.write(zf.read(filename))
                f.close()
                
            if filename.endswith('.jar'):
                print 'Endswith jar'
                jarfile = file( os.path.join(javadir, os.path.basename(filename)), 'wb')
                jarfile.write(zf.read(filename))
                jarfile.close()
    zf.close()
    pass

