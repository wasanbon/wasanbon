#!/usr/bin/env python

import OpenTPR
import OpenRTM_aist
import subprocess
import os
import platform
import signal

rtm_dir='rtm'
rtm_java_jardir=os.path.join(os.getcwd(), rtm_dir, '1.1', 'jar')
openrtm_java=os.path.join(rtm_java_jardir, 'OpenRTM-aist-1.1.0.jar')
commons_cli=os.path.join(rtm_java_jardir, 'commons-cli-1.1.jar')
rtcd_jar=os.path.join(rtm_java_jardir, 'rtcd.jar')

if platform.system() == 'Windows':
    rtm_java_classpath='%s;%s;%s' % (openrtm_java, commons_cli, rtcd_jar)
else:
    rtm_java_classpath='%s:%s:%s' % (openrtm_java, commons_cli, rtcd_jar)

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
        return subprocess.Popen(['rtcd_python', '-f', 'conf/rtc_py.conf'], env=py_env, creationflags=512)
    else:
        return subprocess.Popen(['rtcd_python', '-f', 'conf/rtc_py.conf'], env=py_env)

def start_java_rtcd():
    print '-Starting rtcd_java'
    java_env = os.environ.copy()
    if not "CLASSPATH" in java_env.keys():
        java_env["CLASSPATH"]='.'
    if platform.system() == 'Windows':
        java_env["CLASSPATH"]=java_env["CLASSPATH"] + ';' + rtm_java_classpath
    else:
        java_env["CLASSPATH"]=java_env["CLASSPATH"] + ':' + rtm_java_classpath        
    print java_env["CLASSPATH"]
    if platform.system() == 'Windows':
        return subprocess.Popen(['java', 'rtcd.rtcd', '-f', 'conf/rtc_java.conf'], env=java_env, creationflags=512)
    else:
        return subprocess.Popen(['java', 'rtcd.rtcd', '-f', 'conf/rtc_java.conf'], env=java_env)

endflag = False

def signal_action(num, frame):
    print 'SIGINT captured'
    global endflag
    endflag = True
    pass

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        print 'Starting rtcd processes'
        signal.signal(signal.SIGINT, signal_action)


        process = {
            'cpp' : start_cpp_rtcd(),
            'python' : start_python_rtcd(),
            'java' : start_java_rtcd()
            }

        process_state = {}
        for key in process.keys():
            process_state[key] = False #process[key].returncode != None

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
                p.kill()
        print 'All rtcd process terminated.'
        pass
