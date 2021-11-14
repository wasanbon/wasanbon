# test for wasanbon/core/plugins/admin/rtc_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')


class TestPlugin(unittest.TestCase):

    class FunctionList:
        pass

    def setUp(self):
        import wasanbon.core.plugins.admin.rtc_plugin as m
        self.plugin = m.Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.rtc_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.rtcprofile'], self.plugin.depends())

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.get_rtcs_from_package')
    def test_get_rtcs_from_package(self, mock_get_rtcs_from_package):
        """get_rtcs_from_package normal case"""
        mock_get_rtcs_from_package.return_value = 'test'
        self.assertEqual('test', self.plugin.get_rtcs_from_package('package'))

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.get_rtcs_from_package')
    def test_get_rtc_from_package(self, mock_get_rtcs_from_package, mock_write):
        """get_rtc_from_package normal case"""
        rtc = self.FunctionList()
        setattr(rtc, 'rtcprofile', self.FunctionList)
        setattr(rtc.rtcprofile, 'basicInfo', self.FunctionList)
        setattr(rtc.rtcprofile.basicInfo, 'name', 'test_rtc')
        mock_get_rtcs_from_package.return_value = [rtc]
        self.assertEqual(rtc, self.plugin.get_rtc_from_package('package', 'test_rtc', verbose=False))
        mock_write.assert_not_called()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.get_rtcs_from_package')
    def test_get_rtc_from_package_v(self, mock_get_rtcs_from_package, mock_write):
        """get_rtc_from_package normal case with verbose option"""
        rtc = self.FunctionList()
        setattr(rtc, 'rtcprofile', self.FunctionList)
        setattr(rtc.rtcprofile, 'basicInfo', self.FunctionList)
        setattr(rtc.rtcprofile.basicInfo, 'name', 'test_rtc')
        mock_get_rtcs_from_package.return_value = [rtc]
        package = self.FunctionList()
        setattr(package, 'name', 'test_package_name')
        self.assertEqual(rtc, self.plugin.get_rtc_from_package(package, 'test_rtc', verbose=True))
        mock_write.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.rtc_plugin.get_rtcs_from_package')
    def test_get_rtc_from_package_error(self, mock_get_rtcs_from_package):
        """get_rtc_from_package error case"""
        rtc = self.FunctionList()
        setattr(rtc, 'rtcprofile', self.FunctionList)
        setattr(rtc.rtcprofile, 'basicInfo', self.FunctionList)
        setattr(rtc.rtcprofile.basicInfo, 'name', 'test_rtc')
        mock_get_rtcs_from_package.return_value = [rtc]
        package = self.FunctionList()
        setattr(package, 'name', 'test_package_name')
        import wasanbon
        with self.assertRaises(wasanbon.RTCNotFoundException):
            self.assertEqual(rtc, self.plugin.get_rtc_from_package(package, 'hoge'))


if __name__ == '__main__':
    unittest.main()
