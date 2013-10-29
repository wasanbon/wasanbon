#!/usr/bin/env python
import os, sys, subprocess, shutil
import wasanbon
from wasanbon import util

def pull_and_update(verbose, force, branch):
    cwd = os.getcwd()
    os.chdir(os.path.join(wasanbon.rtm_temp, 'wasanbon'))

    if verbose:
        sys.stdout.write(' - Pulling from %s in branch %s\n' % (wasanbon.setting['common']['repository']['wasanbon']['git'], branch))

    cmd = [wasanbon.setting['local']['git'], 'pull', branch]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = p.stdout.readline()
    if output.strip() == 'Already up-to-date.' and not force:
        sys.stdout.write(output)
        return False
    
    cleanup(verbose=verbose)
    return install(verbose=verbose, force=force)

def clone_and_update(verbose, force, branch):
    cwd = os.getcwd()
    os.chdir(wasanbon.rtm_temp)

    if verbose: 
        sys.stdout.write(' - Cloning %s in branch %s\n' % (wasanbon.setting['common']['repository']['wasanbon']['git'], branch))

    cmd = [wasanbon.setting['local']['git'], 'clone', '-b', branch, 
           wasanbon.setting['common']['repository']['wasanbon']['git']]
    subprocess.call(cmd)

    return install(verbose=verbose, force=force)


def cleanup(verbose):
    dirname = os.path.join(wasanbon.rtm_temp, 'wasanbon')
    if not os.path.isdir(dirname):
        return False

    if verbose:
        sys.stdout.write(' - Cleanly uninstalled.\n')
    
    cwd = os.getcwd()
    os.chdir(dirname)
    if verbose:
        sys.stdout.write(' - Removing Direcotry:' + wasanbon.__path__[0])

    shutil.rmtree(wasanbon.__path__[0])
    
    if verbose:
        sys.stdout.write(' -- Removed.\n')
    
    os.chdir(cwd)
    return True

def install(verbose, force):
    dirname = os.path.join(wasanbon.rtm_temp, 'wasanbon')
    if not os.path.isdir(dirname):
        return False
    cwd = os.getcwd()
    if verbose:
        sys.stdout.write(' - Installing wasanbon from %s.\n' % dirname)

    os.chdir(dirname)
    if verbose:
        sys.stdout.write(' - Removing Build Directory:' + os.path.join(dirname, 'build'))

    if os.path.isdir(os.path.join(dirname, 'build')) :
        if verbose:
            sys.stdout.write(' -- removed\n')
        shutil.rmtree(os.path.join(dirname, 'build'))
    cmd = ['python', 'setup.py', 'install']
    subprocess.call(cmd)
    os.chdir(cwd)
    return True

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, verbose=False, force=False, clean=False):
        cwd = os.getcwd()

        if verbose:
            sys.stdout.write(' - Changing directory to %s\n' % wasanbon.rtm_temp)
            pass
        if len(argv) > 3:
            branch = argv[2]
        else:
            branch = 'master'

        os.chdir(wasanbon.rtm_temp)
        if not os.path.isdir('wasanbon'):
            if not clean:
                clone_and_update(verbose=verbose, force=force, branch=branch)
        else:
            #cleanup(verbose=verbose)
            pull_and_update(verbose=verbose, force=force, branch=branch)

        os.chdir(cwd)
