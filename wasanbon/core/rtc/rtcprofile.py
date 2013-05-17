#!/usr/bin/env python

import os
import sys
from xml.dom import minidom, Node
import xml.etree.ElementTree
import search_rtc

##############
rtc_py_conf_filename = 'rtc_py.conf'
rtc_cpp_conf_filename = 'rtc_cpp.conf'
rtc_java_conf_filename = 'rtc_java.conf'



def get_rtc_py_name_list(rtc_name):
    return ['%s.py' % rtc_name]

def get_rtc_java_name_list(rtc_name):
    return ['%s.jar' % rtc_name]

#################
class InvalidRTCProfileError(Exception):
    def __init__(self, filename_='', msg_=''):
        self.filename = filename_
        self.msg = msg_
        pass

    def __str__(self):
        return 'InvalidRTCProfileError(%s):%s' % (self.filename, self.msg)

class DataPort(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return '%s:%s' % (self.name, self.type)

class RTCProfile(object):

    """
    """
    def __init__(self, filename_):
        try:
            self.filename = filename_
            et = xml.etree.ElementTree.parse(self.filename)
            root = et.getroot()
            [uri, tag] = normalize(root.tag)
            for basicInfo in root.findall('{%s}BasicInfo' % uri):
                self.name = basicInfo.attrib['{%s}name' % uri]
                self.category = basicInfo.attrib['{%s}category' % uri]

            for language in root.findall('{%s}Language' % uri):
                self.language = language.attrib['{%s}kind' % uri]
        
            self.dataports = []
            for dport in root.findall('{%s}DataPorts' % uri):
                self.dataports.append(DataPort(dport.attrib['{%s}name' % uri], dport.attrib['{%s}type' % uri]))
        except Exception, e:
            raise InvalidRTCProfileError(filename, 'Parsing Error')

        
        """"
        if self.getLanguage() == 'C++':
            rtc_conf_name = rtc_cpp_conf_filename
            rtc_file_name_list = get_rtc_cpp_name_list(self.getName())
        elif self.getLanguage() == 'Python':
            rtc_conf_name = rtc_py_conf_filename
            rtc_file_name_list = get_rtc_py_name_list(self.getName())
        elif self.getLanguage() == 'Java':
            rtc_conf_name = rtc_py_conf_filename
            rtc_file_name_list = get_rtc_java_name_list(self.getName())
        else:
            raise InvalidRTCProfileError(filename, 'Unsupported Language(%s)' % getLanguage())
        conf_file_name = self.getName() + '.conf'

        [path_, file_] = os.path.split(self.filename)
        conf_files_ = search_rtc.search_file(path_, conf_file_name)
        rtcs_files_ = search_rtc.search_file(path_, rtc_file_name_list)
        rtcs_files_available_ = []
        
        for file_ in rtcs_files_:
            if file_.count('Debug') > 0:
                print 'RTC file (%s) seems to build in Debug mode.' % file_
                print 'Debug mode binary is not available.'
            else:
                rtcs_files_available_.append(file_)
        rtcs_files_ = rtcs_files_available_

        if len(conf_files_) == 1:
            self.conffile = conf_files_[0]
        elif len(conf_files_) == 0:
            self.conffile = None
        else:
            self.conffile = on_multiple_conffile(self, conf_files_)

        if len(rtcs_files_) == 1:
            self.rtcfile = rtcs_files_[0]
        elif len(rtcs_files_) == 0:
            self.rtcfile = None
        else:
            self.rtcfile = on_multiple_rtcfile(self, rtcs_files)
        """
        pass
    def __str__(self):
        return self.getName() + " in " + self.getLanguage()
        pass

    def getRTCProfileFileName(self):
        return self.filename

    def getCategory(self):
        return self.category

    def getName(self):
        return self.name

    def getLanguage(self):
        return self.language


def on_multiple_conffile(rtcprofile, conffiles):
    raise InvalidRTCProfileError('Multiple %s.conf file' % rtcprofile.getName())
    pass

def on_multiple_rtcfile(rtcprofile, rtcfiles):
    raise InvalidRTCProfileError('Multiple %s.rtc file' % rtcprofile.getName())           
    pass

# Utility Functions
def normalize(name):
    if name[0] == '{':
        uri, tag = name[1:].split('}')
        return [uri, tag]
    
    return ['', name]

def gettag(name):
    [uri, tag] = normalize(name)
    return tag
