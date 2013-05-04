#!/usr/bin/env python

import wasanbon
from wasanbon.core.management import *
import subprocess
import yaml
import os

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        setting = load_settings()
        repo = setting['common']['repository']['wasanbon']
        rtm_temp = setting['common']['path']['RTM_TEMP']
        rtm_home = setting['common']['path']['RTM_HOME']
        home_setting = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
        cwd = os.getcwd()
        os.chdir(rtm_temp)
        if not os.path.isdir('wasanbon'):
            cmd = [os.path.join(home_setting['git_path'], 'git'), 'clone', setting['common']['repository']['wasanbon']]
            subprocess.call(cmd)
            os.chdir('wasanbon')
        else:
            os.chdir('wasanbon')
            cmd = [os.path.join(home_setting['git_path'], 'git'), 'pull']
            output = subprocess.check_output(cmd)
            if output.strip() == 'Already up-to-date.':
                print output
                os.chdir(cwd)
                return 0
        
        cmd = ['python', 'setup.py', 'install']
        subprocess.call(cmd)
        os.chdir(cwd)
