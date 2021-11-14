# test for wasanbon/core/plugins/__init__.py

import unittest
from unittest import mock
from unittest.mock import call, Mock

import os
from optparse import OptionParser

from wasanbon.core import plugins


class TestPlugin(unittest.TestCase):

    def test_manifest(self):
        """test for manifest"""
        test_func = Mock()
        # test
        ret = plugins.manifest(test_func)
        arg_mock = Mock(spec=['parser'])
        ret(arg_mock, kwds1='test2')
        test_func.assert_called_once()
        self.assertIsInstance(arg_mock.parser, OptionParser)

    def test_PluginFunction__init__(self):
        """test for PluginFunction.__init__"""
        # test
        inst = plugins.PluginFunction()
        self.assertEqual(inst._default_property_list,
                         ['admin', 'mgr', 'parser'])
        self.assertIsInstance(inst.admin, plugins.FunctionList)
        self.assertIsInstance(inst.mgr, plugins.FunctionList)
        self.assertIsInstance(inst.parser, OptionParser)
        self.assertTrue(inst.parser.has_option('--verbose'))
        self.assertTrue(inst.parser.has_option('-a'))

    def test_PluginFunction_depends(self):
        """test for PluginFunction.depends"""
        inst = plugins.PluginFunction()
        # test
        self.assertEqual(inst.depends(), [])

    @mock.patch('builtins.print')
    def test_PluginFunction_parse_args(self, print_mock):
        """test for PluginFunction.parse_args"""
        from wasanbon import PrintAlternativeException
        inst = plugins.PluginFunction()
        # test (alt_flag, print_alt_func=None)
        test_arg = ['-a']
        with self.assertRaises(PrintAlternativeException):
            inst.parse_args(test_arg)
        print_mock.assert_has_calls = [call(' ')]
        # test (alt_flag, print_alt_func!=None)
        test_arg = ['-a']
        test_func = Mock()
        with self.assertRaises(PrintAlternativeException):
            inst.parse_args(test_arg, test_func)
        test_func.assert_called_once_with(test_arg)
        # test (no alt_flag)
        test_arg = ['-v']
        ret_opt, ret_argv = inst.parse_args(test_arg)
        self.assertTrue(ret_opt.verbose_flag)
        self.assertEqual(ret_argv, [])

    def test_PluginFunction_get_manifest_functions(self):
        """test for PluginFunction.get_manifest_functions"""
        inst = plugins.PluginFunction()
        ret = inst.get_manifest_functions(nocall=True)
        self.assertEqual(ret, {})

    def test_PluginFunction_get_manifest_function_names(self):
        """test for PluginFunction.get_manifest_function_names"""
        inst = plugins.PluginFunction()
        ret = inst.get_manifest_function_names(nocall=True)
        self.assertEqual(ret, [])

    def test_PluginFunction_is_manifest_plugin(self):
        """test for PluginFunction.is_manifest_plugin"""
        inst = plugins.PluginFunction()
        ret = inst.is_manifest_plugin()
        self.assertFalse(ret)

    def test_PluginFunction_get_functions(self):
        """test for PluginFunction.get_functions"""
        inst = plugins.PluginFunction()
        ret = inst.get_functions()
        expected_ret = {
            'depends': inst.depends,
            'parse_args': inst.parse_args,
            'get_manifest_functions': inst.get_manifest_functions,
            'get_manifest_function_names': inst.get_manifest_function_names,
            'is_manifest_plugin': inst.is_manifest_plugin,
            'get_functions': inst.get_functions,
            'get_properties': inst.get_properties,
            'get_function_names': inst.get_function_names,
        }
        self.assertEqual(ret, expected_ret)

    def test_PluginFunction_get_properties(self):
        """test for PluginFunction.get_properties"""
        inst = plugins.PluginFunction()
        ret = inst.get_properties()
        self.assertEqual(ret, {})

    @mock.patch('wasanbon.core.plugins.Loader.load_plugin')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.listdir')
    def test_Loader__init__(self, listdir_mock, sys_stdout_write, load_plugin_mock):
        """test for Loader.__init__"""
        # mock settings
        listdir_mock.side_effect = [['admin'], ['test_plugin'], []]
        # test
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        self.assertIsInstance(inst._admin, plugins.FunctionList)
        self.assertIsInstance(inst._mgr, plugins.FunctionList)
        self.assertEqual(
            inst._package, {'admin': inst._admin, 'mgr': inst._mgr})
        self.assertEqual(inst._directories, test_dirs)
        sys_calls = [
            call('# Plugin: %s Found.\n' % 'test'),
            call('# Loading %s plugin\n' % 'admin.test'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        load_plugin_mock.assert_called_once()

    @mock.patch('os.listdir')
    def test_Loader_get_plugin_names(self, listdir_mock):
        """test for Loader.get_plugin_names"""
        # test
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        ret = inst.get_plugin_names('admin')
        self.assertEqual(ret, [])

    @mock.patch('os.listdir')
    def test_Loader_get_manifest_plugin_names(self, listdir_mock):
        """test for Loader.get_manifest_plugin_names"""
        # test
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        ret = inst.get_manifest_plugin_names('admin')
        self.assertEqual(ret, [])

    @mock.patch('os.listdir')
    def test_Loader_get_plugins(self, listdir_mock):
        """test for Loader.get_plugins"""
        # test
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        ret = inst.get_plugins('admin')
        self.assertEqual(ret, [])

    @mock.patch('os.listdir')
    def test_Loader_get_plugin(self, listdir_mock):
        """test for Loader.get_plugin"""
        # test
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        inst._admin.test = 'test'
        ret = inst.get_plugin('admin', 'test')
        self.assertIs(ret, 'test')

    @mock.patch('sys.stdout.write')
    @mock.patch('os.listdir')
    def test_Loader_list_package_plugins(self, listdir_mock, sys_stdout_write):
        """test for Loader.list_package_plugins"""
        # mock settings
        listdir_mock.return_value = ['test_plugin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # test
        test_package = 'test_package'
        test_dir = 'test_dir'
        inst.list_package_plugins(test_package, test_dir, verbose=True)
        self.assertEqual(inst._plugin_list, {'{}.test'.format(
            test_package): os.path.join(test_dir, test_package, 'test_plugin')})
        sys_calls = [
            call('# Plugin: %s Found.\n' % 'test'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('wasanbon.core.plugins.Loader.list_package_plugins')
    @mock.patch('os.listdir')
    def test_Loader_list_plugins(self, listdir_mock, list_package_plugins_mock):
        """test for Loader.list_plugins"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # test
        test_dir = 'test_dir'
        inst.list_plugins(test_dir, verbose=True)
        list_package_plugins_mock.assert_has_calls(
            [call('admin', test_dir, verbose=True)])

    @mock.patch('sys.stdout.write')
    @mock.patch('os.listdir')
    def test_Loader_load_plugin_admin_mod_not_none(self, listdir_mock, sys_stdout_write):
        """test for Loader.load_plugin name startwith admin, mod is not None"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        inst._admin.func1 = 'test_func1'
        # test
        test_name = 'admin.func1'
        test_dir = 'test_dir'
        ret = inst.load_plugin(test_name, test_dir, verbose=True)
        self.assertEqual(ret, 'test_func1')
        sys_calls = [
            call('# Loading (%s) in %s\n' % (test_name, test_dir)),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('os.listdir')
    @mock.patch('importlib.util.find_spec')
    @mock.patch('importlib.util.module_from_spec')
    def test_Loader_load_plugin_not_admin_mod_admin1(self, load_module_mock, find_module_mock, listdir_mock, sys_stdout_write):
        """test for Loader.load_plugin name not startwith admin, mod is None, plugin is admin(already loaded)"""
        # mock settings
        mod_spec = Mock()
        find_module_mock.return_value = mod_spec
        test_plugin_depend = 'admin.test_plugin_depends'
        test_plugin = Mock()
        test_plugin.depends.return_value = test_plugin_depend
        test_module = Mock(spec=['Plugin'])
        test_module.Plugin.return_value = test_plugin
        load_module_mock.return_value = test_module
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        inst._plugin_list[test_plugin_depend] = None
        exec('inst._admin.{} = "{}"'.format(
            test_plugin_depend[6:], test_plugin_depend))
        # test
        test_name = 'admin.func1'
        test_dir = 'test_dir'
        ret = inst.load_plugin(test_name, test_dir, verbose=True)
        self.assertEqual(ret, test_plugin)
        sys_calls = [
            call('# Loading (%s) in %s\n' % (test_name, test_dir)),
            call('# Plugin (%s) depends on %s.\n' %
                 (test_name, test_plugin_depend)),
            call('# Plugin %s is already loaded.\n'),
            call('# Loaded (%s) \n' % test_name)
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('traceback.print_exc')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.listdir')
    @mock.patch('importlib.util.find_spec')
    @mock.patch('importlib.util.module_from_spec')
    def test_Loader_load_plugin_mod_admin2(self, load_module_mock, find_module_mock, listdir_mock, sys_stdout_write, print_exc_mock):
        """test for Loader.load_plugin mod isnot  None, plugin is admin(not yet loaded)"""
        # mock settings
        mod_spec = Mock()
        find_module_mock.side_effect = (
            mod_spec, Exception('test'))
        test_plugin_depend = 'admin.test_plugin_depends'
        test_plugin = Mock()
        test_plugin.depends.return_value = test_plugin_depend
        test_module = Mock(spec=['Plugin'])
        test_module.Plugin.return_value = test_plugin
        load_module_mock.return_value = test_module
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        inst._plugin_list[test_plugin_depend] = 'test_dir'
        # test
        test_name = 'admin.func1'
        test_dir = 'test_dir'
        ret = inst.load_plugin(test_name, test_dir, verbose=True)
        self.assertEqual(ret, test_plugin)
        sys_calls = [
            call('# Loading (%s) in %s\n' % (test_name, test_dir)),
            call('# Plugin (%s) depends on %s.\n' %
                 (test_name, test_plugin_depend)),
            call('# Plugin %s is not loaded yet.\n' % test_plugin_depend),
            call('# Loading Plugin (%s) Failed.\n' % test_plugin_depend),
            call('# Loaded (%s) \n' % test_name)
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        self.assertEqual(1, print_exc_mock.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('os.listdir')
    @mock.patch('importlib.util.find_spec')
    @mock.patch('importlib.util.module_from_spec')
    def test_Loader_load_plugin_mod_mgr1(self, load_module_mock, find_module_mock, listdir_mock, sys_stdout_write):
        """test for Loader.load_plugin name mod is not None, plugin is mgr(already loaded)"""
        # mock settings
        mod_spec = Mock()
        find_module_mock.return_value = mod_spec
        test_plugin_depend = 'mgr.test_plugin_depends'
        test_plugin = Mock()
        test_plugin.depends.return_value = test_plugin_depend
        test_module = Mock(spec=['Plugin'])
        test_module.Plugin.return_value = test_plugin
        load_module_mock.return_value = test_module
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        inst._plugin_list[test_plugin_depend] = None
        exec('inst._mgr.{} = "{}"'.format(
            test_plugin_depend[4:], test_plugin_depend))
        # test
        test_name = 'mgr.func1'
        test_dir = 'test_dir'
        ret = inst.load_plugin(test_name, test_dir, verbose=True)
        self.assertEqual(ret, test_plugin)
        sys_calls = [
            call('# Loading (%s) in %s\n' % (test_name, test_dir)),
            call('# Plugin (%s) depends on %s.\n' %
                 (test_name, test_plugin_depend)),
            call('# Plugin %s is already loaded.\n'),
            call('# Loaded (%s) \n' % test_name)
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('traceback.print_exc')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.listdir')
    @mock.patch('importlib.util.find_spec')
    @mock.patch('importlib.util.module_from_spec')
    def test_Loader_load_plugin_mod_mgr2(self, load_module_mock, find_module_mock, listdir_mock, sys_stdout_write, print_exc_mock):
        """test for Loader.load_plugin mod is not None, plugin is mgr(not yet loaded)"""
        # mock settings
        mod_spec = Mock()
        find_module_mock.side_effect = (
            mod_spec, Exception('test'))
        test_plugin_depend = 'mgr.test_plugin_depends'
        test_plugin = Mock()
        test_plugin.depends.return_value = test_plugin_depend
        test_module = Mock(spec=['Plugin'])
        test_module.Plugin.return_value = test_plugin
        load_module_mock.return_value = test_module
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        inst._plugin_list[test_plugin_depend] = 'test_dir'
        # test
        test_name = 'mgr.func1'
        test_dir = 'test_dir'
        ret = inst.load_plugin(test_name, test_dir, verbose=True)
        self.assertEqual(ret, test_plugin)
        sys_calls = [
            call('# Loading (%s) in %s\n' % (test_name, test_dir)),
            call('# Plugin (%s) depends on %s.\n' %
                 (test_name, test_plugin_depend)),
            call('# Plugin %s is not loaded yet.\n' % test_plugin_depend),
            call('# Loading Plugin (%s) Failed.\n' % test_plugin_depend),
            call('# Loaded (%s) \n' % test_name)
        ]
        sys_stdout_write.assert_has_calls(sys_calls)
        self.assertEqual(1, print_exc_mock.call_count)

    @mock.patch('builtins.print')
    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.Loader.get_manifest_plugin_names')
    def test_Loader_print_alternative_long_args(self, get_manifest_mock, listdir_mock, sys_stdout_write):
        """test for Loader.print_alternative length of args > 3"""
        # mock settings
        get_manifest_mock.return_value = ['test1']
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        test_args = ['a', 'b', 'api']
        inst.print_alternative(test_package, test_args)
        sys_calls = [
            call(get_manifest_mock.return_value[0], end=' '),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('builtins.print')
    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.Loader.get_manifest_plugin_names')
    def test_Loader_print_alternative_short_args(self, get_manifest_mock, listdir_mock, sys_stdout_write):
        """test for Loader.print_alternative length of args < 3"""
        # mock settings
        get_manifest_mock.return_value = ['test1']
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        test_args = ['a', 'api']
        inst.print_alternative(test_package, test_args)
        sys_calls = [
            call('list api'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.Loader.print_alternative')
    def test_Loader_run_command_a(self, print_alternative_mock, listdir_mock):
        """test for Loader.run_command -a in args"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        test_args = ['-a', 'api']
        ret = inst.run_command(test_package, '', test_args)
        self.assertEqual(ret, 0)
        print_alternative_mock.assert_called_once_with(
            test_package, [test_args[1]])

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.Loader.print_help')
    @mock.patch('wasanbon.core.plugins.Loader.print_alternative')
    def test_Loader_run_command_h(self, print_alternative_mock, print_help_mock, listdir_mock):
        """test for Loader.run_command -h in args"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        test_args = ['-h', 'api']
        ret = inst.run_command(test_package, '', test_args)
        self.assertEqual(ret, 0)
        print_alternative_mock.assert_not_called()
        print_help_mock.assert_called_once_with(test_package)

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.Loader.print_help')
    @mock.patch('wasanbon.core.plugins.Loader.print_alternative')
    def test_Loader_run_command_short_args(self, print_alternative_mock, print_help_mock, listdir_mock):
        """test for Loader.run_command short args"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        test_args = ['api']
        ret = inst.run_command(test_package, '', test_args)
        self.assertEqual(ret, -1)
        print_alternative_mock.assert_not_called()
        print_help_mock.assert_called_once_with(test_package)

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.Loader.print_list_plugins')
    @mock.patch('wasanbon.core.plugins.Loader.print_help')
    @mock.patch('wasanbon.core.plugins.Loader.print_alternative')
    def test_Loader_run_command_args_list(self, print_alternative_mock, print_help_mock, print_list_mock, listdir_mock):
        """test for Loader.run_command list in args"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        test_args = ['a', 'b', 'list']
        ret = inst.run_command(test_package, '', test_args)
        self.assertEqual(ret, 0)
        print_alternative_mock.assert_not_called()
        print_help_mock.assert_not_called()
        print_list_mock.assert_called_once_with(test_package, False)

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.Loader.print_list_plugins')
    @mock.patch('wasanbon.core.plugins.Loader.print_help')
    @mock.patch('wasanbon.core.plugins.Loader.print_alternative')
    def test_Loader_run_command_args_api_short(self, print_alternative_mock, print_help_mock, print_list_mock, listdir_mock):
        """test for Loader.run_command api in args, short"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        test_args = ['a', '-l', 'api']
        ret = inst.run_command(test_package, '', test_args)
        self.assertEqual(ret, -1)
        print_alternative_mock.assert_not_called()
        print_help_mock.assert_called_once_with(test_package)
        print_list_mock.assert_not_called()

    @mock.patch('os.listdir')
    @mock.patch('wasanbon.core.plugins.Loader.show_api')
    @mock.patch('wasanbon.core.plugins.Loader.print_list_plugins')
    @mock.patch('wasanbon.core.plugins.Loader.print_help')
    @mock.patch('wasanbon.core.plugins.Loader.print_alternative')
    def test_Loader_run_command_args_api(self, print_alternative_mock, print_help_mock, print_list_mock, show_api_mock, listdir_mock):
        """test for Loader.run_command api in args"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        test_args = ['a', 'b', 'api', 'd', '-l']
        ret = inst.run_command(test_package, '', test_args)
        self.assertEqual(ret, None)
        print_alternative_mock.assert_not_called()
        print_help_mock.assert_not_called()
        print_list_mock.assert_not_called()
        show_api_mock.assert_called_once_with(test_package, test_args[3], True)

    @mock.patch('os.listdir')
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.Loader.get_manifest_plugin_names')
    @mock.patch('wasanbon.core.plugins.Loader.get_plugin')
    def test_Loader_print_list_plugins_doc1(self, get_plugin_mock, get_manifest_mock, print_mock, listdir_mock):
        """test for Loader.print_list_plugins doc in plugin and is not None"""
        # mock settings
        test_manifests = ['test1']
        plugin_mock = Mock(spec=['__path__', '__doc__'])
        test_path = 'test_path'
        test_doc = 'test_doc'
        plugin_mock.__path__ = [test_path]
        plugin_mock.__doc__ = test_doc
        get_plugin_mock.return_value = plugin_mock
        get_manifest_mock.return_value = test_manifests
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        inst.print_list_plugins(test_package, True)
        get_manifest_mock.assert_called_once_with(test_package)
        print_calls = [
            call(' - %s:' % test_manifests[0]),
            call('  path : ', test_path),
            call('  doc : |'),
            call('   ', test_doc),
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('os.listdir')
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.Loader.get_manifest_plugin_names')
    @mock.patch('wasanbon.core.plugins.Loader.get_plugin')
    def test_Loader_print_list_plugins_doc2(self, get_plugin_mock, get_manifest_mock, print_mock, listdir_mock):
        """test for Loader.print_list_plugins doc in plugin and is None"""
        # mock settings
        test_manifests = ['test1']
        plugin_mock = Mock(spec=['__path__', '__doc__'])
        test_path = 'test_path'
        test_doc = None
        plugin_mock.__path__ = [test_path]
        plugin_mock.__doc__ = test_doc
        get_plugin_mock.return_value = plugin_mock
        get_manifest_mock.return_value = test_manifests
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        inst.print_list_plugins(test_package, True)
        get_manifest_mock.assert_called_once_with(test_package)
        print_calls = [
            call(' - %s:' % test_manifests[0]),
            call('  path : ', test_path),
            call('  doc : |'),
            call('   (No Help)'),
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('os.listdir')
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.Loader.get_manifest_plugin_names')
    @mock.patch('wasanbon.core.plugins.Loader.get_plugin')
    def test_Loader_print_list_plugins_no_doc(self, get_plugin_mock, get_manifest_mock, print_mock, listdir_mock):
        """test for Loader.print_list_plugins no doc in plugin"""
        # mock settings
        test_manifests = ['test1']
        plugin_mock = Mock(spec=['__path__'])
        test_path = 'test_path'
        plugin_mock.__path__ = [test_path]
        get_plugin_mock.return_value = plugin_mock
        get_manifest_mock.return_value = test_manifests
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package'
        inst.print_list_plugins(test_package, True)
        get_manifest_mock.assert_called_once_with(test_package)
        print_calls = [
            call(' - %s:' % test_manifests[0]),
            call('  path : ', test_path),
            call('  doc : |'),
            call('   (No Help)'),
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('os.listdir')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.Loader.print_help')
    @mock.patch('wasanbon.core.plugins.Loader.get_plugin_names')
    @mock.patch('wasanbon.core.plugins.Loader.get_plugin')
    def test_Loader_show_api_with_doc(self, get_plugin_mock, get_plugin_names_mock, print_help_mock, print_mock, listdir_mock):
        """test for Loader.show_api doc is not None"""
        # mock settings
        test_plugins = ['test1']
        get_plugin_names_mock.return_value = test_plugins
        plugin_path = 'test_path'
        plugin_doc = 'test_doc'
        plugin_prop_name = 'prop1'
        plugin_mock = Mock(spec=['__path__', 'get_properties', '__class__',
                                 '__doc__', plugin_prop_name, 'get_manifest_functions'])
        plugin_props = {plugin_prop_name: None}
        plugin_mock.__path__ = [plugin_path]
        plugin_mock.get_properties.return_value = plugin_props
        plugin_mock.get_manifest_functions.return_value = plugin_props
        plugin_mock.__class__ = plugin_mock
        plugin_mock.prop1 = plugin_mock
        plugin_mock.__doc__ = plugin_doc
        get_plugin_mock.return_value = plugin_mock
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package1'
        test_pluginname = 'test1'
        inst.show_api(test_package, test_pluginname)
        print_help_mock.assert_not_called()
        print_calls = [
            call('%s :\n' % test_pluginname),
            call('  path : %s\n' % plugin_path),
            call('  properties : \n'),
            call('    %s : |\n' % plugin_prop_name),
            call('      %s\n' % plugin_doc),
            call('  methods :\n'),
            call('    %s : |\n' % plugin_prop_name),
            call('      %s\n' % plugin_doc),
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('os.listdir')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.Loader.print_help')
    @mock.patch('wasanbon.core.plugins.Loader.get_plugin_names')
    @mock.patch('wasanbon.core.plugins.Loader.get_plugin')
    def test_Loader_show_api_without_doc(self, get_plugin_mock, get_plugin_names_mock, print_help_mock, print_mock, listdir_mock):
        """test for Loader.show_api doc is None"""
        # mock settings
        test_plugins = ['test1']
        get_plugin_names_mock.return_value = test_plugins
        plugin_path = 'test_path'
        plugin_doc = 'test_doc'
        plugin_prop_name = 'prop1'
        plugin_mock = Mock(
            spec=['__path__', 'get_properties', '__class__', 'get_manifest_functions'])
        plugin_props = {plugin_prop_name: None}
        plugin_mock.__path__ = [plugin_path]
        plugin_mock.get_properties.return_value = plugin_props
        plugin_mock.get_manifest_functions.return_value = plugin_props
        plugin_mock.__class__ = plugin_mock
        get_plugin_mock.return_value = plugin_mock
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package1'
        test_pluginname = 'test1'
        inst.show_api(test_package, test_pluginname)
        print_help_mock.assert_not_called()
        print_calls = [
            call('%s :\n' % test_pluginname),
            call('  path : %s\n' % plugin_path),
            call('  properties : \n'),
            call('    %s : |\n' % plugin_prop_name),
            call('  methods :\n'),
            call('    %s : |\n' % plugin_prop_name),
            call('      No doc.\n'),
        ]
        print_mock.assert_has_calls(print_calls)

    @mock.patch('os.listdir')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.Loader.print_help')
    @mock.patch('wasanbon.core.plugins.Loader.get_plugin_names')
    @mock.patch('wasanbon.core.plugins.Loader.get_plugin')
    def test_Loader_show_api_no_plugin(self, get_plugin_mock, get_plugin_names_mock, print_help_mock, print_mock, listdir_mock):
        """test for Loader.show_api plugin_name is not in plugins"""
        # mock settings
        test_plugins = []
        get_plugin_names_mock.return_value = test_plugins
        plugin_path = 'test_path'
        plugin_doc = 'test_doc'
        plugin_prop_name = 'prop1'
        plugin_mock = Mock(
            spec=['__path__', 'get_properties', '__class__', 'get_manifest_functions'])
        plugin_props = {plugin_prop_name: None}
        plugin_mock.__path__ = [plugin_path]
        plugin_mock.get_properties.return_value = plugin_props
        plugin_mock.get_manifest_functions.return_value = plugin_props
        plugin_mock.__class__ = plugin_mock
        get_plugin_mock.return_value = plugin_mock
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'package1'
        test_pluginname = 'test1'
        inst.show_api(test_package, test_pluginname)
        print_help_mock.assert_called_once_with(test_package)
        print_mock.assert_not_called()

    @mock.patch('os.listdir')
    @mock.patch('builtins.print')
    def test_Loader_print_help_admin(self, print_mock, listdir_mock):
        """test for Loader.print_help admin"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'admin'
        inst.print_help(test_package)
        self.assertTrue(test_package in print_mock.call_args[0][0])

    @mock.patch('os.listdir')
    @mock.patch('builtins.print')
    def test_Loader_print_help_mgr(self, print_mock, listdir_mock):
        """test for Loader.print_help mgr"""
        # mock settings
        listdir_mock.return_value = ['admin']
        test_dirs = ['d1']
        inst = plugins.Loader(test_dirs, True)
        # tests
        test_package = 'mgr'
        inst.print_help(test_package)
        self.assertTrue(test_package in print_mock.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
