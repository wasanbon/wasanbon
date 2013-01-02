#!/usr/bin/env python

import OpenTPR
import OpenRTM_aist
import subprocess
import os
def start_cpp_rtcd():
    print '-Starting rtcd_cpp'
    cpp_env = os.environ.copy()
    return subprocess.Popen(['rtcd', '-f', 'conf/rtc_cpp.conf'], env=cpp_env)

def start_python_rtcd():
    print '-Starting rtcd_py'
    py_env = os.environ.copy()
    return subprocess.Popen(['rtcd_python', '-f', 'conf/rtc_py.conf'], env=py_env)

def start_java_rtcd():
    print '-Starting rtcd_java'
    java_env = os.environ.copy()
    if "CLASSPATH" in java_env.keys():
        print 'No CLASSPATH set'
        java_env["CLASSPATH"]='rtm/1.1/jar/OpenRTM-aist-1.1.0.jar:rtm/1.1/jar/commons-cls-1.1.jar:rtm/1.1/jar/rtcd.jar'
    return subprocess.Popen(['java', 'rtcd.rtcd', '-f', 'conf/rtc_java.conf'], env=java_env)
    
class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        print 'Starting rtcd processes'
        cpp_process = start_cpp_rtcd()
        py_process  = start_python_rtcd()
        java_process = start_java_rtcd()
        while True:
            cpp_process.poll()
            py_process.poll()
            if cpp_process.returncode != None and py_process.returncode != None:
                break

        print 'All rtcd process terminated.'
        pass
    
