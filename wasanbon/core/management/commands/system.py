import os, sys, time, subprocess, signal
import wasanbon
from wasanbon.core import rtc
from wasanbon.core import system
from wasanbon.core.system import run

def signal_action(num, frame):
    print 'SIGINT captured'
    global endflag
    endflag = True
    pass

endflag = False

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv):
        if len(argv) < 3 or argv[2] == 'help':
            show_help_description('system')
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

            sys.stdout.write('Starting RTC-Daemons\n')
            if len(argv) >= 4 and argv[3] == '--nobuild':
                sys.stdout.write('\n - Launch System without System Build.\n\n')
                nobuild=True
            else:
                nobuild=False
            system.run_system(argv, nobuild=nobuild)

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
                    if system.is_all_process_terminated():
                        break
                except Exception, e:
                    print 'Exception Occurred: %s' % repr(e)
                    endflag = True
                    pass
            print 'Terminating All Process....'        
            system.terminate_all_process()
            print 'All rtcd process terminated.'
