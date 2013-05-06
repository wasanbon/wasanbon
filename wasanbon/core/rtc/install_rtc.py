#!/usr/bin/env python

import os, sys
from kotobuki.core.rtc.rtcprofile import *
from kotobuki.core.rtc.packageprofile import *
from kotobuki.core.rtc.rtcconf import *
from xml.dom import minidom, Node
import xml.etree.ElementTree

import kotobuki.core.management.import_tools as importer
settings = importer.import_setting()
packages = importer.import_packages()

class InstallError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        pass
    def __str__(self):
        return 'Installing RTC Error(%s)' % self.msg

def is_installed_rtc(rtcp):
    rtcc = RTCConf(settings.application['conf.' + rtcp.getLanguage()])
    if not 'manager.modules.load_path' in rtcc.keys():
        return False
    paths = [p.strip() for p in rtcc['manager.modules.load_path'].split(',')]
    if not 'manager.modules.preload' in rtcc.keys():
        return False
    files = [f.strip() for f in rtcc['manager.modules.preload'].split(',')]

    pp = PackageProfile(rtcp)
    if not os.path.isfile(pp.getRTCFilePath()):
        return False

    flag = False
    for p in paths:
        for f in files:
            fullpath = os.path.join(p, f)
            if os.path.isfile(fullpath) and os.path.samefile(pp.getRTCFilePath(), fullpath):
                flag = True
    return flag

    
def install_rtc(rtcp):
    rtcc = RTCConf(settings.application['conf.' + rtcp.getLanguage()])
    pp = PackageProfile(rtcp)
    if len(pp.getRTCFilePath()) == 0 :
        print '--Executable of RTC (%s) is not found.' % rtcp.getName()
        return

    [path_, file_] = os.path.split(pp.getRTCFilePath())

    rtcc.append('manager.modules.load_path', path_)
    rtcc.append('manager.modules.preload', file_)
    rtcc.append('manager.components.precreate', rtcp.getName())
    rtcc.sync()
    
def uninstall_rtc(rtcp):
    rtcc = RTCConf(settings.application['conf.' + rtcp.getLanguage()])
    pp = PackageProfile(rtcp)
    if sys.platform == 'win32':
        fileext = '.dll'
    elif sys.platform == 'linux2':
        fileext = '.so'
    elif sys.platform == 'darwin':
        fileext = '.dylib'
    else:
        print '---Unsupported System (%s)' % sys.platform
        return 

    if len(pp.getRTCFilePath()) == 0:
        filename = rtcp.getName() + fileext
        print '---Guessing RTCFileName = %s' % filename
    filename = os.path.basename(pp.getRTCFilePath())
    rtcc.remove('manager.components.precreate', rtcp.getName())
    rtcc.remove('manager.modules.preload', filename)
    rtcc.sync()


def parse_rtc_profile(rtc_profile_filepath):
    print '-Parsing RTC Profile(%s)' % rtc_profile_filepath
    try:
        rtcp = RTCProfile('%s/RTC.xml' % rtc_profile_filepath)
        print '--Found RTC Profile (%s)' % rtcp.getName()
        print '--Language %s' % rtcp.getLanguage()
        if rtcp.getLanguage() == 'C++':
            rtc_conf_name = 'conf/rtc_cpp.conf'
            rtc_file_name = get_rtc_cpp_bin_name(rtcp.getName())
            conf_file_name = rtcp.getName() + '.conf'
        elif rtcp.getLanguage() == 'Python':
            rtc_conf_name = 'conf/rtc_py.conf'
            rtc_file_name = get_rtc_py_name(rtcp.getName())
            conf_file_name = rtcp.getName() + '.conf'
        else:
            pass

        # installing rtc
        sys.stdout.write( '--Searching %s... ' % rtc_file_name )
        [path, file] = rtc_file_search(rtc_profile_filepath, rtc_file_name,  rtcp.getName() if rtcp.getLanguage() == 'C++' else '')
        fullpath = path + file
        if len(fullpath) > 0:
            print 'Found(%s)' % fullpath
            sys.stdout.write('--Parsing rtc.conf(%s)... ' % rtc_conf_name)
            install_rtc(rtc_conf_name, path, 'manager.modules.load_path')
            install_rtc(rtc_conf_name, file, 'manager.modules.preload')
        else:
            print 'Not Found'
            return

        # installing conf file
        sys.stdout.write( '--Searching %s... ' % conf_file_name )
        [path, file] = rtc_file_search(rtc_profile_filepath, conf_file_name)
        fullpath = path + file
        if len(fullpath) > 0:
            print 'Found(%s)' % fullpath
            sys.stdout.write('--Parsing rtc.conf(%s)... ' % rtc_conf_name)
            conf_setting_label = rtcp.getCategory() + '.' + rtcp.getName() + '.config_file'
            install_rtc(rtc_conf_name, fullpath, conf_setting_label)
        else:
            print 'Not Found'
            print 'WARNING:RTC(%s) does not have its own .conf file.' % rtcp.getName()

        # setting precreate config
        sys.stdout.write('--Activating installed RTC(%s)' % rtcp.getName())
        install_rtc(rtc_conf_name, rtcp.getName(), 'manager.components.precreate')

        
    except InvalidRTCProfileError, e:
        print str(e)
        return
 

    
