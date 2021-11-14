# test for wasanbon/core/plugins/admin/rtcprofile_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')


class TestPlugin(unittest.TestCase):

    class FunctionList:
        pass

    def setUp(self):
        import wasanbon.core.plugins.admin.rtcprofile_plugin as m
        self.plugin = m.Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.rtcprofile_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment'], self.plugin.depends())

    def test_rtcprofile(self):
        """rtcprofile normal case"""
        from wasanbon.core.plugins.admin.rtcprofile_plugin import rtcprofile
        self.assertEqual(rtcprofile, self.plugin.rtcprofile)

    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('rtctree.path.parse_path')
    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.RTCProfileBuilder')
    def test_create_rtcprofile_1(self, mock_RTCProfileBuilder, mock_parse_path, mock_RTCTree):
        """create_rtcprofile normal case
        verbose = False
        is_component = True
        """
        ### setting ###
        mock_parse_path.return_value = ['path'], None
        tree = MagicMock(spec=['get_node'])
        comp = MagicMock()
        type(comp).iscomponent = PropertyMock(return_value=True)
        type(comp).properties = {'language': 'lang', 'conf.default': 'conf'}
        p1 = PropertyMock()
        p2 = PropertyMock()
        p3 = PropertyMock()
        p4 = PropertyMock()
        type(p1).porttype = 'hoge'
        type(p2).porttype = 'DataOutPort'
        type(p3).porttype = 'DataInPort'
        type(p4).porttype = 'CorbaPort'
        type(comp).ports = [p1, p2, p3, p4]
        tree.get_node.return_value = comp
        mock_RTCTree.return_value = tree
        rtcb = MagicMock(spec=['setBasicInfo', 'setLanguage', 'appendConfiguration', 'appendDataPort',
                         'appendServicePort', 'appendServiceInterfaceToServicePort', 'buildRTCProfile'])
        rtcb.buildRTCProfile.return_value = 'test'
        mock_RTCProfileBuilder.return_value = rtcb
        ### test ###
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.assertEqual('test', self.plugin.create_rtcprofile(rtc))
        self.assertEqual(1, rtcb.appendConfiguration.call_count)
        self.assertEqual(2, rtcb.appendDataPort.call_count)
        self.assertEqual(1, rtcb.appendServicePort.call_count)

    @mock.patch('traceback.print_exc')
    @mock.patch('sys.stdout.write')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('rtctree.path.parse_path')
    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.RTCProfileBuilder')
    def test_create_rtcprofile_2(self, mock_RTCProfileBuilder, mock_parse_path, mock_RTCTree, mock_write, mock_print_exc):
        """create_rtcprofile error case
        object is not component
        RTCTree.side_effect = [Exception(), tree]
        verbose = True
        is_component = False
        """
        ### setting ###
        mock_parse_path.return_value = ['path'], None
        tree = MagicMock(spec=['get_node'])
        comp = MagicMock()
        type(comp).is_component = PropertyMock(return_value=False)
        tree.get_node.return_value = comp
        mock_RTCTree.side_effect = [Exception(), tree]
        ### test ###
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.assertEqual(None, self.plugin.create_rtcprofile(rtc, verbose=True))
        self.assertEqual(2, mock_RTCTree.call_count)
        self.assertEqual(3, mock_write.call_count)
        mock_print_exc.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.rtcprofile.tostring', return_value='test')
    def test_tostring(self, mock_tostring):
        """tostring normal case"""
        ### test ###
        self.assertEqual('test', self.plugin.tostring('rtcp'))

    @mock.patch('wasanbon.core.plugins.admin.rtcprofile_plugin.compare_rtcprofile', return_value='test')
    def test_compare_rtcprofile(self, mock_compare_rtcprofile):
        """compare_rtcprofile normal case"""
        ### test ###
        self.assertEqual('test', self.plugin.compare_rtcprofile('rtcp0', 'rtcp1'))


if __name__ == '__main__':
    unittest.main()
