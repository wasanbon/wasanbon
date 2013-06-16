import os, sys, shutil
import wasanbon

from wasanbon import util

def create_rtm_home(force, verbose):
    os.umask(0000)
    repo = wasanbon.setting['common']['repository']['wasanbon']
    if not os.path.isdir(wasanbon.rtm_home):
        os.mkdir(wasanbon.rtm_home, 0777)
    if not os.path.isdir(wasanbon.rtm_temp):
        os.mkdir(wasanbon.rtm_temp, 0777)
            
    if sys.platform == 'linux2' or sys.platform == 'darwin':
        home_stat = os.stat(os.environ['HOME'])
        os.chown(wasanbon.rtm_home, home_stat.st_uid, home_stat.st_gid)
        os.chown(wasanbon.rtm_temp, home_stat.st_uid, home_stat.st_gid)

def copy_initial_setting(verbose=False, force=False):
    # Copy initial setting file.
    template_setting_file = os.path.join(wasanbon.__path__[0], 'settings', sys.platform, 'setting.yaml')
    template_repository_file = os.path.join(wasanbon.__path__[0], 'settings', sys.platform, 'repository.yaml')
    local_setting_file = os.path.join(wasanbon.rtm_home, 'setting.yaml')
    local_repository_file = os.path.join(wasanbon.rtm_home, 'repository.yaml')
    if os.path.isfile(local_setting_file) or os.path.isfile(local_repository_file):
        if util.yes_no('There seems to be a setting file in %s. Do you want to initialize?' % wasanbon.rtm_home) == 'yes':
            os.remove(local_repository_file)
            os.remove(local_setting_file)
        else:
            return

    shutil.copyfile(template_setting_file, local_setting_file)
    fout = open(local_repository_file, 'w') # create empty file.
    fout.close()
        
