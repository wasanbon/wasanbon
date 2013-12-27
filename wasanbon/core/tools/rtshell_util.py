import os, sys, subprocess
import yaml
import wasanbon
from wasanbon import lib
import wasanbon.core
from wasanbon import util
from wasanbon.util import git
from wasanbon.core import rtm


def is_installed_rtctree(verbose=False):
    try:
        import rtctree
        return True
    except ImportError, e:
        return False

def is_installed_rtsprofile(verbose=False):
    try:
        import rtsprofile
        return True
    except ImportError, e:
        return False

def is_installed_rtshell(verbose=False):
    try:
        import rtshell
        return True
    except ImportError, e:
        return False
    
def install_rtshell(force=False, verbose=False):
    try:
        import OpenRTM_aist

        if not is_installed_rtctree() or force:
            url = wasanbon.setting['common']['git']['rtctree']
            git.clone_and_setup(url, verbose=True, force=force)
        if not is_installed_rtsprofile() or force:
            url = wasanbon.setting['common']['git']['rtsprofile']
            git.clone_and_setup(url, verbose=True, force=force)
        if not is_installed_rtshell() or force:
            url = wasanbon.setting['common']['git']['rtshell']
            git.clone_and_setup(url, verbose=True, force=force)


    except ImportError, e:
        sys.stdout.write(' - OpenRTM_aist can not be imported. Please install RTM first.\n')
    
