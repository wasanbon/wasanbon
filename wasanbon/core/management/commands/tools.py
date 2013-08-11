import sys, os

import wasanbon
from wasanbon.core import tools 
#from wasanbon.core import system
#from xml.etree import ElementTree
from wasanbon.core import project as prj

class Command(object):
    def __init__(self):
        pass


    def execute_with_argv(self, argv, verbose, clean, force):
        wasanbon.arg_check(argv, 3)

        proj = prj.Project(os.getcwd())

        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            tools.launch_eclipse('RTC_DIR', verbose=verbose)
            return

        if(argv[2] == 'rtcb'):
            print 'Launching Eclipse'
            tools.launch_eclipse('RTC_DIR', verbose=verbose)
            return

        if(argv[2] == 'rtse'):
            print 'Launching Eclipse'
            #system.run_system(nobuild=True, nowait=True, verbose=verbose)
            proj.
            tools.launch_eclipse('RTS_DIR', nonblock=False, verbose=verbose)
            system.terminate_all_process()
            return
    
        wasanbon.show_help_description('tools')
