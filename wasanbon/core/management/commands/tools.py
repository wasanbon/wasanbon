import sys, os

import wasanbon
from wasanbon.core import tools 
from wasanbon.core import system
from xml.etree import ElementTree

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv):
        if len(argv) < 3:
            wasanbon.show_help_description('tools')
            return

        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            tools.launch_eclipse('RTC_DIR')
            return

        if(argv[2] == 'rtcb'):
            print 'Launching Eclipse'
            tools.launch_eclipse('RTC_DIR')
            return

        if(argv[2] == 'rtse'):
            print 'Launching Eclipse'
            """
            xmlfile = os.path.join(os.getcwd(), 'system','RTSE_Files','.project')
            tree = ElementTree.parse(xmlfile)
            elem = tree.getroot()
            for e in elem.getiterator():
                if e.tag == 'link':
                    old_str = e.findtext('location')
            new_str = os.path.join(os.getcwd(), 'system', 'DefaultSystem.xml')

            if os.path.isfile(xmlfile+'_bak'):
                os.remove(xmlfile + '_bak')
            os.rename(xmlfile, xmlfile+'_bak')
            
            fin = open(xmlfile+'_bak', 'r')
            fout = open(xmlfile, 'w')
            for line in fin:
                line = line.replace(old_str, new_str)
                fout.write(line)
            """

            system.run_system(nobuild=True, nowait=True)
            tools.launch_eclipse('RTS_DIR', nonblock=False)
            system.terminate_all_process()
            return
    
        wasanbon.show_help_description('tools')
