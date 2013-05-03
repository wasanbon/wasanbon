#!/usr/bin/env python

import os
import urllib
import platform
import subprocess
import zipfile
import wasanbon.core.management.import_tools as importer
settings = importer.import_setting()
packages = importer.import_packages()

def install_tools():
    rtm_dir = settings.rtm['TOOLS_ROOT']
    if not os.path.isdir(os.path.join(rtm_dir, 'temp')):
        os.makedirs(os.path.join(rtm_dir, 'temp'))

    print 'Installing tools in %s' % platform.system()
    url = packages.packages[platform.system()]['eclipse']
    file = os.path.basename(packages.packages[platform.system()]['eclipse'])
    temppath = os.path.join(rtm_dir, 'temp', file)
    if not os.path.isfile(temppath):
        print '-Downloading eclipse-all-in-one'
        urllib.urlretrieve(url, temppath)
    print '-Uncompressing Eclipse-All-In-One'
    command = ('tar', 'zxf', temppath, '-C', rtm_dir)
    subprocess.call(command)
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
