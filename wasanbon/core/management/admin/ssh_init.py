#!/usr/bin/env python
import os, sys, yaml, shutil, getpass
import wasanbon
from wasanbon import util
from wasanbon.core import platform
from wasanbon.core import tools
from wasanbon.core import rtm
import subprocess
from github import Github

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        cmd = os.path.join(os.path.split(wasanbon.setting['local']['git'])[0], 'ssh-keygen')
        if sys.platform == 'win32':
            cmd = cmd + '.exe'

        path = os.path.join(wasanbon.get_home_path(), '.ssh')
        if not os.path.isdir(path):
            os.makedirs(path)

        file = os.path.join(path, 'id_rsa')

        if not os.path.isfile(file):
            if not util.yes_no("id_rsa file is missing. Create it?") == 'yes':
                return
            subprocess.call([cmd, '-t', 'rsa', '-f', file])
        
        pub_file = file + '.pub'
        
        sys.stdout.write(' - Input Github User Name:')
        user = raw_input()
        sys.stdout.write(' - Input Github Password :')
        passwd = getpass.getpass()
        g = Github(user, passwd)
        user = g.get_user()
        try:
            user.login
        except:
            print ' - Error. Can not login.'
            return

        import socket
        print ' - Input ssh-key name in github (default: %s)' % socket.gethostname()
        name = raw_input()
        if len(name) == 0:
            name = socket.gethostname()
        g.get_user().create_key(name, open(pub_file, "r").read())
    
        
