# test for wasanbon/core/plugins/admin/idl_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock

import sys
sys.path.append('../../')

from wasanbon.core.plugins.admin.idl_plugin import Plugin


class TestPlugin(unittest.TestCase):

    class FunctionList:
        pass

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
        self.assertEqual(['admin.environment'], self.plugin.depends())

    def test_print_alternatives(self):
        """dart normal case"""
        self.assertEqual(None, self.plugin._print_alternatives('args'))

    # @mock.patch('wasanbon.core.plugins.admin.idl_plugin.Plugin._parser', new='test')
    def test_get_global_module(self):
        """get_global_module normal case"""
        plugin = Plugin()
        plugin._parser = self.FunctionList()
        setattr(plugin._parser, 'global_module', 'test')
        self.assertEqual('test', plugin.get_global_module())

    def test_is_primitive(self):
        """is_primitive normal case"""
        plugin = Plugin()
        plugin._parser = self.FunctionList()

        def func(name):
            return 'test'
        setattr(plugin._parser, 'is_primitive', func)
        self.assertEqual('test', plugin.is_primitive('name'))

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.parser.IDLParser')
    def test_forEachIDL_1(self, mock_parser):
        """forEachIDL normal case
        self._parser = None
        """
        plugin = Plugin()
        plugin._parser = None
        plugin = Plugin()
        parser = MagicMock(spec=['forEachIDL'])
        mock_parser.return_value = parser
        plugin.forEachIDL('func')
        mock_parser.assert_called_once()
        parser.forEachIDL.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.parser')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.parser.IDLParser')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.parser.IDLParser.forEachIDL')
    def test_forEachIDL_2(self, mock_forEachIDL, mock_IDLParser, mock_parser):
        """forEachIDL normal case
        self._parser = parser.IDLParser()
        """
        def pseudo_forEachIDL(func, idl_dirs, except_files):
            pass
        plugin = Plugin()
        plugin._parser = self.FunctionList()
        setattr(plugin._parser, 'forEachIDL', pseudo_forEachIDL)
        plugin.forEachIDL('func')
        mock_forEachIDL.assert_not_called()

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.Plugin.forEachIDL')
    def test_parse(self, mock_forEachIDL):
        """parse normal case"""
        self.plugin.parse()
        mock_forEachIDL.assert_called_once()

    # @mock.patch.object(Plugin, '_parser')
    def test_get_idl_parser(self):
        """get_odl_parser normal case"""
        plugin = Plugin()
        plugin._parser = 'test'
        self.assertEqual('test', plugin.get_idl_parser())

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.Plugin.forEachIDL')
    def test_list(self, mock_forEachIDL):
        """list normal case"""
        self.assertEqual(0, self.plugin.list([]))
        mock_forEachIDL.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.Plugin.parse')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_to_dic_1(self, mock_parse_args, mock_yaml_dump, mock_parser, mock_print):
        """to_dic normal case
        detail = True
        """
        plugin = Plugin()
        plugin._parser = MagicMock(spec=['global_module'])
        plugin._parser.global_module = MagicMock(spec=['find_types','to_dic'])
        plugin._parser.global_module.find_types.return_value = 'typs'
        options = self.FunctionList()
        setattr(options, 'verbose_flag', False)
        setattr(options, 'long_flag', False)
        setattr(options, 'detail_flag', True)
        mock_parse_args.return_value = options, []
        mock_yaml_dump.return_value = 'test_to_dic_1'
        plugin.to_dic([])
        mock_yaml_dump.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.Plugin.parse')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_to_dic_2(self, mock_parse_args, mock_yaml_dump, mock_parser, mock_print):
        """to_dic normal case
        detail = False
        """
        plugin = Plugin()
        plugin._parser = MagicMock()
        options = self.FunctionList()
        setattr(options, 'verbose_flag', False)
        setattr(options, 'long_flag', False)
        setattr(options, 'detail_flag', False)
        mock_parse_args.return_value = options, []
        mock_yaml_dump.return_value = 'test_to_dic_2'
        plugin.to_dic([])
        mock_yaml_dump.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.Plugin.parse')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.Plugin.forEachIDL')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.interface.IDLArgument.to_simple_dic')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.module.IDLModule.find_types')
    @mock.patch('wasanbon.arg_check')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_show(self, mock_parse_args, mock_arg_check, mock_find_types, mock_yaml_dump, mock_to_simple_dic, mock_parse, mock_parse_, mock_print):
        """show normal case"""        
        plugin = Plugin()
        plugin._parser = MagicMock(spec=['global_module'])
        plugin._parser.global_module = MagicMock(spec=['find_types'])
        plugin._parser.global_module.find_types.return_value = [MagicMock()]
        options = self.FunctionList()
        setattr(options, 'verbose_flag', False)
        setattr(options, 'long_flag', False)
        setattr(options, 'recursive_flag', False)
        mock_parse_args.return_value = options, ['a', 'b', 'c', 'd']
        mock_find_types.return_value = []
        mock_yaml_dump.return_value = 'test_show'
        mock_to_simple_dic.return_value = 0
        self.assertEqual(0, plugin.show([]))
        mock_yaml_dump.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.Plugin.parse')
    @mock.patch('sys.stdout.write')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.core.plugins.admin.idl_plugin.idl_parser.module.IDLModule.find_types')
    @mock.patch('wasanbon.arg_check')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_show_typs0(self, mock_parse_args, mock_arg_check, mock_find_types, mock_yaml_dump, mock_write, mock_parse):
        """show error case"""
        plugin = Plugin()
        plugin._parser = MagicMock(spec=['global_module'])
        plugin._parser.global_module = MagicMock(spec=['find_types'])
        plugin._parser.global_module.find_types.return_value = []
        options = self.FunctionList()
        setattr(options, 'verbose_flag', False)
        setattr(options, 'long_flag', False)
        setattr(options, 'recursive_flag', False)
        mock_parse_args.return_value = options, ['a', 'b', 'c', 'd']
        mock_find_types.return_value = []
        mock_yaml_dump.return_value = 'test_show'
        self.assertEqual(0, plugin.show([]))
        mock_write.assert_called_once()        
        
if __name__ == '__main__':
    unittest.main()
