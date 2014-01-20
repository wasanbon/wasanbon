import os, sys, yaml, shutil, subprocess, traceback, optparse
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

    def alternative(self):
        return []

    def execute_with_argv(self, args, force=False, verbose=False, clean=False):
        sys.stdout.write(' - Starting wasanbon environment.\n')

        if verbose:
            sys.stdout.write(' - wasanbon init with argv:%s\n' % str(argv))

        if sys.platform == 'win32':
            verbose=True

        sys.stdout.write(' @ Installing RTM_HOME\n')
        if not platform.init_rtm_home(force=force, verbose=verbose):
            sys.stdout.write(' - Can not install commands.\n')
            return False

        sys.stdout.write(' @ Commands are successfully found.\n')

        if proxy:
            addr, port = address.split(':')
            util.set_proxy(addr, port, verbose=True)            
        elif interactive:
            sys.stdout.write(' @ The command line tools must communicate with several internet services.\n')
            if util.no_yes(' @ Do you need to use proxy service?') == 'yes':
                while True:
                    try:
                        sys.stdout.write(' -- Input proxy server address:')
                        addr = raw_input()
                        sys.stdout.write(' -- Input proxy server port:')
                        port = int(raw_input())
                        msg = ('@ Address(%s), Port(%s) : OK?' % (addr, port))
                        if util.yes_no(msg) == 'yes':
                            break
                    except Exception, e:
                        sys.stdout.write(' @ Exception:\n')
                        traceback.print_exc()
                if len(addr) == 0:
                    sys.stdout.write(' --- Invalid Proxy Server Address.\n')
                    sys.stdout.write(' --- Following Process does not use proxy.\n')
                else:
                    util.set_proxy(addr, port, verbose=True)
            else:
                util.omit_proxy(verbose=True)

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

