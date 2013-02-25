#!/usr/bin/env python

from kotobuki.core.rtm.install_rtm import *
from kotobuki.core.rtm.install_tools import *

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        
        if(argv[2] == 'install'):
            print 'Installing OpenRTM-aist'
            install_rtm()

        if(argv[2] == 'status'):
            print 'OpenRTM-aist Status'
            status_rtm()
