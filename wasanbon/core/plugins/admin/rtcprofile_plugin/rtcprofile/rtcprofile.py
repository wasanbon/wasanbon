#!/usr/bin/env python

import os
import traceback
import types
import copy
import sys
from xml.dom import minidom, Node
import xml.etree.ElementTree
# import lxml.etree
#import search_rtc

##############


known_namespaces = {
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'rtc': 'http://www.openrtp.org/namespaces/rtc',
    'rtcDoc': 'http://www.openrtp.org/namespaces/rtc_doc',
    'rtcExt': 'http://www.openrtp.org/namespaces/rtc_ext',
}


def get_short_ns(uri):
    for key, value in list(known_namespaces.items()):
        if uri == value:
            return key
    print('Unknwon Namespace :', uri)
    return None


def get_long_ns(uri):
    for key, value in list(known_namespaces.items()):
        if uri == key:
            return value
    return None

#################


class InvalidRTCProfileError(Exception):
    def __init__(self, filename='', msg_=''):
        self._filename = filename
        self.msg = msg_
        pass

    def __str__(self):
        return 'InvalidRTCProfileError(%s):%s' % (self._filename, self.msg)


class Node(object):
    def __init__(self, node):
        self.__dict__['node'] = node
        self.__dict__['attrib'] = node.attrib
        self.__dict__['children'] = []
        self.__dict__['text'] = node.text

    def setNode(self, node):
        pass

    def __getitem__(self, key):
        # print '::', self.node, ' for ', key
        tokens = key.split(':')
        uri = get_long_ns(tokens[0])
        if not uri:
            print('Unknown URI: ', tokens[0])
            return None
        return self.node.attrib['{%s}%s' % (uri, tokens[1])]

    def __setitem__(self, key, value):
        if key.find('_') > 0:
            tokens = key.split('_')
        else:
            tokens = key.split(':')
        uri = get_long_ns(tokens[0])
        if not uri:
            print('Unknown URI: ', tokens[0])
            return None
        self.node.attrib['{%s}%s' % (uri, tokens[1])] = value

    def deepcopy(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def keys(self):
        return [get_short_ns(key.split('}')[0][1:]) + ':' + key.split('}')[1] for key in list(self.node.attrib.keys())]

    def __getattr__(self, key):
        if key == '__deepcopy__':
            return self.deepcopy
        elif key.find('_') > 0:
            return self.__getitem__(key.replace('_', ':'))
        return self.__getitem__('rtc:' + key)

    def gettext(self):
        return self.node.text

    # def __setattr__(self, name, value):
    #    tokens = name.split(':')
    #    uri = get_long_ns(tokens[0])
    #    if not uri:
    #        print 'Unknown URI: ', tokens[0]
    #    self.node.attrib['{%s}%s' % (uri, tokens[1])] = value
"""
<rtc:RtcProfile rtc:version="0.2" rtc:id="RTC:Ogata Lab Waseda Univ.:Robot:NAO:1.0.0" xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
"""
default_dataport_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:DataPorts xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="rtcExt:dataport_ext" rtcExt:position="RIGHT" rtcExt:variableName="camera" rtc:unit="" rtc:subscriptionType="" rtc:dataflowType="" rtc:interfaceType="" rtc:idlFile="" rtc:type="RTC::CameraImage" rtc:name="camera" rtc:portType="DataOutPort">
        <rtcDoc:Doc rtcDoc:operation="" rtcDoc:occerrence="" rtcDoc:unit="" rtcDoc:semantics="" rtcDoc:number="" rtcDoc:type="" rtcDoc:description=""/>
    </rtc:DataPorts>
"""
default_doc_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
 <rtcDoc:Doc  xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="rtcExt:dataport_ext" rtcDoc:operation="" rtcDoc:occerrence="" rtcDoc:unit="" rtcDoc:semantics="" rtcDoc:number="" rtcDoc:type="" rtcDoc:description="" rtcDoc:license=""/>"""


class Doc(Node):
    def __init__(self, node=None):
        Node.__init__(self, xml.etree.ElementTree.fromstring(node) if type(node)
                      is str else node if node is not None else xml.etree.ElementTree.fromstring(default_doc_profile))
        if node is None:
            self['rtcDoc:description'] = ''
        # self.children.append(self.doc)

    def __getattr__(self, key):
        if key == '__deepcopy__':
            return self.deepcopy
        if key.find('_') > 0:
            return self.__getitem__(key.replace('_', ':'))
        return self.__getitem__('rtcDoc:' + key)


default_properties_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
 <rtcDoc:Doc  xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
rtcExt:name="" rtcExt:value="" />"""


class Properties(Node):
    def __init__(self, node=None):
        Node.__init__(self, xml.etree.ElementTree.fromstring(node) if type(node)
                      is bytes else node if node is not None else xml.etree.ElementTree.fromstring(default_properties_profile))
        if node is None:
            self['rtcExt:name'] = '__widget__'
            self['rtcExt:value'] = 'text'

    def __getattr__(self, key):
        if key == '__deepcopy__':
            return self.deepcopy
        if key.find('_') > 0:
            return self.__getitem__(key.replace('_', ':'))
        return self.__getitem__('rtcExt:' + key)


class DataPort(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_dataport_profile))
        #[uri, tag] = normalize(node.tag)
        #self.serviceInterfaces = []
        # for si in node.findall('{%s}ServiceInterface' % uri):
        #    self.serviceInterfaces.append(Node(si))
        #    self.children.append(Node(si))
        docs = self.node.findall('{%s}Doc' % get_long_ns('rtcDoc'))
        if len(docs) != 0:
            self.doc = Doc(docs[0])
        else:
            self.doc = Doc()

        self.children.append(self.doc)

    def equals(self, dp):
        return self['rtc:name'] == dp['rtc:name'] and \
            self['rtc:type'] == dp['rtc:type'] and \
            self['rtc:portType'] == dp['rtc:portType']


default_serviceport_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:ServicePorts xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="rtcExt:serviceport_ext" rtcExt:position="LEFT" rtc:name="NAO_srv"> 
  <rtcDoc:Doc rtcDoc:ifdescription="" rtcDoc:description=""/>
</rtc:ServicePorts>
"""


class ServicePort(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_serviceport_profile))
        [uri, tag] = normalize(self.node.tag)
        self.serviceInterfaces = []
        for si in self.node.findall('{%s}ServiceInterface' % uri):
            si_ = ServiceInterface(si)
            self.serviceInterfaces.append(si_)
            self.children.append(si_)

        docs = self.node.findall('{%s}Doc' % get_long_ns('rtcDoc'))
        if len(docs) != 0:
            self.doc = Doc(docs[0])
        else:
            self.doc = Doc()
        self.children.append(self.doc)

    def equals(self, sp):
        return self['rtc:name'] == sp['rtc:name']


