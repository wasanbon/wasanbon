# encoding: UTF-8

import os, sys, time
import wasanbon
from wasanbon.core.system import run

process = {}

def is_all_process_terminated():
    flags = []
    global process
    for key in process.keys():
        if process[key].returncode != None:
            flags.append(False)
        else:
            process[key].poll()
            if process[key].returncode == None:
                flags.append(False)
            else:
                flags.append(True)
    if len(flags) != 0:
        print flags
        return all(flags)
    else:
        return False

def run_system(argv, nobuild):
    if not os.path.isdir('log'):
        os.mkdir('log')

    global process
    process['cpp']    = run.start_cpp_rtcd()
    process['python'] = run.start_python_rtcd()
    process['java']   = run.start_java_rtcd()



def terminate_all_process():
    global process
    for key in process.keys():
        process[key].poll()
        if process[key].returncode == None:
            sys.stdout.write(' - Terminating RTC-Daemon(%s)\n' % key)
            process[key].kill()
            

    pass
