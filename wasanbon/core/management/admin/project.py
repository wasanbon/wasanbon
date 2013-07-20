import os, sys
import wasanbon
from wasanbon.core import template

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, argv, verbose, force, clean):
        if len(argv) < 3:
            print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
            return

        if argv[2] == 'create':

            if len(argv) < 4:
                print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
                return
            print ' - Creating workspace %s:' % argv[3]
            template.create_project(argv[3], verbose=verbose)

        elif argv[2] == 'list':
            print ' - Listing projects.'
            projs = template.get_projects(verbose)
            if not projs:
                print '\n No project is found.'
            else:
                for key, item in projs.items():
                    print ' ' + key + ' '*(10-len(key)) + ':' + item
            print ''

        elif argv[2] == 'directory':
            projs = template.get_projects(False)
            if not projs:
                print '.'
            else:
                for key, item in projs.items():
                    if key.strip() == argv[3].strip():
                        print item
                        return
                print '.'

        elif argv[2] == 'unregister':
            if len(argv) < 4:
                print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
                return
            template.unregister_project(argv[3], verbose=verbose)