default_serviceinterface_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:ServiceInterface xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="rtcExt:serviceinterface_ext" rtcExt:variableName="motion" rtc:path="/Users/ysuga/rtm/idl" rtc:type="ssr::ALMotion" rtc:idlFile="/Users/ysuga/rtm/idl/NAO.idl" rtc:instanceName="ALMotion" rtc:direction="Provided" rtc:name="ALMotion">
  <rtcDoc:Doc rtcDoc:docPostCondition="" rtcDoc:docPreCondition="" rtcDoc:docException="" rtcDoc:docReturn="" rtcDoc:docArgument="" rtcDoc:description=""/>
</rtc:ServiceInterface>
"""


class ServiceInterface(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_serviceinterface_profile))
        docs = self.node.findall('{%s}Doc' % get_long_ns('rtcDoc'))
        if len(docs) != 0:
            self.doc = Doc(docs[0])
        else:
            self.doc = Doc()
        self.children.append(self.doc)

    def equals(self, si):
        return self.name == si.name and self.type == si.type and self.direction == si.direction


default_configuration_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:Configuration xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="rtcExt:configuration_ext" rtcExt:variableName="ipaddress" rtc:unit="" rtc:defaultValue="nao.local" rtc:type="string" rtc:name="ipaddress">
  <rtcExt:Properties rtcExt:value="text" rtcExt:name="__widget__"/>
</rtc:Configuration>
"""

