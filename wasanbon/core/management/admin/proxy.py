import os, sys, yaml, shutil, subprocess, traceback, optparse
if sys.platform == 'darwin' or sys.platform == 'linux2':
    import pwd, grp
import wasanbon
from wasanbon import util

class Command(object):
    def __init__(self):
        pass
    
    def alternative(self):
        return []

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):
        if len(argv) >= 3:
            host, port = argv[2].split(':')
            util.set_proxy(host, port, verbose=True)
            return
        else:
            util.omit_proxy(verbose=True)
            return

