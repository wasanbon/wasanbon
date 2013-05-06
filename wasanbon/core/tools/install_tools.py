#!/usr/bin/env python

import os
import urllib
import platform
import subprocess
import zipfile
import sys
import yaml
import wasanbon.core.management.import_tools as importer
from wasanbon.core.management  import *
from wasanbon.core import *

def install_tools():
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    rtm_temp = setting['common']['path']['RTM_TEMP']
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
    url = setting[sys.platform]['packages']['eclipse']
    download_and_unpack(url, rtm_home, unpackonly=True)

    try:
        import rtctree
    except ImportError, e:
        print '-Installing rtctree'
        git_install('rtctree')
    try:
        import rtsprofile
    except ImportError, e:
        print '-Installing rtsprofile'
        git_install('rtsprofile')
    try:
        import rtshell
    except ImportError, e:
        print '-Installing rtshell'
        git_install('rtshell')
        #f = open(os.path.join(os.environ['HOME'],'.bashrc'), 'a')
        #f.write('\nsource /Library/Frameworks/Python.framework/Version/2.7/share/rtshell/shell_support\n')
        #subprocess.call('source /Library/Frameworks/Python.framework/Version/2.7/share/rtshell/shell_support', shell=True)
        #f.close()
    pass


def git_install(key):
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    rtm_temp = setting['common']['path']['RTM_TEMP']
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))

    gitcommand = y['git_path']
    url = setting['common']['git'][key]
    command = [gitcommand, 'clone', url, rtm_temp]
    subprocess.call(command)

    crrdir = os.getcwd()
    os.chdir(os.path.join(rtm_temp, key))
    command = ['python', 'setup.py', 'install', '--record', 'installed_files.txt']
    subprocess.call(command)
    os.chdir(crrdir)
