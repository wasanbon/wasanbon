import os, sys, yaml, shutil, subprocess
if sys.platform == 'darwin' or sys.platform == 'linux2':
    import pwd, grp
import wasanbon
from wasanbon import util

from wasanbon.core import platform
from wasanbon.core import tools
from wasanbon.core import rtm
from wasanbon.core import repositories

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):
        sys.stdout.write(' - Starting wasanbon environment.\n')
        if sys.platform == 'win32':
            verbose=True

        sys.stdout.write(' @ Installing RTM_HOME\n')
        if not platform.init_rtm_home(force=force, verbose=verbose):
            sys.stdout.write(' - Can not install commands.\n')
            return False

        sys.stdout.write(' @ Commands are successfully found.\n')

        if not 'local' in wasanbon.setting.keys():
            wasanbon.setting['local'] = yaml.load(open(os.path.join(wasanbon.rtm_home,
                                                                    'setting.yaml'), 'r'))
        sys.stdout.write(' @ Downloading Repository\n')
        if not repositories.download_repositories(verbose=verbose):
            sys.stdout.write(' - Downloading Failed.\n')
            return False

        sys.stdout.write(' @ Installing RTM\n')
        rtm.install(verbose=verbose, force=force)

        sys.stdout.write(' @ Installing Tools\n')
        tools.install(force=force, verbose=verbose)

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

