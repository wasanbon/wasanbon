import wasanbon
import os, sys, subprocess
import shutil
from wasanbon import util

def __apt_preparation():
    srcsfile = '/etc/apt/sources.list.d/openrtm-aist.list'
    key1 = 'deb http://www.openrtm.org/pub/Linux/ubuntu/ raring main\n'
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

def __ppa_preparation():
    subprocess.call(['add-apt-repository', '-y', 'ppa:openrtm/stable'])
    subprocess.call(['add-apt-repository', '-y', 'ppa:openrtm/unstable'])
    subprocess.call(['apt-get', 'update'])


def is_installed():
    if sys.platform == 'darwin':
        file = 'version.txt'
        path = '/usr/local/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        path = '/usr/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        if ('RTM_ROOT' in os.environ.keys()):
            if os.path.isfile(os.path.join(os.environ['RTM_ROOT'], 'rtm', file)):
                return True
        return False

    elif sys.platform == 'linux2':
        file = 'version.txt'
        path = '/usr/local/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        path = '/usr/include/openrtm-1.1/rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        if ('RTM_ROOT' in os.environ.keys()):
            if os.path.isfile(os.environ['RTM_ROOT'], 'rtm', file):
                return True
        return False

    elif sys.platform == 'win32':
        file = 'version.txt'
        path = 'C:\\Program Files (x86)\\OpenRTM-aist\\1.1\\rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        path = 'C:\\Program Files\\OpenRTM-aist\\1.1\\rtm'
        if os.path.isfile(os.path.join(path, file)):
            return True
        if ('RTM_ROOT' in os.environ.keys()):
            if os.path.isfile(os.environ['RTM_ROOT'], 'rtm', file):
                return True
        return False

    else:
        raise wasanbon.UnsupportedPlatformError()

    return False



def install(force=False, verbose=False):
    if is_installed() and not force:
        if verbose:
            sys.stdout.write(" - OpenRTM C++ Version is already installed.\n")
        return False

    if sys.platform == 'darwin':
        install_cpprtm_osx(force, verbose=verbose)
    elif sys.platform == 'win32':
        install_cpprtm_win(force, verbose=verbose)
    elif sys.platform == 'linux2':
        install_cpprtm_linux(force, verbose=verbose)
    pass


def install_cpprtm_win(force, verbose=False):
    if wasanbon.platform().startswith("windows"):
        sys.stdout.write(' - Windows Detected.\n')
        util.download_and_unpack(wasanbon.setting()[wasanbon.platform()]['packages']['vcpvcr71'], wasanbon.rtm_temp())
        src_dir = os.path.join(wasanbon.rtm_temp(), 'vcpvcr71', 'dll')
        files = ['msvcp71.dll', 'msvcr71.dll']
        if wasanbon.platform().endswith('_x86'):
            dst_dir = 'C:\\Windows\\System32'
        else:
            dst_dir = 'C:\\Windows\\SysWow64'
        sys.stdout.write(' - Copying msvcr71 and msvcp71\n')
        for file in files:
            src_file = os.path.join(src_dir, file)
            dst_file = os.path.join(dst_dir, file)
            if not os.path.isfile(src_file):
                sys.stdout.write(' @ Can not find %s\n' % src_file)
                raise wasanbon.NoSuchFileException()
            if os.path.isfile(dst_dir):
                sys.stdout.write(' - %s is already exists.\n')
            else:
                shutil.copy(src_file, dst_file)
                
    util.download_and_install(wasanbon.setting()[wasanbon.platform()]['packages']['c++'], force=force, verbose=verbose)

def install_cpprtm_linux(force, verbose=False):
    #util.download_and_install(wasanbon.setting[wasanbon.platform]['packages']['c++_ppa'], force=force)
    #__ppa_preparation()
    __apt_preparation()
    util.download_and_install(wasanbon.setting()[wasanbon.platform()]['packages']['c++'], force=force, verbose=verbose)

def install_cpprtm_osx(force=False, verbose=False):
    util.download_and_install(wasanbon.setting()[wasanbon.platform()]['packages']['c++'], force=force, verbose=verbose)
    
    srcdir = '/usr/local/lib/python2.7/site-packages' 
    distdir = os.path.split(wasanbon.__path__[0])[0]

    sys.stdout.write(' - Please check license agreement of Xcode.\n')
    cmd = ['xcodebuild', '-license']
    ret = subprocess.call(cmd)
    if ret < 0:
        return False

    sys.stdout.write(' - Copying omniORBpy modules\n');
    for file in os.listdir(srcdir):
        filepath = os.path.join(srcdir, file)
        distpath = os.path.join(distdir, file)
        if os.path.isfile(filepath):
            if os.path.isfile(distpath) and force:
                os.remove(distpath)
            if not os.path.isfile(distpath):
                shutil.copy2(filepath, distpath)
        elif os.path.isdir(filepath):
            if os.path.isdir(distpath) and force:
                shutil.rmtree(distpath)
            if not os.path.isdir(distpath):
                shutil.copytree(os.path.join(srcdir, file), os.path.join(distdir, file))
    pass

