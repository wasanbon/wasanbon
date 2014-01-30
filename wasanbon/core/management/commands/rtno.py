import sys, os, time

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
            argv = ['--verbose', '-n', 'DefaultSystem01', '-v', '1.0', '-e', 'Sugar Sweet Robotics',  '-o', filepath]
            argv = argv + nameservers
            rtcryo.main(argv=argv)
            sys.stdout.write(' - Saved.\n')
            return
        except omniORB.CORBA.UNKNOWN, e:
            #traceback.print_exc()
            pass
        except Exception, e:
            pass


class Command(object):
    def __init__(self):
        pass


    def alternative(self):
        return ['generate']

    def execute_with_argv(self, argv, verbose, clean, force):
        wasanbon.arg_check(argv, 3)
        _package = pack.Package(os.getcwd())

        if argv[2] == 'generate':
            sys.stdout.write(' - Generating RTno Source Code\n')
            wasanbon.arg_check(argv, 4)
            rtc_name = argv[3]
            tools.generate_rtno_temprate(_package, rtc_name, verbose=True)
        else:
            raise wasanbon.InvalidUsageException()
