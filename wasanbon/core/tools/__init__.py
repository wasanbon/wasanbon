import os, sys
import yaml
import wasanbon
from wasanbon import util
from wasanbon.util import git

def install_tools():
    y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
    url = wasanbon.setting[sys.platform]['packages']['eclipse']
    util.download_and_unpack(url, wasanbon.rtm_home)


    try:
        import rtctree
    except ImportError, e:
        url = wasanbon.setting['common']['git']['rtctree']
        git.clone_and_setup('rtctree', url)
    try:
        import rtsprofile
    except ImportError, e:
        url = wasanbon.setting['common']['git']['rtsprofile']
        git.clone_and_setup('rtsprofile', url)
    try:
        import rtshell
    except ImportError, e:
        url = wasanbon.setting['common']['git']['rtshell']
        git.clone_and_setup('rtshell', url)
    pass

