#!/usr/bin/env python

import os
import sys

from wasanbon import *
import wasanbon.core.management.commands
from optparse import OptionParser, make_option, NO_DEFAULT 
from OptionParserEx import *

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

def autocomplete(self):
    if 'TPR_AUTO_COMPLETE' not in os.environ:
        return
    
    cwords = os.environ['COMP_WORDS'].split()[1:]
    cword = int(os.environ['COMP_CWORDS'])
    
    try:
        curr = cwords[cword-1]
    except IndexError:
        curr = ''
        pass

    subcommands = get_commands().keys() + ['help']
    options = [('--help', None)]
    
    if cword == 1:
        print ' '.join(sorted(filtar(lambda x: x.startswith(curr), subcommands)))
    elif cwords[0] in subcommands and cwords[0] != 'help':
        subcommand_cls = self
        pass
    pass


def show_help_text():
    sys.stdout.write("Help");

def execute(appname):
    import wasanbon
    wasanbon.app_name = app_name

    parser = OptionParserEx(usage="%prog subcommand [options] [args]",
                            version=get_version(),
                            option_list=option_list)
        
    try:
        options, args = parser.parse_args(sys.argv[:])
        if options.settings:
            os.environ['TPR_SETTING_MODULE'] = options.settings
            if options.pythonpath:
                sys.path.insert(0, options.pythonpath)
    except:
        pass

    try:
        subcommand = sys.argv[1]
    except IndexError:
        subcommand = 'help'
        pass

    if subcommand == 'help':
        show_help_text()
    elif len(args) <= 1:
        show_help_text()
    else:
        fetch_subcommand(subcommand).execute_with_argv(sys.argv[:])
        pass
    pass

def fetch_subcommand(subcommand):
    """
    Fetch command directory to find implemented commands.
    You can add command by adding ***.py file.
    """
    command_dir = os.path.join(wasanbon.core.management.__path__[0], 'commands')
    commands = [f[:-3] for f in os.listdir(command_dir) if not f.startswith('_') and f.endswith('.py')]
    app_name = dict([(name, 'wasanbon.core') for name in commands])
    module_name =  'wasanbon.core.management.commands.%s' %  subcommand
    __import__(module_name)
    return sys.modules[module_name].Command()

    
