import os, sys, yaml
import wasanbon
from wasanbon import util
from wasanbon.core.template import *


def check_devtools():
    fin = open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r')
    y = yaml.load(fin)

    flag = False    
    for key in y.keys():
        if len(y[key]) == 0:
            sys.stdout.write('%s can not be found.\n' % key)
            flag = True

    return not flag


def check_and_install_devtools():
    fin = open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r')
    y = yaml.load(fin)
    
    for key in y.keys():
        if len(y[key]) == 0:
            install_cmd(key)


def install_cmd(cmd):
    if cmd == 'java':
        return
    if sys.platform == 'darwin':
        util.download_and_install(wasanbon.setting[sys.platform]['packages'][cmd])
    elif sys.platform == 'win32':
        if cmd == 'emacs':
            util.download_and_unpack(wasanbon.setting[sys.platform]['packages'][cmd],
                                dist_path=wasanbon.setting['common']['path']['RTM_HOME'])
        else:
            util.download_and_install(wasanbon.setting[sys.platform]['packages'][cmd])
    elif sys.platform == 'linux2':
        util.download_and_install(wasanbon.setting['linux2']['packages'][cmd])

    else:
        print 'Unsupported System %s' % sys.platform

