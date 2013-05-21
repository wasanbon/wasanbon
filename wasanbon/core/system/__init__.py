# encoding: UTF-8

import os, sys, time, signal
import wasanbon
from wasanbon.core.system import run

process = {}

def signal_action(num, frame):
    print 'SIGINT captured'
    global endflag
    endflag = True
    pass

endflag = False

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
        return all(flags)
    else:
        return False


def start_process():
    if not os.path.isdir('log'):
        os.mkdir('log')

    global process
    process['cpp']    = run.start_cpp_rtcd()
    process['python'] = run.start_python_rtcd()
    process['java']   = run.start_java_rtcd()


def run_system(nobuild):
    sys.stdout.write('Ctrl+C to stop system.\n')
    signal.signal(signal.SIGINT, signal_action)

    sys.stdout.write('Starting RTC-Daemons\n')
    
    start_process()

    global endflag
    
    if not nobuild:
        interval = 3
        for i in range(0, interval):
            sys.stdout.write('\rwaiting %s seconds to rebuild RTSystem.' % (interval-i))
            sys.stdout.flush()
            time.sleep(1)
            
        while not endflag:
            sys.stdout.write('\n rtresurrect.\n')                    
            if run.exe_rtresurrect():
                time.sleep(1)
                break
        while not endflag:
            sys.stdout.write('\n rtstart.\n')
            if run.exe_rtresurrect():
                time.sleep(1)
                break
    sys.stdout.write('System successfully started.\n')
    while not endflag:
        try:
            time.sleep(0.1)
            if is_all_process_terminated():
                break
        except Exception, e:
            print 'Exception Occurred: %s' % repr(e)
            endflag = True
            pass
    print 'Terminating All Process....'        
    terminate_all_process()
    print 'All rtcd process terminated.'


def terminate_all_process():
    global process
    for key in process.keys():
        process[key].poll()
        if process[key].returncode == None:
            sys.stdout.write(' - Terminating RTC-Daemon(%s)\n' % key)
            process[key].kill()
            

    pass
