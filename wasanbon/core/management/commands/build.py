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
        rtc_name = argv[2]

        if len(argv) >= 4:
            if argv[3] == '--clean':
                rtc_name = argv[2]
                for rtcp in rtcps:
                    if rtcp.getName() == rtc_name or rtc_name == 'all':
                        clean_rtc(rtcp)
                        return
        
        for rtcp in rtcps:
            if rtcp.getName() == rtc_name or rtc_name == 'all':
                build_rtc(rtcp)

