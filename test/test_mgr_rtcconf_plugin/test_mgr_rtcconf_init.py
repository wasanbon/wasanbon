# test for wasanbon/core/plugins/mgr/rtcconf_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    class FunctionList:
        def __init__(self):
            self.dic = {}

        def __getitem__(self, key):
            return self.dic.get(key, "")

        def __setitem__(self, key, value):
            self.dic[key] = value

        def sync(self):
            pass

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.mgr.rtcconf_plugin as m
        self.admin_mock = MagicMock(spec=['package', 'rtcconf'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        self.func = m

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.mgr.rtcconf_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.package', 'admin.rtcconf'], self.plugin.depends())

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_show(self, mock_parse_args, mock_write):
        """show normal case"""
        options = self.FunctionList()
        setattr(options, 'long_flag', False)
        mock_parse_args.return_value = options, None
        package = self.FunctionList()
        setattr(package, 'get_rtcpath', lambda: 'rtcpath')
        setattr(package, 'rtcconf', {'language': 'rtcconf_path'})
        import wasanbon.core.plugins.mgr.rtcconf_plugin as rtcconf_plugin
        temp = rtcconf_plugin.rtcconf_keys
        rtcconf_plugin.rtcconf_keys = ['key']
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.rtcconf).RTCConf = MagicMock(return_value={'key': 'rtcconf'})
        self.assertEqual(0, self.plugin.show(['argv']))
        self.assertEqual(2, mock_write.call_count)
        rtcconf_plugin.rtcconf_keys = temp

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.mgr.rtcconf_plugin.rtcconf_keys', new=['key'])
    def test_show_l(self, mock_parse_args, mock_write):
        """show normal case"""
        options = self.FunctionList()
        setattr(options, 'long_flag', True)
        mock_parse_args.return_value = options, None
        package = self.FunctionList()
        setattr(package, 'get_rtcpath', lambda: 'rtcpath')
        setattr(package, 'rtcconf', {'language': 'rtcconf_path'})
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.rtcconf).RTCConf = MagicMock(return_value={'key': 'rtcconf'})
        self.assertEqual(0, self.plugin.show(['argv']))
        self.assertEqual(4, mock_write.call_count)

    @mock.patch('builtins.print')
    def test_print_alts_1(self, mock_print):
        """_print_alts normal case"""
        import copy
        temp = copy.deepcopy(self.plugin._print_keys)
        self.plugin._print_keys = MagicMock()
        self.plugin._print_alts(['1','2','3','4'])
        self.assertEqual(3, mock_print.call_count)
        self.plugin._print_keys = copy.deepcopy(temp)
        
    @mock.patch('builtins.print')
    def test_print_alts_2(self, mock_print):
        """_print_alts normal case"""
        import copy
        temp = copy.deepcopy(self.plugin._print_keys)
        self.plugin._print_keys = MagicMock()
        self.plugin._print_alts(['1','2','3','4', '5'])
        self.assertEqual(0, mock_print.call_count)
        self.assertEqual(1, self.plugin._print_keys.call_count)
        self.plugin._print_keys = copy.deepcopy(temp)
        
    @mock.patch('builtins.print')
    def test_print_alts_3(self, mock_print):
        """_print_alts normal case"""
        import copy
        temp = copy.deepcopy(self.plugin._print_keys)
        self.plugin._print_keys = MagicMock()
        self.plugin._print_alts(['1','2','3'])
        self.assertEqual(0, mock_print.call_count)
        self.assertEqual(0, self.plugin._print_keys.call_count)
        self.plugin._print_keys = copy.deepcopy(temp)
        
    @mock.patch('builtins.print')
    def test_print_keys(self, mock_print):
        """_print_keys normal case"""
        import copy
        temp = copy.deepcopy(self.func.rtcconf_keys)
        self.func.rtcconf_keys = ['1','2']
        self.plugin._print_keys(['arg'])
        self.assertEqual(2, mock_print.call_count)
        self.func.rtcconf_keys = copy.deepcopy(temp)
        
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_get(self, mock_parse_args, mock_print):
        """get normal case"""
        mock_parse_args.return_value = None, ['hoge1', 'hoge2', 'hoge3', 'lang', 'key']
        package = self.FunctionList()
        setattr(package, 'rtcconf', {'lang': 'test_lang'})
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.rtcconf).RTCConf = MagicMock(return_value={'key': 'test_key'})
        self.plugin.get(['argv'])
        mock_print.assert_called_once_with('test_key')

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_set(self, mock_parse_args, mock_print):
        """set normal case"""
        mock_parse_args.return_value = None, ['hoge1', 'hoge2', 'hoge3', 'lang', 'key', 'val']
        package = self.FunctionList()
        setattr(package, 'rtcconf', self.FunctionList())
        package.rtcconf['lang'] = 'test_lang'
        package.rtcconf['key'] = 'val'
        #setattr(package.rtcconf, 'sync', lambda: None)
        package.rtcconf.sync = MagicMock()
        type(self.admin_mock.package).get_package_from_path = MagicMock(return_value=package)
        rtcconf = MagicMock()
        type(rtcconf).key = 'test_key'
        type(rtcconf).sync = MagicMock()
        type(self.admin_mock.rtcconf).RTCConf = MagicMock(return_value=rtcconf)
        self.plugin.set(['argv'])
        self.assertEqual('val', package.rtcconf['key'])


if __name__ == '__main__':
    unittest.main()
