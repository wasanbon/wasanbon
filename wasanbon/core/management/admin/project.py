import os, sys
import wasanbon
from wasanbon.core.template import init

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, argv):
        if len(argv) < 3:
            print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
            return

        if argv[2] == 'create':
            if len(argv) < 4:
                print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
                return
            init.init_workspace(argv[3])

        elif argv[2] == 'list':
            init.list_workspace()

        elif argv[2] == 'unregister':
            if len(argv) < 4:
                print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
                return
            init.unregister_workspace(argv[3])