default_configurationset_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:ConfigurationSet xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
</rtc:ConfigurationSet>
"""


class Configuration(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_configuration_profile))

        docs = self.node.findall('{%s}Doc' % get_long_ns('rtcDoc'))
        if len(docs) != 0:
            self.doc = Doc(docs[0])
        else:
            self.doc = Doc()
        self.children.append(self.doc)

        props = self.node.findall('{%s}Properties' % get_long_ns('rtcExt'))
        if len(props) != 0:
            self.properties = Properties(props[0])
        else:
            self.properties = Properties()
        self.children.append(self.properties)

        const = self.node.findall('{%s}Constraint' % get_long_ns('rtc'))
        if len(const) != 0:
            self.constraint = Constraint(const[0])
            self.children.append(self.constraint)

    def equals(self, cf):
        return cf.name == self.name

    def __repr__(self):
        return self.name


class ConfigurationSet(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_configurationset_profile))
        [uri, tag] = normalize(self.node.tag)
        self.configurations = []
        for c in self.node.findall('{%s}Configuration' % uri):
            conf = Configuration(c)
            self.configurations.append(conf)
            self.children.append(conf)

    def __repr__(self):
        return self.node.tag


default_constraint_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:Constraint xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
</rtc:Constraint>
"""


class Constraint(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_constraint_profile))
        [uri, tag] = normalize(self.node.tag)
        ut = self.node.findall('{%s}ConstraintUnitType' % get_long_ns('rtc'))
        if len(ut) != 0:
            self.constraintUnitType = ConstraintUnitType(ut[0])
        else:
            self.constraintUnitType = ConstraintUnitType()
        self.children.append(self.constraintUnitType)


default_constraintunittype_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:ConstraintUnitType xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
</rtc:ConstraintUnitType>
"""


class ConstraintUnitType(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_constraintunittype_profile))
        [uri, tag] = normalize(self.node.tag)

        cc = self.node.findall('{%s}Or' % get_long_ns('rtc'))
        if len(cc) != 0:
            self.constraint = Or(cc[0])
            self.children.append(self.constraint)
        else:
            cc = self.node.findall('{%s}Constraint' % get_long_ns('rtc'))
            if len(cc) != 0:
                self.constraint = Constraint(cc[0])
                self.children.append(self.constraint)
            else:
                cc = self.node.findall('{%s}propertyIsEqualTo' % get_long_ns('rtc'))
                if len(cc) != 0:
                    self.constraint = PropertyIsEqualTo(cc[0])
                    self.children.append(self.constraint)
                else:
                    pass
                pass
            pass

    def addChild(self, node):
        self.constraint = node
        self.children.append(node)


default_propertyisequalto_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:propertyIsEqualTo rtc:matchCase="false" xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
</rtc:propertyIsEqualTo>
"""


class PropertyIsEqualTo(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_propertyisequalto_profile))

        cc = self.node.findall('{%s}Literal' % get_long_ns('rtc'))
        if len(cc) != 0:
            self.literal = Literal(cc[0])
        else:
            self.literal = Literal()

        self.children.append(self.literal)


default_literal_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:Literal xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
</rtc:Literal>
"""


class Literal(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_literal_profile))
        self.text = self.node.text


default_or_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:Or xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
</rtc:Or>
"""

default_action_doc_profile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <rtcDoc:Doc xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" rtcDoc:preCondition="" rtcDoc:postCondition="" rtcDoc:description="" />"""


class Or(Node):
    def __init__(self, node=None):
        Node.__init__(self, node if node is not None else xml.etree.ElementTree.fromstring(default_or_profile))

        self.constraints = []
        cc = self.node.findall('{%s}Constraint' % get_long_ns('rtc'))
        for c in cc:
            self.appendConstraint(Constraint(c))
            pass

    def appendConstraint(self, constraint):
        self.constraints.append(constraint)
        self.children.append(constraint)


class Action(Node):
    def __init__(self, node):
        Node.__init__(self, node)
        docs = self.node.findall('{%s}Doc' % get_long_ns('rtcDoc'))
        if len(docs) != 0:
            self.doc = Doc(docs[0])
        else:
            self.doc = Doc(default_action_doc_profile)
        self.children.append(self.doc)

    def setImplemented(self, flag):
        self['rtc:implemented'] = 'true' if flag else 'false'


class Actions(Node):
    def __init__(self, node):
        Node.__init__(self, node)
        [uri, tag] = normalize(node.tag)
        for child in node.getchildren():
            [c_uri, c_tag] = normalize(child.tag)
            a = Action(child)
            self.__dict__[c_tag] = a
            self.children.append(a)


