import os, sys, time, subprocess, signal
import wasanbon
from wasanbon.core import rtc
from wasanbon.core import system
from wasanbon.core.system import run



class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv):
        if len(argv) < 3 or argv[2] == 'help':
            wasanbon.show_help_description('nameserver')
            return

        if argv[2] == 'list':
            show_nameserver_list()
            return


def show_nameserver_list():
    sys.stdout.write('Name Server List:\n')
    
    pass
