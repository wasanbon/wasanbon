# test for wasanbon/core/plugins/admin/builder_plugin/__init__.py Plugin class

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')


class TestPlugin(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.admin.builder_plugin as m
        self.admin_mock = MagicMock(spec=['environment'])
        self.admin_mock.environment(sepc=['getIDE'])
        type(self.admin_mock.environment).path = PropertyMock()
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        self.func = m

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.builder_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.rtc'], self.plugin.depends())

    class FunctionList():
        pass

    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.build_rtc_cpp')
    def test_build_rtc_cpp(self, mock_build_rtc_cpp):
        """build_rtc cpp build case"""
        ### set mock ###
        rtcprofile = self.FunctionList()
        setattr(rtcprofile, 'language', self.FunctionList())
        setattr(rtcprofile.language, 'kind', 'C++')
        mock_build_rtc_cpp.return_value = 'C++ test'
        ### test ###
        self.assertEqual('C++ test', self.plugin.build_rtc(rtcprofile))

    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.build_rtc_java')
    def test_build_rtc_java(self, mock_build_rtc_java):
        """build_rtc java build case"""
        ### set mock ###
        rtcprofile = self.FunctionList()
        setattr(rtcprofile, 'language', self.FunctionList())
        setattr(rtcprofile.language, 'kind', 'Java')
        mock_build_rtc_java.return_value = 'Java test'
        self.assertEqual('Java test', self.plugin.build_rtc(rtcprofile))

    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.build_rtc_python')
    def test_build_rtc_python(self, mock_build_rtc_python):
        """build_rtc python build case"""
        rtcprofile = self.FunctionList()
        setattr(rtcprofile, 'language', self.FunctionList())
        setattr(rtcprofile.language, 'kind', 'Python')
        mock_build_rtc_python.return_value = 'Python test'
        self.assertEqual('Python test', self.plugin.build_rtc(rtcprofile))

    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.clean_rtc_cpp')
    def test_clean_rtc_cpp(self, mock_clean_rtc_cpp):
        """clean_rtc cpp clean case"""
        rtcprofile = self.FunctionList()
        setattr(rtcprofile, 'language', self.FunctionList())
        setattr(rtcprofile.language, 'kind', 'C++')
        mock_clean_rtc_cpp.return_value = 'C++ test'
        self.assertEqual('C++ test', self.plugin.clean_rtc(rtcprofile))

    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.clean_rtc_java')
    def test_clean_rtc_java(self, mock_clean_rtc_java):
        """clean_rtc java clean case"""
        rtcprofile = self.FunctionList()
        setattr(rtcprofile, 'language', self.FunctionList())
        setattr(rtcprofile.language, 'kind', 'Java')
        mock_clean_rtc_java.return_value = 'Java test'
        self.assertEqual('Java test', self.plugin.clean_rtc(rtcprofile))

    @mock.patch('wasanbon.core.plugins.admin.builder_plugin.clean_rtc_python')
    def test_clean_rtc_python(self, mock_clean_rtc_python):
        """clean_rtc python clean case"""
        rtcprofile = self.FunctionList()
        setattr(rtcprofile, 'language', self.FunctionList())
        setattr(rtcprofile.language, 'kind', 'Python')
        mock_clean_rtc_python.return_value = 'Python test'
        self.assertEqual('Python test', self.plugin.clean_rtc(rtcprofile))


if __name__ == '__main__':
    unittest.main()
