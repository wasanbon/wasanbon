#!/usr/bin/env python

import sys
import wasanbon
from wasanbon.core import rtm

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return True

    def execute_with_argv(self, argv):
        if len(argv) < 3:
            wasanbon.show_help_description('rtm')
            return
            
        if(argv[2] == 'install'):
            sys.stdout.write('Installing OpenRTM-aist\n')
            if len(argv) >= 4 and argv[3] == '--force':
                rtm.install_rtm(True)
            else:
                rtm.install_rtm(False)
        elif(argv[2] == 'status'):
            print 'OpenRTM-aist Status'
            ret = rtm.get_status()
            print ' - OpenRTM-aist C++    : %s' % ret['c++']
            print ' - OpenRTM-aist Python : %s' % ret['python']
            print ' - OpenRTM-aist Java   : %s' % ret['java']
                
