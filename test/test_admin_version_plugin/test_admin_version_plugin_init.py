# test for wasanbon/core/plugins/admin/version_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.version_plugin import Plugin


class TestPlugin(unittest.TestCase):

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    @mock.patch('wasanbon.platform')
    @mock.patch('wasanbon.get_version')
    @mock.patch('sys.stdout.write')
    def test_call(self, sys_stdout_write, wasanbon_get_version, wasanbon_platform):
        """__call__ normal case"""
        ### setting ###
        wasanbon_platform.return_value = 'wasanbon.platform'
        wasanbon_get_version.return_value = 'wasanbon.get_version'
        sys_stdout_write.return_value = None
        ### test ###
        plugin = Plugin()
        plugin('test')
        calls = [call('platform version: %s\n' % 'wasanbon.platform'), call('wasanbon version: %s\n' % 'wasanbon.get_version')]
        sys_stdout_write.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
