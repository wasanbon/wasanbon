#!/usr/bin/env python

import os
import urllib
import platform
import subprocess
import zipfile

rtm_dir='rtm'

rtctree_github = 'git://github.com/gbiggs/rtctree.git'
rtshell_github = 'git://github.com/gbiggs/rtshell.git'
rtsprofile_github = 'git://github.com/gbiggs/rtsprofile.git'

eclipse_linux64_filename = 'eclipse_rtmtools_juno_linux_120901.tar.gz'
eclipse_linux64_package = (
    'http://www.ysuga.net/openrtm/rtmtools/%s' % eclipse_linux64_filename,
    os.path.join(rtm_dir, eclipse_linux64_filename))

eclipse_darwin_filename = 'eclipse_rtmtools_juno_mac_120901.tar.gz'
eclipse_darwin_package = (
    'http://www.ysuga.net/openrtm/rtmtools/%s' % eclipse_darwin_filename,
    os.path.join(rtm_dir, eclipse_darwin_filename))

def install_tools():

    if not os.path.isdir(rtm_dir):
        os.mkdir(rtm_dir)

    print 'Installing tools in %s' % platform.system()

    if platform.system() == 'Linux':
        install_tools_linux()
    elif platform.system() == 'Windows':
        install_tools_win()
    elif platform.system() == 'Darwin':
        install_tools_darwin()
    else:
        print 'Unknown System (%s)' % platform.system()
        pass
    pass


def install_tools_win():
    pass

def install_tools_darwin():
    if not os.path.isfile(eclipse_darwin_package[1]):
        print '-Downloading eclipse-all-in-one'
        urllib.urlretrieve(eclipse_darwin_package[0], eclipse_darwin_package[1])

    print '-Uncompressing Eclipse-All-In-One'
    command = ('tar', 'zxf', eclipse_darwin_package[1], '-C', rtm_dir)
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
        f = open(os.path.join(os.environ['HOME'],'.bashrc'), 'a')
        f.write('\nsource /Library/Frameworks/Python.framework/Version/2.7/share/rtshell/shell_support\n')
        subprocess.call('source /Library/Frameworks/Python.framework/Version/2.7/share/rtshell/shell_support', shell=True)
        f.close()
    pass

def install_tools_linux():
    if not os.path.isfile(eclipse_linux64_package[1]):
        print '-Downloading eclipse-all-in-one'
        urllib.urlretrieve(eclipse_linux64_package[0], eclipse_linux64_package[1])

    print '-Uncompressing Eclipse-All-In-One'
    command = ('tar', 'zxf', eclipse_linux64_package[1], '-C', rtm_dir)
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

        f = open(os.path.join(os.environ['HOME'],'.bashrc'), 'a')
        f.write('\n\nsource /usr/local/share/rtshell/shell_support\n')
        subprocss.call('source /usr/local/share/rtshell/shell_support', shell=True)
        f.close()
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
