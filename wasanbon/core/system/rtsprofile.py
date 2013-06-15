#!/usr/bin/env python

import os
import sys
from xml.dom import minidom, Node
import xml.etree.ElementTree





class RTSProfile(object):
    def __init__(self, filename_):
        try:
            self.filename = filename_
            et = xml.etree.ElementTree.parse(self.filename)
            root = et.getroot()
            [uri, tag] = normalize(root.tag)

            """
            for basicInfo in root.findall('{%s}BasicInfo' % uri):
                self.name = basicInfo.attrib['{%s}name' % uri]
                self.category = basicInfo.attrib['{%s}category' % uri]

            for language in root.findall('{%s}Language' % uri):
                self.language = language.attrib['{%s}kind' % uri]
        
            self.dataports = []
            for dport in root.findall('{%s}DataPorts' % uri):
                self.dataports.append(DataPort(dport.attrib['{%s}name' % uri], 
                                               dport.attrib['{%s}type' % uri],
                                               dport.attrib['{%s}portType' % uri]))
            """
        except Exception, e:
            #raise InvalidRTCProfileError(filename, 'Parsing Error')
            pass
