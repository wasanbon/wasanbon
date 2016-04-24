#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, types, optparse, traceback, inspect

import wasanbon
    
def get_subcommand_list(package):
    """ Get Subcommand from Directory
    wasanbon/core/management/%package%
    package can be admin or commands.
    """
    ret = []
    ret.append('help')
    for n in wasanbon.plugins.get_plugin_names(package):
        if wasanbon.plugins.get_plugin(package, n).is_manifest_plugin():
            if not n in ret:
                ret.append(n)
    return ret


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

def show_plugin_help(package, subcommand):
    name = package +'.' + subcommand
    plugin = wasanbon.plugins.get_plugin(package, subcommand)

    print 'Usage : |'
    if '__doc__' in dir(plugin):
        if plugin.__doc__ != None:
            docs = [s.strip() for s in plugin.__doc__.split('\n')]
            for d in docs:
                print '  ', d
        else:
            print '  %s (No Help)' % subcommand
    else:
        print '  %s (No Help)' % subcommand
    
    alts = plugin.get_manifest_function_names()
    print 'Subcommand :'
    for a in alts:
        print '  %s : |' % a
        func = getattr(plugin, a, None)
        if  not func.__doc__ is None:
            docs = [s.strip() for s in func.__doc__.split('\n')]
            for d in docs:
                if not len(d) == 0:
                    print '    %s' % d
        else:
            print '    %s' % 'No Help'

def print_long_help(command, package):
    print 'Usage : '
    print '  ', command, ' [command] (for help, use -h option with subcommand.)'
    print 'Commands :'
    subcommands = get_subcommand_list(package) 
    for subcommand in subcommands:
        if is_plugin_command(package, subcommand):
            plugin = wasanbon.plugins.get_plugin(package, subcommand)
            if '__doc__' in dir(plugin):
                if plugin.__doc__ != None:
                    docs = [s.strip() for s in plugin.__doc__.split('\n')]
                    print '  ', subcommand, ': |'
                    for d in docs:
                        print '    ', d
                else:
                    print '  ', subcommand, ' ' *(15-len(subcommand)) + ': "No Help"'
            else:
                print '  ', subcommand
        else:
            print '  ', subcommand
        

def execute(argv=None):
    if argv == None:
        argv = sys.argv
    command = os.path.basename(argv[0])

    if command == 'wasanbon-admin.py':
        package = 'admin'
    else:
        package = 'mgr'

    opts = get_subcommand_list(package)
    try:
        usage  = '[Usage]\n$ ' + command + ' [subcommand] (for help, use -h option with subcommand.)\n\n'
        usage = usage + '[subcommands]\n'
        for opt in opts:
            usage = usage + ' - ' + opt + '\n'
    except Exception, e:
        traceback.print_exc()
        return 

    opts.append('plugin')
    
    parser = ArgumentParser(usage=usage, add_help_option=False)
    parser.add_option('-h', '--help', help=usage, action='store_true', default=False, dest='help_flag')
    #parser.add_option('-l', '--longmessage', help='Show long help message', action='store_true', default=False, dest='longhelp_flag')
    #parser.add_option('-v', '--verbose', help='You will get more messgaes', action='store_true', default=False, dest='verbose_flag')
    parser.add_option('-a', '--alternative', help="Get subcommand list.", action='store_true', default=False, dest='alter_flag')
    options, args = parser.parse_args(argv[:])

    if options.alter_flag and len(args) == 1:
        return print_alternative(opts)
        
    if len(args) == 1:
        args.append('help')

    subcommand = args[1]
    
    verbose = '-v' in args


    if not subcommand in opts:
        subcommand = 'help'

    if subcommand == 'help':
        print_long_help(command, package)
        return 0


    if options.help_flag == True:
        args = args + ['-h']

    try:
        if options.alter_flag:
            if subcommand == 'plugin':
                return wasanbon.plugins.run_command(package, subcommand, args + ['-a'])
                pass
            else:
                print_module_alternatives(package, subcommand, args=args)
        elif subcommand == 'plugin':
            return wasanbon.plugins.run_command(package, subcommand, args)
        else:
            return run_command(package, subcommand, args)

    except wasanbon.PrintAlternativeException, ex:
        return 0

    except wasanbon.InvalidUsageException, ex:
        run_command(package, subcommand, ['-h'])
        return -1
    except wasanbon.PackageNotFoundException, ex:
        if verbose:
            traceback.print_exc()
        sys.stdout.write('# Package Not Found.\n')

    except wasanbon.RTCNotFoundException, ex:
        
        sys.stdout.write('# RTC Not Found.\n')
        
    except wasanbon.WasanbonException, ex:
        if verbose: traceback.print_exc()
        sys.stdout.write('## WasanbonError. %s\n' % ex.msg())
        return -1
    except Exception, ex:
        if verbose: traceback.print_exc()
        sys.stdout.write('## UnknownError.\n')
        return -1
    return -2


def run_command(package, subcommand, args, options= None):
    """ Execute Plugin Commands """

    if is_plugin_command(package, subcommand): # Check if subcommands are in alternatives
        plugin = wasanbon.plugins.get_plugin(package, subcommand)
        alts = plugin.get_manifest_function_names()
        target_function = None
        for arg in args[2:]:
            if arg.startswith('-'): continue
            if arg in alts:
                target_function = arg
                break
            pass
        if target_function is None and '__call__' in alts:
            return plugin(args)
        elif target_function is None:
            if '-h' in args or '--help' in args:
                show_plugin_help(package, subcommand)
            else:
                raise wasanbon.InvalidUsageException()
        else:
            return getattr(plugin, target_function)(args)
    else:
        raise wasanbon.InvalidUsageException()
    pass


def print_module_alternatives(package, subcommand, args):
    if is_plugin_command(package, subcommand):
        plugin = wasanbon.plugins.get_plugin(package, subcommand)
        
        alts = plugin.get_manifest_function_names()
        can_call = False
        if '__call__' in alts:
            can_call = True

        alts = [a for a in alts if not a == '__call__']
        argv = [arg for arg in args if not arg.startswith('-')]
        if len(argv) == 2 and can_call:
            args.append('-a')
            return plugin(args)
        elif len(argv) >= 3:
            if argv[2] in alts:
                args.append('-a')
                return getattr(plugin, argv[2])(args)

        print_alternative(alts)

    else:
        raise wasanbon.InvalidUsageException()
    pass


def print_alternative(alternative, argv=None):
    for i, cmd in enumerate(alternative):
        sys.stdout.write(cmd)
        if i == len(alternative) - 1:
            sys.stdout.write('\n')
        else:
            sys.stdout.write(' ')
            pass

def is_plugin_command(package, cmd):
    cmds = wasanbon.plugins.get_plugin_names(package)
    return True if cmd in cmds else False
