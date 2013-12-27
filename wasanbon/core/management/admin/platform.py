import sys, os, yaml
import wasanbon
from wasanbon.core import rtm, platform

from wasanbon.core.platform import path, install

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return True

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):

        if len(argv) < 3:
            print ' - To read help, "%s rtm -h"' % os.path.basename(argv[0])
            return

        platform.init_rtm_home(force=False, verbose=verbose, update=False)

        if argv[2] == 'status':
            sys.stdout.write(' - Platform Check...\n')
            path.init_tools_path(verbose=verbose)
            y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
            for cmd, stat in y.items():
                if len(stat.strip()) == 0:
                    stat = 'Not Installed'
                sys.stdout.write(' ' + cmd + ' ' * (10-len(cmd)) + ':' + stat + '\n')
        
        if argv[2] == 'install':
            y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
            for command in argv[3:]:
                sys.stdout.write(' - Installing Command %s\n' % command)
                if not command in y.keys():
                    sys.stdout.write(' - Command is not required by wasanbon.\n')
                    continue
                install.check_command(command, y[command], verbose=True, install=True, force=force)
