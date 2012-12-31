#!/usr/bin/env python

import os
from xml.dom import minidom, Node
import xml.etree.ElementTree


def normalize(name):
    if name[0] == '{':
        uri, tag = name[1:].split('}')
        return [uri, tag]
    
    return ['', name]

def gettag(name):
    [uri, tag] = normalize(name)
    return tag

class InvalidRTCProfileError(Exception):
    def __init__(self, filename_=''):
        self.filename = filename_
        pass

    def __str__(self):
        return 'Invalid RTCProfile Error (%s)' % self.filename

class DataPort(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type


    def __str__(self):
        return '%s:%s' % (self.name, self.type)

class RTCProfile(object):
    
    def __init__(self, filename):
        try:
            self.et = xml.etree.ElementTree.parse(filename)
            root = self.et.getroot()
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
            raise InvalidRTCProfileError(filename)
        
    def getCategory(self):
        return self.category

    def getName(self):
        return self.name

    def getLanguage(self):
        return self.language
