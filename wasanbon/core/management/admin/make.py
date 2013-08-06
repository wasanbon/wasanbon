#!/usr/bin/env python
import os, sys, yaml
import wasanbon
#from wasanbon.core.template import *
#from wasanbon.core.rtc import *
#from wasanbon.core import rtc
import wasanbon.core.project as prj

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, argv, verbose, clean, force):
        if verbose:
            sys.stdout.write(' - Making wasanbon project.\n')

        projs = prj.get_projects(verbose=verbose)
        if len(argv) == 2: # wasanbon-admin.py make
            for proj in projs:
                normpath = os.path.normcase(os.path.normpath(proj.path))
                prefix = os.path.commonprefix([os.getcwd(), normpath])
                if os.path.isdir(prefix) and os.stat(prefix) == os.stat(normpath):
                    if verbose:
                        sys.stdout.write(' - Found %s\n' % proj.name)
                    argv.append(proj.name)


        if len(argv) == 2:
            sys.stdout.write(' - Invalid Usage. To show help, use --help option.\n')
            return

        proj = prj.get_project(argv[2])
        if verbose:
            sys.stdout.write(' - Changing direcotry to %s\n' % proj.path)
        os.chdir(proj.path)
        reload(wasanbon)

        if len(argv) == 3:
            for rtc_ in proj.rtcs:
                if verbose:
                    sys.stdout.write(' - Found RTC %s\n' % rtc_.name)
                normpath = os.path.normcase(os.path.normpath(rtc_.path))
                prefix = os.path.commonprefix([os.getcwd(), normpath])
                if os.path.isdir(prefix) and os.stat(prefix) == os.stat(proj.path):
                    if verbose:
                        sys.stdout.write(' - Found %s\n' % rtc_.name)
                    argv.append(rtc_.name)

        if len(argv) == 3:
            sys.stdout.write(' - Invalid Usage. To show help, use --help option.\n')
            return 

        rtc_ = proj.rtc(argv[3])
        if clean:
            rtc_.clean(verbose=verbose)
        else:
            rtc_.build(verbose=verbose)

            
