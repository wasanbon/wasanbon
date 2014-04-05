#!/usr/bin/env python

import os, traceback
import sys
from xml.dom import minidom, Node
import xml.etree.ElementTree
#import search_rtc

##############
rtc_py_conf_filename = 'rtc_py.conf'
rtc_cpp_conf_filename = 'rtc_cpp.conf'
rtc_java_conf_filename = 'rtc_java.conf'



known_namespaces = {
    'xsi' : 'http://www.w3.org/2001/XMLSchema-instance',
    'rtc' : 'http://www.openrtp.org/namespaces/rtc',
    'rtcDoc' : 'http://www.openrtp.org/namespaces/rtc_doc',
    'rtcExt' : 'http://www.openrtp.org/namespaces/rtc_ext',
}

def get_short_ns(uri):
    for key, value in known_namespaces.items():
        if uri == value:
            return key
    print 'Unknwon Namespace :' , uri
    return None

def get_long_ns(uri):
    for key, value in known_namespaces.items():
        if uri == key:
            return value
    return None

def get_rtc_py_name_list(rtc_name):
    return ['%s.py' % rtc_name]

def get_rtc_java_name_list(rtc_name):
    return ['%s.jar' % rtc_name]

#################
class InvalidRTCProfileError(Exception):
    def __init__(self, filename='', msg_=''):
        self.filename = filename
        self.msg = msg_
        pass

    def __str__(self):
        return 'InvalidRTCProfileError(%s):%s' % (self.filename, self.msg)

class DataPort(object):
    def __init__(self, name, type, portType):
        self.name = name
        self.type = type
        self.portType = portType

    def __str__(self):
        return '%s:%s' % (self.name, self.type)


class Node(object):
    def __init__(self, node):
        self.__dict__['node']  = node

    def setNode(self, node):
        pass

    def __getitem__(self, key):
        tokens = key.split(':')
        uri = get_long_ns(tokens[0])
        if not uri:
            print 'Unknown URI: ' , tokens[0]
        return self.node.attrib['{%s}%s' % (uri, tokens[1])]

    def __setitem__(self, key, value):
        tokens = key.split(':')
        uri = get_long_ns(tokens[0])
        if not uri:
            print 'Unknown URI: ' , tokens[0]
        self.node.attrib['{%s}%s' % (uri, tokens[1])] = value
        
        
    def keys(self):
        return [get_short_ns(key.split('}')[0][1:]) + ':' + key.split('}')[1] for key in self.node.attrib.keys()]

    def __getattr__(self, key):
        return self.__getitem__('rtc:'+key)

    #def __setattr__(self, name, value):
    #    tokens = name.split(':')
    #    uri = get_long_ns(tokens[0])
    #    if not uri:
    #        print 'Unknown URI: ', tokens[0]
    #    self.node.attrib['{%s}%s' % (uri, tokens[1])] = value



def save_rtcprofile(rtcp, filename):
    def save_sub(parent, node):
        for key, value in node.attrib.items():
            name = '%s:%s' % (get_short_ns(key.split('}')[0][1:]), key.split('}')[1])
            parent.set(name, value)
        for key, child in node.children.items():
            name = '%s:%s' % (get_short_ns(key.split('}')[0][1:]), key.split('}')[1])
            elem = xml.etree.ElementTree.SubElement(parent, name)
            save_sub(elem, child)


    root = xml.etree.ElementTree.Element('rtc:RtcProfile')
    for key, value in rtcp.attrib.items():
        name = '%s:%s' % (get_short_ns(key.split('}')[0][1:]), key.split('}')[1])
        root.set(name, value)

    for key, value in known_namespaces.items():
        root.set('xmlns:%s' % key, value)


    #root.set('xmlns:rtcExt', 'http://www.openrtp.org/namespaces/rtc_ext')
    #root.set('xmlns:rtcDoc', "http://www.openrtp.org/namespaces/rtc_doc")
    #root.set('xmlns:rtc', "http://www.openrtp.org/namespaces/rtc")
    #root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

    print xml.etree.ElementTree.tostring(root)
    pass


class RTCProfile(Node):

    """
    """
    def __init__(self, filename="", str=""):
        try:

            self.filename = filename
            if len(filename) > 0:
                et = xml.etree.ElementTree.parse(self.filename)
                root = et.getroot()
            elif len(str) > 0:
                root = xml.etree.ElementTree.fromstring(str)
            self.node = root
            self.attrib = root.attrib
            self.children = {}

            [uri, tag] = normalize(root.tag)
            for basicInfo in root.findall('{%s}BasicInfo' % uri):
                self.name = basicInfo.attrib['{%s}name' % uri]
                self.category = basicInfo.attrib['{%s}category' % uri]
                self.basicInfo = Node(basicInfo)

            for language in root.findall('{%s}Language' % uri):
                self.language = Node(language) #language.attrib['{%s}kind' % uri]
                self.children['{%s}Language'] = language
        
            self.dataports = []
            for dport in root.findall('{%s}DataPorts' % uri):
                self.dataports.append(Node(dport))
                #self.dataports.append(DataPort(dport.attrib['{%s}name' % uri], 
                #                               dport.attrib['{%s}type' % uri],
                #                               dport.attrib['{%s}portType' % uri]))

        except Exception, e:
            traceback.print_exc()
            raise InvalidRTCProfileError(filename, 'Parsing Error')

        pass

    def getDataPorts(self):
        return self.dataports

    def __str__(self):
        return self.getName() + " in " + self.getLanguage()
        pass

    def getRTCProfileFileName(self):
        return self.filename

    def getCategory(self):
        return self.basicInfo.category

    def getName(self):
        return self.basicInfo.name

    def getLanguage(self):
        return self.language.kind


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
