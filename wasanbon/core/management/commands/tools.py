#coding : utf-8
"""
en_US:
 brief : |
  Launch Tools
 description : |
  Launch Tools for RTC development.
  You can launc "RTC Builder", "RT System Editor", and "Arduino"
 subcommands : 
  rtcb : |
   Launch RTC Builder
  rtse : |
   Launch RT System Editor
  arduino : |
   Launch Arduino 

ja_JP:
 brief : |
  Launch Tools
 description : |
  Launch Tools for RTC development.
  You can launc "RTC Builder", "RT System Editor", and "Arduino"
 subcommands : 
  rtcb : |
   Launch RTC Builder
  rtse : |
   Launch RT System Editor
  arduino : |
   Launch Arduino 
"""
import sys, os, time, traceback


import wasanbon
from wasanbon.core import tools 
#from wasanbon.core import system
#from xml.etree import ElementTree
from wasanbon.core import package as pack

from rtshell import rtcryo

def save_all_system(nameservers, filepath='system/DefaultSystem.xml', verbose=False):
    if verbose:
        sys.stdout.write(" - Saving System on %s to %s\n" % (str(nameservers), filepath))
    for i in range(0, 5):
        try:
            sys.stdout.write('\n - Trying to save by rtcryo .....')
            argv = ['--verbose', '-n', 'DefaultSystem01', '-v', '1.0', '-e', 'Sugar Sweet Robotics',  '-o', filepath]
            argv = argv + nameservers
            rtcryo.main(argv=argv)
            sys.stdout.write(' Saved.\n')
            return
        except omniORB.CORBA.UNKNOWN, e:
            #traceback.print_exc()
            pass
        except Exception, e:
            pass



def alternative(argv=None):
    return ['eclipse', 'arduino', 'rtno', 'rtcb', 'rtse']

def execute_with_argv(argv, verbose, clean=False, force=False):
    if True:
        wasanbon.arg_check(argv, 3)

        _package = pack.Package(os.getcwd())

        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            tools.launch_eclipse(_package.rtc_path, verbose=verbose)
            return
        elif(argv[2] == 'arduino'):
            print '- Launching Arduino'
            tools.launch_arduino(".", verbose=verbose)
            return
        elif argv[2] == 'rtno':
            sys.stdout.write(' - RTno\n')
            wasanbon.arg_check(argv, 4)
            if argv[3] == 'template':
                # wasanbon.arg_check(argv, 5)
                rtc_name = argv[4]
                tools.generate_rtno_temprate(_package, rtc_name, verbose=verbose)

        elif(argv[2] == 'rtcb'):
            print 'Launching Eclipse'
            tools.launch_eclipse(_package.rtc_path, verbose=verbose)
            return

        elif(argv[2] == 'rtse'):
            sys.stdout.write(' @ Launching Eclipse\n')
            pack.run_nameservers(_package, verbose=verbose, force=force)
            pack.run_system(_package, verbose=verbose)

            print_delay(_package.get_build_delay())

            #tools.launch_eclipse(_package.system_path, nonblock=False, verbose=verbose)
            tools.launch_eclipse(workbench='.', nonblock=False, verbose=verbose, argv=['--clean'])

            print_delay(_package.get_build_delay())

            save_all_system(['localhost'], verbose=verbose)

            pack.stop_system(_package, verbose=verbose)
            pack.kill_nameservers(_package, verbose=verbose)

        else:
            raise wasanbon.InvalidUsageException()
def print_delay(dt):
    times = dt * 10
    sys.stdout.write(' - Waiting approx. %s seconds\n' % dt)
    for t in range(times):
        percent = float(t) / times
        width = 30
        progress = (int(width*percent)+1)
        sys.stdout.write('\r  [' + '#'*progress + ' '*(width-progress-1) + ']')
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write('\n')
