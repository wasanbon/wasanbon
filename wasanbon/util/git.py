import os, yaml, subprocess

import wasanbon

def clone_and_setup(url):
    distpath = os.path.join(wasanbon.rtm_temp, os.path.basename(url)[:-4])
    if not 'local' in wasanbon.setting.keys():
        wasanbon.setting['local'] = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))

    cmd = [wasanbon.setting['local']['git'], 'clone', url, distpath]
    print cmd
    subprocess.call(cmd)
    crrdir = os.getcwd()
    os.chdir(distpath)
    cmd = ['python', 'setup.py', 'install', '--record', 'installed_files.txt']
    subprocess.call(cmd)
    os.chdir(crrdir)

