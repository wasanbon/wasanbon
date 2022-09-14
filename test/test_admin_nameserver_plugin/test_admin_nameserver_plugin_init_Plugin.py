# test for wasanbon/core/plugins/admin/systeminstaller_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

import wasanbon


def mock_join_func( *args ):
    ret = ""
    for val in args:
        ret = ret + str(val) + '/'
    return ret.rstrip('/')

class TestPlugin(unittest.TestCase):

    def setUp(self):
        import wasanbon.core.plugins.admin.nameserver_plugin as m
        self.admin_mock = MagicMock(spec=['systemeditor'])
        setattr(m, 'admin', self.admin_mock)

        def task_with_wdt(self, func, two, three):
            print(type(func))
            func([])
        task = MagicMock()
        setattr(task, 'task_with_wdt', task_with_wdt)
        setattr(m, 'task', task)

        self.plugin = m.Plugin()
        self.Func = m

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.nameserver_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.systemeditor'], self.plugin.depends())

    def test_get_nameservers_from_package(self):
        """get_nameservers_from_package normal case"""

        package = MagicMock()
        setting = {'nameservers': 'localhost:2809'}
        type(package).setting = setting

        from wasanbon.core.plugins.admin.nameserver_plugin import NameServer
        result = [NameServer('localhost:2809')]

        ### test ###
        self.assertEqual(result[0].path, self.plugin.get_nameservers_from_package(package, verbose=True)[0].path)

    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('rtctree.path.parse_path', return_value=('path', 'port'))
    @mock.patch('sys.stdout.write')
    def test_component_1(self, mock_write, mock_parse_path, mock_RTCTree):
        """component normal case"""

        tree = MagicMock()
        dir_node = MagicMock()
        type(dir_node).is_component = MagicMock(return_value=True)
        type(tree).get_node = MagicMock(return_value=dir_node)
        mock_RTCTree.return_value = tree

        func = MagicMock(return_value='result')

        ### test ###
        self.assertEqual((dir_node, 'result'), self.plugin.component('path', func, verbose=True))

    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('rtctree.path.parse_path', return_value=('path', 'port'))
    @mock.patch('time.sleep')
    @mock.patch('traceback.print_exc')
    @mock.patch('sys.stdout.write')
    def test_component_2(self, mock_write, mock_print_exc, mock_sleep, mock_parse_path, mock_RTCTree):
        """component exception case"""

        tree = MagicMock()
        dir_node = MagicMock()
        type(dir_node).is_component = MagicMock(return_value=True)
        type(tree).get_node = MagicMock(side_effect=Exception())
        mock_RTCTree.return_value = tree

        func = MagicMock(return_value='result')

        ### test ###
        with self.assertRaises(Exception):
            self.assertEqual((dir_node, 'result'), self.plugin.component('path', func, verbose=True))

    @mock.patch('rtctree.path.parse_path')
    @mock.patch('rtctree.tree.RTCTree')
    @mock.patch('sys.stdout.write')
    def test_is_running_1(self, mock_write, mock_RTCTree, mock_parse_path):
        """is_running tree is Not None case"""

        ns = MagicMock()
        type(ns).path = 'ns_path'
        type(ns).tree = None

        import rtctree
        import omniORB
        mock_parse_path.side_effect = [rtctree.exceptions.InvalidServiceError(), omniORB.CORBA.OBJECT_NOT_EXIST(),
                                       ('path', 'port'), ('path', 'port'), ('path', 'port'), ('path', 'port')]

        mock_RTCTree.side_effect = [Exception(), None, MagicMock()]

        ### test ###
        self.assertEqual(True, self.plugin.is_running(ns, try_count=5, verbose=True))
        mock_write.assert_any_call('## Checking Nameservice(ns_path) is running\n')
        mock_write.assert_any_call('### Nameservice(ns_path) is found.\n')

    @mock.patch('os.chdir')
    @mock.patch('os.listdir', return_value=['nameserver_123'])
    @mock.patch('sys.stdout.write')
    def test_get_running_nss_from_pidfile(self, mock_write, mock_listdir, mock_chdir):
        """get_running_nss_from_pidfile normal case"""

        ### test ###
        self.assertEqual([123], self.plugin.get_running_nss_from_pidfile(path='path', verbose=True))

    @mock.patch('os.chdir')
    @mock.patch('os.listdir', return_value=['nameserver_123'])
    @mock.patch('sys.stdout.write')
    def test_get_running_nss_from_pidfile(self, mock_write, mock_listdir, mock_chdir):
        """get_running_nss_from_pidfile normal case"""

        ### test ###
        self.assertEqual([123], self.plugin.get_running_nss_from_pidfile(path='path', verbose=True))

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('os.chdir')
    @mock.patch('os.listdir', return_value=['nameserver_123'])
    @mock.patch('os.remove')
    @mock.patch('sys.stdout.write')
    def test_remove_nss_pidfile(self, mock_write, mock_remove, mock_listdir, mock_chdir, mock_join):
        """remove_nss_pidfile normal case"""

        ### test ###
        self.plugin.remove_nss_pidfile(path='path', verbose=True, pid=123)
        mock_remove.assert_called_once_with('pid/nameserver_123')

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('os.chdir')
    @mock.patch('os.listdir', return_value=['log.dat'])
    @mock.patch('os.remove')
    @mock.patch('sys.stdout.write')
    def test_remove_nss_datfile(self, mock_write, mock_remove, mock_listdir, mock_chdir, mock_join):
        """remove_nss_datfile normal case"""

        ### test ###
        self.plugin.remove_nss_datfile(path='path', verbose=True)
        mock_remove.assert_called_once_with('./log.dat')

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('os.chdir')
    @mock.patch('os.listdir', return_value=['nameserver_123'])
    @mock.patch('os.remove')
    @mock.patch('sys.stdout.write')
    def test_remove_all_nss_pidfile(self, mock_write, mock_remove, mock_listdir, mock_chdir, mock_join):
        """remove_all_nss_pidfile normal case"""

        ### test ###
        self.plugin.remove_nss_pidfile(path='path', verbose=True)
        mock_remove.assert_called_once_with('pid/nameserver_123')

    @mock.patch('sys.stdout.write')
    def test_terminate_1(self, mock_write):
        """terminate adress not localhost case"""

        ns = MagicMock()
        type(ns).address = '192.168.0.1'

        ### test ###
        self.assertEqual(-1, self.plugin.terminate(ns, verbose=True))

    @mock.patch('os.chdir')
    @mock.patch('os.path.isdir', return_value=False)
    @mock.patch('sys.stdout.write')
    def test_terminate_2(self, mock_write, mock_isdir, mock_chdir):
        """terminate pidFilePath not directory case"""

        ns = MagicMock()
        type(ns).address = '127.0.0.1'

        ### test ###
        self.assertEqual(-2, self.plugin.terminate(ns, verbose=True, path='path'))

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.get_running_nss_from_pidfile', return_value=[123])
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.remove_nss_pidfile')
    @mock.patch('os.chdir')
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.listdir', return_value=['omninames_123456'])
    @mock.patch('os.remove')
    @mock.patch('psutil.process_iter')
    @mock.patch('sys.stdout.write')
    def test_terminate_3(self, mock_write, mock_process_iter, mock_remove, mock_listdir, mock_isdir, mock_chdir, mock_remove_nss_pidfile, mock_get_running_nss_from_pidfile, mock_join):
        """terminate pidFilePath normal case"""

        ns = MagicMock()
        type(ns).address = '127.0.0.1'

        proc = MagicMock()
        kill = MagicMock()
        type(proc).pid = 123
        type(proc).kill = kill
        mock_process_iter.return_value = [proc]

        ### test ###
        self.assertEqual(0, self.plugin.terminate(ns, verbose=True, path='path', logdir='./log'))
        kill.assert_called_once()
        mock_remove.assert_called_once_with('./log/omninames_123456')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.launch', return_value=0)
    @mock.patch('sys.stdout.write')
    def test_start_1(self, mock_write, mock_launch, mock_parse_args):
        """start success case"""

        args = ['wasanbon-admin.py', 'nameserver', 'start']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        type(options).port = 2809
        type(options).directory = '.wasanbon'
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.start(args))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.launch', return_value=-1)
    @mock.patch('sys.stdout.write')
    def test_start_2(self, mock_write, mock_launch, mock_parse_args):
        """start failed case"""

        args = ['wasanbon-admin.py', 'nameserver', 'start']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        type(options).port = 2809
        type(options).directory = '.wasanbon'
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(-1, self.plugin.start(args))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.terminate', return_value=0)
    @mock.patch('sys.stdout.write')
    def test_stop_1(self, mock_write, mock_launch, mock_parse_args):
        """stop success case"""

        args = ['wasanbon-admin.py', 'nameserver', 'stop']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        type(options).port = 2809
        type(options).directory = '.wasanbon'
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.stop(args))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.terminate', return_value=-1)
    @mock.patch('sys.stdout.write')
    def test_stop_2(self, mock_write, mock_launch, mock_parse_args):
        """stop failed case"""

        args = ['wasanbon-admin.py', 'nameserver', 'stop']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).force_flag = False
        type(options).port = 2809
        type(options).directory = '.wasanbon'
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(-1, self.plugin.stop(args))

    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.stop', return_value=0)
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.start', return_value=0)
    @mock.patch('sys.stdout.write')
    def test_restart_1(self, mock_write, mock_start, mock_stop):
        """restart success case"""

        args = ['wasanbon-admin.py', 'nameserver', 'restart']

        ### test ###
        self.assertEqual(0, self.plugin.restart(args))

    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.stop', return_value=-1)
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.start', return_value=0)
    @mock.patch('sys.stdout.write')
    def test_restart_2(self, mock_write, mock_start, mock_stop):
        """restart failed case"""

        args = ['wasanbon-admin.py', 'nameserver', 'restart']

        ### test ###
        self.assertEqual(-1, self.plugin.restart(args))

    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.stop', return_value=0)
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.start', return_value=-1)
    @mock.patch('sys.stdout.write')
    def test_restart_3(self, mock_write, mock_start, mock_stop):
        """restart failed case"""

        args = ['wasanbon-admin.py', 'nameserver', 'restart']

        ### test ###
        self.assertEqual(-1, self.plugin.restart(args))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.check_global_running', return_value=True)
    @mock.patch('sys.stdout.write')
    def test_check_running_1(self, mock_write, mock_launch, mock_parse_args):
        """check_running running case"""

        args = ['wasanbon-admin.py', 'nameserver', 'check_running']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).port = 2809
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(1, self.plugin.check_running(args))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.check_global_running', return_value=False)
    @mock.patch('sys.stdout.write')
    def test_check_running_2(self, mock_write, mock_launch, mock_parse_args):
        """check_running Not running case"""

        args = ['wasanbon-admin.py', 'nameserver', 'check_running']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).port = 2809
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.check_running(args))

    @mock.patch('psutil.process_iter')
    def test_check_global_running_1(self, mock_process_iter):
        """check_global_running port is None case"""

        process = MagicMock()
        type(process).name = MagicMock(return_value='omniNames')
        mock_process_iter.return_value = [process]

        ### test ###
        self.assertEqual(True, self.plugin.check_global_running())

    @mock.patch('psutil.process_iter')
    def test_check_global_running_2(self, mock_process_iter):
        """check_global_running port in cmdline case"""

        process = MagicMock()
        type(process).name = MagicMock(return_value='omniNames')
        type(process).cmdline = MagicMock(return_value=['2809'])
        mock_process_iter.return_value = [process]

        ### test ###
        self.assertEqual(True, self.plugin.check_global_running(port=2809))

    @mock.patch('psutil.process_iter')
    def test_check_global_running_3(self, mock_process_iter):
        """check_global_running port not in cmdline case"""

        process = MagicMock()
        type(process).name = MagicMock(return_value='omniNames')
        type(process).cmdline = MagicMock(return_value=['2810'])
        mock_process_iter.return_value = [process]

        ### test ###
        self.assertEqual(False, self.plugin.check_global_running(port=2809))

    @mock.patch('psutil.process_iter')
    def test_check_global_running_4(self, mock_process_iter):
        """check_global_running process none"""

        process = MagicMock()
        type(process).name = MagicMock(return_value='omniNames')
        type(process).cmdline = MagicMock(return_value=['2810'])
        mock_process_iter.return_value = []

        ### test ###
        self.assertEqual(False, self.plugin.check_global_running(port=2809))

    @mock.patch('psutil.process_iter')
    def test_check_global_running_5(self, mock_process_iter):
        """check_global_running AccessDenied"""

        import psutil
        process = MagicMock()
        type(process).name = MagicMock(return_value='omniNames', side_effect=psutil.AccessDenied())
        type(process).cmdline = MagicMock(return_value=['2809'])
        mock_process_iter.return_value = [process]

        ### test ###
        self.assertEqual(False, self.plugin.check_global_running(port=2809))

    @mock.patch('psutil.process_iter')
    def test_check_global_running_6(self, mock_process_iter):
        """check_global_running ZombieProcess"""

        import psutil
        process = MagicMock()
        type(process).name = MagicMock(return_value='omniNames', side_effect=psutil.ZombieProcess(1))
        type(process).cmdline = MagicMock(return_value=['2809'])
        mock_process_iter.return_value = [process]

        ### test ###
        self.assertEqual(False, self.plugin.check_global_running(port=2809))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.NameServer')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.check_global_running', return_value=True)
    @mock.patch('sys.stdout.write')
    def test_tree_1(self, mock_write, mock_check_global_running, mock_Nameserver, mock_parse_args):
        """tree normal case"""

        args = ['wasanbon-admin.py', 'nameserver', 'tree']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = True
        type(options).detail_flag = True
        type(options).port = 2809
        type(options).url = 'localhost'
        mock_parse_args.return_value = options, args

        ns = MagicMock()
        type(ns).yaml_dump = MagicMock()
        mock_Nameserver.return_value = ns

        ### test ###
        self.assertEqual(0, self.plugin.tree(args))

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.NameServer')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.check_global_running', return_value=False)
    @mock.patch('sys.stdout.write')
    def test_tree_2(self, mock_write, mock_check_global_running, mock_Nameserver, mock_parse_args):
        """tree Nameserver is not runnning case"""

        args = ['wasanbon-admin.py', 'nameserver', 'tree']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).long_flag = True
        type(options).detail_flag = True
        type(options).port = 2809
        type(options).url = 'localhost'
        mock_parse_args.return_value = options, args

        ns = MagicMock()
        type(ns).yaml_dump = MagicMock()
        mock_Nameserver.return_value = ns

        ### test ###
        self.assertEqual(-1, self.plugin.tree(args))
        mock_write.assert_any_call('## Nameserver is not running.\n')
        mock_write.assert_any_call('Timeout\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.component', return_value=(MagicMock(), True))
    @mock.patch('sys.stdout.write')
    def test_configure_1(self, mock_write, mock_component, mock_parse_args):
        """configure normal case"""

        args = ['wasanbon-admin.py', 'nameserver', 'configure', 'rtc_path', 'key', 'value']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).set_name = 'default'
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.configure(args))
        mock_write.assert_any_call(' PATH: rtc_path\n')
        mock_write.assert_any_call(' KEY: key\n')
        mock_write.assert_any_call(' VALUE: value\n')
        mock_write.assert_any_call('Success.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.component', return_value=(MagicMock(), False))
    @mock.patch('sys.stdout.write')
    def test_configure_2(self, mock_write, mock_component, mock_parse_args):
        """configure failed case"""

        args = ['wasanbon-admin.py', 'nameserver', 'configure', 'rtc_path', 'key', 'value']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).set_name = 'default'
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.configure(args))
        mock_write.assert_any_call(' PATH: rtc_path\n')
        mock_write.assert_any_call(' KEY: key\n')
        mock_write.assert_any_call(' VALUE: value\n')
        mock_write.assert_any_call('Failed.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.component', side_effect=Exception())
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_configure_3(self, mock_print_exc, mock_write, mock_component, mock_parse_args):
        """configure failed case"""

        args = ['wasanbon-admin.py', 'nameserver', 'configure', 'rtc_path', 'key', 'value']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).set_name = 'default'
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(-1, self.plugin.configure(args))
        mock_write.assert_any_call(' PATH: rtc_path\n')
        mock_write.assert_any_call(' KEY: key\n')
        mock_write.assert_any_call(' VALUE: value\n')
        mock_write.assert_any_call('Failed. Exception occured.\n')
        mock_write.assert_any_call('Timeout\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.component')
    @mock.patch('sys.stdout.write')
    def test_activate_rtc(self, mock_write, mock_component, mock_parse_args):
        """activate_rtc normal case"""

        args = ['wasanbon-admin.py', 'nameserver', 'activate_rtc', 'rtc_path']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.activate_rtc(args))
        mock_write.assert_any_call('# Activating RTC (rtc_path)\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.component')
    @mock.patch('sys.stdout.write')
    def test_deactivate_rtc(self, mock_write, mock_component, mock_parse_args):
        """deactivate_rtc normal case"""

        args = ['wasanbon-admin.py', 'nameserver', 'deactivate_rtc', 'rtc_path']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.deactivate_rtc(args))
        mock_write.assert_any_call('# Deactivating RTC (rtc_path)\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.component')
    @mock.patch('sys.stdout.write')
    def test_reset_rtc(self, mock_write, mock_component, mock_parse_args):
        """reset_rtc normal case"""

        args = ['wasanbon-admin.py', 'nameserver', 'reset_rtc', 'rtc_path']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.reset_rtc(args))
        mock_write.assert_any_call('# Resetting RTC (rtc_path)\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.component')
    @mock.patch('sys.stdout.write')
    def test_exit_rtc(self, mock_write, mock_component, mock_parse_args):
        """exit_rtc normal case"""

        args = ['wasanbon-admin.py', 'nameserver', 'exit_rtc', 'rtc_path']
        options = MagicMock()
        type(options).verbose_flag = True
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.exit_rtc(args))
        mock_write.assert_any_call('# Exiting RTC (rtc_path)\n')

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('os.path.isdir', return_value=False)
    @mock.patch('os.mkdir')
    @mock.patch('os.chdir')
    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.get_running_nss_from_pidfile', return_value=[123])
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.remove_nss_pidfile')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.remove_nss_datfile')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('subprocess.Popen')
    @mock.patch('os.getcwd', return_value='.')
    @mock.patch('builtins.open')
    @mock.patch('time.sleep')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.disable_sig')
    @mock.patch('sys.stdout.write')
    def test_launch_1(self, mock_write, mock_disable_sig, mock_sleep, mock_open, mock_getcwd, mock_Popen, mock_platform, mock_remove_nss_datfile,
                      mock_remove_nss_pidfile, mock_get_running_nss_from_pidfile, mock_process_iter, mock_chdir, mock_mkdir, mock_isdir, mock_join):
        """launch not win32 normal case"""

        ns = MagicMock()
        type(ns).address = 'localhost'
        type(ns).port = 2809
        type(ns).pidFilePath = 'pidFilePath'

        import psutil
        proc = MagicMock()
        kill = MagicMock(side_effect=[psutil.AccessDenied(), 0])
        type(proc).pid = 123
        type(proc).name = MagicMock(return_value='omniNames')
        type(proc).kill = kill
        mock_process_iter.return_value = [proc, proc]

        process = MagicMock()
        type(process).pid = 123

        ### test ###
        self.assertEqual(0, self.plugin.launch(ns, verbose=True, force=True, path='path'))
        mock_remove_nss_datfile.assert_called_once_with(path='path', verbose=True)
        mock_Popen.assert_called_once_with(['rtm-naming', '-p', 2809, '-f'], creationflags=0, stdout=None,
                                           stdin=None, stderr=None, preexec_fn=mock_disable_sig)
        mock_open.assert_called_once_with('pid/nameserver_123', 'w')
        mock_write.assert_any_call("### Command:['rtm-naming', '-p', 2809, '-f']\n")
        mock_write.assert_any_call('## Creating PID file (123)\n')
        mock_write.assert_any_call('### Filename :./pid/nameserver_123\n')

    @mock.patch('os.environ', new_callable=PropertyMock(return_value={'RTM_ROOT':'/usr/include/openrtm-1.2'}))
    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('os.path.isdir', return_value=False)
    @mock.patch('os.mkdir')
    @mock.patch('os.chdir')
    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.get_running_nss_from_pidfile', return_value=[123])
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.remove_nss_pidfile')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.Plugin.remove_nss_datfile')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('subprocess.Popen')
    @mock.patch('os.getcwd', return_value='.')
    @mock.patch('builtins.open')
    @mock.patch('time.sleep')
    @mock.patch('wasanbon.core.plugins.admin.nameserver_plugin.disable_sig')
    @mock.patch('sys.stdout.write')
    def test_launch_2(self, mock_write, mock_disable_sig, mock_sleep, mock_open, mock_getcwd, mock_Popen, mock_platform, mock_remove_nss_datfile,
                      mock_remove_nss_pidfile, mock_get_running_nss_from_pidfile, mock_process_iter, mock_chdir, mock_mkdir, mock_isdir, mock_join, mock_environ):
        """launch win32 normal case"""

        ns = MagicMock()
        type(ns).address = 'localhost'
        type(ns).port = 2809
        type(ns).pidFilePath = 'pidFilePath'

        import psutil
        proc = MagicMock()
        kill = MagicMock(side_effect=[psutil.AccessDenied(), 0])
        type(proc).pid = 123
        type(proc).name = MagicMock(return_value='omniNames')
        type(proc).kill = kill
        mock_process_iter.return_value = [proc, proc]

        process = MagicMock()
        type(process).pid = 123

        ### test ###
        self.assertEqual(0, self.plugin.launch(ns, verbose=True, force=True, path='path'))
        mock_remove_nss_datfile.assert_called_once_with(path='path', verbose=True)
        mock_Popen.assert_called_once_with(['/usr/include/openrtm-1.2/bin/rtm-naming.bat', 2809, '-f'],
                                           creationflags=512, stdout=None, stdin=None, stderr=None, preexec_fn=None)
        mock_open.assert_called_once_with('pid/nameserver_123', 'w')
        mock_write.assert_any_call("### Command:['/usr/include/openrtm-1.2/bin/rtm-naming.bat', 2809, '-f']\n")
        mock_write.assert_any_call('## Creating PID file (123)\n')
        mock_write.assert_any_call('### Filename :./pid/nameserver_123\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    def test_list_connectable_pair_1(self, mock_write, mock_parse_args):
        """list_connectable_pair normal case"""

        args = ['wasanbon-admin.py', 'nameserver', 'list_connectable_pair']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).nameservers = 'localhost:2809'
        mock_parse_args.return_value = options, args

        port1 = MagicMock()
        owner1 = MagicMock()
        type(owner1).full_path = ['', 'full_path1']
        type(port1).name = 'prefix.port_name1'
        type(port1).owner = owner1
        type(port1).get_connections_by_dest = MagicMock(return_value='')
        port2 = MagicMock()
        owner2 = MagicMock()
        type(owner2).full_path = ['', 'full_path2']
        type(port2).name = 'prefix.port_name2'
        type(port2).owner = owner2
        port3 = MagicMock()
        owner3 = MagicMock()
        type(owner3).full_path = ['', 'full_path3']
        type(port3).name = 'prefix.port_name3'
        type(port3).owner = owner3
        type(port3).get_connections_by_dest = MagicMock(return_value='conncted')
        port4 = MagicMock()
        owner4 = MagicMock()
        type(owner4).full_path = ['', 'full_path4']
        type(port4).name = 'prefix.port_name4'
        type(port4).owner = owner4

        pair1 = (port1, port2)
        pair2 = (port3, port4)

        type(self.admin_mock.systemeditor).get_connectable_pairs = MagicMock(return_value=[pair1, pair2])

        ### test ###
        self.assertEqual(0, self.plugin.list_connectable_pair(args))
        mock_write.assert_any_call('/full_path1:port_name1     /full_path2:port_name2\n')
        mock_write.assert_any_call('/full_path3:port_name3 ==> /full_path4:port_name4\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_list_connectable_pair_2(self, mock_print_exc, mock_write, mock_parse_args):
        """list_connectable_pair failed case"""

        args = ['wasanbon-admin.py', 'nameserver', 'list_connectable_pair']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).nameservers = 'localhost:2809'
        mock_parse_args.return_value = options, args

        port1 = MagicMock()
        owner1 = MagicMock()
        type(owner1).full_path = ['', 'full_path1']
        type(port1).name = 'prefix.port_name1'
        type(port1).owner = owner1
        type(port1).get_connections_by_dest = MagicMock(return_value='')
        port2 = MagicMock()
        owner2 = MagicMock()
        type(owner2).full_path = ['', 'full_path2']
        type(port2).name = 'prefix.port_name2'
        type(port2).owner = owner2
        port3 = MagicMock()
        owner3 = MagicMock()
        type(owner3).full_path = ['', 'full_path3']
        type(port3).name = 'prefix.port_name3'
        type(port3).owner = owner3
        import omniORB
        type(port3).get_connections_by_dest = MagicMock(side_effect=omniORB.CORBA.OBJECT_NOT_EXIST())
        port4 = MagicMock()
        owner4 = MagicMock()
        type(owner4).full_path = ['', 'full_path4']
        type(port4).name = 'prefix.port_name4'
        type(port4).owner = owner4

        pair1 = (port1, port2)
        pair2 = (port3, port4)

        type(self.admin_mock.systemeditor).get_connectable_pairs = MagicMock(return_value=[pair1, pair2])

        ### test ###
        self.assertEqual(-1, self.plugin.list_connectable_pair(args))
        mock_write.assert_any_call('Failed. CORBA Exception occured.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('rtshell.path')
    @mock.patch('rtshell.rtcon.connect_ports')
    @mock.patch('sys.stdout.write')
    def test_connect_1(self, mock_write, mock_connect_ports, mock_path, mock_parse_args):
        """list_connectable_pair normal case"""

        args = ['wasanbon-admin.py', 'nameserver', 'connect', 'path1', 'path2']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).no_dups = True
        type(options).name = None
        type(options).id = ''
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.connect(args))
        mock_write.assert_any_call('Success.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('rtshell.path')
    @mock.patch('rtshell.rtcon.connect_ports')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_connect_2(self, mock_print_exc, mock_write, mock_connect_ports, mock_path, mock_parse_args):
        """list_connectable_pair exception case"""

        args = ['wasanbon-admin.py', 'nameserver', 'connect', 'path1', 'path2']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).no_dups = True
        type(options).name = None
        type(options).id = ''
        mock_parse_args.return_value = options, args

        mock_connect_ports.side_effect = Exception()

        ### test ###
        self.assertEqual(-1, self.plugin.connect(args))
        mock_write.assert_any_call('Failed. Exception occured.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('rtshell.path')
    @mock.patch('rtshell.rtdis.disconnect_ports')
    @mock.patch('sys.stdout.write')
    def test_disconnect_1(self, mock_write, mock_connect_ports, mock_path, mock_parse_args):
        """list_connectable_pair normal case"""

        args = ['wasanbon-admin.py', 'nameserver', 'disconnect', 'path1', 'path2']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).no_dups = True
        type(options).name = None
        type(options).id = ''
        mock_parse_args.return_value = options, args

        ### test ###
        self.assertEqual(0, self.plugin.disconnect(args))
        mock_write.assert_any_call('Success.\n')

    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    @mock.patch('rtshell.path')
    @mock.patch('rtshell.rtdis.disconnect_ports')
    @mock.patch('sys.stdout.write')
    @mock.patch('traceback.print_exc')
    def test_disconnect_2(self, mock_print_exc, mock_write, mock_connect_ports, mock_path, mock_parse_args):
        """list_connectable_pair exception case"""

        args = ['wasanbon-admin.py', 'nameserver', 'disconnect', 'path1', 'path2']
        options = MagicMock()
        type(options).verbose_flag = True
        type(options).no_dups = True
        type(options).name = None
        type(options).id = ''
        mock_parse_args.return_value = options, args

        mock_connect_ports.side_effect = Exception()

        ### test ###
        self.assertEqual(-1, self.plugin.disconnect(args))
        mock_write.assert_any_call('Failed. Exception occured.\n')


if __name__ == '__main__':
    unittest.main()
