#!/usr/bin/env python

import os
import sys
from rtcprofile import RTCProfile
from xml.dom import minidom, Node
import xml.etree.ElementTree
from wasanbon.core.rtc import *
from wasanbon.core import *
import yaml

rtcprofile_filename = 'RTC.xml'

def parse_rtcs(argv):
    y = yaml.load(open('setting.yaml','r'))
    rtc_dir = os.path.join(os.getcwd(), y['application']['RTC_DIR'])
    rtcprofiles = find_rtc_profiles(rtc_dir)
    rtcps = []
    for fullpath in rtcprofiles:
        try:
            rtcp = RTCProfile(fullpath)
            rtcps.append(rtcp)
        except Exception, e:
            print str(e)
            print '-Error Invalid RTCProfile file[%s]' % fullpath_
    return rtcps

    
def find_rtc_profiles(rootdir):
    return search_file(rootdir, rtcprofile_filename)


def rtc_file_search(path, rtc_bin_name, rtc_name = ''):
    print 'rtc_search %s' % rtc_name
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(path + '/' + file):
            fullpath = rtc_file_search(path + '/' + file, rtc_bin_name, rtc_name)
            if len(fullpath[0]) > 0:
                return fullpath
        else:
            if file == rtc_bin_name:
                if len(rtc_name) > 0:
                    if sys.platform == 'darwin':
                        ext = 'dylib'
                    elif sys.platform == 'linux2':
                        ext = 'so'
                    elif sys.platform == 'win32':
                        ext = 'dll'
                    else:
                        print 'WARNING Unsupported System (%s)' % sys.platform
                        raise

                    if not os.path.isfile('%s/%s.%s' % (path, rtc_name, ext)):
                        sys.stdout.write('Creating Static Link(%s/%s.%s)' % (path, rtc_name, ext))
                        import subprocess
                        cmd = ('ln', '%s/%s' % (path, rtc_bin_name),  '%s/%s.%s' % (path, rtc_name, ext))
                        subprocess.call(cmd)
                    return [path + '/', rtc_name + '.' + ext]
                return [path + '/', rtc_bin_name]
    return ['', '']