def get_etree(rtcp):
    def save_sub(elem, node):
        # print 'save_sub:', node
        for key, value in list(node.attrib.items()):  # set attribute
            name = '%s:%s' % (get_short_ns(key.split('}')[0][1:]), key.split('}')[1])
            elem.set(name, value)

        if not node.gettext() is None:
            if len(node.gettext().strip()) > 0:
                elem.text = node.gettext()

        for child in node.children:
            key = child.node.tag
            name = '%s:%s' % (get_short_ns(key.split('}')[0][1:]), key.split('}')[1])
            # print ' children:', name
            subelem = xml.etree.ElementTree.SubElement(elem, name)
            save_sub(subelem, child)

    root = xml.etree.ElementTree.Element('rtc:RtcProfile')
    # for key, value in rtcp.attrib.items():
    #    name = '%s:%s' % (get_short_ns(key.split('}')[0][1:]), key.split('}')[1])
    #    root.set(name, value)

    for key, value in list(known_namespaces.items()):
        root.set('xmlns:%s' % key, value)

    save_sub(root, rtcp)
    #root.set('xmlns:rtcExt', 'http://www.openrtp.org/namespaces/rtc_ext')
    #root.set('xmlns:rtcDoc', "http://www.openrtp.org/namespaces/rtc_doc")
    #root.set('xmlns:rtc', "http://www.openrtp.org/namespaces/rtc")
    #root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

    #open('out.xml', 'w').write(xml.etree.ElementTree.tostring(root))
    # print ' - writing', filename
    # print root
    return root


def tostring(rtcp, pretty_print=False):
    #import lxml.etree
    #tree = get_etree(rtcp)
    # return lxml.etree.tostring(tree, pretty_print=pretty_print)
    root = get_etree(rtcp)
    encoding = 'unicode'
    strbuf = xml.etree.ElementTree.tostring(root, encoding=encoding)
    if not pretty_print:
        return strbuf

    output_buf = ''
    tab = ''
    for line in strbuf.replace('>', '>\n').split('\n'):
        if line.startswith('</'):
            tab = tab[:-2]
        output_buf = output_buf + tab + line.strip() + '\n'
        _alone = False
        if line.endswith('/>'):
            # do nothing
            _alone = True
        elif line.startswith('</'):
            pass
        elif line.endswith('>'):
            tab = tab + '  '

    return output_buf
# def parse_buf(s, output)


