import os, sys, shutil, subprocess

import wasanbon 
from wasanbon import util
from . import status

def install_javartm(arg=False):
    if status.is_javartm_installed() and not arg:
        print "Your system have OpenRTM_aist java file in RTM_HOME directory."
        return False
    rtm_root_java = wasanbon.setting['common']['path']['RTM_ROOT_JAVA']
    if not os.path.isdir(rtm_root_java):
        os.makedirs(rtm_root_java)
    util.download_and_unpack(wasanbon.setting['common']['packages']['java'], wasanbon.rtm_temp, force=arg)
    for root, dirs, files in os.walk(os.path.join(wasanbon.rtm_temp, 'OpenRTM-aist')):
        for file in files:
            if file.endswith('.jar'):
                shutil.copyfile(os.path.join(root, file),os.path.join(rtm_root_java, file))
    pass


def install_cpprtm_win(force):
    util.download_and_install(wasanbon.setting['win32']['packages']['c++'], force=force)

def install_pyrtm_win(force):
    util.download_and_install(wasanbon.setting['win32']['packages']['python'], force=force)

def install_cpprtm_osx(force):
    util.download_and_install(wasanbon.setting['darwin']['packages']['c++'], force=force)
    srcdir = '/usr/local/lib/python2.7/site-packages' 
    distdir = os.path.split(wasanbon.__path__[0])[0]
    for file in os.listdir(srcdir):
        filepath = os.path.join(srcdir, file)
        if os.path.isfile(filepath):
            shutil.copy2(os.path.join(srcdir, file), os.path.join(distdir, file))
        elif os.path.isdir(filepath):
            shutil.copytree(os.path.join(srcdir, file), os.path.join(distdir, file))
    pass

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

def install_rtm_linux():
    print '-Installing OpenRTM-aist in Linux'
    p = platform.dist()
    for cmd in linux_package[p[0]]['common']:
        print '-Launching command = ' + str(cmd)
        subprocess.call(cmd)
    for pac in linux_package[p[0]][p[2]]:
        cmd = linux_package[p[0]]['install-cmd'] + tuple([pac])
        print '-Installing with command = ' + str(cmd)
        subprocess.call(cmd)
    install_rtm_java()
    pass

