import os, sys, subprocess, yaml, shutil
import wasanbon
from wasanbon import util
from wasanbon.util import git
from wasanbon.core import rtm
from wasanbon import lib

from rtno_package import *

def _get_arduino_path():
    if sys.platform == 'darwin':
        return os.path.join(wasanbon.rtm_home, 'Arduino.app')
    else:
        return os.path.join(wasanbon.rtm_home, 'arduino-1.0.5')

def _get_library_path():
    if sys.platform == 'darwin':
        return os.path.join(_get_arduino_path(), 'Contents', 'Resources', 'Java', 'libraries')
    else:
        return os.path.join(_get_arduino_path(), 'libraries')

def is_installed_arduino(verbose=False):
    return os.path.isdir(_get_arduino_path())

def install_arduino(verbose=False, force=False):
    if verbose:
        sys.stdout.write(' - Installing Arduino and RTno\n')
    if not os.path.isdir(_get_arduino_path()) or force:
        url = wasanbon.setting[wasanbon.platform]['packages']['arduino']
        util.download_and_unpack(url, wasanbon.rtm_home, force=force, verbose=verbose)

def install_rtno(verbose=False, force=False):
    install_arduino(verbose, force)
    dist_path = os.path.join(_get_library_path(), 'RTno')
    sys.stdout.write(' - Searching RTno Package Installation...\n')
    if os.path.isdir(dist_path):
        sys.stdout.write('    - Found "%s"\n' % dist_path)
        sys.stdout.write('    - You have already installed RTno into your arduino.\n')
        if util.no_yes(' - Do you want to update RTno?') == 'yes':
            git.git_command(['pull'], verbose=verbose)
        return 
    sys.stdout.write(' @ Not Found. Now Installing RTno\n')
    repo = lib.get_repository('RTno', verbose=verbose)
    git.git_command(['clone', repo.url, dist_path], verbose=verbose)

def launch_arduino(workbench, nonblock=True, verbose=False):
    if sys.platform == 'darwin':
        launch_arduino_darwin(workbench, nonblock=nonblock, verbose=verbose)
    elif sys.platform == 'win32':
        launch_arduino_win32(workbench, nonblock=nonblock, verbose=verbose)        

def launch_arduino_darwin(workbench, nonblock=True, verbose=False):
    env = os.environ
    env['RTM_ROOT'] = rtm.get_rtm_root()
    cmd = ['open',  _get_arduino_path()]
    if os.path.isfile(workbench):
        cmd = ['open', '-a', _get_arduino_path(), workbench]
    if verbose:
        sys.stdout.write(' - Launching Arduino. CMD:%s\n' % cmd)
    p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE)
    if not nonblock:
        p.wait()
    return

def launch_arduino_win32(workbench, nonblock=True, verbose=False):
    env = os.environ
    env['RTM_ROOT'] = rtm.get_rtm_root()
    
    if sys.platform == 'win32':
        arduino_cmd = arduino_cmd + '.exe'
    if not os.path.isfile(arduino_cmd):
        sys.stdout.write("Arduino can not be found in %s.\n" % arduino_cmd)
        sys.stdout.write("Please install arduino by 'wasanbon-admin.py tools install' command.\n")
        return

    if not os.path.isfile(workbench):
        cmd = [arduino_cmd]
    else:
        cmd = [arduino_cmd, workbench]

    stdout = None if verbose else subprocess.PIPE

    if sys.platform == 'win32':
        p = subprocess.Popen(cmd, creationflags=512, env=env, stdout=stdout)
    else:
        p = subprocess.Popen(cmd, env=env, stdout=stdout)

    if not nonblock:
        p.wait()


def generate_rtno_temprate(pack, rtc_name, verbose=False):
    temp_file = os.path.join(_get_library_path(), 'RTno', 'examples', 'RTnoTemplate', 'RTnoTemplate.ino')
    target_dir = os.path.join(pack.path, pack.setting['RTC_DIR'], rtc_name)
    if os.path.isdir(target_dir):
        sys.stdout.write(' - Failed to create directory %s\n' % target_dir)
        return False
    target_file = os.path.join(target_dir, rtc_name + '.ino')
    os.mkdir(target_dir)
    shutil.copy(temp_file, target_file)
    return True



def get_rtno_packages(pack, verbose=False):
    rtnos = []
    rtc_path = os.path.join(pack.path, pack.setting['RTC_DIR'])
    for root, dirs, files in os.walk(rtc_path):
        for file in files:
            if file.endswith(".ino"):
                if verbose:
                    sys.stdout.write(' - %s found.\n' % file)
                rtnos.append(RTnoPackageObject(root, file))
    return rtnos


def get_rtno_package(pack, rtno_name, verbose=False):
    rtnos = get_rtno_packages(pack, verbose=False)
    for rtno in rtnos:
        if rtno.name == rtno_name:
            return rtno
    raise wasanbon.RTCNotFoundException()
