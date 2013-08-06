import os, sys, subprocess, signal
import wasanbon
def signal_action(num, frame):
    pass


def edit_rtc(rtc_obj, verbose=False):
    editenv = os.environ.copy()
    if not 'HOME' in editenv.keys():
        editenv['HOME'] = wasanbon.get_home_path()
    if sys.platform == 'darwin':
        cmd = [wasanbon.setting['local']['emacs']]
    else:
        cmd = [wasanbon.setting['local']['emacs'], '-nw']
    
    cmd = cmd + rtc_obj.packageprofile.getSourceFiles()
    signal.signal(signal.SIGINT, signal_action)
    subprocess.call(cmd, env=editenv)
    pass
