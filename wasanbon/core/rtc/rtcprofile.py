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
        self.__dict__['attrib'] = node.attrib
        self.__dict__['children'] = []

    def setNode(self, node):
        pass

    def __getitem__(self, key):
        # print '::', self.node, ' for ', key
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

class ServicePort(Node):
    def __init__(self, node):
        Node.__init__(self, node)
        [uri, tag] = normalize(node.tag)
        self.serviceInterfaces = []
        for si in node.findall('{%s}ServiceInterface' % uri):
            self.serviceInterfaces.append(Node(si))
            self.children.append(Node(si))

class ConfigurationSet(Node):
    def __init__(self, node):
        Node.__init__(self, node)
        [uri, tag] = normalize(node.tag)
        self.configurations = []
        for c in node.findall('{%s}Configuration' % uri):
            self.configurations.append(Node(c))
            self.children.append(Node(c))

class Actions(Node):
    def __init__(self, node):
        Node.__init__(self, node)
        [uri, tag] = normalize(node.tag)
        # print dir(node)
        for child in node.getchildren():
            [c_uri, c_tag] = normalize(child.tag)
            self.__dict__[c_tag] = Node(child)
            self.children.append(Node(child))
            # print c_tag
            
        #self.actions = []
        #for c in node.findall('{%s}Configuration' % uri):
        #    self.actions.append(Node(c))
        #    self.children.append(Node(c))



def save_rtcprofile(rtcp, filename):
    # print 'saving rtcprofile'
    def save_sub(elem, node):
        #print 'saving ', node, ' to ', elem
        for key, value in node.attrib.items(): # set attribute
            #print 'key:', key
            name = '%s:%s' % (get_short_ns(key.split('}')[0][1:]), key.split('}')[1])
            elem.set(name, value)

        for child in node.children:
            key = child.node.tag
            name = '%s:%s' % (get_short_ns(key.split('}')[0][1:]), key.split('}')[1])
            subelem = xml.etree.ElementTree.SubElement(elem, name)
            #elem.append(subelem)
            save_sub(subelem, child)
            


    root = xml.etree.ElementTree.Element('rtc:RtcProfile')
    #for key, value in rtcp.attrib.items():
    #    name = '%s:%s' % (get_short_ns(key.split('}')[0][1:]), key.split('}')[1])
    #    root.set(name, value)

    for key, value in known_namespaces.items():
        root.set('xmlns:%s' % key, value)

    save_sub(root, rtcp)
    #root.set('xmlns:rtcExt', 'http://www.openrtp.org/namespaces/rtc_ext')
    #root.set('xmlns:rtcDoc', "http://www.openrtp.org/namespaces/rtc_doc")
    #root.set('xmlns:rtc', "http://www.openrtp.org/namespaces/rtc")
    #root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

    open('out.xml', 'w').write(xml.etree.ElementTree.tostring(root))
    # print xml.etree.ElementTree.tostring(root)
    pass


class RTCProfile(Node):

    """
    """
    def __init__(self, filename="", str=""):
        try:
            # print str
            self.filename = filename
            if len(filename) > 0:
                et = xml.etree.ElementTree.parse(self.filename)
                root = et.getroot()
            elif len(str) > 0:
                root = xml.etree.ElementTree.fromstring(str)
            self.node = root
            self.attrib = root.attrib
            self.children = []

            [uri, tag] = normalize(root.tag)
            for basicInfo in root.findall('{%s}BasicInfo' % uri):
                self.name = basicInfo.attrib['{%s}name' % uri]
                self.category = basicInfo.attrib['{%s}category' % uri]
                self.basicInfo = Node(basicInfo)
                self.children.append(self.basicInfo)

            for language in root.findall('{%s}Language' % uri):
                self.language = Node(language) #language.attrib['{%s}kind' % uri]
                self.children.append(self.language)

            for action in root.findall('{%s}Actions' % uri):
                self.action = Actions(action)
                self.children.append(self.action)
        
            self.dataports = []
            for dport in root.findall('{%s}DataPorts' % uri):
                self.dataports.append(Node(dport))
                self.children.append(Node(dport))
                #self.dataports.append(DataPort(dport.attrib['{%s}name' % uri], 
                #                               dport.attrib['{%s}type' % uri],
                #                               dport.attrib['{%s}portType' % uri]))

            self.serviceports = []
            for sport in root.findall('{%s}ServicePorts' % uri):
                self.serviceports.append(ServicePort(sport))
                self.children.append(ServicePort(sport))

            self.configurationSets = []
            for cset in root.findall('{%s}ConfigurationSet' % uri):
                self.configurationSets.append(ConfigurationSet(cset))
                self.children.append(ConfigurationSet(cset))

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
