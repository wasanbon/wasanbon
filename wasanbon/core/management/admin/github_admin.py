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
        user = []
        passwd = []
        email = []
        if argv[2] == 'init':
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

            pub_file = os.path.join(wasanbon.get_home_path(), '.ssh', 'id_rsa.pub')
            import socket
            print ' - Input ssh-key name in github (default: %s)' % socket.gethostname()
            name = raw_input()
            if len(name) == 0:
                name = socket.gethostname()
                pass
            g.get_user().create_key(name, open(pub_file, "r").read())
    
        if argv[2] == 'init' or argv[2] == 'set_user':
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
