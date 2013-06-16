import os, sys, yaml, shutil, getpass, subprocess

import wasanbon
from wasanbon import util
from wasanbon.core import platform
from wasanbon.core import tools
from wasanbon.core import rtm

from github import Github

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, force, clean, verbose):
        user = []
        passwd = []
        email = []
        if argv[2] == 'init':
            if verbose:
                print " - Initializing Github account's ssh key"
            sys.stdout.write('  - Input Github User Name:')
            user = raw_input()
            sys.stdout.write('  - Input Github Password :')
            passwd = getpass.getpass()
            g = Github(user, passwd)
            user = g.get_user()
            try:
                user.login
            except:
                print ' - Error. Can not login.'
                return

            pub_file = os.path.join(wasanbon.get_home_path(), '.ssh', 'id_rsa.pub')
            import socket
            sys.stdout.write('  - Input ssh-key name in github (default: %s):' % socket.gethostname())
            name = raw_input()
            if len(name) == 0:
                name = socket.gethostname()
                pass

            if verbose:
                sys.stdout.write('  - Sending SSH-KEY to github.com....')
            key_obj = g.get_user().create_key(name, open(pub_file, "r").read())
            if key_obj:
                if verbose:
                    sys.stdout.write(' completed.\n')
            
    
        if argv[2] == 'init' or argv[2] == 'set_user':
            if verbose:
                sys.stdout.write(" - Initializing host's config (user, email)\n")
            if not user:
                sys.stdout.write(' - Input Git User Name:')
                user = raw_input()
            if not email:
                sys.stdout.write(' - Input Git Email:')
                email = raw_input()
                
            cmd = [wasanbon.setting['local']['git'], 'config', '--global', 'user.name', user]
            subprocess.call(cmd)
            cmd = [wasanbon.setting['local']['git'], 'config', '--global', 'user.email', email]
            subprocess.call(cmd)
            if verbose:
                sys.stdout.write('  - Completed.\n')
