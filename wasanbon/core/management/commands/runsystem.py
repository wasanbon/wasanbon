#!/usr/bin/env python
import subprocess
import os, sys, time
import platform
import signal

import wasanbon
from wasanbon.core.system import run

import OpenRTM_aist


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
        if not os.path.isdir('log'):
            os.mkdir('log')
        sys.stdout.write('Starting RTC-Daemons\n')

        process = {}
        process['cpp']    = run.start_cpp_rtcd()
        process['python'] = run.start_python_rtcd()
        process['java']   = run.start_java_rtcd()

        sys.stdout.write('Ctrl+C to stop system.\n')
        signal.signal(signal.SIGINT, signal_action)

        process_state = {}
        for key in process.keys():
            process_state[key] = False
            
        interval = 3
        sys.stdout.write('waiting %s seconds to rebuild RTSystem.\n' % interval)
        time.sleep(interval)

        sys.stdout.write('Rebuilding RT System from rtsprofile (%s)\n' % wasanbon.setting['application']['system'])
        run.exe_rtresurrect()

        sys.stdout.write('Activating RT System from rtsprofile (%s)\n' % wasanbon.setting['application']['system'])
        run.exe_rtstart()
        
        global endflag
        while not endflag:
            for key in process.keys():
                process[key].poll()
                if process_state[key] == False and process[key].returncode != None:
                    print '%s rtcd stopped (retval=%d)' % (key, process[key].returncode)
                    process_state[key] = True
            if all(process_state.values()):
                print 'All rtcds are stopped'
                break

        print 'Terminating All Process....'
        for key in process.keys():
            if process[key].returncode == None:
                sys.stdout.write(' - Terminating RTC-Daemon(%s)\n' % key)
                process[key].kill()


        print 'All rtcd process terminated.'
        pass
