import os, sys, yaml
import wasanbon
from wasanbon.core.template import *

def check_devtools():
    fin = open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r')
    y = yaml.load(fin)

    flag = False    
    for key in y.keys():
        if len(y[key]) == 0:
            sys.stdout.write('%s can not be found.\n')
            flag = True

    return not flag


def check_and_install_devtools():
    fin = open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r')
    y = yaml.load(fin)

    for key in y.keys():
        if len(y[key]) == 0:
            install_cmd(key)

def install_cmd(cmd):
    if sys.platform == 'darwin':
        download_and_install(wasanbon.setting[sys.platform]['packages'][cmd])
    elif sys.platform == 'win32':
        if cmd == 'emacs':
            download_and_unpack(wasanbon.setting[sys.platform]['packages'][cmd],
                                dist=wasanbon.setting['common']['path']['RTM_HOME'])
        else:
            download_and_install(wasanbon.setting[sys.platform]['packages'][cmd])
    else:
        print 'Unsupported System %s' % sys.platform

def install_cmake():
    if sys.platform == 'darwin':
        install_cmake_osx()
    elif sys.platform == 'win32':
        install_cmake_win32()
    elif sys.platform == 'linux2':
        install_cmake_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_git():
    if sys.platform == 'darwin':
        install_git_osx()
    elif sys.platform == 'win32':
        install_git_win32()
    elif sys.platform == 'linux2':
        install_git_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_doxygen():
    if sys.platform == 'darwin':
        install_doxygen_osx()
    elif sys.platform == 'win32':
        install_doxygen_win32()
    elif sys.platform == 'linux2':
        install_doxygen_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_jdk():
    if sys.platform == 'darwin':
        install_jdk_osx()
    elif sys.platform == 'win32':
        install_jdk_win32()
    elif sys.platform == 'linux2':
        install_jdk_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_svn():
    if sys.platform == 'darwin':
        install_svn_osx()
    elif sys.platform == 'win32':
        install_svn_win32()
    elif sys.platform == 'linux2':
        install_svn_linux()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_emacs():
    if sys.platform == 'win32':
        install_emacs_win32()
    else:
        print 'Unsupported system:%s' % sys.platform
    pass

def install_cmake_osx():
    setting = load_settings()
    download_and_install(setting['darwin']['packages']['cmake'])
    pass

def install_cmake_win32():
    setting = load_settings()
    download_and_install(setting['win32']['packages']['cmake'])
    pass

def install_git_osx():
    setting = load_settings()
    download_and_install(setting['darwin']['packages']['git'])
    pass

def install_git_win32():
    setting = load_settings()
    download_and_install(setting['win32']['packages']['git'])
    pass

def install_doxygen_osx():
    setting = load_settings()
    download_and_install(setting['darwin']['packages']['doxygen'])
    pass

def install_doxygen_win32():
    setting = load_settings()
    download_and_install(setting['win32']['packages']['doxygen'])
    pass

def install_jdk_osx():
    setting = load_settings()
    download_and_install(setting['darwin']['packages']['jdk'])

def install_jdk_win32():
    setting = load_settings()
    download_and_install(setting['win32']['packages']['jdk'])

def install_svn_osx():
    print 'Install Xcode commandline tool. Xcode -> Preference -> Download'

def install_svn_win32():
    setting = load_settings()
    download_and_install(setting['win32']['packages']['svn'])

def install_emacs_win32():
    setting = load_settings()
    #print setting['win32']['packages']['emacs']

