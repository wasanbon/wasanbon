#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, types, optparse, traceback
import wasanbon.core.management
from wasanbon import help
#import wasanbon.core.management.commands
#import wasanbon.core.management.admin


    
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

def show_help_description(package, subcommand):
    sys.stdout.write("\nUsage : %s %s [args...]\n"%  (os.path.basename(sys.argv[0]), subcommand))
    msg =  help.get_help_text(package, subcommand, detail=True)
    if type(msg) == types.ListType:
        for m in msg:
            sys.stdout.write(m + '\n')
    else:
        sys.stdout.write(msg + '\n')

    module_name = 'wasanbon.core.management.' + package + '.' + subcommand
    __import__(module_name)
    print sys.modules[module_name].alternative()

    print "\n\nOptions:"
    print "  -h, --help   Show This Help"

class ArgumentParser(optparse.OptionParser):
    def __init__(self, usage, add_help_option):
        optparse.OptionParser.__init__(self,usage=usage, add_help_option=add_help_option)
        self.__usage = usage
    
    def print_help(self):
        print self.__usage
        pass

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
        usage  = command + ' [subcommand]\n' + 'subcommand:\n'
        for opt in opts:
            usage = usage + ' - ' + opt + ' '*(15-len(opt)) + ':' + help.get_help_text(package, opt) + '\n'
    except Exception, e:
        traceback.print_exc()
        usage = "wasanbon-admin.py"

    parser = ArgumentParser(usage=usage, add_help_option=False)
    try:
        #parser.disable_interspersed_args()
        parser.add_option('-h', '--help', help=usage, action='store_true', default=False, dest='help_flag')
        parser.add_option('-v', '--verbose', help='You will get more messgaes', action='store_true', default=False, dest='verbose_flag')
        parser.add_option('-c', '--clean', help="", action='store_true', default=False, dest='clean_flag')
        parser.add_option('-f', '--force', help='You will force your command execution', action='store_true', default=False, dest='force_flag')
        parser.add_option('-l', '--longformat', help='You will get longer information', action='store_true', default=False, dest='long_flag')
        parser.add_option('-i', '--interactive', help='Launching command interactively', action='store_true', default=False, dest='interactive_flag')
        parser.add_option('-a', '--alternative', help="command alternative", action='store_true', default=False, dest='alter_flag')

    except:
        pass

    try:
        options, args = parser.parse_args(argv[:])
    except:
        traceback.print_exc()
        return

    index = 1
    try:
        while args[index].startswith('-'):
            index = index + 1
        subcommand = args[index]

    except IndexError:
        if len(args) == 1 and options.alter_flag:
            # list subcommands
            subcommands = opts#get_subcommand_list(package)
            for i, subcmd in enumerate(subcommands):
                sys.stdout.write(subcmd)
                if i == len(subcommands) -1:
                    sys.stdout.write('\n')
                else:
                    sys.stdout.write(' ')

            return
        subcommand = 'help'

    #opts = get_subcommand_list(package)
    if not subcommand in opts:
        subcommand = 'help'

    if subcommand == 'help':
        parser.print_help()
        return

    try:
        index = index + 1
        while args[index].startswith('-'):
            index = index + 1
        arg1 = args[index]
        if arg1 == 'help': 
            options.help_flag = True
    except:
        pass
    if options.help_flag == True:
        show_help_description(package, subcommand)
        return


    module_name = 'wasanbon.core.management.%s.%s' % (package, subcommand)
    __import__(module_name)
    comm = sys.modules[module_name].Command()

    try:
        if options.alter_flag:
            alternative = comm.alternative()
            for i, cmd in enumerate(alternative):
                sys.stdout.write(cmd)
                if i == len(alternative) - 1:
                    sys.stdout.write('\n')
                else:
                    sys.stdout.write(' ')
            pass
        else:
            comm.execute_with_argv(args, verbose=options.verbose_flag, clean=options.clean_flag, force=options.force_flag)
    except wasanbon.InvalidUsageException, ex:
        show_help_description(package, subcommand)
        
    except wasanbon.WasanbonException, ex:
        if options.verbose_flag:
            traceback.print_exc()
        sys.stdout.write(' # Error. %s\n' % ex.msg())
    except Exception, ex:
        traceback.print_exc()
    pass

