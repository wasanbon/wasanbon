#!/usr/bin/env python

import os
import sys
import OpenTPR

import OpenTPR.core.management.commands
from OpenTPR import *
from optparse import OptionParser, make_option, NO_DEFAULT 
from TPROptionParser import *


option_list = (
        make_option('-v', '--verbosity', action='store', dest='verbosity', default='1',
            type='choice', choices=['0', '1', '2', '3'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output'),
        make_option('--settings',
            help='The Python path to a settings module, e.g. "myproject.settings.main". If this isn\'t provided, the DJANGO_SETTINGS_MODULE environment variable will be used.'),
        make_option('--pythonpath',
            help='A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".'),
        make_option('--traceback', action='store_true',
            help='Print traceback on exception'),
    )

class Utility(object):
    

    def __init__(self, argv=None):
        self.__argv = argv or sys.argv[:]
        self.__program_name = os.path.basename(self.__argv[0])

    def autocomplete(self):
        if 'TPR_AUTO_COMPLETE' not in os.environ:
            return

        cwords = os.environ['COMP_WORDS'].split()[1:]
        cword = int(os.environ['COMP_CWORDS'])

        try:
            curr = cwords[cword-1]
        except IndexError:
            curr = ''

        subcommands = get_commands().keys() + ['help']
        options = [('--help', None)]

        if cword == 1:
            print ' '.join(sorted(filtar(lambda x: x.startswith(curr), subcommands)))
        elif cwords[0] in subcommands and cwords[0] != 'help':
            subcommand_cls = self


    def execute(self):
        parser = TPROptionParser(usage="%prog subcommand [options] [args]",
                                 version=get_version(),
                                 option_list=option_list)
        
        try:
            options, args = parser.parse_args(self.__argv)
            if options.settings:
                os.environ['TPR_SETTING_MODULE'] = options.settings
            if options.pythonpath:
                sys.path.insert(0, options.pythonpath)
            
        except:
            pass

        try:
            subcommand = self.__argv[1]
        except IndexError:
            subcommand = 'help'
        if subcommand == 'help':
            sys.stdout.write(self.show_help_text() + '\n')
        elif len(args) <= 1:
            sys.stdout.write(self.show_help_text() + '\n')
        else:
            self.fetch_subcommand(subcommand).execute_with_argv(self.__argv)

    def show_help_text(self):
        return 'show_help_text'
    
    def find_commands(self, dir):
        command_dir = os.path.join(dir, 'commands')
        try:
            return [f[:-3] for f in os.listdir(command_dir) if not f.startswith('_') and f.endswith('.py')]
        except OSError:
            return []
        pass
                    
    def fetch_subcommand(self, subcommand):
        app_name = dict([(name, 'OpenTPR.core') for name in self.find_commands(OpenTPR.core.management.__path__[0])])
        module = OpenTPR.core.management.import_module('OpenTPR.core.management.commands.%s' %  subcommand)
        return module.Command()
    


if __name__ == '__main__':
    utility = Utility(None)
    utility.execute()
