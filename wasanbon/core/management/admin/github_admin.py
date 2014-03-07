"""
en_US : 
 brief : |
  This command will setup github authentication to register ssh key to github.com.
 description : |
  If you are core github.com user (like ysuga), You can use this command to upload ssh key to github.com
 subcommands : 
  init : Upload ssh key to github.com
  set_user : this will initiate git config --global user.name|user.email
"""
import os, sys, yaml, shutil, getpass, subprocess

import wasanbon
from wasanbon import util
from wasanbon.core import platform
from wasanbon.core import tools
from wasanbon.core import rtm
from wasanbon.util import git

from github import Github

def init(argv, force, clean, verbose):
    print " - Initializing Github account's ssh key"
    (username, passwd) = wasanbon.user_pass()
    g = Github(username, passwd)
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
    
    sys.stdout.write('  - Sending SSH-KEY to github.com....')

    key_obj = g.get_user().create_key(name, open(pub_file, "r").read())
    if key_obj:
        sys.stdout.write(' completed.\n')
    else:
        sys.stdout.write(' failed.\n')
    

def set_user(argv, force ,clean, verbose):
    sys.stdout.write(" - Initializing host's config (user, email)\n")
    sys.stdout.write(' - Input Git User Name:')
    username = raw_input()
    sys.stdout.write(' - Input Git Email:')
    email = raw_input()
                
    git.git_command(['config', '--global', 'user.name', username])
    git.git_command(['config', '--global', 'user.email', email])
    sys.stdout.write('  - Completed.\n')

def alternative_(argv=None):
    return ['init', 'set_user']

alternative = alternative_
def execute_with_argv(argv, force, clean, verbose):
    if argv[2] == 'init':
        init(argv, force, clean, verbose)
    if argv[2] == 'init' or argv[2] == 'set_user':
        set_user(argv, force, clean, verbose)
