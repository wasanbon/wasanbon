import sys, os

import wasanbon
from wasanbon.core import tools 
from wasanbon import util
#from wasanbon.core import system
#from xml.etree import ElementTree

class Command(object):
    def __init__(self):
        pass


    def execute_with_argv(self, argv, verbose, clean, force):
        wasanbon.arg_check(argv, 3)
        if argv[2] == 'proxy':
            if len(argv) >= 4:
                protocol, addr, port = argv[3].split(':')
                host = protocol + ':' + addr
                util.set_proxy(host, port, verbose=True)
                return
            else:
                util.omit_proxy(verbose=True)
                return

        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            if len(argv) > 3:
                args = argv[3:]
            else:
                args = None
            tools.launch_eclipse('.', argv=args, verbose=verbose)
            return
        if(argv[2] == 'arduino'):
            print '- Launching Arduino'
            if len(argv) > 3:
                args = argv[3:]
            else:
                args = None
            tools.launch_arduino('.', verbose=verbose)
            return

        raise wasanbon.InvalidUsageException()
