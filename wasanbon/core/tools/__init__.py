import os, sys
import yaml
import wasanbon
from wasanbon import util
from wasanbon.util import git

def install_tools():
    y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
    url = wasanbon.setting[sys.platform]['packages']['eclipse']
    util.download_and_unpack(url, wasanbon.rtm_home)

    try:
        import rtctree
    except ImportError, e:
        url = wasanbon.setting['common']['git']['rtctree']
        git.clone_and_setup(url)
    try:
        import rtsprofile
    except ImportError, e:
        url = wasanbon.setting['common']['git']['rtsprofile']
        git.clone_and_setup(url)
    try:
        import rtshell
    except ImportError, e:
        url = wasanbon.setting['common']['git']['rtshell']
        git.clone_and_setup(url)
    pass

def clone_and_setup(url):
    y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))
    url = setting['common']['git'][key]
    cmd = [y['git_path'], 'clone', url, wasanbon.rtm_temp]
    subprocess.call(command)

    crrdir = os.getcwd()
    os.chdir(os.path.join(rtm_temp, key))
    command = ['python', 'setup.py', 'install', '--record', 'installed_files.txt']
    subprocess.call(command)
    os.chdir(crrdir)

