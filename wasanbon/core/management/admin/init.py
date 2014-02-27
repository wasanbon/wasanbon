"""
- Use Initialization of wasanbon's environment.
"""
import sys
import wasanbon
from wasanbon.core import platform

def alternative():
    return []

def execute_with_argv(args, verbose=False):
    sys.stdout.write(' - Starting wasanbon environment.\n')
    
    sys.stdout.write(' - Initializing RTM home directory\n')
    
    platform.init_rtm_home(verbose=verbose)

    