class RTCProfile(Node):

    """
    """

    def __init__(self, filename="", str=""):
        try:
            # print str
            self._filename = filename
            if len(filename) > 0:
                et = xml.etree.ElementTree.parse(self.path)
                root = et.getroot()
            elif len(str) > 0:
                root = xml.etree.ElementTree.fromstring(str)
            else:
                root = xml.etree.ElementTree.fromstring(default_rtcprofile)

            self.node = root
            self.attrib = root.attrib
            self.children = []

            [uri, tag] = normalize(root.tag)
            for basicInfo in root.findall('{%s}BasicInfo' % uri):
                self.name = basicInfo.attrib['{%s}name' % uri]
                self.category = basicInfo.attrib['{%s}category' % uri]
                self.basicInfo = Node(basicInfo)
                docs = basicInfo.findall('{%s}Doc' % get_long_ns('rtcDoc'))
                if len(docs) != 0:
                    self.basicInfo.doc = Doc(docs[0])
                else:
                    self.basicInfo.doc = Doc(default_basicInfo_doc_str)
                self.basicInfo.children.append(self.basicInfo.doc)

                self.children.append(self.basicInfo)

            for language in root.findall('{%s}Language' % uri):
                self.language = Node(language)  # language.attrib['{%s}kind' % uri]
                #docs = language.findall('{%s}Doc' % get_long_ns('rtcDoc'))
                # if len(docs) != 0:
                #    self.language.doc = Doc(docs[0])
                # else:
                #    self.language.doc = Doc()
                # self.language.children.append(self.language.doc)
                self.children.append(self.language)

            for action in root.findall('{%s}Actions' % uri):
                self.actions = Actions(action)
                self.children.append(self.actions)

            self.dataports = []
            for dport in root.findall('{%s}DataPorts' % uri):
                dp = DataPort(dport)
                self.dataports.append(dp)  # Node(dport))
                self.children.append(dp)  # Node(dport))
                # self.dataports.append(DataPort(dport.attrib['{%s}name' % uri],
                #                               dport.attrib['{%s}type' % uri],
                #                               dport.attrib['{%s}portType' % uri]))

            self.serviceports = []
            for sport in root.findall('{%s}ServicePorts' % uri):
                sp = ServicePort(sport)
                self.serviceports.append(sp)
                self.children.append(sp)

            self.configurationSet = None
            # self.children.append(self.configurationSet)
            if len(root.findall('{%s}ConfigurationSet' % uri)) > 1:
                raise InvalidRTCProfileError(filename, 'Multiple ConfigurationSet Node.')

            for cset in root.findall('{%s}ConfigurationSet' % uri):
                cs = ConfigurationSet(cset)
                self.configurationSet = cs
                self.children.append(cs)
                break

        except Exception as e:
            traceback.print_exc()
            raise InvalidRTCProfileError(filename, 'Parsing Error')
        pass

    def getDataPorts(self):
        return self.dataports

    def __str__(self):
        return self.getName() + " in " + self.getLanguage()
        pass

    @property
    def inports(self):
        return [p for p in self.dataports if p.portType == 'DataInPort']

    @property
    def outports(self):
        return [p for p in self.dataports if p.portType == 'DataOutPort']

    # @property
    # def serviceports(self):
    #    return [p for p in self.dataports if p.portType == 'ServicePort']

    @property
    def filename(self):
        # return os.path.basename(self._filename)
        return self._filename

    @property
    def path(self):
        return self._filename

    def getRTCProfileFileName(self):
        return self.path

    def getCategory(self):
        return self.basicInfo.category

    def getName(self):
        return self.basicInfo.name

    def getLanguage(self):
        return self.language.kind


# Utility Functions


def normalize(name):
    if name[0] == '{':
        uri, tag = name[1:].split('}')
        return [uri, tag]

    return ['', name]


default_basicInfo_doc_str = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
  <rtcDoc:Doc xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" rtcDoc:reference="" rtcDoc:license="" rtcDoc:creator="" rtcDoc:algorithm="" rtcDoc:inout="" rtcDoc:description=""/>
