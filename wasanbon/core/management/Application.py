#!/usr/bin/env python

import os
import sys
import yaml

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


def show_help_text(command):
    import locale, yaml, os
    locale_name = locale.getdefaultlocale()[0]
    filename = 'en_US.yaml'
    path = os.path.join(wasanbon.__path__[0], 'locale', 'messages')
    for file in os.listdir(path):

        if file.endswith('.yaml'):
            if file[:len(file)-5] == locale_name:
                filename = locale_name + '.yaml'
    y = yaml.load(open(os.path.join(path, filename), 'r'))
    sys.stdout.write("Usage : %s [subcommand] [args...]\n" % os.path.basename(command))
    sys.stdout.write(" - subcommand : \n")
    for subcommand in get_subcommand_list():
        desc = 'No information'
        if subcommand in y['help']['command']['brief'].keys():
            desc = y['help']['command']['brief'][subcommand]
        sys.stdout.write(("   - %s" + (" " * (18-len(subcommand))) +": %s\n") % (subcommand, desc))
    
def get_subcommand_list():
    import wasanbon.core.management.commands
    ret = [x[:len(x)-3] for x in os.listdir(os.path.join(wasanbon.core.management.__path__[0], 'commands')) if x.endswith('.py') and not x.startswith("__")]
    ret.append('help')
    return ret

def execute():
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
        show_help_text(sys.argv[0])
        return
    elif len(args) <= 1:
        show_help_text(sys.argv[0])
        return
    elif not subcommand in get_subcommand_list():
        show_help_text(sys.argv[0])
        return 

    module_name =  'wasanbon.core.management.commands.%s' %  subcommand
    __import__(module_name)
    comm = sys.modules[module_name].Command()

    comm.execute_with_argv(sys.argv[:])
    pass



    
