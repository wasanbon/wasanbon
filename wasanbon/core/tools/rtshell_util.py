import os, sys, subprocess
import yaml
import wasanbon
from wasanbon import lib
import wasanbon.core
from wasanbon.util import git
from wasanbon.core import rtm


def is_installed_rtctree(verbose=False):
    try:
        import rtctree
        if verbose:
            sys.stdout.write(' - rtctree is already installed.\n')
        return True
    except ImportError, e:
        return False

def is_installed_rtsprofile(verbose=False):
    try:
        import rtsprofile
        if verbose:
            sys.stdout.write(' - rtsprofile is already installed.\n')
        return True
    except ImportError, e:
        return False

def is_installed_rtshell(verbose=False):
    try:
        import rtshell
        if verbose:
            sys.stdout.write(' - rtshell is already installed.\n')
        return True
    except ImportError, e:
        return False
    
def install_rtshell(force=False, verbose=False):
    try:
        import OpenRTM_aist

        if not is_installed_rtctree(verbose=verbose) or force:
            url = wasanbon.setting()['common']['git']['rtctree']
            git.clone_and_setup(url, verbose=True, force=force)
        if not is_installed_rtsprofile(verbose=verbose) or force:
            url = wasanbon.setting()['common']['git']['rtsprofile']
            git.clone_and_setup(url, verbose=True, force=force)
        if not is_installed_rtshell(verbose=verbose) or force:
            url = wasanbon.setting()['common']['git']['rtshell']
            git.clone_and_setup(url, verbose=True, force=force)


    except ImportError, e:
        sys.stdout.write(' - OpenRTM_aist can not be imported. Please install RTM first.\n')
    