"""

default_rtcprofile = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rtc:RtcProfile rtc:version="0.2" rtc:id="RTC:MODULE_VENDOR:MODULE_CATEGORY:MODULE_NAME:MODULE_VERSION" xmlns:rtcExt="http://www.openrtp.org/namespaces/rtc_ext" xmlns:rtcDoc="http://www.openrtp.org/namespaces/rtc_doc" xmlns:rtc="http://www.openrtp.org/namespaces/rtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <rtc:BasicInfo xsi:type="rtcExt:basic_info_ext" rtcExt:saveProject="PROJECT_NAME" rtc:updateDate="2013-07-18T11:35:13.287+09:00" rtc:creationDate="2013-07-17T13:19:33+09:00" rtc:version="MODULE_VERSION" rtc:vendor="MODULE_VENDOR" rtc:maxInstances="1" rtc:executionType="PeriodicExecutionContext" rtc:executionRate="1000.0" rtc:description="MODULE_DESCRIPTION" rtc:category="MODULE_CATEGORY" rtc:componentKind="DataFlowComponent" rtc:activityType="PERIODIC" rtc:componentType="STATIC" rtc:name="MODULE_NAME">
        <rtcDoc:Doc rtcDoc:reference="" rtcDoc:license="" rtcDoc:creator="" rtcDoc:algorithm="" rtcDoc:inout="" rtcDoc:description=""/>
        <rtcExt:VersionUpLogs></rtcExt:VersionUpLogs>
    </rtc:BasicInfo>
    <rtc:Actions>
        <rtc:OnInitialize xsi:type="rtcDoc:action_status_doc" rtc:implemented="true"/>
        <rtc:OnFinalize xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
        <rtc:OnStartup xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
        <rtc:OnShutdown xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
        <rtc:OnActivated xsi:type="rtcDoc:action_status_doc" rtc:implemented="true"/>
        <rtc:OnDeactivated xsi:type="rtcDoc:action_status_doc" rtc:implemented="true"/>
        <rtc:OnAborting xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
        <rtc:OnError xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
        <rtc:OnReset xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
        <rtc:OnExecute xsi:type="rtcDoc:action_status_doc" rtc:implemented="true"/>
        <rtc:OnStateUpdate xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
        <rtc:OnRateChanged xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
        <rtc:OnAction xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
        <rtc:OnModeChanged xsi:type="rtcDoc:action_status_doc" rtc:implemented="false"/>
    </rtc:Actions>
    <rtc:ConfigurationSet>
<!--
        <rtc:Configuration xsi:type="rtcExt:configuration_ext" rtcExt:variableName="ipaddress" rtc:unit="" rtc:defaultValue="nao.local" rtc:type="string" rtc:name="ipaddress">
            <rtcExt:Properties rtcExt:value="text" rtcExt:name="__widget__"/>
        </rtc:Configuration>
-->
    </rtc:ConfigurationSet>
<!--
    <rtc:DataPorts xsi:type="rtcExt:dataport_ext" rtcExt:position="RIGHT" rtcExt:variableName="camera" rtc:unit="" rtc:subscriptionType="" rtc:dataflowType="" rtc:interfaceType="" rtc:idlFile="" rtc:type="RTC::CameraImage" rtc:name="camera" rtc:portType="DataOutPort">
        <rtcDoc:Doc rtcDoc:operation="" rtcDoc:occerrence="" rtcDoc:unit="" rtcDoc:semantics="" rtcDoc:number="" rtcDoc:type="" rtcDoc:description=""/>
    </rtc:DataPorts>
-->
<!--
    <rtc:ServicePorts xsi:type="rtcExt:serviceport_ext" rtcExt:position="LEFT" rtc:name="NAO_srv">
        <rtc:ServiceInterface xsi:type="rtcExt:serviceinterface_ext" rtcExt:variableName="motion" rtc:path="/Users/ysuga/rtm/idl" rtc:type="ssr::ALMotion" rtc:idlFile="/Users/ysuga/rtm/idl/NAO.idl" rtc:instanceName="ALMotion" rtc:direction="Provided" rtc:name="ALMotion"/>
        <rtc:ServiceInterface xsi:type="rtcExt:serviceinterface_ext" rtcExt:variableName="textToSpeech" rtc:path="/Users/ysuga/rtm/idl" rtc:type="ssr::ALTextToSpeech" rtc:idlFile="/Users/ysuga/rtm/idl/NAO.idl" rtc:instanceName="ALTextToSpeech" rtc:direction="Provided" rtc:name="ALTextToSpeech"/>
        <rtc:ServiceInterface xsi:type="rtcExt:serviceinterface_ext" rtcExt:variableName="behaviorManager" rtc:path="/Users/ysuga/rtm/idl" rtc:type="ssr::ALBehaviorManager" rtc:idlFile="/Users/ysuga/rtm/idl/NAO.idl" rtc:instanceName="ALBehaviorManager" rtc:direction="Provided" rtc:name="ALBehaviorManager"/>
        <rtc:ServiceInterface xsi:type="rtcExt:serviceinterface_ext" rtcExt:variableName="memory" rtc:path="/Users/ysuga/rtm/idl" rtc:type="ssr::ALMemory" rtc:idlFile="/Users/ysuga/rtm/idl/NAO.idl" rtc:instanceName="ALMemory" rtc:direction="Provided" rtc:name="ALMemory"/>
        <rtc:ServiceInterface xsi:type="rtcExt:serviceinterface_ext" rtcExt:variableName="leds" rtc:path="/Users/ysuga/rtm/idl" rtc:type="ssr::ALLeds" rtc:idlFile="/Users/ysuga/rtm/idl/NAO.idl" rtc:instanceName="ALLeds" rtc:direction="Provided" rtc:name="ALLeds"/>
        <rtc:ServiceInterface xsi:type="rtcExt:serviceinterface_ext" rtcExt:variableName="videoDevice" rtc:path="/Users/ysuga/rtm/idl" rtc:type="ssr::ALVideoDevice" rtc:idlFile="/Users/ysuga/rtm/idl/NAO.idl" rtc:instanceName="ALVideoDevice" rtc:direction="Provided" rtc:name="ALVideoDevice"/>
    </rtc:ServicePorts>
-->
    <rtc:Language xsi:type="rtcExt:language_ext" rtc:kind="Language">
    </rtc:Language>
</rtc:RtcProfile>
"""


