# test for wasanbon/core/plugins/mgr/tools_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.mgr.tools_plugin import Plugin
#import importlib


class TestPlugin(unittest.TestCase):

    class FunctionList:
        pass

    def setUp(self):
        import wasanbon
        self.admin = wasanbon.plugins._admin
        self.plugin = wasanbon.plugins._mgr.tools

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.eclipse', 'admin.package'], self.plugin.depends())

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_rtcb(self, mock_parse_args):
        """rtcb normal case"""
        options = self.FunctionList()
        setattr(options, 'verbose_flag', False)
        mock_parse_args.return_value = options, None
        package = self.FunctionList()
        setattr(package, 'get_rtcpath', lambda: 'rtcpath')
        self.admin.package.get_package_from_path = MagicMock(return_value=package)
        self.admin.eclipse.launch_eclipse = MagicMock(return_value='test')
        self.assertEqual('test', self.plugin.rtcb([]))


if __name__ == '__main__':
    unittest.main()
