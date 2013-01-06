#!/usr/bin/env python

import OpenTPR
import OpenRTM_aist
import subprocess
import os
import signal

rtm_dir='rtm/'
rtm_java_jardir='%s1.1/jar/' % rtm_dir
rtm_java_classpath='%sOpenRTM-aist-1.1.0.jar:%scommons-cli-1.1.jar:%srtcd.jar' % (rtm_java_jardir, rtm_java_jardir, rtm_java_jardir)


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
    if not "CLASSPATH" in java_env.keys():
        java_env["CLASSPATH"]='.'
    java_env["CLASSPATH"]=java_env["CLASSPATH"] + ':' + rtm_java_classpath
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
        for key in {'cpp', 'python', 'java'}: #process.keys():
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

        for p in process.values():
            p.terminate()
        print 'All rtcd process terminated.'
        pass
