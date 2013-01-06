#!/usr/bin/env python

import os
import urllib
import platform
import subprocess
import zipfile

rtm_dir='rtm/'
rtm_java_filename = 'OpenRTM-aist-Java-1.1.0-RC1-jar.zip'

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


java_package = (
    'http://www.openrtm.org/pub/OpenRTM-aist/java/1.1.0/%s' % rtm_java_filename, '%s%s' % (rtm_dir, rtm_java_filename))

class Command(object):
    def __init__(self):
        pass


    def execute_with_argv(self, argv):
        
        if(argv[2] == 'install'):
            print 'Installing OpenRTM-aist'
            p = platform.dist()
            if platform.system() == 'Linux':
                for cmd in linux_package[p[0]]['common']:
                    print '-Launching command = ' + str(cmd)
                    subprocess.call(cmd)
                for pac in linux_package[p[0]][p[2]]:
                    cmd = linux_package[p[0]]['install-cmd'] + tuple([pac])
                    print '-Installing with command = ' + str(cmd)
                    subprocess.call(cmd)
            if not os.path.isdir(rtm_dir):
                os.mkdir(rtm_dir)
            if not os.path.isfile(java_package[1]):
                urllib.urlretrieve(java_package[0], java_package[1])
            zf = zipfile.ZipFile(java_package[1])
            for filename in zf.namelist():
                path=rtm_dir + filename.lstrip('OpenRTM-aist/')
                directory, fname = os.path.split(path)
                if not os.path.isdir(directory):
                    os.makedirs(directory)

                if len(fname) > 0:
                    if not os.path.isfile(path):
                        f = file(path, 'wb')
                        f.write(zf.read(filename))
                        f.close()
            zf.close()
                
        pass
