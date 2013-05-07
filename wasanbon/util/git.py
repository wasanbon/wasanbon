import os, yaml, subprocess

import wasanbon

def clone_and_setup(distname, url):
    #y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
    distpath = os.path.join(wasanbon.rtm_temp, distname)
    cmd = [wasanbon.setting['local']['git'], 'clone', url, wasanbon.rtm_temp, distpath]
    subprocess.call(command)

    crrdir = os.getcwd()
    os.chdir(distpath)
    command = ['python', 'setup.py', 'install', '--record', 'installed_files.txt']
    subprocess.call(command)
    os.chdir(crrdir)

