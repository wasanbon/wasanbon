#!/usr/bin/env python

import os, sys
from OpenTPR.core.rtc.rtcprofile import *
from xml.dom import minidom, Node
import xml.etree.ElementTree

class InstallError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        pass
    def __str__(self):
        return 'Installing RTC Error(%s)' % self.msg


def install_rtc(rtcprofile_):
    print '--Installing RTC(%s)' % rtcprofile_.getFile()
    

def install_rtc__(rtc_conf_name, rtc_file_name, label_name, auto_uninstall = False):
    preloaded_ = False
    print '--Installing RTC(%s)' % rtc_file_name
    os.rename(rtc_conf_name, rtc_conf_name + '.bak')
    fin = open(rtc_conf_name + '.bak', 'r')
    fout = open(rtc_conf_name, 'w')

    while True:
        line = fin.readline()
        if not line:
            break
        if line.strip().startswith(label_name):
            line_output = label_name + ':'
            first_flag = True
            while line.strip().endswith('\\'):
                line = line.strip().split('\\')[0] + fin.readline()
            files = line.strip().split(':')[1].split(',')
            for file in files:
                if file.strip() == rtc_file_name:
                    print '---%s is already installed' % rtc_file_name
                    preloaded_ = True
                if len(file.strip()) > 0 and (os.path.isfile(file.strip()) or (not auto_uninstall)):
                    if not first_flag:
                        line_output = line_output + ' ,'
                    first_flag = False
                    line_output = line_output + file
                else:
                    print '---Uninstall RTC(%s)' % file
            line = line_output
            if not preloaded_:
                print '---%s is successfully installed' % rtc_file_name
                preloaded_ = True
                if not first_flag:
                    line = line + ', '
                line = line + rtc_file_name
            line = line + '\n'
        fout.write(line)
        
    fin.close()
    os.remove(rtc_conf_name + '.bak')
    if not preloaded_:
        print '---%s is installed' % rtc_file_name
        fout.write('%s: %s\n\n' % (label_name, rtc_file_name))
    fout.close()
    pass



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
 

    
