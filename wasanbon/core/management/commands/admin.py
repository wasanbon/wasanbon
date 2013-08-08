import sys, os, getpass
#from xml.etree import ElementTree
#import wasanbon
#from wasanbon.core import tools 
#from wasanbon.core import system
#from wasanbon.core.template.init import *
from wasanbon.core import project as prj

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, force, verbose, clean):
        if len(argv) < 3:
            print 'To read help, input "mgr.py admin help"'
            return

        proj = prj.Project(os.getcwd())

        if argv[2] == 'register':
            proj.register(verbose=verbose)
            #appname = os.path.basename(os.getcwd())
            #appdir  = os.getcwd()
            #print ' - Trying to register %s to %s' % (appname, os.path.join(wasanbon.rtm_home, "workspace.yaml"))
            
            # register_workspace(appname, appdir, verbose=verbose)

        elif argv[2] == 'git_init':
            proj.git_init(verbose=verbose)
            return 

        elif argv[2] == 'github_init':
            sys.stdout.write('Initializing GIT repository in %s\n' % proj.name)
            sys.stdout.write('Username@github:')
            user = raw_input()
            passwd = getpass.getpass()

            proj.github_init(user=user, passwd = passwd, verbose=verbose)

            return

