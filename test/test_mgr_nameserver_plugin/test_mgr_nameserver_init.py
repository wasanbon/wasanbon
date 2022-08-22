# test for wasanbon/core/plugins/mgr/nameserver_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    def setUp(self):
        import wasanbon.core.plugins.mgr.nameserver_plugin as m
        self.admin_mock = MagicMock(spec=['nameserver', 'package'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        self.func = m

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.mgr.nameserver_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.nameserver', 'admin.package'], self.plugin.depends())

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_list(self, mock_parse_args, mock_write):
        """list normal case"""
        options = MagicMock()
        setattr(options, 'verbose_flag', False)
        mock_parse_args.return_value = options, None
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value='package')
        ns = MagicMock()
        setattr(ns, 'path', 'path')
        type(self.admin_mock.nameserver).get_nameservers_from_package = MagicMock(return_value=[ns, ns])
        self.assertEqual(0, self.plugin.list(['argv']))
        mock_write.assert_has_calls([call(' - path\n'), call(' - path\n')])

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_is_running(self, mock_parse_args, mock_write):
        """is_running normal case
        verbose = False
        name server is running(ret = True)
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', False)
        mock_parse_args.return_value = options, None
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value='package')
        ns = MagicMock()
        setattr(ns, 'path', 'test_path')
        type(self.admin_mock.nameserver).get_nameservers_from_package = MagicMock(return_value=[ns])
        type(self.admin_mock.nameserver).is_running = MagicMock(return_value=True)
        self.assertEqual(0, self.plugin.is_running(['argv']))
        mock_write.assert_has_calls([call('## Name Server (test_path) is running.\n')])

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_is_running_v(self, mock_parse_args, mock_write):
        """is_running normal case
        verbose = True
        name server is running(ret = False)
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        mock_parse_args.return_value = options, None
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value='package')
        ns = MagicMock()
        setattr(ns, 'path', 'test_path')
        type(self.admin_mock.nameserver).get_nameservers_from_package = MagicMock(return_value=[ns])
        type(self.admin_mock.nameserver).is_running = MagicMock(return_value=False)
        self.assertEqual(-1, self.plugin.is_running(['argv']))
        mock_write.assert_has_calls([call('# Checking NameServer test_path\n'), call('## Name Server (test_path) is not running.\n')])

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_terminate(self, mock_parse_args):
        """terminate normal case
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        setattr(options, 'force_flag', False)
        mock_parse_args.return_value = options, None
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value='package')
        ns = MagicMock()
        setattr(ns, 'path', 'test_path')
        type(self.admin_mock.nameserver).get_nameservers_from_package = MagicMock(return_value=[ns, ns, ns])
        type(self.admin_mock.nameserver).terminate = MagicMock(side_effect=[-1, -2, 0])
        self.assertEqual(-2, self.plugin.terminate(['argv']))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_launch(self, mock_parse_args):
        """launch normal case
        """
        options = MagicMock()
        setattr(options, 'verbose_flag', True)
        setattr(options, 'force_flag', False)
        mock_parse_args.return_value = options, None
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value='package')
        ns = MagicMock()
        setattr(ns, 'path', 'test_path')
        type(self.admin_mock.nameserver).get_nameservers_from_package = MagicMock(return_value=[ns, ns, ns])
        type(self.admin_mock.nameserver).terminate = MagicMock(side_effect=[-1, -2, 0])
        self.assertEqual(-2, self.plugin.terminate(['argv']))


if __name__ == '__main__':
    unittest.main()
