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


def install(force=False, verbose=False):
    if is_installed() and not force:
        sys.stdout.write(' - OpenRTM Python Version is already installed.\n')
        return True

    if verbose:
        sys.stdout.write(' - Your system can not import OpenRTM_aist package.\n')
        
    if sys.platform == 'darwin':
        install_pyrtm_osx(force)
    elif sys.platform == 'win32':
        install_pyrtm_win(force)
    elif sys.platform == 'linux2':
        install_pyrtm_linux(force)

    if not is_installed():
        if verbose:
            sys.stdout.write(' - Your system can not import OpenRTM_aist package.\n')
        return False

    sys.stdout.write(' - Your system can safely import OpenRTM_aist package.\n')
    return True


def install_pyrtm_win(force, verbose=True):
    util.download_and_install(wasanbon.setting[wasanbon.platform]['packages']['python'], force=force, verbose=verbose)

def install_pyrtm_linux(force, verbose=True):
    util.download_and_install(wasanbon.setting[wasanbon.platform]['packages']['python'], force=force)
    install_pyrtm_osx(force, verbose=verbose) # install from source.

def install_pyrtm_osx(force, verbose=True):
    if not 'local' in wasanbon.setting.keys():
        wasanbon.setting['local'] = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))

    stdout = None if verbose else subprocess.PIPE
    old_dir = os.getcwd()
    os.chdir(wasanbon.rtm_temp)
    reponame = wasanbon.setting['common']['svn']['python']
    cmd = [wasanbon.setting['local']['svn'], 'co', reponame]
    ret = subprocess.call(cmd, stdout=stdout)
    if reponame.endswith('/'):
        reponame = reponame[:-1]
    dirname = os.path.basename(reponame)
    os.chdir(dirname)
    cmd = ['python', 'setup.py', 'build_core']
    ret = subprocess.call(cmd, stdout=stdout)
    cmd = ['python', 'setup.py', 'install']
    ret = subprocess.call(cmd, stdout=stdout)
    cmd = ['python', 'setup.py', 'install_example']
    ret = subprocess.call(cmd, stdout=stdout)
    os.chdir(old_dir)
