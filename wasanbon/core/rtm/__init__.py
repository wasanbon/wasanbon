import os, sys, shutil, subprocess
import wasanbon
from . import cpp, python, java

rtm_root_hints = ['/usr/local/include/openrtm-1.1', '/usr/include/openrtm-1.1']

def get_status():
    return {'c++' : cpp.is_installed() ,
            'python' : python.is_installed() ,
            'java' : java.is_installed() }


def get_rtm_root():
    if 'RTM_ROOT' in os.environ.keys():
        return os.environ['RTM_ROOT']
    else:
        for hint in rtm_root_hints:
            if os.path.isfile(os.path.join(hint, 'rtm', 'version.txt')):
                return hint
        return ""


def install(force=False):
    if sys.platform == 'linux2':
        __ppa_preparation()

    cpp.install(force)
    python.install(force)
    java.install(force)

    if sys.platform == 'darwin':
        post_install_darwin(force)
    
    pass

def __ppa_preparation():
    subprocess.call(['add-apt-repository',  'ppa:openrtm/stable'])
    subprocess.call(['add-apt-repository',  'ppa:openrtm/unstable'])
    subprocess.call(['apt-get', 'update'])

def __apt_preperation():
    srcsfile = '/etc/apt/sources.list.d/openrtm-aist.list'
    key1 = 'deb http://www.openrtm.org/pub/Linux/ubuntu/ precise main\n'
    #key2 = 'deb http://www.openrtm.org/pub/Linux/ubuntu/ precise-unstable main'
    if os.path.isfile(srcsfile):
        flag1 = False
            #flag2 = False
        file = open(srcsfile, 'r+w')
        for line in file:
            if line.strip() == key1:
                flag1 = True
                #if line.strip() == key2:
                #    flag2 = True

        if not flag1:
            file.write(key1)
        #if not flag2:
        #    file.write(key2)
        file.close()
    else:
        file = open(srcsfile, 'w')
        file.write(key1)
        #file.write(key2)
        file.close()

    subprocess.call(['apt-get', 'update'])

def post_install_darwin(force):
    start_str = '#-- Starting Setup Script of wasanbon --#'
    stop_str  = '#-- Ending Setup Script of wasanbon --#'
    target = os.path.join(wasanbon.get_home_path(), ".bash_profile")
    script = open(os.path.join(wasanbon.__path__[0], "settings", "darwin", "bashrc"), "r").read()
    
    
    if os.path.isfile(target):
        erase = False
        file = open(target, "r")
        fout = open(target + '.bak', "w")
        for line in file:
            if line.strip() == start_str:
                erase = True
                continue

            elif line.strip() == stop_str:
                erase = False
                continue

            if not erase:
                fout.write(line)
        
        file.close()
        fout.close()

        os.remove(target)
        os.rename(target + ".bak" , target)

        fout = open(target, "a")
    else:
        fout = open(target, "w")

    fout.write("\n\n" + start_str + "\n")
    fout.write(script)
    fout.write("\n" + stop_str + "\n\n")
            

    fout.close()
    pass


