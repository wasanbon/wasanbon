import os, sys
import yaml
import wasanbon
from wasanbon import util


def install_tools():
    y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
    url = wasanbon.setting[sys.platform]['packages']['eclipse']
    util.download_and_unpack(url, wasanbon.rtm_home)

    try:
        import rtctree
    except ImportError, e:
        url = setting['common']['git']['rtctree']
        util.git.clone_and_setup(url)
    try:
        import rtsprofile
    except ImportError, e:
        url = setting['common']['git']['rtsprofile']
        util.git.clone_and_setup(url)
    try:
        import rtshell
    except ImportError, e:
        url = setting['common']['git']['rtshell']
        util.git.clone_and_setup(url)
    pass


