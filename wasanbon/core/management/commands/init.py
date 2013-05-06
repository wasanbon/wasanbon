#!/usr/bin/env python

import wasanbon
from wasanbon.core.management import *
from wasanbon.core.tools import *
from wasanbon.core.template import *
import os
import yaml


def search_command(cmd, hints):
    if sys.platform == 'win32':
        cmd = cmd + '.exe'
    for path in os.environ['PATH'].split(':'):
        fullpath = os.path.join(path, cmd)
        if os.path.isfile(fullpath):
            return fullpath
    for hint in hints:
        if os.path.isfile(hint):
            return hint
    return ""
    
def search_cmake(hints):
    cmd = 'cmake'
    return search_command(cmd, hints)

def search_git(hints):
    cmd = 'git'
    return search_command(cmd, hints)

def search_doxygen(hints):
    cmd = 'doxygen'
    return search_command(cmd, hints)

def search_jdk(hints):
    cmd = 'javac'
    return search_command(cmd, hints)

def search_svn(hints):
    cmd = 'svn'
    return search_command(cmd, hints)

def search_msbuild(hints):
    cmd = 'msbuild'
    return search_command(cmd, hints)

def init_tools_path():
    setting = load_settings()
    rtm_home = setting['common']['path']['RTM_HOME']
    filename = os.path.join(rtm_home, 'setting.yaml')
    tempfile = os.path.join(rtm_home, 'setting.yaml.bak')
    os.rename(filename, tempfile)
    fin = open(tempfile, 'r')
    fout = open(filename, 'w')
    y = yaml.load(fin)

    y['cmake_path']   = search_cmake(setting[sys.platform]['hints']['cmake'])
    y['git_path']     = search_git(setting[sys.platform]['hints']['git'])
    y['doxygen_path'] = search_doxygen(setting[sys.platform]['hints']['doxygen'])
    y['jdk_path']     = search_jdk(setting[sys.platform]['hints']['jdk'])
    y['svn_path']     = search_svn(setting[sys.platform]['hints']['svn'])

    if sys.platform == 'win32':
        y['msbuild_path'] = search_msbuild(setting[sys.platform]['hints']['msbuild'])

    yaml.dump(y, fout, encoding='utf8', allow_unicode=True)

    fin.close()
    fout.close()
    os.remove(tempfile)


class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        setting = load_settings()
        repo = setting['common']['repository']['wasanbon']
        rtm_home = setting['common']['path']['RTM_HOME']
        if not os.path.isdir(rtm_home):
            os.mkdir(rtm_home, 0777)
        rtm_temp = setting['common']['path']['RTM_TEMP']
        if not os.path.isdir(rtm_temp):
            os.mkdir(rtm_temp, 0777)
        rtm_root_java = setting['common']['path']['RTM_ROOT_JAVA']
        if not os.path.isdir(rtm_root_java):
            os.mkdir(rtm_root_java, 0777)
        
        if os.path.isfile(os.path.join(rtm_home, 'setting.yaml')):
            if yes_no('There seems to be a setting file in %s. Do you want to initialize?' % rtm_home) == 'yes':
                os.remove(os.path.join(rtm_home, 'setting.yaml'))
                print 'start init'

        fin = open(os.path.join(wasanbon.__path__[0], 'settings/setting.yaml'), 'r')
        fout = open(os.path.join(rtm_home, 'setting.yaml'), 'w')

        for line in fin:
            fout.write(line)

        fin.close()
        fout.close()

        init_tools_path()

        if len(argv) >= 3:
            if argv[2] == '--install':
                check_and_install_devtools()
                check_devtools()
        else:
            if not check_devtools():
                print 'If you want to install devtools, sudo python wasanbon-admin.py init --install'
