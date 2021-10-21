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
        import wasanbon.core.plugins.mgr.system_plugin as m
        self.admin_mock = MagicMock(spec=['package', 'rtc', 'systeminstaller', 'systemlauncher',
                                    'systembuilder', 'nameserver', 'systemeditor', 'rtcconf'])
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
        from wasanbon.core.plugins.mgr.system_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.package', 'admin.rtc', 'admin.systeminstaller', 'admin.systemlauncher',
                         'admin.systembuilder', 'admin.nameserver', 'admin.systemeditor', 'admin.rtcconf'], self.plugin.depends())

    @mock.patch('builtins.print')
    def test_print_rtcs_1(self, mock_print):
        """print_rtcs no_rtc case"""

        package = None
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = []
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        args = []
        self.plugin._print_rtcs(args)
        mock_print.assert_not_called()

    @mock.patch('builtins.print')
    def test_print_rtcs_2(self, mock_print):
        """print_rtcs rtc case"""

        package = None
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        ### test ###
        args = []
        self.plugin._print_rtcs(args)
        mock_print.assert_called_once_with('test_name')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_install_1(self, mock_parse_args):
        """install all no rtc case"""

        args = ['./mgr.py', 'system', 'install', 'all']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        type(options).standalone_flag = False
        type(options).allow_duplicate = False
        mock_parse_args.return_value = options, args

        package = None
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = []
        get_rtcs_from_package = MagicMock(return_value=rtcs)
        type(self.admin_mock.rtc).get_rtcs_from_package = get_rtcs_from_package

        install_rtc_in_package = MagicMock()
        type(self.admin_mock.systeminstaller).install_rtc_in_package = install_rtc_in_package

        ### test ###
        self.assertEqual(0, self.plugin.install(args))
        get_rtcs_from_package.assert_called_once()
        install_rtc_in_package.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_install_2(self, mock_parse_args):
        """install select rtc case"""

        args = ['./mgr.py', 'system', 'install', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        type(options).standalone_flag = False
        type(options).allow_duplicate = False
        mock_parse_args.return_value = options, args

        package = None
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        install_rtc_in_package = MagicMock(return_value=1)
        type(self.admin_mock.systeminstaller).install_rtc_in_package = install_rtc_in_package

        ### test ###
        self.assertEqual(1, self.plugin.install(args))
        get_rtc_from_package.assert_called_once()
        install_rtc_in_package.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_uninstall_1(self, mock_parse_args):
        """uninstall all rtc case"""

        args = ['./mgr.py', 'system', 'uninstall', 'test_name']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = None
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcs = [self.get_rtc()]
        get_rtc_from_package = MagicMock(return_value=rtcs[0])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        uninstall_rtc_from_package = MagicMock(return_value=1)
        type(self.admin_mock.systeminstaller).uninstall_rtc_from_package = uninstall_rtc_from_package

        ### test ###
        self.assertEqual(1, self.plugin.uninstall(args))
        get_rtc_from_package.assert_called_once()
        uninstall_rtc_from_package.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_terminate_1(self, mock_print_exc, mock_write, mock_parse_args):
        """terminate deactivate failed case"""

        args = ['./mgr.py', 'system', 'terminate']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = None
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        deactivate_system = MagicMock(side_effect=wasanbon.BuildSystemException())
        type(self.admin_mock.systembuilder).deactivate_system = deactivate_system

        ### test ###
        self.assertEqual(-1, self.plugin.terminate(args))
        deactivate_system.assert_called_once()
        mock_write.assert_any_call('# Build System Failed.\n')
        mock_print_exc.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_terminate_2(self, mock_print_exc, mock_write, mock_parse_args):
        """terminate deactivate failed case"""

        args = ['./mgr.py', 'system', 'terminate']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = None
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        deactivate_system = MagicMock(side_effect=Exception())
        type(self.admin_mock.systembuilder).deactivate_system = deactivate_system

        ### test ###
        self.assertEqual(-1, self.plugin.terminate(args))
        deactivate_system.assert_called_once()
        mock_print_exc.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_terminate_3(self, mock_print_exc, mock_write, mock_parse_args):
        """terminate terminate failed case"""

        args = ['./mgr.py', 'system', 'terminate']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = None
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        deactivate_system = MagicMock()
        type(self.admin_mock.systembuilder).deactivate_system = deactivate_system

        exit_all_rtcs = MagicMock()
        type(self.admin_mock.systemlauncher).exit_all_rtcs = exit_all_rtcs

        terminate_system = MagicMock(side_effect=Exception())
        type(self.admin_mock.systemlauncher).terminate_system = terminate_system

        ### test ###
        self.assertEqual(-1, self.plugin.terminate(args))
        deactivate_system.assert_called_once()
        exit_all_rtcs.assert_called_once()
        terminate_system.assert_called_once()
        mock_print_exc.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_terminate_4(self, mock_print_exc, mock_write, mock_parse_args):
        """terminate terminate success case"""

        args = ['./mgr.py', 'system', 'terminate']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = None
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        deactivate_system = MagicMock()
        type(self.admin_mock.systembuilder).deactivate_system = deactivate_system

        exit_all_rtcs = MagicMock()
        type(self.admin_mock.systemlauncher).exit_all_rtcs = exit_all_rtcs

        terminate_system = MagicMock()
        type(self.admin_mock.systemlauncher).terminate_system = terminate_system

        ### test ###
        self.assertEqual(0, self.plugin.terminate(args))
        deactivate_system.assert_called_once()
        exit_all_rtcs.assert_called_once()
        terminate_system.assert_called_once()
        mock_print_exc.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    @mock.patch('wasanbon.sleep')
    @mock.patch('signal.signal')
    def test_run_1(self, mock_signal, mock_sleep, mock_print_exc, mock_write, mock_parse_args):
        """run background case"""

        args = ['./mgr.py', 'system', 'run']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = True
        type(options).wakeuptimeout = 10
        type(options).systemfile = 'test'
        type(options).plain_flag = False
        type(options).quiet_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock()
        get_systempath.return_value = './test'
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock()
        get_package_from_path.return_value = package
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ns = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        nss = [ns]
        get_nameservers_from_package = MagicMock()
        get_nameservers_from_package.return_value = nss
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package

        is_running = MagicMock(return_value=False)
        type(self.admin_mock.nameserver).is_running = is_running

        launch = MagicMock()
        type(self.admin_mock.nameserver).launch = launch

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        build_system = MagicMock()
        type(self.admin_mock.systembuilder).build_system = build_system

        activate_system = MagicMock()
        type(self.admin_mock.systembuilder).activate_system = activate_system

        ### test ###
        self.assertEqual(0, self.plugin.run(args))
        get_package_from_path.assert_called_once()
        get_nameservers_from_package.assert_called_once()
        is_running.assert_called_once()
        launch_system.assert_called_once()
        build_system.assert_called_once()
        activate_system.assert_called_once()
        mock_signal.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    @mock.patch('wasanbon.sleep')
    @mock.patch('signal.signal')
    def test_run_2(self, mock_signal, mock_sleep, mock_print_exc, mock_write, mock_platform, mock_parse_args):
        """run deactivate failed case"""

        args = ['./mgr.py', 'system', 'run']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = False
        type(options).wakeuptimeout = 10
        type(options).systemfile = 'test'
        type(options).plain_flag = False
        type(options).quiet_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock()
        get_systempath.return_value = './test'
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock()
        get_package_from_path.return_value = package
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ns = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        nss = [ns]
        get_nameservers_from_package = MagicMock()
        get_nameservers_from_package.return_value = nss
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package

        is_running = MagicMock(return_value=False)
        type(self.admin_mock.nameserver).is_running = is_running

        launch = MagicMock()
        type(self.admin_mock.nameserver).launch = launch

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        build_system = MagicMock()
        type(self.admin_mock.systembuilder).build_system = build_system

        activate_system = MagicMock()
        type(self.admin_mock.systembuilder).activate_system = activate_system

        is_rtcd_launched = MagicMock(return_value=False)
        type(self.admin_mock.systemlauncher).is_rtcd_launched = is_rtcd_launched

        is_standalone_rtcs_launched = MagicMock(return_value=False)
        type(self.admin_mock.systemlauncher).is_standalone_rtcs_launched = is_standalone_rtcs_launched

        deactivate_system = MagicMock(side_effect=wasanbon.BuildSystemException())
        type(self.admin_mock.systembuilder).deactivate_system = deactivate_system

        ### test ###
        self.assertEqual(-1, self.plugin.run(args))
        get_package_from_path.assert_called_once()
        get_nameservers_from_package.assert_called_once()
        is_running.assert_called_once()
        launch_system.assert_called_once()
        build_system.assert_called_once()
        activate_system.assert_called_once()
        is_rtcd_launched.assert_any_call(package, 'Java', verbose=True)
        is_rtcd_launched.assert_any_call(package, 'Python', verbose=True)
        is_rtcd_launched.assert_any_call(package, 'C++', verbose=True)
        is_standalone_rtcs_launched.assert_called_once()
        deactivate_system.assert_called_once()
        mock_write.assert_any_call('# Build System Failed.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    @mock.patch('wasanbon.sleep')
    @mock.patch('signal.signal')
    def test_run_3(self, mock_signal, mock_sleep, mock_print_exc, mock_write, mock_platform, mock_parse_args):
        """run deactivate failed case"""

        args = ['./mgr.py', 'system', 'run']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = False
        type(options).wakeuptimeout = 10
        type(options).systemfile = 'test'
        type(options).plain_flag = False
        type(options).quiet_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./test')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ns = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        nss = [ns]
        get_nameservers_from_package = MagicMock(return_value=nss)
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package

        is_running = MagicMock(return_value=False)
        type(self.admin_mock.nameserver).is_running = is_running

        launch = MagicMock()
        type(self.admin_mock.nameserver).launch = launch

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        build_system = MagicMock()
        type(self.admin_mock.systembuilder).build_system = build_system

        activate_system = MagicMock()
        type(self.admin_mock.systembuilder).activate_system = activate_system

        is_rtcd_launched = MagicMock(return_value=False)
        type(self.admin_mock.systemlauncher).is_rtcd_launched = is_rtcd_launched

        is_standalone_rtcs_launched = MagicMock(return_value=False)
        type(self.admin_mock.systemlauncher).is_standalone_rtcs_launched = is_standalone_rtcs_launched

        deactivate_system = MagicMock(side_effect=Exception())
        type(self.admin_mock.systembuilder).deactivate_system = deactivate_system

        ### test ###
        self.assertEqual(-1, self.plugin.run(args))
        get_package_from_path.assert_called_once()
        get_nameservers_from_package.assert_called_once()
        is_running.assert_called_once()
        launch_system.assert_called_once()
        build_system.assert_called_once()
        activate_system.assert_called_once()
        is_rtcd_launched.assert_any_call(package, 'Java', verbose=True)
        is_rtcd_launched.assert_any_call(package, 'Python', verbose=True)
        is_rtcd_launched.assert_any_call(package, 'C++', verbose=True)
        is_standalone_rtcs_launched.assert_called_once()
        deactivate_system.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    @mock.patch('wasanbon.sleep')
    @mock.patch('signal.signal')
    def test_run_4(self, mock_signal, mock_sleep, mock_print_exc, mock_write, mock_platform, mock_parse_args):
        """run terminate failed case"""

        args = ['./mgr.py', 'system', 'run']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = False
        type(options).wakeuptimeout = 10
        type(options).systemfile = 'test'
        type(options).plain_flag = False
        type(options).quiet_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock()
        get_systempath.return_value = './test'
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock()
        get_package_from_path.return_value = package
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ns = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        nss = [ns]
        get_nameservers_from_package = MagicMock(return_value=nss)
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package

        is_running = MagicMock(return_value=False)
        type(self.admin_mock.nameserver).is_running = is_running

        launch = MagicMock()
        type(self.admin_mock.nameserver).launch = launch

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        build_system = MagicMock()
        type(self.admin_mock.systembuilder).build_system = build_system

        activate_system = MagicMock()
        type(self.admin_mock.systembuilder).activate_system = activate_system

        is_rtcd_launched = MagicMock(return_value=False)
        type(self.admin_mock.systemlauncher).is_rtcd_launched = is_rtcd_launched

        is_standalone_rtcs_launched = MagicMock(return_value=False)
        type(self.admin_mock.systemlauncher).is_standalone_rtcs_launched = is_standalone_rtcs_launched

        deactivate_system = MagicMock()
        type(self.admin_mock.systembuilder).deactivate_system = deactivate_system

        exit_all_rtcs = MagicMock()
        type(self.admin_mock.systemlauncher).exit_all_rtcs = exit_all_rtcs

        terminate_system = MagicMock(side_effect=Exception())
        type(self.admin_mock.systemlauncher).terminate_system = terminate_system

        ### test ###
        self.assertEqual(-1, self.plugin.run(args))
        get_package_from_path.assert_called_once()
        get_nameservers_from_package.assert_called_once()
        is_running.assert_called_once()
        launch_system.assert_called_once()
        build_system.assert_called_once()
        activate_system.assert_called_once()
        is_rtcd_launched.assert_any_call(package, 'Java', verbose=True)
        is_rtcd_launched.assert_any_call(package, 'Python', verbose=True)
        is_rtcd_launched.assert_any_call(package, 'C++', verbose=True)
        is_standalone_rtcs_launched.assert_called_once()
        deactivate_system.assert_called_once()
        exit_all_rtcs.assert_called_once()
        terminate_system.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    @mock.patch('wasanbon.sleep')
    @mock.patch('signal.signal')
    def test_run_5(self, mock_signal, mock_sleep, mock_print_exc, mock_write, mock_platform, mock_parse_args):
        """run success case"""

        args = ['./mgr.py', 'system', 'run']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = False
        type(options).wakeuptimeout = 10
        type(options).systemfile = 'test'
        type(options).plain_flag = False
        type(options).quiet_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock()
        get_systempath.return_value = './test'
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock()
        get_package_from_path.return_value = package
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ns = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        nss = [ns]
        get_nameservers_from_package = MagicMock(return_value=nss)
        terminate = MagicMock()
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package
        type(self.admin_mock.nameserver).terminate = terminate

        is_running = MagicMock(return_value=False)
        type(self.admin_mock.nameserver).is_running = is_running

        launch = MagicMock()
        type(self.admin_mock.nameserver).launch = launch

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        build_system = MagicMock()
        type(self.admin_mock.systembuilder).build_system = build_system

        activate_system = MagicMock()
        type(self.admin_mock.systembuilder).activate_system = activate_system

        is_rtcd_launched = MagicMock(return_value=False)
        type(self.admin_mock.systemlauncher).is_rtcd_launched = is_rtcd_launched

        is_standalone_rtcs_launched = MagicMock(return_value=False)
        type(self.admin_mock.systemlauncher).is_standalone_rtcs_launched = is_standalone_rtcs_launched

        deactivate_system = MagicMock()
        type(self.admin_mock.systembuilder).deactivate_system = deactivate_system

        exit_all_rtcs = MagicMock()
        type(self.admin_mock.systemlauncher).exit_all_rtcs = exit_all_rtcs

        terminate_system = MagicMock()
        type(self.admin_mock.systemlauncher).terminate_system = terminate_system

        ### test ###
        self.assertEqual(0, self.plugin.run(args))
        get_package_from_path.assert_called_once()
        get_nameservers_from_package.assert_called_once()
        is_running.assert_called_once()
        launch_system.assert_called_once()
        build_system.assert_called_once()
        activate_system.assert_called_once()
        is_rtcd_launched.assert_any_call(package, 'Java', verbose=True)
        is_rtcd_launched.assert_any_call(package, 'Python', verbose=True)
        is_rtcd_launched.assert_any_call(package, 'C++', verbose=True)
        is_standalone_rtcs_launched.assert_called_once()
        deactivate_system.assert_called_once()
        exit_all_rtcs.assert_called_once()
        terminate_system.assert_called_once()
        terminate.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('time.sleep')
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('wasanbon.util.yes_no', side_effect=['no'])
    @mock.patch('os.getcwd')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('builtins.input', return_value='input_test')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    @mock.patch('traceback.print_exc')
    def test_build_1(self, mock_print_exc, mock_rename, mock_timestampstr, mock_isfile, mock_input, mock_choice, mock_write, mock_getcwd, mock_yes_no, mock_no_yes, mock_sleep, mock_parse_args):
        """build failed case"""

        args = ['./mgr.py', 'system', 'build']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = False
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        mock_getcwd.return_value = 'test'

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).get_systempath = get_systempath
        type(package).name = 'package_name'
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        ns = MagicMock()
        refresh = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        type(ns).refresh = refresh
        rtc = self.get_rtc()
        type(ns).rtcs = [rtc]
        nss = [ns]
        get_nameservers_from_package = MagicMock(return_value=nss)
        terminate = MagicMock()
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package
        type(self.admin_mock.nameserver).terminate = terminate

        pairs = [['pair1', 'pair2']]
        get_connectable_pairs = MagicMock(return_value=pairs)
        type(self.admin_mock.systemeditor).get_connectable_pairs = get_connectable_pairs

        get_port_full_path = MagicMock(side_effect=['full1', 'full2'])
        type(self.admin_mock.systembuilder).get_port_full_path = get_port_full_path

        connect_ports = MagicMock()
        type(self.admin_mock.systembuilder).connect_ports = connect_ports

        get_component_full_path = MagicMock(side_effect=[wasanbon.BuildSystemException()])
        type(self.admin_mock.systembuilder).get_component_full_path = get_component_full_path

        ### test ###
        self.assertEqual(-1, self.plugin.build(args))
        get_package_from_path.assert_has_calls([call('test', verbose=True), call('test')])
        mock_sleep.assert_has_calls([call(10)])
        launch_system.assert_called_once()
        refresh.assert_called_once()
        get_port_full_path.assert_any_call('pair1')
        get_port_full_path.assert_any_call('pair2')
        mock_no_yes.assert_has_calls([call('# Connect? (full1->full2)\n')])
        connect_ports.assert_called_once_with('pair1', 'pair2', verbose=True)
        mock_write.assert_any_call('## Connected.\n')
        get_component_full_path.assert_called_once_with(rtc)
        mock_write.assert_any_call('# Build System Failed.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('time.sleep')
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('wasanbon.util.yes_no', side_effect=['no'])
    @mock.patch('os.getcwd')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('builtins.input', return_value='input_test')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    @mock.patch('traceback.print_exc')
    def test_build_2(self, mock_print_exc, mock_rename, mock_timestampstr, mock_isfile, mock_input, mock_choice, mock_write, mock_getcwd, mock_yes_no, mock_no_yes, mock_sleep, mock_parse_args):
        """build failed case"""

        args = ['./mgr.py', 'system', 'build']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = False
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        mock_getcwd.return_value = 'test'

        package = MagicMock()
        get_systempath = MagicMock()
        get_systempath.return_value = '.system'
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).get_systempath = get_systempath
        type(package).name = 'package_name'
        get_package_from_path = MagicMock()
        get_package_from_path.return_value = package
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        ns = MagicMock()
        refresh = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        type(ns).refresh = refresh
        rtc = self.get_rtc()
        type(ns).rtcs = [rtc]
        nss = [ns]
        get_nameservers_from_package = MagicMock(return_value=nss)
        terminate = MagicMock()
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package
        type(self.admin_mock.nameserver).terminate = terminate

        get_connectable_pairs = MagicMock(return_value=[['pair1', 'pair2']])
        type(self.admin_mock.systemeditor).get_connectable_pairs = get_connectable_pairs

        get_port_full_path = MagicMock(side_effect=['full1', 'full2'])
        type(self.admin_mock.systembuilder).get_port_full_path = get_port_full_path

        connect_ports = MagicMock()
        type(self.admin_mock.systembuilder).connect_ports = connect_ports

        get_component_full_path = MagicMock(side_effect=[Exception()])
        type(self.admin_mock.systembuilder).get_component_full_path = get_component_full_path

        ### test ###
        self.assertEqual(-1, self.plugin.build(args))
        get_package_from_path.assert_has_calls([call('test', verbose=True), call('test')])
        mock_sleep.assert_has_calls([call(10)])
        launch_system.assert_called_once()
        refresh.assert_called_once()
        get_port_full_path.assert_any_call('pair1')
        get_port_full_path.assert_any_call('pair2')
        mock_no_yes.assert_has_calls([call('# Connect? (full1->full2)\n')])
        connect_ports.assert_called_once_with('pair1', 'pair2', verbose=True)
        mock_write.assert_any_call('## Connected.\n')
        get_component_full_path.assert_called_once_with(rtc)

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('time.sleep')
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('wasanbon.util.yes_no', side_effect=['no'])
    @mock.patch('os.getcwd')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('builtins.input', return_value='input_test')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    @mock.patch('traceback.print_exc')
    def test_build_3(self, mock_print_exc, mock_rename, mock_timestampstr, mock_isfile, mock_input, mock_choice, mock_write, mock_getcwd, mock_yes_no, mock_no_yes, mock_sleep, mock_parse_args):
        """build aborted case"""

        args = ['./mgr.py', 'system', 'build']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = False
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        mock_getcwd.return_value = 'test'

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).get_systempath = get_systempath
        type(package).name = 'package_name'
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        ns = MagicMock()
        refresh = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        type(ns).refresh = refresh
        rtc = self.get_rtc()
        type(ns).rtcs = [rtc]
        nss = [ns]
        get_nameservers_from_package = MagicMock(return_value=nss)
        terminate = MagicMock()
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package
        type(self.admin_mock.nameserver).terminate = terminate

        get_connectable_pairs = MagicMock(return_value=[['pair1', 'pair2']])
        type(self.admin_mock.systemeditor).get_connectable_pairs = get_connectable_pairs

        get_port_full_path = MagicMock(side_effect=['full1', 'full2'])
        type(self.admin_mock.systembuilder).get_port_full_path = get_port_full_path

        connect_ports = MagicMock()
        type(self.admin_mock.systembuilder).connect_ports = connect_ports

        get_component_full_path = MagicMock(side_effect=['rtc_name'])
        type(self.admin_mock.systembuilder).get_component_full_path = get_component_full_path

        save_to_file = MagicMock(side_effect=[Exception(), None])
        type(self.admin_mock.systemeditor).save_to_file = save_to_file

        exit_all_rtcs = MagicMock()
        type(self.admin_mock.systemlauncher).exit_all_rtcs = exit_all_rtcs

        terminate_system = MagicMock(side_effect=[Exception()])
        type(self.admin_mock.systemlauncher).terminate_system = terminate_system

        ### test ###
        self.assertEqual(-1, self.plugin.build(args))
        get_package_from_path.assert_has_calls([call('test', verbose=True), call('test')])
        mock_sleep.assert_has_calls([call(10)])
        launch_system.assert_called_once()
        refresh.assert_called_once()
        get_port_full_path.assert_any_call('pair1')
        get_port_full_path.assert_any_call('pair2')
        mock_no_yes.assert_has_calls([call('# Connect? (full1->full2)\n')])
        mock_yes_no.assert_has_calls([call('# Save System ?')])
        connect_ports.assert_called_once_with('pair1', 'pair2', verbose=True)
        mock_write.assert_any_call('## Connected.\n')
        get_component_full_path.assert_called_once_with(rtc)
        mock_choice.assert_called_once()
        mock_write.assert_any_call('## Aborted.')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('time.sleep')
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('wasanbon.util.yes_no', side_effect=['yes', 'yes', 'yes', 'yes', 'no', 'yes'])
    @mock.patch('os.getcwd')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('builtins.input', return_value='input_test')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    @mock.patch('traceback.print_exc')
    def test_build_4(self, mock_print_exc, mock_rename, mock_timestampstr, mock_isfile, mock_input, mock_choice, mock_write, mock_getcwd, mock_yes_no, mock_no_yes, mock_sleep, mock_parse_args):
        """build terminate_failed case"""

        args = ['./mgr.py', 'system', 'build']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = False
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        mock_getcwd.return_value = 'test'

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).get_systempath = get_systempath
        type(package).name = 'package_name'
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        ns = MagicMock()
        refresh = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        type(ns).refresh = refresh
        rtc = self.get_rtc()
        type(ns).rtcs = [rtc]
        nss = [ns]
        get_nameservers_from_package = MagicMock(return_value=nss)
        terminate = MagicMock()
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package
        type(self.admin_mock.nameserver).terminate = terminate

        get_connectable_pairs = MagicMock(return_value=[['pair1', 'pair2']])
        type(self.admin_mock.systemeditor).get_connectable_pairs = get_connectable_pairs

        get_port_full_path = MagicMock(side_effect=['full1', 'full2'])
        type(self.admin_mock.systembuilder).get_port_full_path = get_port_full_path

        connect_ports = MagicMock()
        type(self.admin_mock.systembuilder).connect_ports = connect_ports

        get_component_full_path = MagicMock(side_effect=['rtc_name'])
        type(self.admin_mock.systembuilder).get_component_full_path = get_component_full_path

        save_to_file = MagicMock(side_effect=[Exception(), None])
        type(self.admin_mock.systemeditor).save_to_file = save_to_file

        exit_all_rtcs = MagicMock()
        type(self.admin_mock.systemlauncher).exit_all_rtcs = exit_all_rtcs

        terminate_system = MagicMock(side_effect=[Exception()])
        type(self.admin_mock.systemlauncher).terminate_system = terminate_system

        ### test ###
        self.assertEqual(-1, self.plugin.build(args))
        get_package_from_path.assert_has_calls([call('test', verbose=True), call('test')])
        mock_sleep.assert_has_calls([call(10), call(1.0)])
        launch_system.assert_called_once()
        refresh.assert_called_once()
        get_port_full_path.assert_any_call('pair1')
        get_port_full_path.assert_any_call('pair2')
        mock_no_yes.assert_has_calls([call('# Connect? (full1->full2)\n')])
        mock_yes_no.assert_has_calls([call('# Save System ?'), call('# Rename filename? (default:default_system_filepath)'),
                                      call('# New Filename = input_test. Okay?'), call('## Overwrite?'), call('# Okay?'), call('# Okay?')])
        connect_ports.assert_called_once_with('pair1', 'pair2', verbose=True)
        mock_write.assert_any_call('## Connected.\n')
        get_component_full_path.assert_called_once_with(rtc)
        mock_choice.assert_called_once()
        mock_write.assert_any_call('# Input:')
        mock_write.assert_any_call('## Saving to .system/input_test\n')
        mock_write.assert_any_call('## Rename existing file to input_test20211001000000\n')
        mock_write.assert_any_call('# Input Vendor Name:')
        mock_write.assert_any_call('# Input Version:')
        mock_write.assert_any_call('# Input System Name (package_name):')
        mock_write.assert_any_call('# Input Description of System (abstract):')
        mock_write.assert_any_call('## Vendor Name = input_test\n')
        mock_write.assert_any_call('## Version     = input_test\n')
        mock_write.assert_any_call('## System Name = input_test\n')
        mock_write.assert_any_call('## Abstract    = input_test\n')
        mock_write.assert_any_call('# Retry')
        mock_write.assert_any_call('# Saving to .system/input_test\n')
        mock_print_exc.assert_called_once()
        exit_all_rtcs.assert_called_once()
        terminate_system.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('time.sleep')
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('wasanbon.util.yes_no', side_effect=['yes', 'yes', 'yes', 'yes', 'no', 'yes'])
    @mock.patch('os.getcwd', return_value='test')
    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('builtins.input', return_value='input_test')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    @mock.patch('traceback.print_exc')
    def test_build_5(self, mock_print_exc, mock_rename, mock_timestampstr, mock_isfile, mock_input, mock_choice, mock_write, mock_getcwd, mock_yes_no, mock_no_yes, mock_sleep, mock_parse_args):
        """build success case"""

        args = ['./mgr.py', 'system', 'build']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).background_flag = False
        type(options).wakeuptimeout = 10
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).get_systempath = get_systempath
        type(package).name = 'package_name'
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        launch_system = MagicMock()
        type(self.admin_mock.systemlauncher).launch_system = launch_system

        ns = MagicMock()
        refresh = MagicMock()
        type(ns).address = 'localhost'
        type(ns).path = 'ns_path'
        type(ns).refresh = refresh
        rtc = self.get_rtc()
        type(ns).rtcs = [rtc]
        nss = [ns]
        get_nameservers_from_package = MagicMock(return_value=nss)
        terminate = MagicMock()
        type(self.admin_mock.nameserver).get_nameservers_from_package = get_nameservers_from_package
        type(self.admin_mock.nameserver).terminate = terminate

        pairs = [['pair1', 'pair2']]
        get_connectable_pairs = MagicMock(return_value=pairs)
        type(self.admin_mock.systemeditor).get_connectable_pairs = get_connectable_pairs

        get_port_full_path = MagicMock(side_effect=['full1', 'full2'])
        type(self.admin_mock.systembuilder).get_port_full_path = get_port_full_path

        connect_ports = MagicMock()
        type(self.admin_mock.systembuilder).connect_ports = connect_ports

        get_component_full_path = MagicMock(side_effect=['rtc_name'])
        type(self.admin_mock.systembuilder).get_component_full_path = get_component_full_path

        save_to_file = MagicMock(side_effect=[Exception(), None])
        type(self.admin_mock.systemeditor).save_to_file = save_to_file

        exit_all_rtcs = MagicMock()
        type(self.admin_mock.systemlauncher).exit_all_rtcs = exit_all_rtcs

        terminate_system = MagicMock()
        type(self.admin_mock.systemlauncher).terminate_system = terminate_system

        ### test ###
        self.assertEqual(0, self.plugin.build(args))
        get_package_from_path.assert_has_calls([call('test', verbose=True), call('test')])
        mock_sleep.assert_has_calls([call(10), call(1.0)])
        launch_system.assert_called_once()
        refresh.assert_called_once()
        get_port_full_path.assert_any_call('pair1')
        get_port_full_path.assert_any_call('pair2')
        mock_no_yes.assert_has_calls([call('# Connect? (full1->full2)\n')])
        mock_yes_no.assert_has_calls([call('# Save System ?'), call('# Rename filename? (default:default_system_filepath)'),
                                      call('# New Filename = input_test. Okay?'), call('## Overwrite?'), call('# Okay?'), call('# Okay?')])
        connect_ports.assert_called_once_with('pair1', 'pair2', verbose=True)
        mock_write.assert_any_call('## Connected.\n')
        get_component_full_path.assert_called_once_with(rtc)
        mock_choice.assert_called_once()
        mock_write.assert_any_call('# Input:')
        mock_write.assert_any_call('## Saving to .system/input_test\n')
        mock_write.assert_any_call('## Rename existing file to input_test20211001000000\n')
        mock_write.assert_any_call('# Input Vendor Name:')
        mock_write.assert_any_call('# Input Version:')
        mock_write.assert_any_call('# Input System Name (package_name):')
        mock_write.assert_any_call('# Input Description of System (abstract):')
        mock_write.assert_any_call('## Vendor Name = input_test\n')
        mock_write.assert_any_call('## Version     = input_test\n')
        mock_write.assert_any_call('## System Name = input_test\n')
        mock_write.assert_any_call('## Abstract    = input_test\n')
        mock_write.assert_any_call('# Retry')
        mock_write.assert_any_call('# Saving to .system/input_test\n')
        mock_print_exc.assert_called_once()
        exit_all_rtcs.assert_called_once()
        terminate_system.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.open')
    @mock.patch('rtsprofile.rts_profile.RtsProfile')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('wasanbon.util.yes_no', side_effect=['no'])
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.input', return_value='input_test')
    def test_configure_1(self, mock_input, mock_write, mock_yes_no, mock_choice, mock_rtsprofile, mock_open, mock_parse_args):
        """configure abort case"""

        args = ['./mgr.py', 'system', 'configure']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = "systemfile"
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).get_systempath = get_systempath
        type(package).name = 'package_name'
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtsprofile = MagicMock()
        type(rtsprofile).components = [self.get_rtc()]
        mock_rtsprofile.return_value = rtsprofile

        ### test ###
        self.assertEqual(0, self.plugin.configure(args))
        get_package_from_path.assert_called_once()
        mock_open.assert_called_once()
        mock_rtsprofile.assert_called_once()
        mock_yes_no.assert_has_calls([call("Save System?")])
        mock_write.assert_any_call('# Aborted \n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.open')
    @mock.patch('rtsprofile.rts_profile.RtsProfile')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('wasanbon.util.yes_no', side_effect=['yes'])
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.input', return_value='input_test')
    def test_configure_2(self, mock_input, mock_write, mock_no_yes, mock_yes_no, mock_choice, mock_rtsprofile, mock_open, mock_parse_args):
        """configure rename yes case"""

        args = ['./mgr.py', 'system', 'configure']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = "systemfile"
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).get_systempath = get_systempath
        type(package).name = 'package_name'
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtsprofile = MagicMock()
        type(rtsprofile).components = [self.get_rtc()]
        mock_rtsprofile.return_value = rtsprofile

        ### test ###
        self.assertEqual(0, self.plugin.configure(args))
        get_package_from_path.assert_called_once()
        mock_rtsprofile.assert_called_once()
        mock_yes_no.assert_has_calls([call("Save System?")])
        mock_no_yes.assert_has_calls([call('Rename Filename?')])

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.open')
    @mock.patch('rtsprofile.rts_profile.RtsProfile')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('wasanbon.util.yes_no', side_effect=['yes'])
    @mock.patch('wasanbon.util.no_yes', side_effect=['no', 'no'])
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.input', return_value='input_test')
    @mock.patch('os.rename', side_effect=[Exception(), None])
    @mock.patch('traceback.print_exc')
    def test_configure_3(self, mock_print_exc, mock_rename, mock_input, mock_write, mock_no_yes, mock_yes_no, mock_choice, mock_rtsprofile, mock_open, mock_parse_args):
        """configure rename no case"""

        args = ['./mgr.py', 'system', 'configure']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = "systemfile"
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).get_systempath = get_systempath
        type(package).name = 'package_name'
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtsprofile = MagicMock()
        type(rtsprofile).components = [self.get_rtc()]
        mock_rtsprofile.return_value = rtsprofile

        ### test ###
        self.assertEqual(0, self.plugin.configure(args))
        get_package_from_path.assert_called_once()
        mock_rtsprofile.assert_called_once()
        mock_yes_no.assert_has_calls([call("Save System?")])
        mock_no_yes.assert_has_calls([call('Rename Filename?'), call('Rename Filename?')])
        mock_write.assert_any_call('## Exception occurred when renaming file.\n')
        mock_print_exc.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('builtins.open')
    @mock.patch('rtsprofile.rts_profile.RtsProfile')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('wasanbon.util.yes_no', side_effect=['yes'])
    @mock.patch('wasanbon.util.no_yes', side_effect=['no', 'no'])
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.input', return_value='input_test')
    @mock.patch('os.rename')
    @mock.patch('traceback.print_exc')
    def test_configure_4(self, mock_print_exc, mock_rename, mock_input, mock_write, mock_no_yes, mock_yes_no, mock_choice, mock_rtsprofile, mock_open, mock_parse_args):
        """configure rename no case"""

        args = ['./mgr.py', 'system', 'configure']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = "systemfile"
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).get_systempath = get_systempath
        type(package).name = 'package_name'
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtsprofile = MagicMock()
        type(rtsprofile).components = [self.get_rtc()]
        mock_rtsprofile.return_value = rtsprofile

        fout = MagicMock()
        write = MagicMock()
        write.side_effect = [Exception(), None]
        type(fout).write = write
        mock_open.return_value = fout

        ### test ###
        self.assertEqual(0, self.plugin.configure(args))
        get_package_from_path.assert_called_once()
        mock_rtsprofile.assert_called_once()
        mock_yes_no.assert_has_calls([call("Save System?")])
        mock_no_yes.assert_has_calls([call('Rename Filename?'), call('Rename Filename?')])
        mock_write.assert_any_call('## Exception occurred when saving file.\n')
        mock_print_exc.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.listdir')
    @mock.patch('wasanbon.util.choice')
    def test_switch_5(self, mock_choice, mock_listdir, mock_parse_args):
        """switch choice filename case"""

        args = ['./mgr.py', 'system', 'switch', 'none']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        mock_listdir.return_value = ['DefaultSystem.xml']

        ### test ###
        self.assertEqual(0, self.plugin.switch(args))
        get_package_from_path.assert_called_once()
        mock_choice.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.listdir')
    @mock.patch('wasanbon.util.choice')
    @mock.patch('yaml.safe_load')
    @mock.patch('os.path.isdir', return_value=False)
    @mock.patch('os.mkdir')
    @mock.patch('os.rename')
    @mock.patch('yaml.dump')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('sys.stdout.write')
    def test_switch_1(self, mock_write, mock_timestampstr, mock_open, mock_dump, mock_rename, mock_mkdir, mock_isdir, mock_safe_load, mock_choice, mock_listdir, mock_parse_args):
        """switch choice filename case"""

        args = ['./mgr.py', 'system', 'switch', 'DefaultSystem.xml']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).setting_file_path = 'setting_file_path'
        type(package).path = 'path'
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        mock_listdir.return_value = ['DefaultSystem.xml', '.ngdata', 'notxml']

        ### test ###
        self.assertEqual(0, self.plugin.switch(args))
        get_package_from_path.assert_called_once()
        mock_choice.assert_not_called()
        mock_write.assert_any_call('# Select System File is (DefaultSystem.xml).\n')
        mock_mkdir.assert_called_once_with('path/backup')
        mock_rename.assert_called_once_with('setting_file_path', 'path/backup/setting.yaml20211001000000')
        mock_open.assert_has_calls([call('setting_file_path', 'r'), call('setting_file_path', 'w')])

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.listdir', return_value=['DefaultSystem.xml', '.ngdata', 'notxml'])
    @mock.patch('sys.stdout.write')
    def test_list_2(self, mock_write, mock_listdir, mock_parse_args):
        """list normal case"""

        args = ['./mgr.py', 'system', 'list']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).setting_file_path = 'setting_file_path'
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).path = 'path'
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.list(args))
        get_package_from_path.assert_called_once()
        mock_write.assert_any_call('- DefaultSystem.xml\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.listdir', return_value=['DefaultSystem.xml', '.ngdata', 'notxml'])
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open', return_value='open_result')
    @mock.patch('rtsprofile.rts_profile.RtsProfile', side_effect=Exception())
    @mock.patch('traceback.print_exc')
    def test_list_3(self, mock_print_exc, mock_RtsProfile, mock_open, mock_write, mock_listdir, mock_parse_args):
        """list long rtsprofile exception case"""

        args = ['./mgr.py', 'system', 'list']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).setting_file_path = 'setting_file_path'
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).path = 'path'
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.list(args))
        get_package_from_path.assert_called_once()
        mock_open.assert_called_once_with('.system/DefaultSystem.xml', 'r')
        mock_RtsProfile.assert_called_once_with('open_result')
        mock_write.assert_any_call('DefaultSystem.xml : \n')
        mock_write.assert_any_call('  status : error\n')
        mock_print_exc.assert_called_once()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('os.listdir', return_value=['DefaultSystem.xml', '.ngdata', 'notxml'])
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open', return_value='open_result')
    @mock.patch('rtsprofile.rts_profile.RtsProfile')
    @mock.patch('traceback.print_exc')
    def test_list_4(self, mock_print_exc, mock_RtsProfile, mock_open, mock_write, mock_listdir, mock_parse_args):
        """list long case"""

        args = ['./mgr.py', 'system', 'list']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='.system')
        type(package).setting_file_path = 'setting_file_path'
        type(package).default_system_filepath = 'default_system_filepath'
        type(package).path = 'path'
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtsp = MagicMock()
        type(rtsp).id = 'rtsp_id'
        type(rtsp).abstract = 'rtsp_abstract'
        component = MagicMock()
        type(component).instance_name = 'comp_instance_name'
        type(component).id = 'comp_id'
        type(component).path_uri = 'comp_path_uri'
        type(component).is_required = 'comp_is_required'
        type(component).active_configuration_set = 'comp_active_configuration_set'
        configuration_set = MagicMock()
        type(configuration_set).id = 'configuration_set_id'
        configuration_data = MagicMock()
        type(configuration_data).name = 'conf_name'
        type(configuration_data).data = 'conf_data'
        type(configuration_set).configuration_data = [configuration_data]
        type(component).configuration_sets = [configuration_set]
        type(rtsp).components = [component]
        mock_RtsProfile.return_value = rtsp

        ### test ###
        self.assertEqual(0, self.plugin.list(args))
        get_package_from_path.assert_called_once()
        mock_open.assert_called_once_with('.system/DefaultSystem.xml', 'r')
        mock_RtsProfile.assert_called_once_with('open_result')
        mock_write.assert_any_call('DefaultSystem.xml : \n')
        mock_write.assert_any_call('  default  : False\n'),
        mock_write.assert_any_call('  status   : success\n'),
        mock_write.assert_any_call('  id       : rtsp_id\n'),
        mock_write.assert_any_call('  abstract : rtsp_abstract\n'),
        mock_write.assert_any_call('  components:\n'),
        mock_write.assert_any_call('    comp_instance_name : \n'),
        mock_write.assert_any_call('      id                       : comp_id\n'),
        mock_write.assert_any_call('      path_uri                 : comp_path_uri\n'),
        mock_write.assert_any_call('      is_required              : comp_is_required\n'),
        mock_write.assert_any_call('      active_configuration_set : comp_active_configuration_set\n'),
        mock_write.assert_any_call('      configurations_sets :\n'),
        mock_write.assert_any_call('        configuration_set_id : \n'),
        mock_write.assert_any_call('          conf_name : conf_data\n')
        mock_print_exc.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_list_5(self, mock_write, mock_parse_args):
        """list_rtc normal case"""

        args = ['./mgr.py', 'system', 'list_rtc']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = True
        mock_parse_args.return_value = options, args

        package = MagicMock()
        language = 'Python'
        rtcconf_path = 'conf/rtc_py.conf'
        rtcconf_dict = {language: rtcconf_path}
        type(package).rtcconf = rtcconf_dict

        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        rtcconf = {'corba.master_manager': 'corba.master_manager_data', 'corba.nameservers': 'corba.nameservers_data',
                   'manager.components.precreate': 'manager.components.precreate_data'}
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        ### test ###
        self.assertEqual(0, self.plugin.list_rtc(args))
        get_package_from_path.assert_called_once()
        mock_write.assert_any_call('Python :\n'),
        mock_write.assert_any_call('  conf_file : conf/rtc_py.conf\n'),
        mock_write.assert_any_call('  rtcd :\n'),
        mock_write.assert_any_call('    uri            : corba.master_manager_data\n'),
        mock_write.assert_any_call('    nameservers    : corba.nameservers_data\n'),
        mock_write.assert_any_call('    installed_rtcs : manager.components.precreate_data\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch('builtins.print')
    def test_dump_1(self, mock_print, mock_isfile, mock_write, mock_parse_args):
        """dump file not found case"""

        args = ['./mgr.py', 'system', 'dump']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = "systemfile"
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).default_system_filepath = 'default_system_filepath'
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(-1, self.plugin.dump(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_called_once_with('./system/systemfile')
        mock_print.assert_called_once_with('# File Not Found.')
        mock_write.assert_not_called()

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.print')
    @mock.patch('builtins.open', return_value=['open_line_data'])
    def test_dump_2(self, mock_open, mock_print, mock_isfile, mock_write, mock_parse_args):
        """dump file not found case"""

        args = ['./mgr.py', 'system', 'dump']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = None
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).default_system_filepath = 'default_system_filepath'
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.dump(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_called_once_with('default_system_filepath')
        mock_print.assert_not_called()
        mock_open.assert_called_once_with('default_system_filepath', 'r')
        mock_write.assert_called_once_with('open_line_data')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.print')
    @mock.patch('builtins.open', return_value=['open_line_data'])
    @mock.patch('wasanbon.util.yes_no', side_effect=['no'])
    def test_cat_1(self, mock_yes_no, mock_open, mock_print, mock_isfile, mock_write, mock_parse_args):
        """cat abort case"""

        args = ['./mgr.py', 'system', 'cat', 'input_data']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = 'systemfile'
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).default_system_filepath = 'default_system_filepath'
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.cat(args))
        mock_write.assert_any_call('## Input Data is input_data\n')
        get_package_from_path.assert_called_once()
        mock_yes_no.assert_called_once_with('## Write Input Data to ./system/systemfile?')
        mock_write.assert_any_call('## Aborted.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.print')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.util.yes_no', side_effect=['yes'])
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    def test_cat_2(self, mock_rename, mock_timestampstr, mock_yes_no, mock_open, mock_print, mock_isfile, mock_write, mock_parse_args):
        """cat success case"""

        args = ['./mgr.py', 'system', 'cat', 'input_data']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).systemfile = None
        mock_parse_args.return_value = options, args

        package = MagicMock()
        type(package).default_system_filepath = 'default_system_filepath'
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.cat(args))
        mock_write.assert_any_call('## Input Data is input_data\n')
        get_package_from_path.assert_called_once()
        mock_yes_no.assert_called_once_with('## Write Input Data to default_system_filepath?')
        mock_rename.assert_called_once_with('default_system_filepath', 'default_system_filepath20211001000000')
        mock_open.assert_called_once_with('default_system_filepath', 'w')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=False)
    def test_copy_1(self, mock_isfile, mock_write, mock_parse_args):
        """copy file not founded case"""

        args = ['./mgr.py', 'system', 'copy', 'src_file_name', 'dest_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(-1, self.plugin.copy(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_called_once_with('./system/src_file_name')
        mock_write.assert_any_call('## No System File exists.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.util.no_yes', side_effect=['no'])
    def test_copy_2(self, mock_no_yes, mock_isfile, mock_write, mock_parse_args):
        """copy abort case"""

        args = ['./mgr.py', 'system', 'copy', 'src_file_name', 'dest_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.copy(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_has_calls([call('./system/src_file_name'), call('./system/dest_file_name')])
        mock_no_yes.assert_called_once_with('# Overwrite? (./system/dest_file_name):')
        mock_write.assert_any_call('## Aborted.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    @mock.patch('shutil.copyfile')
    def test_copy_3(self, mock_copyfile, mock_rename, mock_timestampstr, mock_no_yes, mock_isfile, mock_write, mock_parse_args):
        """copy normal case"""

        args = ['./mgr.py', 'system', 'copy', 'src_file_name', 'dest_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.copy(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_has_calls([call('./system/src_file_name'), call('./system/dest_file_name')])
        mock_no_yes.assert_called_once_with('# Overwrite? (./system/dest_file_name):')
        mock_rename.assert_called_once_with('./system/dest_file_name', './system/dest_file_name20211001000000')
        mock_copyfile.assert_called_once_with('./system/src_file_name', './system/dest_file_name')
        mock_write.assert_any_call('## Success\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=False)
    def test_delete_1(self, mock_isfile, mock_write, mock_parse_args):
        """delete file not founded case"""

        args = ['./mgr.py', 'system', 'delete', 'src_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(-1, self.plugin.delete(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_called_once_with('./system/src_file_name')
        mock_write.assert_any_call('## No System File exists.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.util.no_yes', side_effect=['no'])
    def test_delete_2(self, mock_no_yes, mock_isfile, mock_write, mock_parse_args):
        """delete abort case"""

        args = ['./mgr.py', 'system', 'delete', 'src_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.delete(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_has_calls([call('./system/src_file_name')])
        mock_no_yes.assert_called_once_with('# Delete? (./system/src_file_name):')
        mock_write.assert_any_call('## Aborted.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('wasanbon.util.no_yes', side_effect=['yes'])
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('os.rename')
    def test_delete_3(self, mock_rename, mock_timestampstr, mock_no_yes, mock_isfile, mock_write, mock_parse_args):
        """delete normal case"""

        args = ['./mgr.py', 'system', 'delete', 'src_file_name']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        mock_parse_args.return_value = options, args

        package = MagicMock()
        get_systempath = MagicMock(return_value='./system')
        type(package).get_systempath = get_systempath
        get_package_from_path = MagicMock(return_value=package)
        type(self.admin_mock.package).get_package_from_path = get_package_from_path

        ### test ###
        self.assertEqual(0, self.plugin.delete(args))
        get_package_from_path.assert_called_once()
        mock_isfile.assert_has_calls([call('./system/src_file_name')])
        mock_no_yes.assert_called_once_with('# Delete? (./system/src_file_name):')
        mock_rename.assert_called_once_with('./system/src_file_name', './system/src_file_name20211001000000')
        mock_write.assert_any_call('## Success\n')


if __name__ == '__main__':
    unittest.main()
