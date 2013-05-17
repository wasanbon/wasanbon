import os, sys, time, subprocess, signal

import wasanbon
from wasanbon.core import rtc
from wasanbon.core.system import run

def print_usage(argv):
    print 'Usage: %s system [subcommand] ...\n' % argv[0]
    print ' - subcommand: '
    print '   - install : %s' % ' '
    pass


endflag = False

def signal_action(num, frame):
    print 'SIGINT captured'
    global endflag
    endflag = True

    pass


class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv):
        if len(argv) < 3 or argv[2] == 'help':
            print_usage(argv)
            return
        rtcps = rtc.parse_rtcs()
        if(argv[2] == 'install'):
            print 'Installing RTC %s' % argv[3]
            for rtcp in rtcps:
                if rtcp.getName() == argv[3]:
                    rtc.install(rtcp)

        elif(argv[2] == 'run'):
            sys.stdout.write('Ctrl+C to stop system.\n')
            signal.signal(signal.SIGINT, signal_action)

            if not os.path.isdir('log'):
                os.mkdir('log')
            sys.stdout.write('Starting RTC-Daemons\n')
        
            process = {}
            process['cpp']    = run.start_cpp_rtcd()
            process['python'] = run.start_python_rtcd()
            process['java']   = run.start_java_rtcd()
            
            
            process_state = {}
            for key in process.keys():
                process_state[key] = False
                pass

            interval = 3
            for i in range(0, interval):
                sys.stdout.write('\rwaiting %s seconds to rebuild RTSystem.' % (interval-i))
                sys.stdout.flush()
                time.sleep(1)
            
            sys.stdout.write('\nRebuilding RT System from rtsprofile (%s)\n' % wasanbon.setting['application']['system'])
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
                        pass

                if all(process_state.values()):
                    print 'All rtcds are stopped'
                    break
                pass
            print 'Terminating All Process....'
            for key in process.keys():
                if process[key].returncode == None:
                    sys.stdout.write(' - Terminating RTC-Daemon(%s)\n' % key)
                    process[key].kill()


            print 'All rtcd process terminated.'
            pass

