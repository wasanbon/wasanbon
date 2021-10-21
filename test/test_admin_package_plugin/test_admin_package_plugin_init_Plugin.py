# test for wasanbon/core/plugins/admin/package_plugin/__init__.py

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
        ### setting mock ###
        import wasanbon.core.plugins.admin.package_plugin as m
        self.admin_mock = MagicMock(spec=['rtcconf', 'rtc', 'systemlauncher'])
        self.admin_mock.rtcconf(spec=[''])
        self.admin_mock.rtc(spec=['get_rtcs_from_package'])
        self.admin_mock.systemlauncher(spec=['is_launched'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        ### setting parse_args return option ###
        self.options = self.FunctionList()
        flags = ['verbose_flag', 'long_flag', 'running_flag', 'quiet_flag', 'remove_flag']
        for flag in flags:
            ## default: False ##
            setattr(self.options, flag, False)

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.package_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.rtcconf', 'admin.rtc', 'admin.systemlauncher'], self.plugin.depends())

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_packages')
    def test_print_packages(self, mock_get_packages, mock_print):
        """print_packages normal case"""
        ret = self.FunctionList()
        setattr(ret, 'name', 'test')
        mock_get_packages.return_value = [ret]
        self.plugin.print_packages('')
        mock_print.has_any_call('test')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.create_package')
    def test_create_package(self, mock_create_package):
        """create_packages normal case"""
        mock_create_package.return_value = 'test'
        self.assertEqual('test', self.plugin.create_package('a'))

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_packages')
    @mock.patch('builtins.sorted')
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_list_1(self, mock_parse_args, mock_print, mock_sorted, mock_get_packages):
        """list normal case
        verbose_flag = False
        quiet_flag = False
        running_flag = False
        long_flag = False
        """
        ### setting ###
        mock_parse_args.return_value = self.options, []
        p = self.FunctionList()
        setattr(p, 'name', 'test_name')
        mock_sorted.return_value = [p]
        mock_get_packages.return_value = 0
        ### test ###
        self.assertEqual(0, self.plugin.list('args'))
        mock_print.assert_any_call('test_name')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_packages')
    @mock.patch('builtins.sorted')
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_list_2(self, mock_parse_args, mock_print, mock_sorted, mock_get_packages):
        """list normal case
        verbose_flag = False
        quiet_flag = False
        running_flag = True
        long_flag = False
        """
        ### setting ###
        self.options.running_flag = True
        self.admin_mock.systemlauncher.is_launched.return_value = False
        mock_parse_args.return_value = self.options, []
        p = self.FunctionList()
        setattr(p, 'name', 'test_name')
        mock_sorted.return_value = [p]
        mock_get_packages.return_value = 0
        ### test ###
        self.assertEqual(0, self.plugin.list('args'))
        mock_print.assert_not_called()

    @mock.patch('os.path.basename')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_packages')
    @mock.patch('builtins.sorted')
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_list_3(self, mock_parse_args, mock_print, mock_sorted, mock_get_packages, mock_basename):
        """list normal case
        verbose_flag = False
        quiet_flag = False
        running_flag = False
        long_flag = True
        """
        ### setting ###
        self.options.long_flag = True
        mock_parse_args.return_value = self.options, []
        p = self.FunctionList()
        setattr(p, 'name', 'test_name')
        setattr(p, 'description', 'test_description')
        setattr(p, 'path', 'test_path')
        setattr(p, 'get_rtcpath', lambda fullpath: 'test_rtcpath')
        setattr(p, 'get_confpath', lambda fullpath: 'test_confpath')
        setattr(p, 'get_binpath', lambda fullpath: 'test_binpath')
        setattr(p, 'get_systempath', lambda fullpath: 'test_systempath')
        setattr(p, 'setting', self.FunctionList())
        setattr(p.setting, 'get', lambda a, b: 'test_nameserver')
        setattr(p, 'rtcconf', {'C++': 'test_C++', 'Python': 'test_Python', 'Java': 'test_Java'})
        setattr(p, 'default_system_filepath', 'test_default_system')
        mock_sorted.return_value = [p]
        mock_get_packages.return_value = 0
        r = self.FunctionList()
        setattr(r, 'rtcprofile', self.FunctionList())
        setattr(r.rtcprofile, 'basicInfo', self.FunctionList())
        setattr(r.rtcprofile.basicInfo, 'name', 'rtc_name')
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [r]
        self.admin_mock.systemlauncher.is_launched.return_value = 'run'
        mock_basename.side_effect = ['C++', 'Python', 'Java']
        ### test ###
        self.assertEqual(0, self.plugin.list('args'))
        self.assertEqual(17, mock_print.call_count)

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_packages')
    def test_directory(self, mock_get_packages, mock_print):
        """directory normal case"""
        ### setting ###
        p1 = self.FunctionList()
        p2 = self.FunctionList()
        setattr(p1, 'name', 'test1')
        setattr(p1, 'path', 'test1_path')
        setattr(p2, 'name', 'test2')
        mock_get_packages.return_value = [p1, p2]
        ### test ###
        self.assertEqual(0, self.plugin.directory(['a', 'b', 'c', 'test1']))
        mock_print.assert_any_call('test1_path')

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.create_package')
    def test_create(self, mock_create_package, mock_write):
        """create normal case"""
        mock_create_package.return_value = 'test'
        self.assertEqual('test', self.plugin.create(['a', 'b', 'c', 'd']))

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.register_package')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.PackageObject')
    @mock.patch('os.path.join')
    @mock.patch('os.path.isfile')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.isabs')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_register_1(self, mock_parse_args, mock_isabs, mock_isdir, mock_isfile, mock_join, mock_PackageObject, mock_register_package, mock_write):
        """register normal case"""
        ### setting ###
        mock_parse_args.return_value = self.options, ['a', 'b', 'c', 'd']
        mock_isabs.return_value = True
        mock_isdir.return_value = True
        mock_join.return_value = 'setting_file_path'
        mock_isfile.return_value = True
        p = self.FunctionList()
        setattr(p, 'name', 'test_name')
        setattr(p, 'path', 'test_path')
        mock_PackageObject.return_value = p
        ### test ###
        self.assertEqual(0, self.plugin.register([]))
        mock_register_package.assert_any_call('test_name', 'test_path')

    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.normpath')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.register_package')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.PackageObject')
    @mock.patch('os.path.join')
    @mock.patch('os.path.isfile')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.isabs')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_register_2(self, mock_parse_args, mock_isabs, mock_isdir, mock_isfile, mock_join, mock_PackageObject, mock_register_package, mock_normpath, mock_write):
        """register normal case 2"""
        ### setting ###
        mock_parse_args.return_value = self.options, ['a', 'b', 'c', 'd']
        mock_isabs.return_value = False
        mock_normpath.return_value = 'test_normpath'
        mock_isdir.return_value = True
        mock_join.return_value = 'setting_file_path'
        mock_isfile.return_value = True
        p = self.FunctionList()
        setattr(p, 'name', 'test_name')
        setattr(p, 'path', 'test_path')
        mock_PackageObject.return_value = p
        ### test ###
        self.assertEqual(0, self.plugin.register([]))
        mock_register_package.assert_any_call('test_name', 'test_path')
        mock_normpath.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.isabs')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_register_error_1(self, mock_parse_args, mock_isabs, mock_isdir, mock_write):
        """register error case 1"""
        ### setting ###
        mock_parse_args.return_value = self.options, ['a', 'b', 'c', 'd']
        mock_isabs.return_value = True
        mock_isdir.return_value = False
        ### test ###
        self.assertEqual(-1, self.plugin.register([]))
        mock_write.assert_any_call('# Can not find d.\n')

    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.join')
    @mock.patch('os.path.isfile')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.isabs')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_register_error_2(self, mock_parse_args, mock_isabs, mock_isdir, mock_isfile, mock_join, mock_write):
        """register error case 2"""
        ### setting###
        mock_parse_args.return_value = self.options, ['a', 'b', 'c', 'd']
        mock_isabs.return_value = True
        mock_isdir.return_value = True
        join_ret_value = 'setting_file_path'
        mock_join.return_value = join_ret_value
        mock_isfile.return_value = False
        ### test ###
        self.assertEqual(-1, self.plugin.register([]))
        mock_write.assert_any_call('# Setting file %s can not be found.\n' % join_ret_value)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.delete_package')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_delete(self, mock_parse_args, mock_delete_package, mock_write):
        """delete normal case"""
        mock_parse_args.return_value = self.options, ['a', 'b', 'c', 'd']
        mock_delete_package.return_value = 0
        self.assertEqual(0, self.plugin.delete('args'))

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.package_plugin.delete_package')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_delete_1(self, mock_parse_args, mock_delete_package, mock_write):
        """delete normal case"""
        mock_parse_args.return_value = self.options, ['a', 'b', 'c', 'd']
        mock_delete_package.return_value = 2
        self.assertEqual(1, self.plugin.delete('args'))

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.delete_package')
    def test_delete_package(self, mock_delete_package):
        """delete_package normal case"""
        mock_delete_package.return_value = 'test'
        self.assertEqual('test', self.plugin.delete_package('package_name'))

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_package_from_path')
    def test_get_package_from_path(self, mock_get_package_from_path):
        """get_package_from_path normal case"""
        mock_get_package_from_path.return_value = 'test'
        self.assertEqual('test', self.plugin.get_package_from_path('path'))

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_packages')
    def test_get_packages(self, mock_get_packages):
        """get_packages normal case"""
        mock_get_packages.return_value = 'test'
        self.assertEqual('test', self.plugin.get_packages())

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_package')
    def test_get_package(self, mock_get_package):
        """get_package normal case"""
        mock_get_package.return_value = 'test'
        self.assertEqual('test', self.plugin.get_package('name'))

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.validate_package')
    def test_validate_package(self, mock_validate_package):
        """validate_package normal case"""
        mock_validate_package.return_value = 'test'
        self.assertEqual('test', self.plugin.validate_package('package'))


if __name__ == '__main__':
    unittest.main()
