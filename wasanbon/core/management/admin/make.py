#!/usr/bin/env python
import os, sys, optparse, traceback
import wasanbon
import wasanbon.core.package as pack


def alternative(argv=None):
    return []
    

def execute_with_argv(argv, verbose):

    usage = "wasanbon-admin.py repository [subcommand] ...\n"
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    #parser.add_option('-l', '--long', help='show status in long format', action='store_true', default=False, dest='long_flag')
    parser.add_option('-s', '--service', help='set upstream service',  default='github', metavar='SERVICE', dest='service')
    parser.add_option('-c', '--clean', help='Clean up binaries',  action='store_true', default=False, dest='clean_flag')

    try:
        options, argv = parser.parse_args(argv[:])
    except:
        traceback.print_exc()
        return


    clean = options.clean_flag

    if verbose:
        sys.stdout.write(' @ Making wasanbon package.\n')
    _packages = pack.get_packages(verbose=verbose)


    if len(argv) == 2: # wasanbon-admin.py make. This can be called if current directory is in the package
        for _package in _packages:
            normpath = os.path.normcase(os.path.normpath(_package.path))
            prefix = os.path.commonprefix([os.getcwd(), normpath])
            if os.path.isdir(prefix) and os.stat(prefix) == os.stat(normpath):
                if verbose:
                    sys.stdout.write(' - Found Package (%s)\n' % _package.name)
                    pass
                argv.append(_package.name)

    wasanbon.arg_check(argv, 3)

    _package = pack.get_package(argv[2])
    if verbose:
        sys.stdout.write(' - Changing direcotry to %s\n' % _package.path)
    curdir = os.getcwd()
    os.chdir(_package.path)
    reload(wasanbon)

    if len(argv) == 3:
        for rtc_ in _package.rtcs:
            if verbose:
                sys.stdout.write(' - Found RTC %s\n' % rtc_.name)
            normpath = os.path.normcase(os.path.normpath(rtc_.path))
            prefix = os.path.commonprefix([curdir, normpath])
            if verbose:
                sys.stdout.write(' - normpath = %s\n' % normpath)
                sys.stdout.write(' - prefix = %s\n' % prefix)
            if os.path.isdir(prefix) and os.stat(prefix) == os.stat(rtc_.path):
                if verbose:
                    sys.stdout.write(' - Match %s\n' % rtc_.name)
                    pass
                argv.append(rtc_.name)

    if len(argv) == 3:
        # The package is specified successfully but RTC is not specified.
        # In this case, all rtc is built.
        for _rtc in _package.rtcs:
            if verbose:
                sys.stdout.write(' - Add RTC (%s) to build list.\n' % _rtc.name)
            argv.append(_rtc.name)

    for name in argv[3:]:
        _rtc = _package.rtc(name)
        if clean:
            _rtc.clean(verbose=verbose)
        else:
            _rtc.build(verbose=verbose)

            
