#!/usr/bin/env python
import os, sys, yaml
import wasanbon
from wasanbon.core.template import *
from wasanbon.core.rtc import *
from wasanbon.core import rtc

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, argv, verbose, clean, force):
        if verbose:
            sys.stdout.write(' - Making wasanbon project.\n')

        curdir = os.path.normcase(os.path.normpath(os.getcwd()))
        ws = get_projects(verbose=verbose)
        if not ws:
            print ' - Error: workspace list can not be found.'
            return

        if len(argv) < 3: # Search parent Directory
            for key, path in ws.items():
                pp = os.path.normcase(os.path.normpath(path))
                plist = [curdir, pp]
                prefix = os.path.commonprefix(plist)
                if os.path.isdir(prefix) and os.stat(prefix) == os.stat(pp):
                    print 'Found in %s' % key
                    argv.append(key)

        if len(argv) < 3:
            wasanbon.show_help_description('make')
            return

        if not argv[2] in ws.keys():
            print ' - Error: %s can not be found.' % argv[2]
            return
        
        os.chdir(ws[argv[2]])
        reload(wasanbon)

        if len(argv) < 4:
            rtcps = rtc.parse_rtcs()
            for rtcp in rtcps:
                pp = os.path.normcase(os.path.normpath(os.path.dirname(rtcp.filename)))
                plist = [curdir, pp]
                prefix = os.path.commonprefix(plist)
                if os.path.isdir(prefix) and os.stat(prefix) == os.stat(pp):
                    print 'Found RTC: %s' % key
                    argv.append(rtcp.basicInfo.name)

        if clean:
            argv.append('--clean')

        rtcps = rtc.parse_rtcs()
        if '--clean' in argv:
            clean_all = True if 'all' in argv else False
            for i in range(3, len(argv)):
                rtc_name = argv[i]
                for rtcp in rtcps:
                    if rtcp.basicInfo.name == rtc_name or clean_all:
                        print 'Cleanup RTC(%s).' % rtcp.basicInfo.name
                        clean_rtc(rtcp)
            return
        else:
            build_all = True if 'all' in argv else False
            for i in range(3, len(argv)):
                rtc_name = argv[i]
                for rtcp in rtcps:
                    if rtcp.basicInfo.name == rtc_name or build_all:
                        print 'Building rtc [%s]' % rtcp.basicInfo.name
                        build_rtc(rtcp)
            return