class RTCProfileBuilder():
    """
    Class Interface for RTC Profile Builder.

    Using member method, RTC Profile is built with user defined parameters.
    If you give the default parameter for constructor, you can modify the RTCP by this interface.
    You can get RTCP data by using buildRTCProfile method.
    """

    def __init__(self, rtcp=None):
        if rtcp:
            self.rtcp = copy.deepcopy(rtcp)
        else:
            self.rtcp = RTCProfile()

    def setBasicInfo(self, name, category, vendor, version, description=""):
        self.rtcp.basicInfo['rtc:name'] = name
        self.rtcp.basicInfo['rtc:vendor'] = vendor
        self.rtcp.basicInfo['rtc:category'] = category
        self.rtcp.basicInfo['rtc:version'] = str(version)
        self.rtcp.basicInfo['rtc:description'] = description
        self.rtcp['rtc:id'] = 'RTC:%s:%s:%s:%s' % (vendor, category, name, str(version))

    def setLanguage(self, language):
        self.rtcp.language['rtc:kind'] = language

    def appendDataPort(self, portType, type, name):
        # print 'appendDataPort:', portType, ':', type, ':', name
        dp = DataPort()
        dp['rtc:type'] = type
        dp['rtc:name'] = name
        dp['rtcExt:variableName'] = name
        dp['rtc:portType'] = portType
        if portType == 'DataOutPort':
            dp['rtcExt:position'] = 'RIGHT'
        elif portType == 'DataInPort':
            dp['rtcExt:position'] = 'LEFT'

        # print dp print dp.name
        self.rtcp.dataports.append(dp)
        self.rtcp.children.append(dp)

    def removeDataPort(self, dp):
        for d in self.rtcp.dataports:
            if d.equals(dp):
                self.rtcp.dataports.remove(d)
                self.rtcp.children.remove(d)

    def appendServicePort(self, name):
        sp = ServicePort()
        sp['rtc:name'] = name
        self.rtcp.serviceports.append(sp)
        self.rtcp.children.append(sp)

    def removeServicePort(self, sp):
        for s in self.rtcp.serviceports:
            if s.equals(sp):
                self.rtcp.serviceports.remove(s)
                self.rtcp.children.remove(s)

        pass

    def removeServiceInterfaceFromServicePort(self, servicePortName, serviceInterfaceName):
        for sp in self.rtcp.serviceports:
            if sp.name == servicePortName:
                for si in sp.serviceInterfaces:
                    if si.name == serviceInterfaceName:
                        sp.serviceInterfaces.remove(si)
                        sp.children.remove(si)
                        return
        pass

    def appendServiceInterfaceToServicePort(self, servicePortName, path, idlFile, type, direction, name, instanceName=None):
        si = ServiceInterface()
        si['rtc:name'] = name
        si['rtc:instanceName'] = instanceName if instanceName else name
        si['rtc:type'] = type
        si['rtc:direction'] = direction
        si['rtc:path'] = path
        si['rtc:idlFile'] = idlFile

        for sp in self.rtcp.serviceports:
            if sp.name == servicePortName:
                sp.serviceInterfaces.append(si)
                sp.children.append(si)
                return

        class ServicePortNotFoundException(Exception):
            pass
        raise ServicePortNotFoundException()

    def removeConfiguration(self, name):
        for cf in self.rtcp.configurationSet.configurations:
            if cf.name == name:
                self.rtcp.configurationSet.configurations.remove(cf)
                self.rtcp.configurationSet.children.remove(cf)
        pass

    def appendConfiguration(self, type, name, defaultValue):
        cf = Configuration()
        cf['rtc:name'] = name
        cf['rtcExt:variableName'] = name
        cf['rtc:type'] = type
        cf['rtc:defaultValue'] = defaultValue
        try:
            if self.rtcp.configurationSet == None:
                cs = ConfigurationSet()
                self.rtcp.configurationSet = cs
                self.rtcp.children.append(cs)
        except:
            traceback.print_exc()
            raise AttributeError()

        self.rtcp.configurationSet.configurations.append(cf)
        self.rtcp.configurationSet.children.append(cf)

    def buildRTCProfile(self):
        return self.rtcp
