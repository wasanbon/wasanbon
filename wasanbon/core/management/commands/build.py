#!/usr/bin/env python

from wasanbon.core.rtc import *
from wasanbon.core import rtc

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        rtcps = rtc.parse_rtcs()
        if len(argv) < 3:
            print_usage()
            return

        if '--clean' in argv:
            clean_all = True if 'all' in argv else False

            for i in range(3, len(argv)):
                rtc_name = argv[i]
                if not rtc_name == '--clean':
                    continue
                for rtcp in rtcps:
                    if rtcp.getName() == rtc_name or clean_all:
                        clean_rtc(rtcp)
            return
        else:
            build_all = True if 'all' in argv else False
            for i in range(3, len(argv)):
                rtc_name = argv[i]
                if not rtc_name == '--clean':
                    continue
                for rtcp in rtcps:
                    if rtcp.getName() == rtc_name or clean_all:
                        build_rtc(rtcp)
            return
            

                    

