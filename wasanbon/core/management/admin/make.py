#!/usr/bin/env python
import os, sys
import wasanbon
import wasanbon.core.project as prj

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, argv, verbose, clean, force):
        if verbose:
            sys.stdout.write(' @ Making wasanbon project.\n')
        projs = prj.get_projects(verbose=verbose)

        if len(argv) == 2: # wasanbon-admin.py make
            for proj in projs:
                normpath = os.path.normcase(os.path.normpath(proj.path))
                prefix = os.path.commonprefix([os.getcwd(), normpath])
                if os.path.isdir(prefix) and os.stat(prefix) == os.stat(normpath):
                    if verbose:
                        sys.stdout.write(' - Found Project (%s)\n' % proj.name)
                    argv.append(proj.name)

        wasanbon.arg_check(argv, 3)

        proj = prj.get_project(argv[2])
        if verbose:
            sys.stdout.write(' - Changing direcotry to %s\n' % proj.path)
        curdir = os.getcwd()
        os.chdir(proj.path)
        reload(wasanbon)

        if len(argv) == 3:
            for rtc_ in proj.rtcs:
                if verbose:
                    sys.stdout.write(' - Found RTC %s\n' % rtc_.name)
                normpath = os.path.normcase(os.path.normpath(rtc_.path))
                prefix = os.path.commonprefix([curdir, normpath])
                if verbose:
                    sys.stdout.write(' - normpath = %s\n' % normpath)
                    sys.stdout.write(' - prefix = %s\n' % prefix)
                if os.path.isdir(prefix) and os.stat(prefix) == os.stat(rtc_.path):
                    if verbose:
                        sys.stdout.write(' - Found %s\n' % rtc_.name)
                    argv.append(rtc_.name)

        wasanbon.arg_check(argv, 4)

        rtc_ = proj.rtc(argv[3])
        if clean:
            rtc_.clean(verbose=verbose)
        else:
            rtc_.build(verbose=verbose)

            
