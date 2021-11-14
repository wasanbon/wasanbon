# test for wasanbon/core/plugins/admin/rtcprofile_plugin/rtcprofile/rtcprofile.py

import unittest
import xml
from unittest import mock
from unittest.mock import Mock

from wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile import rtcprofile


class TestPlugin(unittest.TestCase):

    def test_get_short_ns(self):
        """test for get_short_ns"""
        # test (hit key)
        test_uri = 'http://www.w3.org/2001/XMLSchema-instance'
        ret = rtcprofile.get_short_ns(test_uri)
        self.assertEqual(ret, 'xsi')
        # test (no key)
        test_uri = 'aaaa'
        ret = rtcprofile.get_short_ns(test_uri)
        self.assertEqual(ret, None)

    def test_get_long_ns(self):
        """test for get_long_ns"""
        # test (hit key)
        test_uri = 'xsi'
        ret = rtcprofile.get_long_ns(test_uri)
        self.assertEqual(ret, 'http://www.w3.org/2001/XMLSchema-instance')
        # test (no key)
        test_uri = 'aaaa'
        ret = rtcprofile.get_short_ns(test_uri)
        self.assertEqual(ret, None)

    def test_InvalidRTCProfileError(self):
        """test for InvalidRTCProfileError"""
        test_filename = 'test_filename'
        test_msg = 'test_msg'
        # test
        inst = rtcprofile.InvalidRTCProfileError(test_filename, test_msg)
        expected_str = 'InvalidRTCProfileError(%s):%s' % (
            test_filename, test_msg)
        self.assertEqual('{}'.format(inst), expected_str)

    def test_Node_init(self):
        """test for Node.__init__ & gettext"""
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = 'a'
        test_node.text = 'b'
        # test
        inst = rtcprofile.Node(test_node)
        self.assertEqual(inst.node, test_node)
        self.assertEqual(inst.attrib, test_node.attrib)
        self.assertEqual(inst.children, [])
        self.assertEqual(inst.text, test_node.text)
        self.assertEqual(inst.gettext(), test_node.text)

    def test_Node_getitem_has_key(self):
        """test for Node.__getitem__ has key"""
        test_node = Mock(spec=['attrib', 'text'])
        test_ret = 'test_1'
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': test_ret}
        test_node.text = 'b'
        inst = rtcprofile.Node(test_node)
        # test
        test_key = 'xsi:t1'
        ret = inst[test_key]
        self.assertEqual(ret, test_ret)

    def test_Node_getitem_no_key(self):
        """test for Node.__getitem__ has key"""
        test_node = Mock(spec=['attrib', 'text'])
        test_ret = 'test_1'
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': test_ret}
        test_node.text = 'b'
        inst = rtcprofile.Node(test_node)
        # test
        test_key = 'aaaa:t1'
        ret = inst[test_key]
        self.assertEqual(ret, None)

    def test_Node_setitem_has_key(self):
        """test for Node.__setitem__ has key"""
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {}
        test_node.text = 'b'
        test_value = 'test_value'
        inst = rtcprofile.Node(test_node)
        # test
        test_key = 'xsi:t1'
        inst[test_key] = test_value
        self.assertEqual(
            inst.node.attrib['{http://www.w3.org/2001/XMLSchema-instance}t1'], test_value)

    def test_Node_setitem_no_key(self):
        """test for Node.__setitem__ has key"""
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {}
        test_node.text = 'b'
        test_value = 'test_value'
        inst = rtcprofile.Node(test_node)
        # test
        test_key = 'aaaa:t1'
        inst[test_key] = test_value
        self.assertFalse(
            '{http://www.w3.org/2001/XMLSchema-instance}t1' in inst.node.attrib)

    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.rtcprofile.get_short_ns')
    def test_Node_keys(self, get_short_ns_mock):
        """test for Node.keys"""
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1'}
        test_node.text = 'b'
        inst = rtcprofile.Node(test_node)
        # mock patch settings
        get_short_ns_mock.return_value = 'test1'
        # test
        expected_ret = ['test1:t1']
        self.assertEqual(inst.keys(), expected_ret)

    def test_Node__getattr__(self):
        """test for Node.__getattr__ key __"""
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1',
            '{http://www.openrtp.org/namespaces/rtc}t1': 't1',
        }
        test_node.text = 'b'
        inst = rtcprofile.Node(test_node)
        # test
        expected_ret = 't1'
        self.assertEqual(inst.xsi_t1, expected_ret)
        self.assertEqual(inst.t1, expected_ret)

    def test_Doc(self):
        """test for Doc.__init__ & __getattr__"""
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1',
            '{http://www.openrtp.org/namespaces/rtc_doc}t1': 't1',
        }
        test_node.text = 'b'
        # test
        inst = rtcprofile.Doc(test_node)
        # __getattr__
        expected_ret = 't1'
        self.assertEqual(inst.xsi_t1, expected_ret)
        self.assertEqual(inst.t1, expected_ret)

    def test_Properties(self):
        """test for Properties.__init__ & __getattr__"""
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1',
            '{http://www.openrtp.org/namespaces/rtc_ext}t1': 't1',
        }
        test_node.text = 'b'
        # test
        inst = rtcprofile.Properties(test_node)
        # __getattr__
        expected_ret = 't1'
        self.assertEqual(inst.xsi_t1, expected_ret)
        self.assertEqual(inst.t1, expected_ret)

    def test_DataPort(self):
        """test for DataPort.__init__ & equals"""
        # test
        inst = rtcprofile.DataPort()
        # equals
        test_dict = {
            'rtc:name': 1,
            'rtc:type': 2,
            'rtc:portType': 3,
        }
        self.assertFalse(inst.equals(test_dict))

    def test_ServicePort(self):
        """test for ServicePort.__init__ & equals"""
        # test
        inst = rtcprofile.ServicePort()
        # equals
        test_dict = {
            'rtc:name': 1,
        }
        self.assertFalse(inst.equals(test_dict))

    def test_ServiceInterface(self):
        """test for ServiceInterface.__init__ & equals"""
        # test
        inst = rtcprofile.ServiceInterface()
        # equals
        test_dict = Mock()
        test_dict.name = 'test1'
        test_dict.type = 'test2'
        test_dict.direction = 'test3'
        self.assertFalse(inst.equals(test_dict))

    def test_Configuration(self):
        """test for Configuration.__init__ & equals"""
        # test
        inst = rtcprofile.Configuration()
        # equals
        test_dict = Mock()
        test_dict.name = 'test1'
        self.assertFalse(inst.equals(test_dict))
        # __repr__
        self.assertEqual(repr(inst), inst.name)

    def test_ConfigurationSet(self):
        """test for ConfigurationSet.__init__ & __repr__"""
        # test
        inst = rtcprofile.ConfigurationSet()
        # __repr__
        self.assertEqual(repr(inst), inst.node.tag)

    def test_Constraint(self):
        """test for Constraint.__init__"""
        # test
        _ = rtcprofile.Constraint()

    def test_ConstraintUnitType(self):
        """test for ConstraintUnitType.__init__ & addChild"""
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1',
            '{http://www.openrtp.org/namespaces/rtc_ext}t1': 't1',
        }
        test_node.text = 'b'
        # test
        inst = rtcprofile.ConstraintUnitType()
        # addChild
        inst.addChild(test_node)
        self.assertEqual(inst.constraint, test_node)
        self.assertEqual(inst.children, [test_node])

    def test_PropertyIsEqualTo(self):
        """test for PropertyIsEqualTo.__init__ """
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1',
            '{http://www.openrtp.org/namespaces/rtc_ext}t1': 't1',
        }
        test_node.text = 'b'
        # test
        _ = rtcprofile.PropertyIsEqualTo()

    def test_Literal(self):
        """test for Literal.__init__ """
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1',
            '{http://www.openrtp.org/namespaces/rtc_ext}t1': 't1',
        }
        test_node.text = 'b'
        # test
        _ = rtcprofile.Literal()

    def test_Or(self):
        """test for Or.__init__ & appendConstraint"""
        test_node = Mock(spec=['attrib', 'text'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1',
            '{http://www.openrtp.org/namespaces/rtc_ext}t1': 't1',
        }
        test_node.text = 'b'
        # test
        inst = rtcprofile.Or()
        # appendConstraint
        inst.appendConstraint(test_node)
        self.assertEqual(inst.constraints, [test_node])
        self.assertEqual(inst.children, [test_node])

    def test_Action(self):
        """test for Action.__init__ & setImplemented"""
        test_node = Mock(spec=['attrib', 'text', 'findall'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1',
            '{http://www.openrtp.org/namespaces/rtc_ext}t1': 't1',
        }
        test_node.text = 'b'
        test_node.findall.return_value = []
        # test
        inst = rtcprofile.Action(test_node)
        # setImplemented
        inst.setImplemented(True)
        self.assertEqual(inst['rtc:implemented'], 'true')

    def test_Actions(self):
        """test for Actions.__init__ """
        test_node = Mock(
            spec=['attrib', 'text', 'tag', 'getchildren', 'findall'])
        test_node.attrib = {
            '{http://www.w3.org/2001/XMLSchema-instance}t1': 't1',
            '{http://www.openrtp.org/namespaces/rtc_ext}t1': 't1',
        }
        test_node.text = 'b'
        test_node.tag = 'c'
        test_node.getchildren.return_value = [test_node]
        test_node.findall.return_value = [test_node]
        # test
        _ = rtcprofile.Actions(test_node)

    def test_get_etree(self):
        """test for get_etree """
        test_node1 = Mock(
            spec=['attrib', 'node', 'tag', 'children', 'gettext'])
        test_node1.attrib = {
            '{http://www.openrtp.org/namespaces/rtc_ext}t1': 't1',
        }
        test_node1.tag = '{http://www.openrtp.org/namespaces/rtc_ext}test_tag'
        test_node1.gettext.return_value = 'test_text1'
        test_node1.node = test_node1
        test_node1.children = []
        test_node = Mock(spec=['attrib', 'node', 'tag', 'children', 'gettext'])
        test_node.attrib = {
            '{http://www.openrtp.org/namespaces/rtc_ext}t': 't',
        }
        test_node.gettext.return_value = 'test_text'
        test_node.children = [test_node1]
        ret = rtcprofile.get_etree(test_node)
        self.assertEqual(ret.get('rtcExt:t'), 't')
        self.assertEqual(ret.text, 'test_text')
        self.assertEqual(ret[0].get('rtcExt:t1'), 't1')

    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.rtcprofile.get_etree')
    def test_get_tostring_pretty_pring(self, get_etree_mock):
        """test for tostring pretty_print"""
        # mock patch settings
        test_root_et = xml.etree.ElementTree.Element('test_root')
        get_etree_mock.return_value = test_root_et
        test_node = Mock(spec=['attrib', 'node', 'tag', 'children', 'gettext'])
        test_node.attrib = {
            '{http://www.openrtp.org/namespaces/rtc_ext}t': 't',
        }
        test_node.gettext.return_value = 'test_text'
        test_node.children = []
        ret = rtcprofile.tostring(test_node, False)
        self.assertEqual(ret, xml.etree.ElementTree.tostring(
            test_root_et, 'unicode'))

    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.rtcprofile.get_etree')
    def test_get_tostring(self, get_etree_mock):
        """test for tostring"""
        # mock patch settings
        test_root_et = xml.etree.ElementTree.Element('test_root')
        get_etree_mock.return_value = test_root_et
        test_node = Mock(spec=['attrib', 'node', 'tag', 'children', 'gettext'])
        test_node.attrib = {
            '{http://www.openrtp.org/namespaces/rtc_ext}t': 't',
        }
        test_node.gettext.return_value = 'test_text'
        test_node.children = []
        ret = rtcprofile.tostring(test_node, True)
        expected_ret = '<test_root />\n\n'
        self.assertEqual(ret, expected_ret)

    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.rtcprofile.ConfigurationSet')
    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.rtcprofile.Actions')
    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.rtcprofile.normalize')
    @mock.patch('xml.etree.ElementTree')
    def test_RTCProfile__init__(self, et_mock, normalize_mock, actions_mock, configurationset_mock):
        """test for RTCProfile.__init__"""
        # mock patch settings
        normalize_mock.return_value = ('test_uri', None)
        root_mock = Mock()
        root_mock.attrib = {
            '{test_uri}name': 'test_uri_name',
            '{test_uri}category': 'category',
        }
        root_mock.findall.return_value = [root_mock]
        et_mock.parse.return_value = et_mock
        et_mock.getroot.return_value = root_mock
        test_filename = 'test_filename'
        test_str = 'test_str'
        # test
        inst = rtcprofile.RTCProfile(test_filename, test_str)
        self.assertEqual(inst._filename, test_filename)
        self.assertEqual(inst.node, root_mock)
        self.assertEqual(inst.attrib, root_mock.attrib)
        self.assertEqual(inst.getDataPorts(), inst.dataports)
        self.assertEqual(inst.getRTCProfileFileName(), inst.path)

    def test_normalize(self):
        """test for normalize"""
        test_name = '{a}b'
        ret = rtcprofile.normalize(test_name)
        self.assertEqual(ret, ['a', 'b'])
        test_name = 'ab'
        ret = rtcprofile.normalize(test_name)
        self.assertEqual(ret, ['', 'ab'])

    def test_RTCProfileBuilder(self):
        """test for RTCProfileBuilder.__init__"""
        inst = rtcprofile.RTCProfileBuilder()
        self.assertIsInstance(inst.rtcp, rtcprofile.RTCProfile)
        inst = rtcprofile.RTCProfileBuilder('abc')
        self.assertIsInstance(inst.rtcp, str)

    def test_RTCProfileBuilder_setBasicInfo(self):
        """test for RTCProfileBuilder.setBasicInfo"""
        test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        # test
        test_name = 'name'
        test_category = 'category'
        test_vendor = 'vendor'
        test_version = 'version'
        test_description = 'description'
        inst.setBasicInfo(test_name, test_category,
                          test_vendor, test_version, test_description)
        self.assertEqual(inst.rtcp.basicInfo['rtc:name'], test_name)
        self.assertEqual(inst.rtcp.basicInfo['rtc:vendor'], test_vendor)
        self.assertEqual(inst.rtcp.basicInfo['rtc:category'], test_category)
        self.assertEqual(inst.rtcp.basicInfo['rtc:version'], test_version)
        self.assertEqual(
            inst.rtcp.basicInfo['rtc:description'], test_description)
        self.assertEqual(inst.rtcp['rtc:id'], 'RTC:%s:%s:%s:%s' % (
            test_vendor, test_category, test_name, test_version))

    def test_RTCProfileBuilder_setLanguage(self):
        """test for RTCProfileBuilder.setLanguage"""
        # test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder()
        # test
        test_lang = 'lang'
        inst.setLanguage(test_lang)
        self.assertEqual(inst.rtcp.language['rtc:kind'], test_lang)

    def test_RTCProfileBuilder_appendDataPort(self):
        """test for RTCProfileBuilder.appendDataPort"""
        test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        # test
        test_proto = 'DataInPort'
        test_type = 'type'
        test_name = 'name'
        inst.appendDataPort(test_proto, test_type, test_name)
        self.assertEqual(inst.rtcp.dataports[0]['rtc:type'], test_type)
        self.assertEqual(inst.rtcp.dataports[0]['rtc:name'], test_name)
        self.assertEqual(
            inst.rtcp.dataports[0]['rtcExt:variableName'], test_name)
        self.assertEqual(inst.rtcp.dataports[0]['rtc:portType'], test_proto)
        self.assertEqual(inst.rtcp.dataports[0]['rtcExt:position'], 'LEFT')
        self.assertEqual(inst.rtcp.children[-1]['rtc:type'], test_type)
        self.assertEqual(inst.rtcp.children[-1]['rtc:name'], test_name)
        self.assertEqual(
            inst.rtcp.children[-1]['rtcExt:variableName'], test_name)
        self.assertEqual(inst.rtcp.children[-1]['rtc:portType'], test_proto)
        self.assertEqual(inst.rtcp.children[-1]['rtcExt:position'], 'LEFT')

    def test_RTCProfileBuilder_removeDataPort(self):
        """test for RTCProfileBuilder.removeDataPort"""
        test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        # test
        test_proto = 'DataInPort'
        test_type = 'type'
        test_name = 'name'
        inst.appendDataPort(test_proto, test_type, test_name)
        len_children = len(inst.rtcp.children)
        inst.removeDataPort(inst.rtcp.dataports[-1])
        self.assertEqual(len(inst.rtcp.dataports), 0)
        self.assertEqual(len(inst.rtcp.children), len_children-1)

    def test_RTCProfileBuilder_appendServicePort(self):
        """test for RTCProfileBuilder.appendServicePort"""
        test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        # test
        test_name = 'name'
        inst.appendServicePort(test_name)
        self.assertEqual(inst.rtcp.serviceports[-1]['rtc:name'], test_name)
        self.assertEqual(inst.rtcp.children[-1]['rtc:name'], test_name)

    def test_RTCProfileBuilder_removeServicePort(self):
        """test for RTCProfileBuilder.removeServicePort"""
        test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        # test
        test_name = 'name'
        inst.appendServicePort(test_name)
        len_children = len(inst.rtcp.children)
        inst.removeServicePort(inst.rtcp.serviceports[-1])
        self.assertEqual(len(inst.rtcp.serviceports), 0)
        self.assertEqual(len(inst.rtcp.children), len_children-1)

    def test_RTCProfileBuilder_appendServiceInterfaceToServicePort(self):
        """test for RTCProfileBuilder.appendServiceInterfaceToServicePort"""
        test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        test_name = 'portname'
        test_portname = 'portname'
        test_path = 'path'
        test_idlFile = 'idl'
        test_type = 'type'
        test_direction = 'direction'
        test_instanceName = 'instanceName'
        # test(no service port)
        with self.assertRaises(Exception):
            inst.appendServiceInterfaceToServicePort(
                test_portname, test_path, test_idlFile, test_type, test_direction, test_name, test_instanceName)
        # test
        inst.appendServicePort(test_name)
        inst.appendServiceInterfaceToServicePort(
            test_portname, test_path, test_idlFile, test_type, test_direction, test_name, test_instanceName)
        self.assertEqual(
            inst.rtcp.serviceports[-1].serviceInterfaces[-1]['rtc:name'], test_name)
        self.assertEqual(
            inst.rtcp.serviceports[-1].serviceInterfaces[-1]['rtc:instanceName'], test_instanceName)
        self.assertEqual(
            inst.rtcp.serviceports[-1].serviceInterfaces[-1]['rtc:type'], test_type)
        self.assertEqual(
            inst.rtcp.serviceports[-1].serviceInterfaces[-1]['rtc:direction'], test_direction)
        self.assertEqual(
            inst.rtcp.serviceports[-1].serviceInterfaces[-1]['rtc:path'], test_path)
        self.assertEqual(
            inst.rtcp.serviceports[-1].serviceInterfaces[-1]['rtc:idlFile'], test_idlFile)
        self.assertEqual(
            inst.rtcp.serviceports[-1].children[-1]['rtc:name'], test_name)
        self.assertEqual(
            inst.rtcp.serviceports[-1].children[-1]['rtc:instanceName'], test_instanceName)
        self.assertEqual(
            inst.rtcp.serviceports[-1].children[-1]['rtc:type'], test_type)
        self.assertEqual(
            inst.rtcp.serviceports[-1].children[-1]['rtc:direction'], test_direction)
        self.assertEqual(
            inst.rtcp.serviceports[-1].children[-1]['rtc:path'], test_path)
        self.assertEqual(
            inst.rtcp.serviceports[-1].children[-1]['rtc:idlFile'], test_idlFile)

    def test_RTCProfileBuilder_removeServiceInterfaceFromServicePort(self):
        """test for RTCProfileBuilder.removeServiceInterfaceFromServicePort"""
        test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        test_name = 'portname'
        inst.appendServicePort(test_name)
        # test
        test_portname = 'portname'
        test_path = 'path'
        test_idlFile = 'idl'
        test_type = 'type'
        test_direction = 'direction'
        test_name = 'name'
        test_instanceName = 'instanceName'
        inst.appendServiceInterfaceToServicePort(
            test_portname, test_path, test_idlFile, test_type, test_direction, test_name, test_instanceName)
        len_children = len(inst.rtcp.serviceports[-1].children)
        inst.removeServiceInterfaceFromServicePort(test_portname, test_name)
        self.assertEqual(len(inst.rtcp.serviceports[-1].serviceInterfaces), 0)
        self.assertEqual(
            len(inst.rtcp.serviceports[-1].children), len_children-1)

    def test_RTCProfileBuilder_appendConfiguration(self):
        """test for RTCProfileBuilder.appendConfiguration"""
        test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        test_name = 'portname'
        test_type = 'type'
        test_default_value = 'value'
        # test
        inst.appendConfiguration(test_type, test_name, test_default_value)
        self.assertIsInstance(inst.rtcp.configurationSet,
                              rtcprofile.ConfigurationSet)
        self.assertIsInstance(
            inst.rtcp.children[-1], rtcprofile.ConfigurationSet)
        self.assertEqual(
            inst.rtcp.configurationSet.configurations[-1]['rtc:name'], test_name)
        self.assertEqual(
            inst.rtcp.configurationSet.configurations[-1]['rtcExt:variableName'], test_name)
        self.assertEqual(
            inst.rtcp.configurationSet.configurations[-1]['rtc:type'], test_type)
        self.assertEqual(
            inst.rtcp.configurationSet.configurations[-1]['rtc:defaultValue'], test_default_value)
        self.assertEqual(
            inst.rtcp.configurationSet.children[-1]['rtc:name'], test_name)
        self.assertEqual(
            inst.rtcp.configurationSet.children[-1]['rtcExt:variableName'], test_name)
        self.assertEqual(
            inst.rtcp.configurationSet.children[-1]['rtc:type'], test_type)
        self.assertEqual(
            inst.rtcp.configurationSet.children[-1]['rtc:defaultValue'], test_default_value)

    def test_RTCProfileBuilder_appendConfiguration(self):
        """test for RTCProfileBuilder.appendConfiguration raise error"""
        test_rtcp = rtcprofile.RTCProfile()
        test_rtcp.configurationSet = None
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        test_name = 'portname'
        test_type = 'type'
        test_default_value = 'value'
        # test
        self.assertNotIsInstance(
            inst.rtcp.configurationSet, rtcprofile.ConfigurationSet)
        with mock.patch.object(rtcprofile, 'ConfigurationSet', side_effect=Exception('test')):
            with self.assertRaises(AttributeError):
                inst.appendConfiguration(
                    test_type, test_name, test_default_value)
        self.assertIsNone(inst.rtcp.configurationSet)

    def test_RTCProfileBuilder_buildRTCProfile(self):
        """test for RTCProfileBuilder.buildRTCProfile"""
        test_rtcp = rtcprofile.RTCProfile()
        inst = rtcprofile.RTCProfileBuilder(test_rtcp)
        self.assertEqual(inst.buildRTCProfile(), inst.rtcp)


if __name__ == '__main__':
    unittest.main()
