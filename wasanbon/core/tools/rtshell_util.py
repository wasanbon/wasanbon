import os, sys, subprocess
import yaml
import wasanbon
from wasanbon import lib
import wasanbon.core
from wasanbon import util
from wasanbon.util import git
from wasanbon.core import rtm

def install_rtshell(force=False, verbose=False):
    try:
        import OpenRTM_aist

        if force:
            url = wasanbon.setting['common']['git']['rtctree']
            git.clone_and_setup(url, force=True, verbose=verbose)
            url = wasanbon.setting['common']['git']['rtsprofile']
            git.clone_and_setup(url, force=True, verbose=verbose)
            url = wasanbon.setting['common']['git']['rtshell']
            git.clone_and_setup(url, force=True, verbose=verbose)

        else:
            try:
                import rtctree
            except ImportError, e:
                
                url = wasanbon.setting['common']['git']['rtctree']
                git.clone_and_setup(url, verbose=True)
            try:
                import rtsprofile
            except ImportError, e:
                url = wasanbon.setting['common']['git']['rtsprofile']
                git.clone_and_setup(url, verbose=True)
            try:
                import rtshell
            except ImportError, e:
                url = wasanbon.setting['common']['git']['rtshell']
                git.clone_and_setup(url, verbose=True)
            pass

    except ImportError, e:
        sys.stdout.write('OpenRTM_aist can not be imported. Please install RTM first.\n')
    
