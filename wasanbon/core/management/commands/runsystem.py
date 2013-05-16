#!/usr/bin/env python

#import OpenRTM_aist
import subprocess
import os
import platform
import signal

import rtctree
from rtshell import rtresurrect, rtstart

import wasanbon

import OpenRTM_aist
#if platform.system() == 'Windows':
#    rtm_java_classpath='%s;%s;%s' % (openrtm_java, commons_cli, rtcd_jar)
#else:
#    rtm_java_classpath='%s:%s:%s' % (openrtm_java, commons_cli, rtcd_jar)

def start_cpp_rtcd():
    print '-Starting rtcd_cpp'
    cpp_env = os.environ.copy()

    if platform.system() == 'Windows':
        return subprocess.Popen(['rtcd', '-f', 'conf/rtc_cpp.conf'], env=cpp_env, creationflags=512)
    else:
        return subprocess.Popen(['rtcd', '-f', 'conf/rtc_cpp.conf'], env=cpp_env)


def start_python_rtcd():
    print '-Starting rtcd_py'
    py_env = os.environ.copy()
    if platform.system() == 'Windows':
        p = subprocess.Popen(['rtcd_python', '-f', 'conf/rtc_py.conf'], env=py_env, creationflags=512, stdin=subprocess.PIPE)
        p.stdin.write('N')
        return p
    else:
        return subprocess.Popen(['rtcd_python', '-f', 'conf/rtc_py.conf'], env=py_env)
 

def start_java_rtcd():
    print '-Starting rtcd_java'
    rtm_java_classpath = os.path.join(wasanbon.rtm_home, 'jar')
    java_env = os.environ.copy()
    if not "CLASSPATH" in java_env.keys():
        java_env["CLASSPATH"]='.'
    if platform.system() == 'Windows':
        sep = ';'
    else:
        sep = ':'
    for jarfile in os.listdir(rtm_java_classpath):
        java_env["CLASSPATH"]=java_env["CLASSPATH"] + sep + os.path.join(rtm_java_classpath, jarfile)
    if platform.system() == 'Windows':
        return subprocess.Popen([wasanbon.setting['local']['java'], 'rtcd.rtcd', '-f', 'conf/rtc_java.conf'], env=java_env, creationflags=512)
    else:
        return subprocess.Popen([wasanbon.setting['local']['java'], 'rtcd.rtcd', '-f', 'conf/rtc_java.conf'], env=java_env)

endflag = False


manager = []


def signal_action(num, frame):
    print 'SIGINT captured'
    global endflag
    endflag = True
    #manager.terminate()
    pass

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        print 'Starting rtcd processes'


        if not os.path.isdir('log'):
            os.mkdir('log')

        process = {
            'cpp' : start_cpp_rtcd(),
            'python' : start_python_rtcd(),
            'java' : start_java_rtcd()
            }

        """
        global manager
        manager = OpenRTM_aist.Manager.init(['rtcd_python', '-f', 'conf/rtc_py.conf'])
        manager.activateManager()
        manager.runManager(False)
        """
        signal.signal(signal.SIGINT, signal_action)


        process_state = {}
        for key in process.keys():
            process_state[key] = False #process[key].returncode != None

        rtsprofile =[ wasanbon.setting['application']['system'] ]
        rtresurrect.main(rtsprofile)
        rtstart.main(rtsprofile)


        global endflag
        while not endflag:
            for key in process.keys():
                process[key].poll()
                if process_state[key] == False and process[key].returncode != None:
                    print '%s rtcd stopped (retval=%d)' % (key, process[key].returncode)
                    process_state[key] = True
            if all(process_state.values()):
                print 'All rtcd stopped'
                break

        print 'Terminating All Process....'
        for p in process.values():
            if p.returncode == None:
                print 'Terminating process...'
                p.kill()
        print 'All rtcd process terminated.'
        pass
