"""
- Use Initialization of wasanbon's environment.
"""
import sys, traceback
import wasanbon
#from wasanbon.core import platform

def alternative():
    return []

def execute_with_argv(args, verbose=False):
    sys.stdout.write(' - Starting wasanbon environment.\n')
    
    sys.stdout.write(' - Initializing RTM home directory\n')

    try:
        __import__('yaml')
    except ImportError, ex:
        traceback.print_exc()
        sys.stdout.write(' - Impot Error. You need to install PyYAML module.\n')
        ret = raw_input(' @ Do you want to install PyYAML automatically?(Y/n):')
        if ret == '' or ret.startswith('Y') or ret.startswith('y'):
            install_pyyaml(force=True, verbose=verbose)
            return True
        
    platform.init_rtm_home(verbose=verbose)

    
def install_pyyaml(force=False, verbose=False):
    __import__('wasanbon.setup')
    setup = sys.modules['wasanbon.setup']
    if not setup.download_and_install('pyyaml', force=force, verbose=verbose):
        sys.stdout.write(' @ Error. There may be "download" directory in the current path.\n')
