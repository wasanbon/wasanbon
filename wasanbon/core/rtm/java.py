import os, sys, shutil, subprocess

import wasanbon 
from wasanbon import util


def is_installed():
    return os.path.isfile(os.path.join(wasanbon.setting()['common']['path']['RTM_ROOT_JAVA'], wasanbon.setting()['common']['file']['RTM_JAR']))


def install(force=False, verbose=False):
    if is_installed() and not force:
        sys.stdout.write(" - OpenRTM Java Version is already installed.\n")
        return False
    rtm_root_java = wasanbon.setting()['common']['path']['RTM_ROOT_JAVA']
    if not os.path.isdir(rtm_root_java):
        os.makedirs(rtm_root_java)
    util.download_and_unpack(wasanbon.setting()['common']['packages']['java'], wasanbon.rtm_temp(), force=force)
    for root, dirs, files in os.walk(os.path.join(wasanbon.rtm_temp(), 'OpenRTM-aist')):
        for file in files:
            if file.endswith('.jar'):
                shutil.copyfile(os.path.join(root, file),os.path.join(rtm_root_java, file))
    pass

