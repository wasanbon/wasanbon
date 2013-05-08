#!/usr/bin/env python

import os, sys
import wasanbon
from wasanbon.core import rtc
from wasanbon import util
from wasanbon.core.rtc import git
rtcprofile_filename = 'RTC.xml'

def print_usage():
    return

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

def parse_rtcs():
    rtc_dir = os.path.join(os.getcwd(), 
                           wasanbon.setting['application']['RTC_DIR'])
    rtcprofiles = util.search_file(rtc_dir, 'RTC.xml')
    rtcps = []
    for fullpath in rtcprofiles:
        try:
            rtcp = rtc.RTCProfile(fullpath)
            rtcps.append(rtcp)
        except Exception, e:
            print str(e)
            print '-Error Invalid RTCProfile file[%s]' % fullpath_
    return rtcps

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        rtcps = parse_rtcs()
        if argv[2] == 'list':
            for rtcp in rtcps:
                print_rtc_profile(rtcp)
                pp = rtc.PackageProfile(rtcp)
                print_package_profile(pp)

        if argv[2] == 'git_init':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            for rtcp in rtcps:
                if rtcname == rtcp.getName():
                    sys.stdout.write('Initializing GIT repository in %s\n' % rtcname)
                    git.git_init(rtcp)
        pass

    

