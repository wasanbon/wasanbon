import sys, os
import wasanbon
from wasanbon.core import rtm, tools
from wasanbon.core.rtm import cpp, python, java
class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return True

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):
        wasanbon.arg_check(argv, 3)
            
        if(argv[2] == 'install'):
            wasanbon.arg_check(argv, 4)
            if 'all' in argv:
                argv = ['c++', 'python', 'java', 'eclipse', 'arduino']
            else:
                argv = argv[3:]
            for arg in argv:
                if arg == 'c++':
                    cpp.install(force=force, verbose=verbose)
                elif arg == 'python':
                    python.install(force=force, verbose=verbose)
                elif arg == 'java':
                    java.install(force=force, verbose=verbose)
                elif arg == 'eclipse':
                    tools.install_eclipse(force=force, verbose=verbose)
                elif arg == 'arduino':
                    tools.install_rtno(force=force, verbose=verbose)

        elif(argv[2] == 'status'):
            sys.stdout.write(' - Checking OpenRTM-aist installation\n')
            sys.stdout.write('    - OpenRTM-aist C++    : %s\n' % cpp.is_installed())
            sys.stdout.write('    - OpenRTM-aist Python : %s\n' % python.is_installed())
            sys.stdout.write('    - OpenRTM-aist Java   : %s\n' % java.is_installed())
            sys.stdout.write(' - Checking tools intallation\n')
            sys.stdout.write('    - rtshell : %s\n' % tools.is_installed_rtshell())
            sys.stdout.write('    - eclipse : %s\n' % tools.is_installed_eclipse())
            sys.stdout.write('    - arduino : %s\n' % tools.is_installed_arduino())
        elif argv[2] == 'launch':
            wasanbon.arg_check(argv, 4)
            if argv[3] == 'eclipse':
                if len(argv) > 4:
                    args = argv[4:]
                else:
                    args = None
                tools.launch_eclipse('.', argv=args, verbose=verbose)
            elif argv[3] == 'arduino':
                sys.stdout.write('- Launching Arduino\n')
                if len(argv) > 4:
                    args = argv[4:]
                else:
                    args = None
                tools.launch_arduino('.', verbose=verbose)



                
