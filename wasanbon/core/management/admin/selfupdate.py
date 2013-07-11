#!/usr/bin/env python

import wasanbon
import os, sys, subprocess, shutil
from wasanbon import util


def pull_and_update(verbose, force):
    cwd = os.getcwd()
    os.chdir(os.path.join(wasanbon.rtm_temp, 'wasanbon'))

    if verbose:
        sys.stdout.write(' - Pulling from %s\n' % wasanbon.setting['common']['repository']['wasanbon']['git'])

    cmd = [wasanbon.setting['local']['git'], 'pull']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = p.stdout.readline()
    if output.strip() == 'Already up-to-date.':
        sys.stdout.write(output)
        return False

    return install(verbose=verbose, force=force)

def clone_and_update(verbose, force):
    cwd = os.getcwd()
    os.chdir(wasanbon.rtm_temp)

    if verbose: 
        sys.stdout.write(' - Cloning %s\n' % wasanbon.setting['common']['repository']['wasanbon']['git'])

    cmd = [wasanbon.setting['local']['git'], 'clone', 
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
    shutil.rmtree(wasanbon.__path__[0])
    
    os.chdir(cwd)
    return True

def install(verbose, force):
    dirname = os.path.join(wasanbon.rtm_temp, 'wasanbon')
    if not os.path.isdir(dirname):
        return False
    cwd = os.getcwd()
    if verbose:
        sys.stdout.write(' - Installing wasanbon from %s.\n' % dirname)

    if force:
        cleanup(verbose)

    

    os.chdir(dirname)
    if os.path.isdir(os.path.join(dirname, 'build')) :
        shutil.rmtree('build')
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
        os.chdir(wasanbon.rtm_temp)
        if not os.path.isdir('wasanbon'):
            if not clean:
                clone_and_update(verbose=verbose, force=force)
        else:
            if clean:
                cleanup(verbose=verbose)
            else:
                pull_and_update(verbose=verbose, force=force)

        os.chdir(cwd)
