#!/usr/bin/env python

import wasanbon
import os, sys, subprocess, shutil
from wasanbon import util


def pull_and_update(verbose):
    cwd = os.getcwd()
    os.chdir(os.path.join(wasanbon.rtm_temp, 'wasanbon'))

    if verbose:
        sys.stdout.write(' - Pulling from %s\n' % wasanbon.setting['common']['repository']['wasanbon']['git'])
        pass

    cmd = [wasanbon.setting['local']['git'], 'pull']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = p.stdout.readline()
    if output.strip() == 'Already up-to-date.':
        sys.stdout.write(output)
        return

    install(verbose)

def clone_and_update(verbose):
    if verbose: 
        sys.stdout.write(' - Cloning %s\n' % wasanbon.setting['common']['repository']['wasanbon']['git'])
        pass

    cmd = [wasanbon.setting['local']['git'], 
           'clone', 
           wasanbon.setting['common']['repository']['wasanbon']['git']]
    subprocess.call(cmd)
    os.chdir('wasanbon')
    pass

def cleanup(verbose):
    cwd = os.getcwd()
    os.chdir(os.path.join(wasanbon.rtm_temp, 'wasanbon'))
    if verbose:
        sys.stdout.write(' - Cleanly uninstalled.\n')
    shutil.rmtree(wasanbon.__path__[0])
    shutil.rmtree('build')
    os.chdir(cwd)
    pass

def install(verbose):
    cwd = os.getcwd()
    os.chdir(os.path.join(wasanbon.rtm_temp, 'wasanbon'))
    cmd = ['python', 'setup.py', 'install']
    subprocess.call(cmd)
    os.chdir(cwd)
    pass

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, verbose=False, force=False, clean=False):
        cwd = os.getcwd()
        if verbose:
            sys.stdout.write(' - Changing directory to %s\n' % wasanbon.rtm_temp)
        os.chdir(wasanbon.rtm_temp)

        if not os.path.isdir('wasanbon'):
        else:

        if clean:
            cleanup(verbose)
        else:
            install(verbose)
        os.chdir(cwd)
