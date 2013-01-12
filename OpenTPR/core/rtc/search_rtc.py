#!/usr/bin/env python

import os
import sys
from rtcprofile import RTCProfile
#import OpenTPR.core.rtc.rtcprofile.RTCProfile
from xml.dom import minidom, Node

import xml.etree.ElementTree

root_dir_name = 'rtcs'
rtcprofile_filename = 'RTC.xml'

def parse_rtcs():
    print 'Parsing default rtc directory (%s)' % root_dir_name

    """
    rtcs_dir = os.listdir(root_dir_name)
    for sub_dir_name in rtcs_dir:
        files = os.listdir('%s/%s' % (root_dir_name, sub_dir_name))
        if rtc_profile_filename in files:
            parse_rtc_profile('%s/%s' % (root_dir_name, sub_dir_name))
    """
    rtcprofiles_ = find_rtc_profiles(os.path.join(os.getcwd(), root_dir_name))
    rtcps_ = []
    for fullpath_ in rtcprofiles_:
        print 'Found RTCProfile in %s' % fullpath_
        try:
            rtcp_ = RTCProfile(fullpath_)
            rtcps_.append(rtcp_)
        except Exception, e:
            print str(e)
            print '-Error Invalid RTCProfile file[%s]' % fullpath_
    return rtcps_

def search_file(rootdir, filename):
    found_files_ = []
    if type(filename) is list:
        for file_ in filename:
            found_files_ = found_files_ + search_file(rootdir, file_)
        return found_files_

    files = os.listdir(rootdir)

    for file_ in files:
        fullpath_ = os.path.join(rootdir, file_)
        if os.path.isdir(fullpath_):
            found_files_ = found_files_ + search_file(fullpath_, filename)
        else:
            if file_ == filename:
                found_files_.append(fullpath_)
    return found_files_
    
def find_rtc_profiles(rootdir):
    return search_file(rootdir, rtcprofile_filename)

                            
def is_rtcprofile(filepath_):
    path_, file_ = os.path.split(filepath_)
    if file_ == rtcprofile_filename:
        return True
    return False


def scanNode(obj, node, level = 0):
    msg = node.__class__.__name__
    if node.nodeType == Node.ELEMENT_NODE:
        msg += ", tag: " + node.tagName
    if node.nodeType == Node.TEXT_NODE:
        msg += " (" + node.wholeText + ")"
    print " " * level * 4, msg
    if node.hasChildNodes:
        for child in node.childNodes:
            scanNode(child, level + 1)

def rtc_file_search(path, rtc_bin_name, rtc_name = ''):
    #print 'rtc_search %s' % rtc_name
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




