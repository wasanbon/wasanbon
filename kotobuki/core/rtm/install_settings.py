import os

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
