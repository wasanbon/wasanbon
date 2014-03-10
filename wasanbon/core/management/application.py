#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, types, optparse, traceback, inspect

import wasanbon
from wasanbon import help
    
def get_subcommand_list(package):
    """
    Get Subcommand from Directory
    wasanbon/core/management/%package%
    package can be admin or commands.
    """
    #mod = __import__('wasanbon.core.management.' + package)
    ret = [x[:len(x)-3] for x in os.listdir(os.path.join(wasanbon.core.management.__path__[0], package)) if x.endswith('.py') and not x.startswith("__")]
    ret.append('help')
    return ret

def show_help_description(package, subcommand, long=False):
    print help.get_help_text(package, subcommand, long)

class ArgumentParser(optparse.OptionParser):
    def __init__(self, usage, add_help_option):
        optparse.OptionParser.__init__(self,usage=usage, add_help_option=add_help_option)
        self.__usage = usage
    
    def print_help(self):
        print self.__usage
        pass

    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                optparse.OptionParser._process_args(self,largs,rargs,values)
            except (optparse.BadOptionError, optparse.AmbiguousOptionError), e:
                largs.append(e.opt_str)

def execute(argv=None):
    if argv == None:
        argv = sys.argv
    command = os.path.basename(argv[0])

    if command == 'wasanbon-admin.py':
        package = 'admin'
    else:
        package = 'commands'

    opts = get_subcommand_list(package)
    try:
        usage  = '[Usage]\n$ ' + command + ' [subcommand] (for help, use -h option with subcommand.)\n\n'
        usage = usage + '[subcommands]\n'
        for opt in opts:
            usage = usage + ' - ' + opt + '\n'
    except Exception, e:
        traceback.print_exc()
        return 

    
    parser = ArgumentParser(usage=usage, add_help_option=False)
    parser.add_option('-h', '--help', help=usage, action='store_true', default=False, dest='help_flag')
    parser.add_option('-l', '--longmessage', help='Show long help message', action='store_true', default=False, dest='longhelp_flag')
    parser.add_option('-v', '--verbose', help='You will get more messgaes', action='store_true', default=False, dest='verbose_flag')
    parser.add_option('-a', '--alternative', help="Get subcommand list.", action='store_true', default=False, dest='alter_flag')
    options, args = parser.parse_args(argv[:])

    if options.alter_flag and len(args) == 1:
        return print_alternative(opts)
        
    if len(args) == 1:
        args.append('help')

    subcommand = args[1]

    if not subcommand in opts:
        subcommand = 'help'

    if subcommand == 'help':
        parser.print_help()
        return

    if options.help_flag == True:
        show_help_description(package, subcommand, options.longhelp_flag)
        return

    # If not help but option is add
    if options.longhelp_flag:
        args = args + ['-l']

    module_name = 'wasanbon.core.management.%s.%s' % (package, subcommand)
    __import__(module_name)
    mod = sys.modules[module_name]

    try:
        if options.alter_flag:
            print_alternative(mod.alternative(args))
        else:
            mod.execute_with_argv(args, verbose=options.verbose_flag)

    except wasanbon.InvalidUsageException, ex:
        show_help_description(package, subcommand)
    except wasanbon.WasanbonException, ex:
        if options.verbose_flag:
            traceback.print_exc()
        sys.stdout.write(' # Error. %s\n' % ex.msg())
    except Exception, ex:
        traceback.print_exc()
    pass

def print_alternative(alternative, argv=None):
    for i, cmd in enumerate(alternative):
        sys.stdout.write(cmd)
        if i == len(alternative) - 1:
            sys.stdout.write('\n')
        else:
            sys.stdout.write(' ')
            pass
