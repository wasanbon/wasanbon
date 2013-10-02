import os, sys, yaml
import wasanbon
from wasanbon import util

def check_commands(verbose=False, install=False):
    y = yaml.load(open(os.path.join(wasanbon.rtm_home, 'setting.yaml'), 'r'))
    return [check_command(cmd, y[cmd], verbose=verbose, install=install) for cmd in y.keys()]


def check_command(cmd_key, cmd_path, verbose=False, install=False):
    if os.path.isfile(cmd_path):
        if verbose: 
            sys.stdout.write(' - command [%s] is installed.\n' % cmd_key)
        return True
    if verbose:
        sys.stdout.write(' - command [%s] is NOT installed.\n' % cmd_key)

    if install:
        return install_command(cmd_key, verbose=verbose)

    return False

def install_command(cmd, verbose=False):
    if verbose:
        sys.stdout.write(' - installing command [%s]\n' % cmd)

    if cmd == 'java':
        return

    if sys.platform == 'darwin':
        return util.download_and_install(wasanbon.setting[wasanbon.platform]['packages'][cmd],
                                  verbose=verbose)
    elif sys.platform == 'win32':
        if cmd == 'emacs':
            return util.download_and_unpack(wasanbon.setting[wasanbon.platform]['packages'][cmd],
                                     dist_path=wasanbon.setting['common']['path']['RTM_HOME'],
                                     verbose=verbose)
        else:
            return util.download_and_install(wasanbon.setting[wasanbon.platform]['packages'][cmd], 
                                      verbose=verbose)
    elif sys.platform == 'linux2':
        return util.download_and_install(wasanbon.setting['linux2']['packages'][cmd],
                                  verbose=verbose)
    raise wasanbon.UnsupportedPlatformError()


