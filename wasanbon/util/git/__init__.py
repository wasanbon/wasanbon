import sys, os, subprocess, yaml
import shutil
import wasanbon

from github_obj  import *
from git_obj import *

def clone_and_setup(url, verbose=False, force=False):
    if verbose:
        sys.stdout.write(' - Clone and setup.py: %s\n' % url)
    distpath = os.path.join(wasanbon.rtm_temp, os.path.basename(url)[:-4])
    if not 'local' in wasanbon.setting.keys():
        wasanbon.setting['local'] = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))

    stdout = None if verbose else subprocess.PIPE

    if os.path.isdir(distpath):
        print ' - Path (%s) is existing' % distpath
        if not force:
            print ' - Aborting'
            return
        else:
            print ' - Force to install'
            if verbose:
                print ' - Removing Path (%S)' % distpath
            shutil.rmtree(distpath)


    cmd = [wasanbon.setting['local']['git'], 'clone', url, distpath]
    if verbose:
        print ' - Cloning %s' % url
    git_command(['clone', url], verbose=verbose)

    crrdir = os.getcwd()
    os.chdir(distpath)
    cmd = ['python', 'setup.py', 'install', '--record', 'installed_files.txt']
    if verbose:
        print ' - Install (setup.py install) in %s' % distpath
    subprocess.call(cmd, stdout=stdout)

    os.chdir(crrdir)


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
