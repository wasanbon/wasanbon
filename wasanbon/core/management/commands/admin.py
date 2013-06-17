import sys, os

import wasanbon
from wasanbon.core import tools 
from wasanbon.core import system
from xml.etree import ElementTree
from wasanbon.core.template.init import *

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv, verbose, clean, force):
        if len(argv) < 3:
            print 'To read help, input "mgr.py admin help"'
            return

        if argv[2] == 'register':
            appname = os.path.basename(os.getcwd())
            appdir  = os.getcwd()
            print ' - Trying to register %s to %s' % (appname, os.path.join(wasanbon.rtm_home, "workspace.yaml"))
            
            register_workspace(appname, appdir, verbose=verbose)

