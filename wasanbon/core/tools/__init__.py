import os, sys, subprocess
import yaml
import wasanbon
import wasanbon.core
from wasanbon import util
from wasanbon.util import git
from wasanbon.core import rtm

def install_tools(force=False):
    y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
    url = wasanbon.setting[sys.platform]['packages']['eclipse']
    util.download_and_unpack(url, wasanbon.rtm_home, force)

    try:
        import OpenRTM_aist
    except ImportError, e:
        sys.stdout.write('OpenRTM_aist can not be imported. Please install RTM first.\n')
        return

    try:
        import rtctree
    except ImportError, e:
        url = wasanbon.setting['common']['git']['rtctree']
        git.clone_and_setup(url)
    try:
        import rtsprofile
    except ImportError, e:
        url = wasanbon.setting['common']['git']['rtsprofile']
        git.clone_and_setup(url)
    try:
        import rtshell
    except ImportError, e:
        url = wasanbon.setting['common']['git']['rtshell']
        git.clone_and_setup(url)
    pass


def launch_eclipse(workbench):
    eclipse_dir = os.path.join(wasanbon.rtm_home, 'eclipse')
    eclipse_cmd = os.path.join(eclipse_dir, "eclipse")

    env = os.environ
    env['RTM_ROOT'] = rtm.get_rtm_root()
    print rtm.get_rtm_root()

    if sys.platform == 'win32':
        eclipse_cmd = eclipse_cmd + '.exe'
    if not os.path.isfile(eclipse_cmd):
        sys.stdout.write("Eclipse can not be found in %s.\n" % eclipse_cmd)
        sys.stdout.write("Please install eclipse by 'wasanbon-admin.py tools install' command.\n")
        return

    if not os.path.isfile(os.path.join(os.getcwd(), "setting.yaml")):
        cmd = [eclipse_cmd]
    else:
        if 'RTC_DIR' in wasanbon.setting['application'].keys():
            sys.stdout.write("Starting eclipse in current project directory.\n")
            cmd = [eclipse_cmd, '-data', os.path.join(os.getcwd(), wasanbon.setting['application'][workbench])]
        else:
            cmd = [eclipse_cmd]

    if sys.platform == 'win32':
        subprocess.Popen(cmd, creationflags=512, env=env)
    else:
        subprocess.Popen(cmd, env=env)

    
