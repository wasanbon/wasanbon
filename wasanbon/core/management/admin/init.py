#!/usr/bin/env python
import os, sys, yaml, shutil
import wasanbon
from wasanbon import util
from wasanbon.core import platform
from wasanbon.core import tools
from wasanbon.core import rtm



def search_command(cmd, hints):
    if sys.platform == 'win32':
        cmd = cmd + '.exe'
    
    path_splitter = ';' if sys.platform == 'win32' else (':' if sys.platform == 'darwin' else ':')

    for path in os.environ['PATH'].split(path_splitter):
        fullpath = os.path.join(path, cmd)
        if os.path.isfile(fullpath):
            return fullpath
    for hint in hints:
        if os.path.isfile(hint):
            return hint
    return ""

def search_cmd_all(dict):
    for cmd in dict.keys():
        dict[cmd] = search_command(cmd, wasanbon.setting[sys.platform]['hints'][cmd])

    return dict

def init_tools_path():
    filename = os.path.join(wasanbon.rtm_home, 'setting.yaml')
    tempfile = os.path.join(wasanbon.rtm_home, 'setting.yaml.bak')
    if os.path.isfile(tempfile):
        os.remove(tempfile)

    os.rename(filename, tempfile)
    fin = open(tempfile, 'r')
    fout = open(filename, 'w')
    y = yaml.load(fin)

    y = search_cmd_all(y)

    yaml.dump(y, fout, encoding='utf8', allow_unicode=True)

    fin.close()
    fout.close()
    os.remove(tempfile)


class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return True

    def execute_with_argv(self, argv):
        if len(argv) > 3 and argv[2] == 'help':
            wasanbon.show_help_description('init')


        os.umask(0000)
        repo = wasanbon.setting['common']['repository']['wasanbon']
        if not os.path.isdir(wasanbon.rtm_home):
            os.mkdir(wasanbon.rtm_home, 0777)
        if not os.path.isdir(wasanbon.rtm_temp):
            os.mkdir(wasanbon.rtm_temp, 0777)
        
        template_setting_file = os.path.join(wasanbon.__path__[0], 'settings', sys.platform, 'setting.yaml')
        template_repository_file = os.path.join(wasanbon.__path__[0], 'settings', sys.platform, 'repository.yaml')
        local_setting_file = os.path.join(wasanbon.rtm_home, 'setting.yaml')
        local_repository_file = os.path.join(wasanbon.rtm_home, 'repository.yaml')
        if os.path.isfile(local_setting_file):
            if util.yes_no('There seems to be a setting file in %s. Do you want to initialize?' % wasanbon.rtm_home) == 'yes':
                os.remove(local_setting_file)
                shutil.copyfile(template_setting_file, local_setting_file)
            else:
                return
        else:
            shutil.copyfile(template_setting_file, local_setting_file)
        if os.path.isfile(local_repository_file):
            if util.yes_no('There seems to be a repository file in %s. Do you want to initialize?' % wasanbon.rtm_home) == 'yes':
                os.remove(local_repository_file)
                shutil.copyfile(template_repository_file, local_repository_file)

            else:
                return
        else:
            shutil.copyfile(template_repository_file, local_repository_file)
        init_tools_path()

        platform.check_and_install_devtools()

        if platform.check_devtools():
            sys.stdout.write('Wasanbon initialization OK.\n')
        else:
            sys.stdout.write('If you want to install devtools, sudo wasanbon-admin.py init --install\n')

        init_tools_path()

        rtm.install_rtm(False)

        tools.install_tools()

        if sys.platform == 'win32':
            sys.stdout.write("Please Reboot Windows to properly configure your system.\n")
        
