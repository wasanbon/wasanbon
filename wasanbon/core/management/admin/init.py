"""
- Use Initialization of wasanbon's environment.
"""
import sys, traceback
import wasanbon
#from wasanbon.core import platform


def try_import_and_install(pack, verbose=False, force=False):
    if verbose:
        sys.stdout.write(' - Trying to import %s module.\n' % pack)
    try:
        __import__(pack)
        return sys.modules[pack]
    except ImportError, ex:
        traceback.print_exc()
        sys.stdout.write(' - Import Error. You need to install python-%s module.\n' % pack)
        sys.stdout.write(' @ AUTOMATIC INSTALL\n')
        sys.stdout.write(' @ You will may need to invoke the command with superuser privileges to install.\n')
        ret = raw_input(' @ Do you want to install python-%s automatically?(Y/n):' % pack)
        if ret == '' or ret.startswith('Y') or ret.startswith('y'):
            __import__('wasanbon.setup')
            setup = sys.modules['wasanbon.setup']
            if not setup.download_and_install(pack, force=force, verbose=verbose):
                sys.stdout.write(' @ Error. There may be "download" directory in the current path.\n')
    return False
    
def alternative():
    return []

def execute_with_argv(args, verbose=False):
    sys.stdout.write(' - Starting wasanbon environment.\n')
    sys.stdout.write(' - Initializing RTM home directory\n')

    force = True

    yaml = try_import_and_install('yaml', verbose=verbose, force=force)
    github = try_import_and_install('github', verbose=verbose, force=force)

    if not all([yaml, github]):
        sys.stdout.write(' @ Try wasanbon-admin.py init again.\n')
        return False

    __import__('wasanbon.core.platform')
    platform = sys.modules['wasanbon.core.platform']        
    platform.init_rtm_home(verbose=verbose)
 
