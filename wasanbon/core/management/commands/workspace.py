#!/usr/bin/env python


from wasanbon.core.template.init import *

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if argv[2] == 'init':
            if len(argv) < 3:
                print 'USAGE: wasanbon.py workspace init [YOUR WORKSPACE NAME]'
            init_workspace(argv[3])
