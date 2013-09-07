import os, sys, shutil, subprocess
import wasanbon
from wasanbon import util

def is_installed():
    try:
        import OpenRTM_aist
        return True
    except ImportError, e:
        return False
    pass


def install(force=False):
    if is_installed() and not force:
        print " - Your system has OpenRTM_aist package in PYTHONPATH."
        return False
    if sys.platform == 'darwin':
        install_pyrtm_osx(force)
    elif sys.platform == 'win32':
        install_pyrtm_win(force)
    elif sys.platform == 'linux2':
        install_pyrtm_linux(force)
    pass


def install_pyrtm_win(force):
    util.download_and_install(wasanbon.setting[wasanbon.platform]['packages']['python'], force=force)


def install_pyrtm_linux(force):
    #util.download_and_install(wasanbon.setting['linux2']['packages']['python_ppa'], force=force)
    install_pyrtm_osx(force) # install from source.

def install_pyrtm_osx(force):
    if not 'local' in wasanbon.setting.keys():
        wasanbon.setting['local'] = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))

    old_dir = os.getcwd()
    os.chdir(wasanbon.rtm_temp)
    reponame = wasanbon.setting['common']['svn']['python']
    cmd = [wasanbon.setting['local']['svn'], 'co', reponame]
    ret = subprocess.call(cmd)
    if reponame.endswith('/'):
        reponame = reponame[:-1]
    dirname = os.path.basename(reponame)
    os.chdir(dirname)
    cmd = ['python', 'setup.py', 'build_core']
    ret = subprocess.call(cmd)
    cmd = ['python', 'setup.py', 'install']
    ret = subprocess.call(cmd)
    cmd = ['python', 'setup.py', 'install_example']
    ret = subprocess.call(cmd)
    os.chdir(old_dir)
