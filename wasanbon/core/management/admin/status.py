import sys, os, yaml
import wasanbon
from wasanbon.core import rtm, platform
from wasanbon.core.platform import path, install
from wasanbon.core import rtm, tools
from wasanbon.core.rtm import cpp, python, java

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return True

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):
        #wasanbon.arg_check(argv, 2)

        platform.init_rtm_home(force=False, verbose=verbose, update=False)

        sys.stdout.write(' - Checking Platform installation.\n')
        path.init_tools_path(verbose=verbose)
        y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
        for cmd, stat in y.items():
            if len(stat.strip()) == 0:
                stat = 'Not Installed'
            sys.stdout.write('    - ' + cmd + ' ' * (10-len(cmd)) + ':' + stat + '\n')
            pass

        sys.stdout.write(' - Checking OpenRTM-aist installation\n')
        sys.stdout.write('    - rtm_c++    (OpenRTM-aist C++)    : %s\n' % cpp.is_installed())
        sys.stdout.write('    - rtm_python (OpenRTM-aist Python) : %s\n' % python.is_installed())
        sys.stdout.write('    - rtm_java   (OpenRTM-aist Java)   : %s\n' % java.is_installed())
        sys.stdout.write(' - Checking tools intallation\n')
        sys.stdout.write('    - rtshell : %s\n' % tools.is_installed_rtshell())
        sys.stdout.write('    - eclipse : %s\n' % tools.is_installed_eclipse())
        sys.stdout.write('    - arduino : %s\n' % tools.is_installed_arduino())
        

        
