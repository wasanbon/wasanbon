import os, sys, yaml
import wasanbon
from wasanbon import util

def check_commands(verbose=False, install=False):
    if verbose:
        sys.stdout.write(' - Now checking Installation of commands.\n')
    y = yaml.load(open(os.path.join(wasanbon.rtm_home(), 'setting.yaml'), 'r'))
    return [check_command(cmd, y[cmd], verbose=verbose, install=install) for cmd in y.keys()]


def check_command(cmd_key, cmd_path, verbose=False, install=False, force=False):
    if os.path.isfile(cmd_path):
        if verbose: 
            sys.stdout.write('   - command [%s] is installed.\n' % cmd_key)
            pass
        if not force:
            return True
        else:
            sys.stdout.write('   @ command [%s] is forced to install....\n' % cmd_key)
    elif verbose:
        sys.stdout.write('   @ command [%s] is NOT installed.\n' % cmd_key)

    if install:
        return install_command(cmd_key, verbose=verbose, force=force)

    return False

def install_command(cmd, verbose=False, force=False):
    if verbose:
        sys.stdout.write(' - Installing command [%s]\n' % cmd)

    if cmd == 'java':
        return False

    if sys.platform == 'darwin':
        return util.download_and_install(wasanbon.setting()[wasanbon.platform()]['packages'][cmd],
                                  verbose=verbose, force=force)
    elif sys.platform == 'win32':
        if cmd == 'emacs':
            return util.download_and_unpack(wasanbon.setting()[wasanbon.platform()]['packages'][cmd],
                                     dist_path=wasanbon.setting()['common']['path']['RTM_HOME'],
                                     verbose=verbose, force=force)
        else:
            return util.download_and_install(wasanbon.setting()[wasanbon.platform()]['packages'][cmd], 
                                      verbose=verbose, force=force)
    elif sys.platform == 'linux2':
        return util.download_and_install(wasanbon.setting()[wasanbon.platform()]['packages'][cmd],
                                  verbose=verbose, force=force)
    raise wasanbon.UnsupportedPlatformError()


