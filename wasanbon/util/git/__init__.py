import sys, os, subprocess

from github_obj  import *
from git_obj import *

import wasanbon

def git_command(commands, path='.', verbose = False, pipe=False):
    cur_dir = os.getcwd()
    
    os.chdir(path)
    gitenv = os.environ.copy()
    if not 'HOME' in gitenv.keys():
        gitenv['HOME'] = wasanbon.get_home_path()
        if verbose:
            sys.stdout.write(' - Environmental Variable  HOME (%s) is added.\n' % gitenv['HOME'])

    if verbose:
        sys.stdout.write(" - GIT command %s in repository\n" % (repr(commands)))

    cmd = [wasanbon.setting['local']['git']] + commands
    stdout = None if verbose else subprocess.PIPE
    stderr = None if verbose else subprocess.PIPE

    if verbose:
        sys.stdout.write(' - COMMAND:')
        for c in cmd:
            sys.stdout.write(c + ' ')
        sys.stdout.write('\n')
    if not pipe:
        p = subprocess.call(cmd, env=gitenv, stdout=stdout, stderr=stderr)
    else:
        p = subprocess.Popen(cmd, env=gitenv, stdout=stdout, stderr=stderr)
    os.chdir(cur_dir)
    return p
