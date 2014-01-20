#!/usr/bin/env python
import os, sys
import wasanbon
import wasanbon.core.package as pack

class Command(object):
    def __init__(self):
        pass

    def alternative(self):
        return []
    
    def execute_with_argv(self, argv, verbose, clean, force):
        if verbose:
            sys.stdout.write(' @ Making wasanbon package.\n')
        _packages = pack.get_packages(verbose=verbose)

        if len(argv) == 2: # wasanbon-admin.py make
            for _package in _packages:
                normpath = os.path.normcase(os.path.normpath(_package.path))
                prefix = os.path.commonprefix([os.getcwd(), normpath])
                if os.path.isdir(prefix) and os.stat(prefix) == os.stat(normpath):
                    if verbose:
                        sys.stdout.write(' - Found Package (%s)\n' % _package.name)
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
                #if verbose:
                #    sys.stdout.write(' - normpath = %s\n' % normpath)
                #    sys.stdout.write(' - prefix = %s\n' % prefix)
                if os.path.isdir(prefix) and os.stat(prefix) == os.stat(rtc_.path):
                    if verbose:
                        sys.stdout.write(' - Match %s\n' % rtc_.name)
                    argv.append(rtc_.name)

        wasanbon.arg_check(argv, 4)

        rtc_ = _package.rtc(argv[3])
        if clean:
            rtc_.clean(verbose=verbose)
        else:
            rtc_.build(verbose=verbose)

            
