# test for wasanbon/core/plugins/mgr/admin_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import time
import threading

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.mgr.rtc_plugin as m
        self.admin_mock = MagicMock(spec=['package', 'rtc', 'rtcconf', 'rtcprofile', 'builder', 'systeminstaller', 'systemlauncher', 'editor'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        self.func = m

    def get_rtc(self):
        basicInfo = MagicMock()
        type(basicInfo).name = PropertyMock(return_value='test_name')
        type(basicInfo).description = PropertyMock(return_value='test_description')
        type(basicInfo).category = PropertyMock(return_value='test_category')
        type(basicInfo).vendor = PropertyMock(return_value='test_vendor')
        dataport = MagicMock()
        type(dataport).name = PropertyMock(return_value='dataport_name')
        type(dataport).portType = PropertyMock(return_value='dataport_porttype')
        type(dataport).type = PropertyMock(return_value='dataport_type')
        serviceInterface = MagicMock()
        type(serviceInterface).name = PropertyMock(return_value='serviceInterface_name')
        type(serviceInterface).type = PropertyMock(return_value='serviceInterface_type')
        type(serviceInterface).instanceName = PropertyMock(return_value='serviceInterface_instanceName')
        serviceport = MagicMock()
        type(serviceport).name = PropertyMock(return_value='serviceport_name')
        type(serviceport).serviceInterfaces = PropertyMock(return_value=[serviceInterface])
        language = MagicMock()
        type(language).kind = PropertyMock(return_value='language_kind')
        rtcprofile = MagicMock()
        type(rtcprofile).basicInfo = PropertyMock(return_value=basicInfo)
        type(rtcprofile).dataports = PropertyMock(return_value=[dataport])
        type(rtcprofile).serviceports = PropertyMock(return_value=[serviceport])
        type(rtcprofile).language = PropertyMock(return_value=language)
        rtc = MagicMock()
        type(rtc).rtcprofile = PropertyMock(return_value=rtcprofile)
        type(rtc).path = PropertyMock(return_value='path')
        return rtc

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.mgr.rtc_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.package', 'admin.rtc', 'admin.rtcconf', 'admin.rtcprofile',
                         'admin.builder', 'admin.systeminstaller', 'admin.systemlauncher', 'admin.editor'], self.plugin.depends())

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_list_1(self, mock_parse_args):
        """list no rtc case"""

        args = ['./mgr.py', 'rtc', 'list']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = False
        type(options).detail_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        get_rtcs_from_package = MagicMock(return_value=[])
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.list(args))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.print')
    def test_list_2(self, mock_print, mock_parse_args):
        """list rtc case"""

        args = ['./mgr.py', 'rtc', 'list']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = False
        type(options).detail_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.list(args))
        mock_print.assert_any_call(' - ' + 'test_name')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.print')
    def test_list_3(self, mock_print, mock_parse_args):
        """list rtc long format case"""

        args = ['./mgr.py', 'rtc', 'list']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = True
        type(options).detail_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.list(args))
        mock_print.assert_any_call('test_name : ')
        mock_print.assert_any_call('  basicInfo : ')
        mock_print.assert_any_call('    description : ' + 'test_description')
        mock_print.assert_any_call('    category    : ' + 'test_category')
        mock_print.assert_any_call('    vendor      : ' + 'test_vendor')
        mock_print.assert_any_call('  dataports : ')
        mock_print.assert_any_call('     - ' + 'dataport_name')
        mock_print.assert_any_call('  serviceports :')
        mock_print.assert_any_call('     - ' + 'serviceport_name')
        mock_print.assert_any_call('')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.print')
    def test_list_4(self, mock_print, mock_parse_args):
        """list rtc long format case"""

        args = ['./mgr.py', 'rtc', 'list']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = True
        type(options).detail_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.list(args))
        mock_print.assert_any_call('test_name : ')
        mock_print.assert_any_call('  basicInfo : ')
        mock_print.assert_any_call('    description : ' + 'test_description')
        mock_print.assert_any_call('    category    : ' + 'test_category')
        mock_print.assert_any_call('    vendor      : ' + 'test_vendor')
        mock_print.assert_any_call('  dataports : ')
        mock_print.assert_any_call('    ' + 'dataport_name' + ':')
        mock_print.assert_any_call('      portType : ' + 'dataport_porttype')
        mock_print.assert_any_call('      type     : ' + 'dataport_type')
        mock_print.assert_any_call('  serviceports :')
        mock_print.assert_any_call('    ' + 'serviceport_name' + ':')
        mock_print.assert_any_call('      ' + 'serviceInterface_name' + ':')
        mock_print.assert_any_call('        type         : ' + 'serviceInterface_type')
        mock_print.assert_any_call('        instanceName : ' + 'serviceInterface_instanceName')
        mock_print.assert_any_call('  language : ')
        mock_print.assert_any_call('    kind        : ' + 'language_kind')
        mock_print.assert_any_call('')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    def test_build_1(self, mock_write, mock_platform, mock_parse_args):
        """build all no rtc case"""

        args = ['./mgr.py', 'rtc', 'build', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).only_flag = False
        type(options).standalone_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = []
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.build(args))
        mock_write.assert_any_call('Build Summary:\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('sys.stdout.write')
    def test_build_2(self, mock_write, mock_platform, mock_parse_args):
        """build all no rtc win case"""

        args = ['./mgr.py', 'rtc', 'build', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).only_flag = False
        type(options).standalone_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = []
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.build(args))
        mock_write.assert_any_call('# In Windows, always build with verbose option.\n')
        mock_write.assert_any_call('Build Summary:\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    def test_build_3(self, mock_write, mock_platform, mock_parse_args):
        """build all rtc failed case"""

        args = ['./mgr.py', 'rtc', 'build', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).only_flag = False
        type(options).standalone_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        build_rtc = MagicMock(return_value=(None, None))
        type(self.admin_mock.builder).build_rtc = build_rtc

        ### test ###
        self.assertEqual(-1, self.plugin.build(args))
        mock_write.assert_any_call('# Building RTC (test_name)\n')
        mock_write.assert_any_call('## Failed.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    def test_build_4(self, mock_write, mock_platform, mock_parse_args):
        """build all rtc not_standalone case"""

        args = ['./mgr.py', 'rtc', 'build', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).only_flag = False
        type(options).standalone_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        build_rtc = MagicMock(return_value=('ret', 'msg'))
        type(self.admin_mock.builder).build_rtc = build_rtc

        is_installed = MagicMock(return_value=False)
        type(self.admin_mock.systeminstaller).is_installed = is_installed

        install_rtc_in_package = MagicMock()
        type(self.admin_mock.systeminstaller).install_rtc_in_package = install_rtc_in_package

        ### test ###
        self.assertEqual(0, self.plugin.build(args))
        mock_write.assert_any_call('# Building RTC (test_name)\n')
        mock_write.assert_any_call('## Success.\n')
        mock_write.assert_any_call('## Installing RTC (standalone=False).\n')
        mock_write.assert_any_call('### Success.\n')
        mock_write.assert_any_call(' - Build RTC (test_name)                Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    def test_build_5(self, mock_write, mock_platform, mock_parse_args):
        """build all rtc not_standalone case"""

        args = ['./mgr.py', 'rtc', 'build', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).only_flag = False
        type(options).standalone_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        build_rtc = MagicMock(return_value=('ret', 'msg'))
        type(self.admin_mock.builder).build_rtc = build_rtc

        is_installed = MagicMock(return_value=False)
        type(self.admin_mock.systeminstaller).is_installed = is_installed

        install_rtc_in_package = MagicMock()
        type(self.admin_mock.systeminstaller).install_rtc_in_package = install_rtc_in_package

        ### test ###
        self.assertEqual(0, self.plugin.build(args))
        is_installed.assert_not_called()
        mock_write.assert_any_call('# Building RTC (test_name)\n')
        mock_write.assert_any_call('## Success.\n')
        mock_write.assert_any_call('## Installing RTC (standalone=True).\n')
        mock_write.assert_any_call('### Success.\n')
        mock_write.assert_any_call(' - Build RTC (test_name)                Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    def test_build_6(self, mock_write, mock_platform, mock_parse_args):
        """build select rtc not_standalone case"""

        args = ['./mgr.py', 'rtc', 'build', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).only_flag = False
        type(options).standalone_flag = False
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        build_rtc = MagicMock(return_value=('ret', 'msg'))
        type(self.admin_mock.builder).build_rtc = build_rtc

        is_installed = MagicMock(return_value=False)
        type(self.admin_mock.systeminstaller).is_installed = is_installed

        install_rtc_in_package = MagicMock()
        type(self.admin_mock.systeminstaller).install_rtc_in_package = install_rtc_in_package

        ### test ###
        self.assertEqual(0, self.plugin.build(args))
        mock_write.assert_any_call('# Building RTC (test_name)\n')
        mock_write.assert_any_call('## Success.\n')
        mock_write.assert_any_call('## Installing RTC (standalone=False).\n')
        mock_write.assert_any_call('### Success.\n')
        mock_write.assert_any_call(' - Build RTC (test_name)                Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_clean_1(self, mock_write, mock_parse_args):
        """clean all no rtc case"""

        args = ['./mgr.py', 'rtc', 'clean', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = []
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.clean(args))
        mock_write.assert_any_call('# Cleanup RTCs\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_clean_2(self, mock_write, mock_parse_args):
        """clean all rtc failed case"""

        args = ['./mgr.py', 'rtc', 'clean', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        clean_rtc = MagicMock(return_value=(None, None))
        type(self.admin_mock.builder).clean_rtc = clean_rtc

        ### test ###
        self.assertEqual(-1, self.plugin.clean(args))
        mock_write.assert_any_call('# Cleanup RTCs\n')
        mock_write.assert_any_call('# Cleanuping RTC test_name\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_clean_3(self, mock_write, mock_parse_args):
        """clean select rtc success case"""

        args = ['./mgr.py', 'rtc', 'clean', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        clean_rtc = MagicMock(return_value=('ret', 'msg'))
        type(self.admin_mock.builder).clean_rtc = clean_rtc

        ### test ###
        self.assertEqual(0, self.plugin.clean(args))
        mock_write.assert_any_call('# Cleanup RTCs\n')
        mock_write.assert_any_call('# Cleanuping RTC test_name\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_delete_1(self, mock_write, mock_parse_args):
        """delete all rtc no_rtc case"""

        args = ['./mgr.py', 'rtc', 'delete', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = []
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.delete(args))
        mock_write.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('shutil.rmtree')
    def test_delete_2(self, mock_rmtree, mock_isdir, mock_write, mock_parse_args):
        """delete all rtc no_rtc case"""

        args = ['./mgr.py', 'rtc', 'delete', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        self.assertEqual(0, self.plugin.delete(args))
        mock_write.assert_any_call('# Deleting RTC (test_name)\n')
        mock_isdir.assert_called_once()
        mock_rmtree.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('shutil.rmtree')
    def test_delete_3(self, mock_rmtree, mock_isdir, mock_write, mock_parse_args):
        """delete select rtc no_rtc case"""

        args = ['./mgr.py', 'rtc', 'delete', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        ### test ###
        self.assertEqual(0, self.plugin.delete(args))
        mock_write.assert_any_call('# Deleting RTC (test_name)\n')
        mock_isdir.assert_called_once()
        mock_rmtree.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_edit_1(self, mock_write, mock_parse_args):
        """edit normal case"""

        args = ['./mgr.py', 'rtc', 'edit', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        edit_rtc = MagicMock()
        type(self.admin_mock.editor).edit_rtc = edit_rtc

        ### test ###
        self.assertEqual(0, self.plugin.edit(args))
        mock_write.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=0)
    def test_edit_2(self, mock_run_rtc_in_package, mock_write, mock_parse_args):
        """run normal case"""

        args = ['./mgr.py', 'rtc', 'run', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        ### test ###
        self.assertEqual(0, self.plugin.run(args))
        mock_write.assert_not_called()

    @mock.patch('signal.signal')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    @mock.patch('os.remove')
    def test_run_1(self, mock_remove, mock_isfile, mock_write, mock_platform, mock_signal):
        """test_run_rtc_in_package normal case"""

        package = MagicMock()
        type(package).rtcconf = {'language_kind': 'language_path'}
        rtc = self.get_rtc()

        rtcconf = MagicMock()
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        uninstall_all_rtc_from_package = MagicMock()
        install_rtc_in_package = MagicMock()
        type(self.admin_mock.systeminstaller).uninstall_all_rtc_from_package = uninstall_all_rtc_from_package
        type(self.admin_mock.systeminstaller).install_rtc_in_package = install_rtc_in_package

        launch_rtcd = MagicMock()
        type(self.admin_mock.systemlauncher).launch_rtcd = launch_rtcd

        ### test ###
        self.assertEqual(0, self.plugin.run_rtc_in_package(package, rtc, verbose=True, background=True))
        mock_signal.assert_called_once()
        mock_write.assert_any_call('# Executing RTC test_name\n')

    @mock.patch('signal.signal')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    @mock.patch('os.remove')
    @mock.patch('builtins.print')
    def test_run_2(self, mock_print, mock_remove, mock_isfile, mock_write, mock_platform, mock_signal):
        """test_run_rtc_in_package failed case"""

        package = MagicMock()
        type(package).rtcconf = {'language_kind': 'language_path'}
        rtc = self.get_rtc()

        rtcconf = MagicMock()
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        uninstall_all_rtc_from_package = MagicMock()
        install_rtc_in_package = MagicMock()
        type(self.admin_mock.systeminstaller).uninstall_all_rtc_from_package = uninstall_all_rtc_from_package
        type(self.admin_mock.systeminstaller).install_rtc_in_package = install_rtc_in_package

        launch_rtcd = MagicMock(side_effect=wasanbon.RepositoryNotFoundException())
        type(self.admin_mock.systemlauncher).launch_rtcd = launch_rtcd

        ### test ###
        self.assertEqual(-1, self.plugin.run_rtc_in_package(package, rtc, verbose=True, background=False))
        mock_signal.assert_called_once()
        mock_write.assert_any_call('# Executing RTC test_name\n')

    @mock.patch('sys.stdout.write')
    def test_terminate_rtcd_1(self, mock_write):
        """test_terminate_rtcd normal case"""

        package = MagicMock()
        exit_all_rtcs = MagicMock()
        terminate_system = MagicMock()
        type(self.admin_mock.systeminstaller).exit_all_rtcs = exit_all_rtcs
        type(self.admin_mock.systeminstaller).terminate_system = terminate_system

        ### test ###
        self.assertEqual(0, self.plugin.terminate_rtcd(package, verbose=True))
        mock_write.assert_any_call('# Terminating RTCDs.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=-1)
    def test_download_profile_1(self, mock_run_rtc_in_package, mock_terminate_rtcd, mock_print, mock_parse_args):
        """download_profile failed case"""

        args = ['./mgr.py', 'rtc', 'download_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        ### test ###
        self.assertEqual(-1, self.plugin.download_profile(args))
        mock_print.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=0)
    @mock.patch('wasanbon.sleep')
    def test_download_profile_2(self, mock_sleep, mock_run_rtc_in_package, mock_terminate_rtcd, mock_print, mock_parse_args):
        """download_profile normal case"""

        args = ['./mgr.py', 'rtc', 'download_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        create_rtcprofile = MagicMock()
        type(self.admin_mock.rtcprofile).create_rtcprofile = create_rtcprofile

        tostring = MagicMock(return_value='tostring.return_value')
        type(self.admin_mock.rtcprofile).tostring = tostring

        ### test ###
        self.assertEqual(0, self.plugin.download_profile(args))
        mock_sleep.assert_called_once_with(10)
        mock_print.assert_called_once_with('tostring.return_value')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=-1)
    @mock.patch('sys.stdout.write')
    def test_verify_profile_1(self, mock_write, mock_run_rtc_in_package, mock_terminate_rtcd, mock_parse_args):
        """verify_profile failed case"""

        args = ['./mgr.py', 'rtc', 'verify_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        ### test ###
        self.assertEqual(-1, self.plugin.verify_profile(args))
        mock_write.assert_called_once_with('# Starting RTC.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=0)
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.sleep')
    def test_verify_profile_2(self, mock_sleep, mock_write, mock_run_rtc_in_package, mock_terminate_rtcd, mock_parse_args):
        """verify_profile failed case"""

        args = ['./mgr.py', 'rtc', 'verify_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        create_rtcprofile = MagicMock()
        type(self.admin_mock.rtcprofile).create_rtcprofile = create_rtcprofile

        compare_rtcprofile = MagicMock(return_value=True)
        type(self.admin_mock.rtcprofile).compare_rtcprofile = compare_rtcprofile

        ### test ###
        self.assertEqual(-1, self.plugin.verify_profile(args))
        mock_sleep.assert_called_once_with(10)
        mock_write.assert_any_call('# Starting RTC.\n')
        mock_write.assert_any_call('# Acquiring RTCProfile from Inactive RTC\n')
        mock_write.assert_any_call('# Comparing Acquired RTCProfile and Existing RTCProfile.\n')
        mock_write.assert_any_call('Failed.\n# RTCProfile must be updated.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=0)
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.sleep')
    def test_verify_profile_3(self, mock_sleep, mock_write, mock_run_rtc_in_package, mock_terminate_rtcd, mock_parse_args):
        """verify_profile success case"""

        args = ['./mgr.py', 'rtc', 'verify_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        create_rtcprofile = MagicMock()
        type(self.admin_mock.rtcprofile).create_rtcprofile = create_rtcprofile

        compare_rtcprofile = MagicMock(return_value=False)
        type(self.admin_mock.rtcprofile).compare_rtcprofile = compare_rtcprofile

        ### test ###
        self.assertEqual(0, self.plugin.verify_profile(args))
        mock_sleep.assert_called_once_with(10)
        mock_write.assert_any_call('# Starting RTC.\n')
        mock_write.assert_any_call('# Acquiring RTCProfile from Inactive RTC\n')
        mock_write.assert_any_call('# Comparing Acquired RTCProfile and Existing RTCProfile.\n')
        mock_write.assert_any_call('Succeeded.\n# RTCProfile is currently matches to binary.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.sleep')
    def test_update_profile_1(self, mock_sleep, mock_write, mock_run_rtc_in_package, mock_terminate_rtcd, mock_parse_args):
        """update_profile nodiff and standalone case"""

        args = ['./mgr.py', 'rtc', 'update_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).dry_flag = False
        type(options).filename = None
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        is_installed = MagicMock(return_value=True)
        type(self.admin_mock.systeminstaller).is_installed = is_installed

        launch_standalone_rtc = MagicMock()
        type(self.admin_mock.systemlauncher).launch_standalone_rtc = launch_standalone_rtc

        create_rtcprofile = MagicMock()
        type(self.admin_mock.rtcprofile).create_rtcprofile = create_rtcprofile

        compare_rtcprofile = MagicMock(return_value=False)
        type(self.admin_mock.rtcprofile).compare_rtcprofile = compare_rtcprofile

        ### test ###
        self.assertEqual(0, self.plugin.update_profile(args))
        mock_write.assert_any_call('# Starting RTC.\n')
        launch_standalone_rtc.assert_called_once()
        mock_sleep.assert_called_once_with(10)
        mock_write.assert_any_call('# Acquiring RTCProfile from Inactive RTC\n')
        mock_write.assert_any_call('# Comparing Acquired RTCProfile and Existing RTCProfile.\n')
        mock_write.assert_any_call('Succeed.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=-1)
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.sleep')
    def test_update_profile_2(self, mock_sleep, mock_write, mock_run_rtc_in_package, mock_terminate_rtcd, mock_parse_args):
        """update_profile run error case"""

        args = ['./mgr.py', 'rtc', 'update_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).dry_flag = False
        type(options).filename = None
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        is_installed = MagicMock(return_value=False)
        type(self.admin_mock.systeminstaller).is_installed = is_installed

        launch_standalone_rtc = MagicMock()
        type(self.admin_mock.systemlauncher).launch_standalone_rtc = launch_standalone_rtc

        ### test ###
        self.assertEqual(-1, self.plugin.update_profile(args))
        mock_write.assert_any_call('# Starting RTC.\n')
        launch_standalone_rtc.assert_not_called()
        mock_run_rtc_in_package.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=0)
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.sleep')
    def test_update_profile_3(self, mock_sleep, mock_write, mock_run_rtc_in_package, mock_terminate_rtcd, mock_parse_args):
        """update_profile dry case"""

        args = ['./mgr.py', 'rtc', 'update_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).dry_flag = True
        type(options).filename = ''
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        is_installed = MagicMock(return_value=False)
        type(self.admin_mock.systeminstaller).is_installed = is_installed

        launch_standalone_rtc = MagicMock()
        type(self.admin_mock.systemlauncher).launch_standalone_rtc = launch_standalone_rtc

        tostring = MagicMock(return_value='tostring.return_value')
        type(self.admin_mock.rtcprofile).tostring = tostring

        ### test ###
        self.assertEqual(0, self.plugin.update_profile(args))
        mock_write.assert_any_call('# Starting RTC.\n')
        launch_standalone_rtc.assert_not_called()
        mock_run_rtc_in_package.assert_called_once()
        mock_write.assert_any_call('tostring.return_value')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=0)
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.sleep')
    def test_update_profile_4(self, mock_sleep, mock_write, mock_run_rtc_in_package, mock_terminate_rtcd, mock_parse_args):
        """update_profile save failed case"""

        args = ['./mgr.py', 'rtc', 'update_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).dry_flag = False
        type(options).filename = ''
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        is_installed = MagicMock(return_value=False)
        type(self.admin_mock.systeminstaller).is_installed = is_installed

        launch_standalone_rtc = MagicMock()
        type(self.admin_mock.systemlauncher).launch_standalone_rtc = launch_standalone_rtc

        tostring = MagicMock(return_value=None)
        type(self.admin_mock.rtcprofile).tostring = tostring

        ### test ###
        self.assertEqual(-1, self.plugin.update_profile(args))
        mock_write.assert_any_call('# Starting RTC.\n')
        launch_standalone_rtc.assert_not_called()
        mock_run_rtc_in_package.assert_called_once()
        mock_write.assert_any_call('# RTC Profile save failed.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.mgr.rtc_plugin.Plugin.run_rtc_in_package', return_value=0)
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.sleep')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.timestampstr')
    @mock.patch('os.rename')
    @mock.patch('builtins.open')
    def test_update_profile_5(self, mock_open, mock_rename, mock_timestampstr, mock_isfile, mock_sleep, mock_write, mock_run_rtc_in_package, mock_terminate_rtcd, mock_parse_args):
        """update_profile success case"""

        args = ['./mgr.py', 'rtc', 'update_profile', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).dry_flag = False
        type(options).filename = ''
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        get_package_from_path = MagicMock()
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        is_installed = MagicMock(return_value=False)
        type(self.admin_mock.systeminstaller).is_installed = is_installed

        launch_standalone_rtc = MagicMock()
        type(self.admin_mock.systemlauncher).launch_standalone_rtc = launch_standalone_rtc

        tostring = MagicMock(return_value='tostring.return_value')
        type(self.admin_mock.rtcprofile).tostring = tostring

        ### test ###
        self.assertEqual(0, self.plugin.update_profile(args))
        mock_write.assert_any_call('# Starting RTC.\n')
        launch_standalone_rtc.assert_not_called()
        mock_run_rtc_in_package.assert_called_once()
        mock_isfile.assert_called_once()
        mock_rename.assert_called_once()
        mock_open.assert_called_once()
        mock_write.assert_any_call('Succeed.\n')


if __name__ == '__main__':
    unittest.main()
