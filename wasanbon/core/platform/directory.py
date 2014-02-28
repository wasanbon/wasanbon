import os, sys, shutil
import wasanbon
from wasanbon import util

def create_rtm_home(force, verbose):
    if verbose:
        sys.stdout.write(' - Initializing RTM_HOME.\n')
    os.umask(0000)
    repo = wasanbon.setting()['common']['repository']['wasanbon']
    rtm_home = wasanbon.rtm_home()
    rtm_temp = wasanbon.rtm_temp()
    if not os.path.isdir(rtm_home):
        if verbose:
            sys.stdout.write(' - No RTM_HOME found. Creating RTM_HOME in %s\n' % wasanbon.rtm_home())
        os.mkdir(rtm_home, 0777)
        
    if not os.path.isdir(rtm_temp):
        if verbose:
            sys.stdout.write(' - No RTM_HOME found. Creating RTM_TEMP in %s\n' % wasanbon.rtm_temp())
        os.mkdir(rtm_temp, 0777)
            
    if sys.platform == 'linux2' or sys.platform == 'darwin':
        if verbose:
            sys.stdout.write(' - Changing the Ownership of RTM_HOME and RTM_TEMP\n')
        home_stat = os.stat(os.environ['HOME'])
        os.chown(rtm_home, home_stat.st_uid, home_stat.st_gid)
        os.chown(rtm_temp, home_stat.st_uid, home_stat.st_gid)


def copy_setting_file(verbose=False, force=False):
    # Copy initial setting file.
    if verbose:
        sys.stdout.write(' - Copying initial setting files to RTM_HOME.\n')

    template_setting_file = os.path.join(wasanbon.__path__[0], 'settings', wasanbon.platform(), 'setting.yaml')
    local_setting_file = os.path.join(wasanbon.rtm_home(), 'setting.yaml')
    if os.path.isfile(local_setting_file):
        if not force:
            if verbose and util.no_yes(' - There seems to be a setting file in %s.\n - Do you want to initialize?' % wasanbon.rtm_home()) == 'yes':
                os.remove(local_setting_file)
            else:
                return
        else:
            os.remove(local_setting_file)

    if verbose:
        sys.stdout.write(" - Copying %s to %s\n" % (template_setting_file, local_setting_file))
    shutil.copyfile(template_setting_file, local_setting_file)


def copy_repository_file(verbose=False, force=False):
    # Copy initial setting file.
    if verbose:
        sys.stdout.write(' - Copying initial setting files to RTM_HOME.\n')

    template_repository_file = os.path.join(wasanbon.__path__[0], 'settings', wasanbon.platform(), 'repository.yaml')
    local_repository_file = os.path.join(wasanbon.rtm_home(), 'repository.yaml')
    if os.path.isfile(local_repository_file):
        if not force:
            if verbose and util.no_yes(' - There seems to be a setting file in %s.\n - Do you want to initialize?' % wasanbon.rtm_home()) == 'yes':
                os.remove(local_repository_file)
            else:
                return
        else:
            os.remove(local_repository_file)

    fout = open(local_repository_file, 'w') # create empty file.
    fout.close()
        
