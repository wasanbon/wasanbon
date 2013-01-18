#!/usr/bin/env python

import os
import urllib
import platform
import subprocess
import zipfile

rtm_dir='rtm'

linux_package = {
    'Ubuntu' : { 
        'common': (
            ('rm', '-rf', '/etc/apt/sources.list.d/openrtm-aist.list'),
            ('sh', '-c', "echo \"deb http://www.openrtm.org/pub/Linux/ubuntu/ precise main\" >> /etc/apt/sources.list.d/openrtm-aist.list"), 
            ('sh', '-c', "echo \"deb http://www.openrtm.org/pub/Linux/ubuntu/ precise-unstable main\" >> /etc/apt/sources.list.d/openrtm-aist.list"), 
            ('apt-get', 'update')),
        'install-cmd': ('apt-get', 'install', '-y', '--force-yes'),
        'precise': (
            'gcc', 'g++', 'make', 'uuid-dev', 'cmake-gui', 'doxygen', 
            'libcv2.3', 'libcv-dev', 'libcvaux2.3', 
            'libcvaux-dev', 'libhighgui-dev', 'libhighgui2.3',
            'libopencv-contrib-dev', 'libopencv-contrib2.3',
            'libomniorb4-1', 'libomniorb4-dev', 
            'omniidl', 'omniorb-nameserver',
            'openrtm-aist', 'openrtm-aist-dev', 
            'openrtm-aist-example', 'openrtm-aist-doc',
            'python-omniorb-omg', 'omniidl-python', 
            'openrtm-aist-python', 'openrtm-aist-python-example',
            'openjdk-7-jre', 'openjdk-7-jdk'
            )
        }
    }


rtm_java_filename = 'OpenRTM-aist-Java-1.1.0-RC1-jar.zip'
java_package = (
    'http://www.openrtm.org/pub/OpenRTM-aist/java/1.1.0/%s' % rtm_java_filename,  os.path.join(rtm_dir, rtm_java_filename))

rtm_cpp_win_filename = 'OpenRTM-aist-1.1.0-RELEASE_vc10.msi'
cpp_win_package = (
    'http://www.openrtm.org/pub/Windows/OpenRTM-aist/cxx/1.1/%s' % rtm_cpp_win_filename, os.path.join(rtm_dir, rtm_cpp_win_filename))


rtm_py_win_filename = 'OpenRTM-aist-Python-1.1.0-RC1.msi'
py_win_package = (
    'http://www.openrtm.org/pub/Windows/OpenRTM-aist/python/%s' % rtm_py_win_filename, os.path.join(rtm_dir, rtm_py_win_filename))

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

def install_rtm_win():
    if not os.path.isfile(cpp_win_package[1]):
        print '-Downloading OpenRTM-aist C++'
        urllib.urlretrieve(cpp_win_package[0], cpp_win_package[1])
    if not 'RTM_ROOT' in os.environ.keys():
        print '-Installing OpenRTM-aist C++'
        cmd = ('msiexec', '/i', os.path.join(os.getcwd(), cpp_win_package[1]))
        subprocess.call(cmd)
    try:
        import OpenRTM_aist
    except ImportError, e:
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

