#!/usr/bin/env python
import wasanbon
from wasanbon.core.template.init import *

class Command(object):
    def __init__(self):
        pass
    
    def is_admin(self):
        return True

    def execute_with_argv(self, argv):
        if len(argv) < 4:
            wasanbon.show_help_description('project')
            return
        if argv[3] == 'help':
            wasanbon.show_help_description('project')
            return

        init_workspace(argv[3])
