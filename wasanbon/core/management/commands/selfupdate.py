#!/usr/bin/env python

import wasanbon
import os, sys, subprocess

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        cwd = os.getcwd()
        os.chdir(wasanbon.rtm_temp)
        if not os.path.isdir('wasanbon'):
            cmd = [wasanbon.setting['local']['git'], 
                   'clone', 
                   wasanbon.setting['common']['repository']['wasanbon']]
            subprocess.call(cmd)
            os.chdir('wasanbon')
        else:
            os.chdir('wasanbon')
            cmd = [wasanbon.setting['local']['git'],
                   'pull']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output = p.stdout.readline()
            if output.strip() == 'Already up-to-date.':
                print output
                os.chdir(cwd)
                return 0
        
        cmd = ['python', 'setup.py', 'install']
        subprocess.call(cmd)
        os.chdir(cwd)
