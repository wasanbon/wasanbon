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
    
        
