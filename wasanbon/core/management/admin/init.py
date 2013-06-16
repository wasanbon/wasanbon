import os, sys, yaml, shutil, subprocess
if sys.platform == 'darwin' or sys.platform == 'linux2':
    import pwd, grp
import wasanbon
from wasanbon import util

from wasanbon.core import platform
from wasanbon.core import tools
from wasanbon.core import rtm


class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):
        sys.stdout.write(' - Starting wasanbon environment.\n')

        if not platform.init_rtm_home(force=force, verbose=verbose):
            sys.stdout.write(' - Can not install commands.\n')

        sys.stdout.write(' - Commands are successfully found.\n')

        if not 'local' in wasanbon.setting.keys():
            wasanbon.setting['local'] = yaml.load(open(os.path.join(wasanbon.rtm_home,
                                                                    'setting.yaml'), 'r'))

        rtm.install(force=force)

        tools.install(force=force)

        if sys.platform == 'win32':
            sys.stdout.write("\n=========================================================\n");
            sys.stdout.write("\n");
            sys.stdout.write(" Please Reboot Windows to properly configure your system.\n")
            sys.stdout.write("\n");
            sys.stdout.write("\n=========================================================\n");

        elif sys.platform == 'darwin' or sys.platform == 'linux2':
            sys.stdout.write("\nchanging owner setting of RTM_HOME(%s)\n" % wasanbon.rtm_home)
            home_stat = os.stat(wasanbon.get_home_path())
            
            cmd = ['chown', '-R',  pwd.getpwuid(home_stat.st_uid)[0] + ':' +  grp.getgrgid(home_stat.st_gid)[0], wasanbon.rtm_home]
            subprocess.call(cmd)

