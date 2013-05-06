#!/usr/bin/env python

from wasanbon.core.rtc import *


class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        rtcps = parse_rtcs(argv)
        if len(argv) < 3:
            print_usage()

        if len(argv) >= 4:
            if argv[3] == '--clean':
                rtc_name = argv[2]
                for rtcp in rtcps:
                    if rtcp.getName() == rtc_name:
                        clean_rtc(rtcp)
                        return
        rtc_name = argv[2]
        for rtcp in rtcps:
            if rtcp.getName() == rtc_name:
                build_rtc(rtcp)
