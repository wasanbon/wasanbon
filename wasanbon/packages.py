import os


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

packages = {
    'Windows' : {
        'c++' : 'http://www.openrtm.org/pub/Windows/OpenRTM-aist/cxx/1.1/OpenRTM-aist-1.1.0-RELEASE_vc10.msi',
        'python' : 'http://www.openrtm.org/pub/Windows/OpenRTM-aist/python/OpenRTM-aist-Python-1.1.0-RC1.msi',
        'java' : 'http://www.openrtm.org/pub/OpenRTM-aist/java/1.1.0/OpenRTM-aist-Java-1.1.0-RC1-jar.zip',
        'eclipse' : 'http://www.ysuga.net/openrtm/rtmtools/eclipse_rtmtools_juno_win32_120901.tar.gz',
        },
    'Linux'  : {
        'java' : 'http://www.openrtm.org/pub/OpenRTM-aist/java/1.1.0/OpenRTM-aist-Java-1.1.0-RC1-jar.zip',
        'eclipse' : 'http://www.ysuga.net/openrtm/rtmtools/eclipse_rtmtools_juno_linux_120901.tar.gz',
        },
    'Darwin' : {
        'c++' : 'http://sugarsweetrobotics.com/pub/Darwin/OpenRTM-aist/cxx/1.1/OpenRTM-aist-1.1.0-RELEASE.dmg',
        'java' : 'http://www.openrtm.org/pub/OpenRTM-aist/java/1.1.0/OpenRTM-aist-Java-1.1.0-RC1-jar.zip',
        'eclipse' : 'http://openrtm.org/pub/openrtp/packages/1.1.0.rc4v20130216/eclipse421-openrtp110rc4v20130216-macosx-cocoa-x86_64.tar.gz',



        #'ecilpse' : 'http://www.ysuga.net/openrtm/rtmtools/eclipse_rtmtools_juno_mac_120901.tar.gz',
        },
    'rtctree' :'git://github.com/gbiggs/rtctree.git',
    'rtshell' : 'git://github.com/gbiggs/rtshell.git',
    'rtsprofile' : 'git://github.com/gbiggs/rtsprofile.git',
}


rtcs = {
    

}
