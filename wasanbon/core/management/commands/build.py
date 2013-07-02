#!/usr/bin/env python

import wasanbon
from wasanbon.core.rtc import *
from wasanbon.core import rtc

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, verbose, force, clean):
        rtcps = rtc.parse_rtcs()
        if len(argv) < 3:
            wasanbon.show_help_description('build')
            return

        if '--clean' in argv:
            clean_all = True if 'all' in argv else False
            for i in range(2, len(argv)):
                rtc_name = argv[i]
                for rtcp in rtcps:
                    if rtcp.getName() == rtc_name or clean_all:
                        print 'Cleanup RTC(%s).' % rtcp.getName()
                        clean_rtc(rtcp)
            return
        else:
            build_all = True if 'all' in argv else False
            for i in range(2, len(argv)):
                rtc_name = argv[i]
                for rtcp in rtcps:
                    if rtcp.getName() == rtc_name or build_all:
                        print 'Building rtc [%s]' % rtcp.getName()
                        build_rtc(rtcp)
            return
            

                    

