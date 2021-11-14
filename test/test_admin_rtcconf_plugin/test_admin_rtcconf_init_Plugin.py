# test for wasanbon/core/plugins/admin/rtcconf_plugin/__init__.py

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
        import wasanbon.core.plugins.admin.rtcconf_plugin as m
        self.plugin = m.Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.rtcconf_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment'], self.plugin.depends())

    @mock.patch('builtins.print')
    def test_call(self, mock_print):
        """call normal case"""
        self.plugin('argv')
        mock_print.assert_any_call('# rtcconf plugin version 1.0.0')

    @mock.patch('wasanbon.core.plugins.admin.rtcconf_plugin.RTCConf')
    def test_RTCConf(self, mock_RTCConf):
        """RTCConf normal case"""
        mock_RTCConf.return_value = 'test_RTCConf'
        self.assertEqual('test_RTCConf', self.plugin.RTCConf('rtcconf'))


if __name__ == '__main__':
    unittest.main()
