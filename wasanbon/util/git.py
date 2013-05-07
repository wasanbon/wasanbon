import os, yaml, subprocess

import wasanbon

def clone_and_setup(url):
    #y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
    distpath = os.path.join(wasanbon.rtm_temp, os.path.basename(url)[:-4])
    cmd = [wasanbon.setting['local']['git'], 'clone', url, distpath)
    subprocess.call(cmd)
    crrdir = os.getcwd()
    os.chdir(distpath)
    cmd = ['python', 'setup.py', 'install', '--record', 'installed_files.txt']
    subprocess.call(cmd)
    os.chdir(crrdir)

