#!/usr/bin/env python

from wasanbon.core.tools import *

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        
        if(argv[2] == 'install'):
            print 'Installing Tools'
            install_tools()
        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            launch_eclipse()
