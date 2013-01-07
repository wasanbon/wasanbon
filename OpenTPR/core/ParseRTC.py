#!/usr/bin/env python

import os
import sys
from OpenTPR.core.RTCProfile import *
from xml.dom import minidom, Node

import xml.etree.ElementTree

def parse_rtcs():
    root_dir_name = 'rtcs'
    rtc_profile_filename = 'RTC.xml'
    print 'Parsing default rtc directory (%s)' % root_dir_name
    rtcs_dir = os.listdir(root_dir_name)
    for sub_dir_name in rtcs_dir:
        files = os.listdir('%s/%s' % (root_dir_name, sub_dir_name))
        if rtc_profile_filename in files:
            parse_rtc_profile('%s/%s' % (root_dir_name, sub_dir_name))
    

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

def get_rtc_cpp_bin_name(rtc_name):
    if sys.platform == 'darwin':
        return 'lib%s.%s' % (rtc_name.lower(), 'dylib')
    elif sys.platform == 'win32':
        return '%s.%s' % (rtc_name.lower(), 'dll')
    elif sys.platform == 'linux2':
        return 'lib%s.%s' % (rtc_name.lower(), 'so')
    else:
        print 'ERROR:Unsupported Operating System(%s)' % sys.platform

def get_rtc_py_name(rtc_name):
    return '%s.py' % rtc_name

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




def install_rtc(rtc_conf_name, rtc_file_name, label_name, auto_uninstall = False):
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
 

    
