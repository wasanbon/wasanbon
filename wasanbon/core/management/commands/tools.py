import sys, os

import wasanbon
from wasanbon.core import tools 
#from wasanbon.core import system
#from xml.etree import ElementTree
from wasanbon.core import project as prj

from rtshell import rtcryo

def save_all_system(nameservers, filepath='system/DefaultSystem.xml', verbose=False):
    if verbose:
        sys.stdout.write(" - Saving System on %s to %s\n" % (str(nameservers), filepath))
    try:
        argv = ['--verbose', '-n', 'DefaultSystem01', '-v', '1.0', '-e', 'Sugar Sweet Robotics',  '-o', filepath]
        argv = argv + nameservers
        rtcryo.main(argv=argv)
    except omniORB.CORBA.UNKNOWN, e:
        traceback.print_exc()
        pass
    except Exception, e:
        traceback.print_exc()
        return False

class Command(object):
    def __init__(self):
        pass


    def execute_with_argv(self, argv, verbose, clean, force):
        wasanbon.arg_check(argv, 3)

        proj = prj.Project(os.getcwd())

        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            tools.launch_eclipse(proj.rtc_path, verbose=verbose)
            return
        if(argv[2] == 'arduino'):
            print '- Launching Arduino'
            tools.launch_arduino(".", verbose=verbose)
            return

        if(argv[2] == 'rtcb'):
            print 'Launching Eclipse'
            tools.launch_eclipse(proj.rtc_path, verbose=verbose)
            return

        if(argv[2] == 'rtse'):
            sys.stdout.write(' @ Launching Eclipse\n')
            nss = proj.get_nameservers(verbose=verbose)
            for ns in nss:
                if not ns.check_and_launch(verbose=verbose, force=force):
                    sys.stdout.write(' @ NameService %s is not running\n' % ns.path)
                    return False
            
            proj.launch_all_rtcd(verbose=verbose)
            tools.launch_eclipse(proj.system_path, nonblock=False, verbose=verbose)
            
            ns_addrs = [ns.path for ns in nss]
            save_all_system(['localhost'])
            proj.terminate_all_rtcd(verbose=verbose)
            
            for ns in nss:
                ns.kill()

        raise wasanbon.InvalidUsageException()
