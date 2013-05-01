#!/usr/bin/env python

from kotobuki.core.rtc.search_rtc import *
from kotobuki.core.rtc.rtcprofile import *

def print_rtc_profile(rtcp):
    str ='-RTC name=' + rtcp.getName() + '\''
    str = str + '---Language:' + rtcp.getLanguage() + '\n'
    str = str + '---Category:' + rtcp.getCategory() + '\n'
    str = str + '---RTC.xml :' + rtcp.getRTCProfileFileName() + '\n'
    print str


class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if argv[2] == 'list':
            rtcps = parse_rtcs(argv)
            for rtcp in rtcps:
                print_rtc_profile(rtcp)
        pass
