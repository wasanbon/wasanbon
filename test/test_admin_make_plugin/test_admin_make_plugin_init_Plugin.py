# test for wasanbon/core/plugins/admin/make_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')


class TestPlugin(unittest.TestCase):

    class FunctionList:
        pass

    def setUp(self):
        ### setting mock ###
        import wasanbon.core.plugins.admin.make_plugin as m
        self.admin_mock = MagicMock(spec=['package', 'rtc', 'builder', 'systeminstaller'])
        self.admin_mock.package(spec=['get_package', 'get_packages'])
        self.admin_mock.rtc(spec=['get_rtcs_from_package'])
        self.admin_mock.builder(spec=['build_rtc', 'clean_rtc'])
        self.admin_mock.systeminstaller(spec=['install_rtc_in_package'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        ### setting parse_args return option ###
        self.options = self.FunctionList()
        flags = ['verbose_flag', 'only_flag', 'standalone_flag', 'clean_flag']
        for flag in flags:
            ## default: False ##
            setattr(self.options, flag, False)

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.make_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.package', 'admin.rtc', 'admin.builder', 'admin.systeminstaller'], self.plugin.depends())

    @mock.patch('builtins.print')
    def test_print_alternatives(self, mock_print):
        """_print_alternatives normal case"""
        p = MagicMock()
        type(p).name = 'test'
        self.admin_mock.package.get_packages.return_value = [p, p]
        self.plugin._print_alternatives('args')
        mock_print.assert_has_calls([call('test'), call('test')])

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.make_plugin.isparent')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_call_1(self, mock_parse_args, mock_isparent, mock_write):
        """__call__ normal case
        argv>=3
        verbose = False
        only = False
        standalone = False
        clean = False
        """
        ### setting ###
        argv = ['1', '2', '3']
        mock_parse_args.return_value = self.options, argv
        self.admin_mock.package.get_package.return_value = 'package'
        rtc = MagicMock(spec=['rtcprofile'])
        type(rtc).path = 'rtc_path'
        rtc.rtcprofile(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc, rtc]
        mock_isparent.side_effect = [False, False]
        self.admin_mock.builder.build_rtc.return_value = (1, 'msg')
        ### test ###
        self.assertEqual(0, self.plugin('test_argv'))
        self.admin_mock.package.get_package.assert_called_once()
        self.assertEqual(2, mock_isparent.call_count)
        self.assertEqual(2, self.admin_mock.builder.build_rtc.call_count)
        self.assertEqual(2, self.admin_mock.systeminstaller.install_rtc_in_package.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.make_plugin.isparent')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_call_2(self, mock_parse_args, mock_isparent, mock_write):
        """__call__ normal case
        argv<3
        verbose = True
        only = True
        standalone = False
        clean = False
        """
        ### setting ###
        argv = ['1', '2']
        self.options.verbose_flag = True
        self.options.only_flag = True
        mock_parse_args.return_value = self.options, argv
        package1 = MagicMock()
        package2 = MagicMock()
        type(package1).path = ''
        type(package2).path = ''
        type(package2).name = 'package_name'
        self.admin_mock.package.get_packages.return_value = [package1, package2]
        rtc = MagicMock(spec=['rtcprofile'])
        type(rtc).path = 'rtc_path'
        rtc.rtcprofile(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc, rtc]
        mock_isparent.side_effect = [False, True, False, True]
        self.admin_mock.builder.build_rtc.return_value = (1, 'msg')
        ### test ###
        self.assertEqual(0, self.plugin('test_argv'))
        self.admin_mock.package.get_packages.assert_called_once()
        self.assertEqual(4, mock_isparent.call_count)
        self.assertEqual(1, self.admin_mock.builder.build_rtc.call_count)
        self.assertEqual(0, self.admin_mock.systeminstaller.install_rtc_in_package.call_count)
        mock_write.assert_any_call('# Found Package package_name\n')
        mock_write.assert_any_call('## Found RTC rtc_name\n')

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.make_plugin.isparent')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_call_build_rtc_ret_false(self, mock_parse_args, mock_isparent, mock_write):
        """__call__ build_rtc_ret == False
        argv<3
        verbose = True
        only = True
        standalone = False
        clean = False
        """
        ### setting ###
        argv = ['1', '2']
        self.options.verbose_flag = True
        self.options.only_flag = True
        mock_parse_args.return_value = self.options, argv
        package1 = MagicMock()
        package2 = MagicMock()
        type(package1).path = ''
        type(package2).path = ''
        type(package2).name = 'package_name'
        self.admin_mock.package.get_packages.return_value = [package1, package2]
        rtc = MagicMock(spec=['rtcprofile'])
        type(rtc).path = 'rtc_path'
        rtc.rtcprofile(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc, rtc]
        mock_isparent.side_effect = [False, True, False, True]
        self.admin_mock.builder.build_rtc.return_value = (False, 'msg')
        ### test ###
        self.assertEqual(-1, self.plugin('test_argv'))
        self.admin_mock.package.get_packages.assert_called_once()
        self.assertEqual(4, mock_isparent.call_count)
        self.assertEqual(1, self.admin_mock.builder.build_rtc.call_count)
        self.assertEqual(0, self.admin_mock.systeminstaller.install_rtc_in_package.call_count)
        mock_write.assert_any_call('# Found Package package_name\n')
        mock_write.assert_any_call('## Found RTC rtc_name\n')

    @mock.patch('wasanbon.core.plugins.admin.package_plugin.get_package')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_call_package_none(self, mock_parse_args, mock_get_package):
        """__call__ package==None
        argv>=3
        """
        argv = ['1', '2', '3']
        mock_parse_args.return_value = self.options, argv
        self.admin_mock.package.get_package.return_value = None
        import wasanbon
        with self.assertRaises(wasanbon.PackageNotFoundException):
            self.plugin('test_argv')

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.make_plugin.isparent')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_call_clean_flag_true(self, mock_parse_args, mock_isparent, mock_write):
        """__call__ normal case
        argv>=3
        verbose = False
        only = False
        standalone = False
        clean = True
        """
        ### setting ###
        self.options.clean_flag = True
        argv = ['1', '2', '3']
        mock_parse_args.return_value = self.options, argv
        self.admin_mock.package.get_package.return_value = 'package'
        rtc = MagicMock(spec=['rtcprofile'])
        type(rtc).path = 'rtc_path'
        rtc.rtcprofile(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc, rtc]
        mock_isparent.side_effect = [False, False]
        self.admin_mock.builder.clean_rtc.return_value = (1, 'msg')
        ### test ###
        self.assertEqual(0, self.plugin('test_argv'))
        self.admin_mock.package.get_package.assert_called_once()
        self.assertEqual(2, mock_isparent.call_count)
        self.assertEqual(2, self.admin_mock.builder.clean_rtc.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.make_plugin.isparent')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_call_clean_rtc_ret_true(self, mock_parse_args, mock_isparent, mock_write):
        """__call__ clean_rtc return_value ret == True
        argv>=3
        verbose = False
        only = False
        standalone = False
        clean = True
        """
        ### setting ###
        self.options.clean_flag = True
        argv = ['1', '2', '3']
        mock_parse_args.return_value = self.options, argv
        self.admin_mock.package.get_package.return_value = 'package'
        rtc = MagicMock(spec=['rtcprofile'])
        type(rtc).path = 'rtc_path'
        rtc.rtcprofile(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc, rtc]
        mock_isparent.side_effect = [False, False]
        self.admin_mock.builder.clean_rtc.return_value = (False, 'msg')
        ### test ###
        self.assertEqual(-1, self.plugin('test_argv'))
        self.admin_mock.package.get_package.assert_called_once()
        self.assertEqual(2, mock_isparent.call_count)
        self.assertEqual(2, self.admin_mock.builder.clean_rtc.call_count)


if __name__ == '__main__':
    unittest.main()
