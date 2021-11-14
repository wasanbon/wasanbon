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
        self.plugin = Plugin()

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
        self.assertEqual(0, self.plugin.Idlcompiler())
        mock_generate_converter.assert_called_once()


if __name__ == '__main__':
    unittest.main()
