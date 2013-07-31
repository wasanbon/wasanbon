import os, yaml, subprocess
import shutil
import wasanbon

def clone_and_setup(url, verbose=False, force=False):
    distpath = os.path.join(wasanbon.rtm_temp, os.path.basename(url)[:-4])
    if not 'local' in wasanbon.setting.keys():
        wasanbon.setting['local'] = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))

    stdout = None if verbose else subprocess.PIPE

    if os.path.isdir(distpath):
        print ' - Path (%S) is existing' % distpath
        if force:
            print ' - Force to install'
            if verbose:
                print ' - Removing Path (%S)' % distpath
            shutil.rmtree(distpath)

    cmd = [wasanbon.setting['local']['git'], 'clone', url, distpath]
    if verbose:
        print ' - Cloning %s' % url
    subprocess.call(cmd, stdout=stdout)
    crrdir = os.getcwd()
    os.chdir(distpath)
    cmd = ['python', 'setup.py', 'install', '--record', 'installed_files.txt']
    if verbose:
        print ' - Install (setup.py install) in %s' % distpath
    subprocess.call(cmd, stdout=stdout)
    os.chdir(crrdir)

    
