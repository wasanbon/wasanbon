import os, sys, shutil, subprocess
import wasanbon
from . import cpp, python, java

rtm_root_hints = ['/usr/local/include/openrtm-1.1', '/usr/include/openrtm-1.1']


def get_rtm_root():
    if 'RTM_ROOT' in os.environ.keys():
        return os.environ['RTM_ROOT']
    else:
        for hint in rtm_root_hints:
            if os.path.isfile(os.path.join(hint, 'rtm', 'version.txt')):
                return hint
        return ""

def post_install_care(force=False):
    if sys.platform == 'darwin':
        post_install_darwin(force, verbose)

    if sys.platform == 'linux2':
        post_install_linux2(force)
    pass
    
def install(force=False, verbose=False):
    if sys.platform == 'linux2':
        __ppa_preparation()

    cpp.install(force, verbose=verbose)
    python.install(force, verbose=verbose)
    java.install(force, verbose=verbose)
    post_install_care(force=force)
    
    pass


def post_install_darwin(force, verbose=False):
    return


def post_install_linux2(force):
    return 

