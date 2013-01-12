#!/usr/bin/env python

from OpenTPR.core.rtm.install_rtm import *
from OpenTPR.core.rtm.install_tools import *

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        
        if(argv[2] == 'install'):
            print 'Installing OpenRTM-aist'
            install_rtm()
            install_tools()
