#!/usr/bin/env python
import wasanbon
from wasanbon.core.template.init import *

class Command(object):
    def __init__(self):
        pass
    
    def is_admin(self):
        return True

    def execute_with_argv(self, argv):
        if len(argv) < 3:
            wasanbon.show_help_description('project')
            return
        if argv[2] == 'help':
            wasanbon.show_help_description('project')
            return
        if argv[2] == 'create':
            if len(argv) < 4:
                wasanbon.show_help_description('project')
                return
            init_workspace(argv[3])
        elif argv[2] == 'list':
            list_workspace()
        elif argv[2] == 'unregister':
            if len(argv) < 4:
                wasanbon.show_help_description('project')
                return
            unregister_workspace(argv[3])

