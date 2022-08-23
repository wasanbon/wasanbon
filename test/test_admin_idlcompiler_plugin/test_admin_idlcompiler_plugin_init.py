# test for wasanbon/core/plugins/admin/idlcompiler_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.idlcompiler_plugin import Plugin

class TestPlugin(unittest.TestCase):

    def setUp(self):
        import wasanbon.core.plugins.admin.idlcompiler_plugin as m
        self.admin_mock = MagicMock(spec=['idl'])
        self.admin_mock.idl(spec=['parse', 'get_idl_parser'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()        

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.idl'], self.plugin.depends())

    @mock.patch('wasanbon.core.plugins.admin.idlcompiler_plugin.dart_converter.generate_converter')
    def test_dart(self, mock_generate_converter):
        """dart normal case"""
        self.assertEqual(0, self.plugin.dart([]))
        self.admin_mock.idl.parse.assert_called_once()
        self.admin_mock.idl.get_idl_parser.assert_called_once()

if __name__ == '__main__':
    unittest.main()
