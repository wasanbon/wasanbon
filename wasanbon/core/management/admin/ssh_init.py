import os, sys, yaml, shutil, getpass, subprocess
import wasanbon
from wasanbon import util

class Command(object):
    def __init__(self):
        pass

    def alternative(self):
        return []

    def execute_with_argv(self, argv, verbose, force, clean):
        sys.stdout.write(' - Initializing ssh-key\n')
        cmd = os.path.join(os.path.split(wasanbon.setting()['local']['git'])[0], '..', 'bin',  'ssh-keygen')
        if sys.platform == 'win32':
            cmd = cmd + '.exe'

        path = os.path.join(wasanbon.get_home_path(), '.ssh')
        if not os.path.isdir(path):
            if verbose:
                print ' - Creating .ssh folder (%s)' % path
            os.makedirs(path)

        file = os.path.join(path, 'id_rsa')
        if not os.path.isfile(file):
            if not util.yes_no(" - id_rsa file is missing. Create it?") == 'yes':
                sys.stdout.write(' - Aborted.\n')
                return
            sys.stdout.write(' - Creating ssh key-gen.\n')

            cmds = [cmd, '-t', 'rsa', '-f', file]
            sys.stdout.write(' - Command = %s\n' % cmds)

            subprocess.call(cmds)
        else:
            sys.stdout.write(' - $HOME/.ssh/id_rsa file found.\n')
