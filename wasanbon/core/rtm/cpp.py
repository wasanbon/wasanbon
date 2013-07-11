import wasanbon
import os, sys

from wasanbon import util

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
            if os.path.isfile(os.environ['RTM_ROOT'], 'rtm', file):
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



def install(force=False):
    if is_installed() and not force:
        print " - Your system seems to have OpenRTM C++."
        return False

    if sys.platform == 'darwin':
        install_cpprtm_osx(force)
    elif sys.platform == 'win32':
        install_cpprtm_win(force)
    elif sys.platform == 'linux2':
        install_cpprtm_linux(force)
    pass


def install_cpprtm_win(force):
    util.download_and_install(wasanbon.setting['win32']['packages']['c++'], force=force)

def install_cpprtm_linux(force):
    util.download_and_install(wasanbon.setting['linux2']['packages']['c++_ppa'], force=force)

def install_cpprtm_osx(force):
    util.download_and_install(wasanbon.setting['darwin']['packages']['c++'], force=force)
    srcdir = '/usr/local/lib/python2.7/site-packages' 
    distdir = os.path.split(wasanbon.__path__[0])[0]
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

