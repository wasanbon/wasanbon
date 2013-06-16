#!/usr/bin/env python

import wasanbon
import os, sys, subprocess, shutil
from wasanbon import util

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, verbose=False, force=False, clean=False):
        cwd = os.getcwd()
        #if not os.path.isdir(wasanbon.rtm_temp):
        #    os.umask(0000)
        #    os.mkdir(wasanbon.rtm_temp, 0777)
        os.chdir(wasanbon.rtm_temp)

        if not os.path.isdir('wasanbon'):
            cmd = [wasanbon.setting['local']['git'], 
                   'clone', 
                   wasanbon.setting['common']['repository']['wasanbon']['git']]
            subprocess.call(cmd)
            os.chdir('wasanbon')
        else:
            os.chdir('wasanbon')
            cmd = [wasanbon.setting['local']['git'],
                   'pull']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output = p.stdout.readline()
            if output.strip() == 'Already up-to-date.':
                sys.stdout.write(output)
                os.chdir(cwd)
                return 0
        if clean:
            shutil.rmtree(wasanbon.__path__[0])
            shutil.rmtree('build')
        cmd = ['python', 'setup.py', 'install']
        subprocess.call(cmd)
        os.chdir(cwd)
