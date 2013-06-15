#!/usr/bin/env python

import os
import sys
import yaml


import wasanbon
import wasanbon.core.management.commands
import wasanbon.core.management.admin
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

    
def get_subcommand_list():
    import wasanbon.core.management.commands
    ret = [x[:len(x)-3] for x in os.listdir(os.path.join(wasanbon.core.management.__path__[0], 'commands')) if x.endswith('.py') and not x.startswith("__")]
    ret.append('help')
    return ret

def get_admincommand_list():
    import wasanbon.core.management.admin
    ret = [x[:len(x)-3] for x in os.listdir(os.path.join(wasanbon.core.management.__path__[0], 'admin')) if x.endswith('.py') and not x.startswith("__")]
    ret.append('help')
    return ret


def show_help_brief(is_admin):
    sys.stdout.write("\nUsage : %s [subcommand] [args...]\n\n"%  os.path.basename(sys.argv[0]))

    if is_admin:
        helps = wasanbon.get_help_text(['help','general', 'admin'])
        for help in helps:
            sys.stdout.write(" %s\n" % help) 
        sys.stdout.write("\n - subcommand : \n")
        for subcommand in get_admincommand_list():
            sys.stdout.write(("   - %s" + (" " * (18-len(subcommand))) +": %s\n") % (subcommand, wasanbon.get_help_text(['help','command', 'brief', subcommand])))
    else:
        helps = wasanbon.get_help_text(['help','general', 'command'])
        for help in helps:
            sys.stdout.write(" %s\n" % help) 
        sys.stdout.write("\n - subcommand : \n")
        for subcommand in get_subcommand_list():
            sys.stdout.write(("   - %s" + (" " * (18-len(subcommand))) +": %s\n") % (subcommand, wasanbon.get_help_text(['help','command', 'brief', subcommand])))
    print " "


def execute():
    parser = OptionParserEx(usage="%prog subcommand [options] [args]",
                            version=wasanbon.get_version(),
                            option_list=option_list)
        
    try:
        options, args = parser.parse_args(sys.argv[:])
        if options.settings:
            os.environ['TPR_SETTING_MODULE'] = options.settings
            if options.pythonpath:
                sys.path.insert(0, options.pythonpath)
    except:
        pass

    command = os.path.basename(sys.argv[0])
    if command == 'wasanbon-admin.py':
        is_admin = True
    else:
        is_admin = False

    try:
        subcommand = sys.argv[1]
    except IndexError:
        subcommand = 'help'
        pass

    if subcommand == 'help':
        show_help_brief(is_admin=is_admin)
        return
    elif len(args) <= 1:
        show_help_brief(is_admin=is_admin)
        return
    elif is_admin:
        if not subcommand in get_admincommand_list():
            show_help_brief(is_admin=is_admin)
            return 
    elif not subcommand in get_subcommand_list():
        show_help_brief(is_admin=is_admin)
        return

    if len(sys.argv) >= 3 and sys.argv[2] == 'help':
        wasanbon.show_help_description(subcommand)
        return
    if is_admin:
        module_name =  'wasanbon.core.management.admin.%s' %  subcommand
    else:
        module_name =  'wasanbon.core.management.commands.%s' %  subcommand
    __import__(module_name)
    comm = sys.modules[module_name].Command()

    comm.execute_with_argv(sys.argv[:])
    pass



    
