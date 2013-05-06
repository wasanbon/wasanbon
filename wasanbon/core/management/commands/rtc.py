#!/usr/bin/env python

from wasanbon.core.rtc import *


def print_rtc_profile(rtcp):
    str = rtcp.getName() + ' : \n'
    str = str + '    name       : ' + rtcp.getName() + '\n'
    str = str + '    language   : ' + rtcp.getLanguage() + '\n'
    str = str + '    category   : ' + rtcp.getCategory() + '\n'
    filename = rtcp.getRTCProfileFileName()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = str + '    RTC.xml    : ' + filename + '\n'
    sys.stdout.write(str)

def print_package_profile(pp):
    filename = pp.getRTCFilePath()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = '    executable : ' + filename + '\n'
    sys.stdout.write(str)

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        rtcps = parse_rtcs(argv)
        if argv[2] == 'list':
            for rtcp in rtcps:
                print_rtc_profile(rtcp)
                pp = parse_package_profile(rtcp)
                print_package_profile(pp)

        if argv[2] == 'build':
            if len(argv) >= 3:
                rtc_name = argv[3]
                for rtcp in rtcps:
                    if rtcp.getName() == rtc_name:
                        build_rtc(rtcp)
        if argv[2] == 'clean':
            if len(argv) >= 3:
                rtc_name = argv[3]
                for rtcp in rtcps:
                    if rtcp.getName() == rtc_name:
                        clean_rtc(rtcp)
        pass

    

