import os, sys, subprocess
import yaml
import wasanbon
from wasanbon import lib
import wasanbon.core
from wasanbon import util
from wasanbon.util import git
from wasanbon.core import rtm

def install(force=False, verbose=False):
    y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))

    try:
        import OpenRTM_aist

        if force:
            url = wasanbon.setting['common']['git']['rtctree']
            git.clone_and_setup(url)
            url = wasanbon.setting['common']['git']['rtsprofile']
            git.clone_and_setup(url)
            url = wasanbon.setting['common']['git']['rtshell']
            git.clone_and_setup(url)

        else:
            try:
                import rtctree
            except ImportError, e:
                url = wasanbon.setting['common']['git']['rtctree']
                git.clone_and_setup(url, verbose=verbose)
            try:
                import rtsprofile
            except ImportError, e:
                url = wasanbon.setting['common']['git']['rtsprofile']
                git.clone_and_setup(url, verbose=verbose)
            try:
                import rtshell
            except ImportError, e:
                url = wasanbon.setting['common']['git']['rtshell']
                git.clone_and_setup(url, verbose=verbose)
            pass

    except ImportError, e:
        sys.stdout.write('OpenRTM_aist can not be imported. Please install RTM first.\n')
    
    eclipse_dir = os.path.join(wasanbon.rtm_home, 'eclipse')
    if not os.path.isdir(eclipse_dir) or force:
        url = wasanbon.setting[sys.platform]['packages']['eclipse']
        util.download_and_unpack(url, wasanbon.rtm_home, force=force, verbose=verbose)

def install_arduino(verbose=False, force=False):
    arduino_dir = os.path.join(wasanbon.rtm_home, 'arduino')
    if not os.path.isdir(arduino_dir) or force:
        url = wasanbon.setting[sys.platform]['packages']['arduino']
        util.download_and_unpack(url, wasanbon.rtm_home, force)

def install_rtno(verbose=False, force=False):
    install_arduino(verbose, force)
    arduino_dir = os.path.join(wasanbon.rtm_home, 'Arduino.app', 'Contents', 'Resources', 'Java')
    dist_path = os.path.join(arduino_dir, 'libraries', 'RTno')
    if os.path.isdir(dist_path):
        print ' - Error exit.'
        return 
    repo = lib.get_repository('RTno', verbose=verbose)
    git.git_command(['clone', repo.url, dist_path], verbose=verbose)
    
    

def launch_eclipse(workbench = ".", argv=None, nonblock=True, verbose=False):
    eclipse_dir = os.path.join(wasanbon.rtm_home, 'eclipse')
    eclipse_cmd = os.path.join(eclipse_dir, "eclipse")

    env = os.environ
    env['RTM_ROOT'] = rtm.get_rtm_root()

    if sys.platform == 'win32':
        eclipse_cmd = eclipse_cmd + '.exe'
    if not os.path.isfile(eclipse_cmd):
        sys.stdout.write("Eclipse can not be found in %s.\n" % eclipse_cmd)
        sys.stdout.write("Please install eclipse by 'wasanbon-admin.py tools install' command.\n")
        return

    if not os.path.isdir(workbench) or workbench == '.':
        if verbose:
            sys.stdout.write("Starting eclipse in current directory.\n")
        cmd = [eclipse_cmd]
    else:
        if verbose:
            sys.stdout.write("Starting eclipse in current project directory(%s).\n" % workbench)
        cmd = [eclipse_cmd, '-data', workbench]

    if argv != None:
        cmd = cmd + argv

    if sys.platform == 'win32':
        p = subprocess.Popen(cmd, creationflags=512, env=env, stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE)

    if not nonblock:
        p.wait()


def launch_arduino(workbench, nonblock=True, verbose=False):
    env = os.environ
    env['RTM_ROOT'] = rtm.get_rtm_root()


    if sys.platform == 'darwin':
        arduino_dir = os.path.join(wasanbon.rtm_home, 'Arduino.app')
        cmd = ['open', arduino_dir]
        p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE)
        if not nonblock:
            p.wait()
        return


    if sys.platform == 'win32':
        arduino_cmd = arduino_cmd + '.exe'
    if not os.path.isfile(arduino_cmd):
        sys.stdout.write("Arduino can not be found in %s.\n" % arduino_cmd)
        sys.stdout.write("Please install arduino by 'wasanbon-admin.py tools install' command.\n")
        return

    if not os.path.isfile(os.path.join(os.getcwd(), "setting.yaml")):
        cmd = [arduino_cmd]
    else:
        if 'RTC_DIR' in wasanbon.setting['application'].keys():
            sys.stdout.write("Starting arduino in current project directory.\n")
            cmd = [arduino_cmd, '-data', os.path.join(os.getcwd(), wasanbon.setting['application'][workbench])]
        else:
            cmd = [arduino_cmd]

    if sys.platform == 'win32':
        p = subprocess.Popen(cmd, creationflags=512, env=env, stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE)

    if not nonblock:
        p.wait()

    
