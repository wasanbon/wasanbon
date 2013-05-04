#!/usr/bin/env python

import os
import urllib
import platform
import subprocess
import zipfile
import sys
import wasanbon.core.management.import_tools as importer
from wasanbon.core.management  import *
from wasanbon.core import *

def install_tools():
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    rtm_temp = setting['common']['path']['RTM_TEMP']
    url = setting[sys.platform]['packages']['eclipse']
    download_and_unpack(url, rtm_home)

    """
    try:
        import rtctree
    except ImportError, e:
        print '-Installing rtctree'
        git_install(rtctree_github, 'rtm/rtctree')
    try:
        import rtsprofile
    except ImportError, e:
        print '-Installing rtsprofile'
        git_install(rtsprofile_github, 'rtm/rtsprofile')
    try:
        import rtshell
    except ImportError, e:
        print '-Installing rtshell'
        git_install(rtshell_github, 'rtm/rtshell')
        #f = open(os.path.join(os.environ['HOME'],'.bashrc'), 'a')
        #f.write('\nsource /Library/Frameworks/Python.framework/Version/2.7/share/rtshell/shell_support\n')
        #subprocess.call('source /Library/Frameworks/Python.framework/Version/2.7/share/rtshell/shell_support', shell=True)
        #f.close()
    pass
    """

def git_install(url_, dir_):
    if os.path.isdir(dir_):
        return
    current_dir = os.getcwd()
    gitcommand = 'git'
    command = (gitcommand, 'clone', url_, dir_)
    subprocess.call(command)

    os.chdir(os.path.join(current_dir, dir_))
    command = ('python', 'setup.py', 'install', '--record', 'installed_files.txt')
    subprocess.call(command)
    os.chdir(current_dir)
