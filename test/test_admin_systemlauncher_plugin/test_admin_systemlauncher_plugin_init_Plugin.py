# test for wasanbon/core/plugins/admin/systemlauncher_plugin/__init__.py Plugin class

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')


class TestPlugin(unittest.TestCase):

    class FunctionList():
        pass

    def setUp(self):
        ### setting admin mock ###
        import wasanbon.core.plugins.admin.systemlauncher_plugin as m
        self.admin_mock = MagicMock(spec=['rtc', 'systeminstaller'])
        self.admin_mock.rtc(sepc=['get_rtcs_from_package'])
        self.admin_mock.systeminstaller(spec=['get_installed_rtc_names', 'get_rtcd_manager_addresses'])
        #type(self.admin_mock.environment).path = PropertyMock()
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.systemlauncher_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.systeminstaller', 'admin.rtcconf', 'admin.rtc'], self.plugin.depends())

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.launch_rtcd', return_value='process')
    def test_launch_system_1(self, mock_launch_rtcd):
        """ launch_system normal case 
        type(console_bind) != list
        verbose == False
        standalone == False
        """
        ### test ###
        self.plugin.launch_system('pack', console_bind='C++', standalone=False)
        calls = [call('pack', 'C++', verbose=True),
                 call('pack', 'Java', verbose=False),
                 call('pack', 'Python', verbose=False)]
        mock_launch_rtcd.assert_has_calls(calls)

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.launch_standalone_rtcs')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.launch_rtcd', return_value='process')
    def test_launch_system_2(self, mock_launch_rtcd, mock_launch_standalone_rtcs):
        """ launch_system normal case 
        type(console_bind) != list
        verbose == True
        standalone == True
        """
        ### test ###
        self.plugin.launch_system('pack', verbose=True, console_bind='C++', standalone=True)
        calls = [call('pack', 'C++', verbose=True),
                 call('pack', 'Java', verbose=True),
                 call('pack', 'Python', verbose=True)]
        mock_launch_rtcd.assert_has_calls(calls)
        mock_launch_standalone_rtcs.assert_called_once()

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.get_standalone_rtc_pids')
    @mock.patch('sys.stdout.write')
    def test_is_standalone_rtc_launched_1(self, mock_write, mock_rtc_pids, mock_process_iter):
        """is_standalone_rtc_launched normal case
        verbose == True
        proc.status == 'zombie'
        """
        ### setting ###
        mock_rtc_pids.return_value = ['hoge', 'pid']
        proc = MagicMock(spec=['status'])
        type(proc).pid = PropertyMock(return_value='pid')
        proc.status.return_value = 'zombie'
        mock_process_iter.return_value = [proc]
        ### test ###
        self.assertEqual(False, self.plugin.is_standalone_rtc_launched('package', 'command', verbose=True))
        self.assertEqual(2, mock_write.call_count)

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.get_standalone_rtc_pids')
    @mock.patch('sys.stdout.write')
    def test_is_standalone_rtc_launched_2(self, mock_write, mock_rtc_pids, mock_process_iter):
        """is_standalone_rtc_launched normal case
        verbose == False
        proc.status != 'zombie'
        """
        ### setting ###
        mock_rtc_pids.return_value = ['hoge', 'pid']
        proc = MagicMock(spec=['status'])
        type(proc).pid = PropertyMock(return_value='pid')
        proc.status.return_value = 'hoge'
        mock_process_iter.return_value = [proc]
        ### test ###
        self.assertEqual(True, self.plugin.is_standalone_rtc_launched('package', 'command', verbose=False))
        self.assertEqual(0, mock_write.call_count)

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_standalone_rtc_launched')
    def test_is_standalone_rtcs_launched(self, mock_rtc_launched):
        """is_standalone_rtcs_launched normal case"""
        ### setting ###
        package = MagicMock()
        type(package).standalone_rtc_commands = ['command']
        mock_rtc_launched.return_value = True
        ### test ###
        self.assertEqual(True, self.plugin.is_standalone_rtcs_launched(package))

    @mock.patch('os.remove')
    @mock.patch('os.listdir')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_get_standalone_rtc_pids_1(self, mock_join, mock_isdir, mock_mkdir, mock_listdir, mock_remove):
        """get_standalone_rtc_pids normal case
        os.path.isdir = False
        autoremove = False
        """
        ### setting ###
        package = MagicMock()
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc, rtc]
        command = MagicMock(spec=['find'])
        command.find.side_effect = [-1, 0]
        mock_listdir.return_value = ['hoge', 'rtc_rtc_name_123']
        mock_join.side_effect = ['piddir', 'remove_file']
        mock_isdir.return_value = False
        ### test ###
        self.assertEqual([int('123')], self.plugin.get_standalone_rtc_pids(package, command))
        self.assertEqual(1, mock_join.call_count)
        self.assertEqual(2, mock_mkdir.call_count)

    @mock.patch('os.remove')
    @mock.patch('os.listdir')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_get_standalone_rtc_pids_2(self, mock_join, mock_isdir, mock_mkdir, mock_listdir, mock_remove):
        """get_standalone_rtc_pids normal case
        os.path.isdir = True
        autoremove = True
        """
        ### setting ###
        package = MagicMock()
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc, rtc]
        command = MagicMock(spec=['find'])
        command.find.side_effect = [-1, 0]
        mock_listdir.return_value = ['hoge', 'rtc_rtc_name_123']
        mock_join.side_effect = ['piddir', 'remove_file']
        mock_isdir.return_value = True
        ### test ###
        self.assertEqual([int('123')], self.plugin.get_standalone_rtc_pids(package, command, autoremove=True))
        self.assertEqual(2, mock_join.call_count)
        self.assertEqual(0, mock_mkdir.call_count)

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_standalone_rtc_with_command')
    @mock.patch('sys.stdout.write')
    def test_terminate_standalone_rtcs_1(self, mock_write, mock_terminate_rtc):
        """terminate_standalone_rtcs
        verbose=False
        """
        ### setting ###
        package = MagicMock()
        type(package).standalone_rtc_commands = ['hoge']
        mock_terminate_rtc.return_value = 0
        ### test ###
        self.assertEqual(0, self.plugin.terminate_standalone_rtcs(package))
        mock_write.assert_not_called()

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_standalone_rtc_with_command')
    @mock.patch('sys.stdout.write')
    def test_terminate_standalone_rtcs_2(self, mock_write, mock_terminate_rtc):
        """terminate_standalone_rtcs
        verbose=True
        """
        ### setting ###
        package = MagicMock()
        type(package).standalone_rtc_commands = ['hoge']
        mock_terminate_rtc.return_value = -1
        ### test ###
        self.assertEqual(-1, self.plugin.terminate_standalone_rtcs(package, verbose=True))
        mock_write.assert_called_once()

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_standalone_rtc_with_command')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_terminate_standalone_rtc_1(self, mock_join, mock_isdir, mock_mkdir, mock_terminate_rtc):
        """terminate_standalone_rtc normal case
        os.path.isdir = False
        command.find = -1
        """
        ### setting ###
        package = MagicMock()
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        command = MagicMock(spec=['find'])
        command.find.side_effect = [-1]
        type(package).standalone_rtc_commands = [command]
        mock_join.return_value = 'piddir'
        mock_isdir.return_value = False
        mock_terminate_rtc.return_value = 'hoge'
        ### test ###
        self.assertEqual(-1, self.plugin.terminate_standalone_rtc(package, rtc))
        self.assertEqual(2, mock_mkdir.call_count)

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_standalone_rtc_with_command')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_terminate_standalone_rtc_2(self, mock_join, mock_isdir, mock_mkdir, mock_terminate_rtc):
        """terminate_standalone_rtc normal case
        os.path.isdir = True
        command.find = 0
        """
        ### setting ###
        package = MagicMock()
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        command = MagicMock(spec=['find'])
        command.find.side_effect = [0]
        type(package).standalone_rtc_commands = [command]
        mock_join.return_value = 'piddir'
        mock_isdir.return_value = True
        mock_terminate_rtc.return_value = 'hoge'
        ### test ###
        self.assertEqual('hoge', self.plugin.terminate_standalone_rtc(package, rtc))
        self.assertEqual(0, mock_mkdir.call_count)

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.get_standalone_rtc_pids')
    @mock.patch('sys.stdout.write')
    def test_terminate_standalone_rtc_with_command_1(self, mock_write, mock_rtc_pids, mock_process_iter):
        """terminate_standalone_rtc_with_command normal case
        command.find = 0
        command.find(rtc_name) <= 0
        verbose = False
        """
        ### setting ###
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_pacakge.return_value = [rtc]
        command = MagicMock(spec=['find'])
        command.find.side_effect = [-1]
        ### test ###
        self.assertEqual(0, self.plugin.terminate_standalone_rtc_with_command('package', command, verbose=False))

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.get_standalone_rtc_pids')
    @mock.patch('sys.stdout.write')
    def test_terminate_standalone_rtc_with_command_2(self, mock_write, mock_rtc_pids, mock_process_iter):
        """terminate_standalone_rtc_with_command normal case
        command.find = 0
        command.find(rtc_name) >= 0
        verbose = False
        proc.pid != pid
        """
        ### setting ###
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc]
        command = MagicMock(spec=['find'])
        command.find.side_effect = [0]
        mock_rtc_pids.return_value = ['hoge']
        proc = MagicMock(spec=['children', 'kill'])
        type(proc).pid = PropertyMock(return_value='pid')
        proc.children.return_value = 'hoge'
        mock_process_iter.return_value = [proc]
        ### test ###
        self.assertEqual(0, self.plugin.terminate_standalone_rtc_with_command('package', command, verbose=False))
        mock_rtc_pids.assert_called_once()
        mock_write.assert_not_called()

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.get_standalone_rtc_pids')
    @mock.patch('sys.stdout.write')
    def test_terminate_standalone_rtc_with_command_3(self, mock_write, mock_rtc_pids, mock_process_iter):
        """terminate_standalone_rtc_with_command normal case
        command.find = 0
        command.find(rtc_name) >= 0
        verbose = True
        proc.pid != pid
        """
        ### setting ###
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc]
        command = MagicMock(spec=['find'])
        command.find.side_effect = [0]
        mock_rtc_pids.return_value = ['hoge']
        proc = MagicMock(spec=['children', 'kill'])
        type(proc).pid = PropertyMock(return_value='pid')
        proc.children.return_value = 'hoge'
        mock_process_iter.return_value = [proc]
        ### test ###
        self.assertEqual(0, self.plugin.terminate_standalone_rtc_with_command('package', command, verbose=True))
        mock_rtc_pids.assert_called_once()
        mock_write.assert_called_once()

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.get_standalone_rtc_pids')
    @mock.patch('sys.stdout.write')
    def test_terminate_standalone_rtc_with_command_4(self, mock_write, mock_rtc_pids, mock_process_iter):
        """terminate_standalone_rtc_with_command normal case
        command.find = 0
        command.find(rtc_name) >= 0
        verbose = False
        proc.pid == pid
        """
        ### setting ###
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc]
        command = MagicMock(spec=['find'])
        command.find.side_effect = [0]
        mock_rtc_pids.return_value = ['pid']
        proc = MagicMock(spec=['children', 'kill'])
        type(proc).pid = PropertyMock(return_value='pid')
        proc.kill.side_effect = [True]
        child = MagicMock(spec=['kill'])
        type(child).pid = 'pid'
        child.kill.side_effect = [True]
        proc.children.return_value = [child]
        mock_process_iter.return_value = [proc]
        ### test ###
        self.assertEqual(0, self.plugin.terminate_standalone_rtc_with_command('package', command, verbose=False))
        mock_rtc_pids.assert_called_once()
        self.assertEqual(0, mock_write.call_count)
        self.assertEqual(1, child.kill.call_count)
        self.assertEqual(1, proc.kill.call_count)

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.get_standalone_rtc_pids')
    @mock.patch('sys.stdout.write')
    def test_terminate_standalone_rtc_with_command_5(self, mock_write, mock_rtc_pids, mock_process_iter):
        """terminate_standalone_rtc_with_command normal case
        command.find = 0
        command.find(rtc_name) >= 0
        verbose = True
        proc.pid == pid
        """
        ### setting ###
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc]
        command = MagicMock(spec=['find'])
        command.find.side_effect = [0]
        mock_rtc_pids.return_value = [123]
        proc = MagicMock(spec=['children', 'kill'])
        type(proc).pid = PropertyMock(return_value=123)
        proc.kill.side_effect = [True]
        child = MagicMock(spec=['kill'])
        type(child).pid = 123
        child.kill.side_effect = [True]
        proc.children.return_value = [child]
        mock_process_iter.return_value = [proc]
        ### test ###
        self.assertEqual(0, self.plugin.terminate_standalone_rtc_with_command('package', command, verbose=True))
        mock_rtc_pids.assert_called_once()
        self.assertEqual(3, mock_write.call_count)
        self.assertEqual(1, child.kill.call_count)
        self.assertEqual(1, proc.kill.call_count)

    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_standslone_rtc_1(self, mock_join, mock_isdir, mock_mkdir):
        """launch_standalone_rtc normal case
        os.path.isdir = False
        verbose = False
        command < 0
        """
        ### setting ###
        mock_isdir.return_value = False
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        command = MagicMock(spec=['find'])
        command.find.return_value = -1
        package = MagicMock()
        type(package).standalone_rtc_commands = [command]
        ### test ###
        self.assertEqual(0, self.plugin.launch_standalone_rtc(package, rtc))
        self.assertEqual(2, mock_mkdir.call_count)

    @mock.patch('builtins.open')
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_standalone_rtc')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_standalone_rtc_launched')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_standslone_rtc_2(self, mock_join, mock_isdir, mock_mkdir, mock_write, mock_rtc_launch, mock_terminate_rtc, mock_PIPE, mock_Popen, mock_open):
        """launch_standalone_rtc normal case
        os.path.isdir = True
        verbose = True
        command >= 0
        is_standalone_rtc_launched = False
        stdout = True
        """
        ### setting ###
        mock_isdir.return_value = True
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        command = MagicMock(spec=['find'])
        command.find.return_value = 0
        package = MagicMock()
        type(package).standalone_rtc_commands = [command]
        mock_rtc_launch.return_value = False
        ### test ###
        self.assertEqual(0, self.plugin.launch_standalone_rtc(package, rtc, verbose=True, stdout=True))
        self.assertEqual(0, mock_mkdir.call_count)
        self.assertEqual(0, mock_terminate_rtc.call_count)
        self.assertEqual(1, mock_write.call_count)
        mock_Popen.assert_called_once_with(command, stdout=None, stderr=None, shell=True)

    @mock.patch('builtins.open')
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_standalone_rtc')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_standalone_rtc_launched')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_standslone_rtc_3(self, mock_join, mock_isdir, mock_mkdir, mock_write, mock_rtc_launch, mock_terminate_rtc, mock_PIPE, mock_Popen, mock_open):
        """launch_standalone_rtc normal case
        os.path.isdir = True
        verbose = True
        command >= 0
        is_standalone_rtc_launched = True
        stdout = False
        """
        ### setting ###
        mock_isdir.return_value = True
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        command = MagicMock(spec=['find'])
        command.find.return_value = 0
        package = MagicMock()
        type(package).standalone_rtc_commands = [command]
        mock_rtc_launch.return_value = True
        ### test ###
        self.assertEqual(0, self.plugin.launch_standalone_rtc(package, rtc, verbose=True, stdout=False))
        self.assertEqual(0, mock_mkdir.call_count)
        self.assertEqual(1, mock_terminate_rtc.call_count)
        self.assertEqual(1, mock_write.call_count)
        mock_Popen.assert_called_once_with(command, stdout='PIPE', stderr='PIPE', shell=True)

    @mock.patch('sys.stdout.write')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_standslone_rtcs_1(self, mock_join, mock_isdir, mock_mkdir, mock_write):
        """launch_standalone_rtc normal case
        os.path.isdir = False
        verbose = False
        command.find < 0
        """
        ### setting ###
        mock_isdir.return_value = False
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        command = MagicMock(spec=['find'])
        command.find.return_value = -1
        package = MagicMock()
        type(package).standalone_rtc_commands = [command]
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc]
        ### test ###
        self.assertEqual(0, self.plugin.launch_standalone_rtcs(package, verbose=False, stdout=True))
        self.assertEqual(2, mock_mkdir.call_count)
        self.assertEqual(0, mock_write.call_count)

    @mock.patch('builtins.open')
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_standalone_rtc')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_standalone_rtc_launched')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_standslone_rtcs_2(self, mock_join, mock_isdir, mock_mkdir, mock_write, mock_rtc_launch, mock_terminate_rtc, mock_PIPE, mock_Popen, mock_open):
        """launch_standalone_rtc normal case
        os.path.isdir = True
        verbose = True
        command >= 0
        is_standalone_rtc_launched = False
        stdout = True
        """
        ### setting ###
        mock_isdir.return_value = True
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        command = MagicMock(spec=['find'])
        command.find.return_value = 0
        package = MagicMock()
        type(package).standalone_rtc_commands = [command]
        mock_rtc_launch.return_value = False
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc]
        ### test ###
        self.assertEqual(0, self.plugin.launch_standalone_rtcs(package, verbose=True, stdout=True))
        self.assertEqual(0, mock_mkdir.call_count)
        self.assertEqual(0, mock_terminate_rtc.call_count)
        self.assertEqual(1, mock_write.call_count)
        mock_Popen.assert_called_once_with(command, stdout=None, stderr=None, shell=True)

    @mock.patch('builtins.open')
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_standalone_rtc')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_standalone_rtc_launched')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_standslone_rtcs_3(self, mock_join, mock_isdir, mock_mkdir, mock_write, mock_rtc_launch, mock_terminate_rtc, mock_PIPE, mock_Popen, mock_open):
        """launch_standalone_rtc normal case
        os.path.isdir = True
        verbose = True
        command >= 0
        is_standalone_rtc_launched = True
        stdout = False
        """
        ### setting ###
        mock_isdir.return_value = True
        rtc = MagicMock(spec=['rtcprofile'])
        rtc.rtcprofile = MagicMock(spec=['basicInfo'])
        type(rtc.rtcprofile.basicInfo).name = 'rtc_name'
        command = MagicMock(spec=['find'])
        command.find.return_value = 0
        package = MagicMock()
        type(package).standalone_rtc_commands = [command]
        mock_rtc_launch.return_value = True
        self.admin_mock.rtc.get_rtcs_from_package.return_value = [rtc]
        ### test ###
        self.assertEqual(0, self.plugin.launch_standalone_rtcs(package, verbose=True, stdout=False))
        self.assertEqual(0, mock_mkdir.call_count)
        self.assertEqual(1, mock_terminate_rtc.call_count)
        self.assertEqual(1, mock_write.call_count)
        mock_Popen.assert_called_once_with(command, stdout='PIPE', stderr='PIPE', shell=True)

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_standalone_rtcs')
    def test_terminate_system(self, mock_terminate_rtcs, mock_terminate_rtcd):
        """terminate_system normal case"""
        ### test ###
        self.plugin.terminate_system('package')
        mock_terminate_rtcs.assert_called_once()
        self.assertEqual(3, mock_terminate_rtcd.call_count)

    @mock.patch('os.remove')
    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test__get_rtcd_pid_1(self, mock_join, mock_isdir, mock_listdir, mock_remove):
        """_get_rtcd_pid normal case
        os.path.isdir = False
        """
        ### setting ###
        mock_join.return_value = 'piddir'
        mock_isdir.return_value = False
        package = MagicMock()
        type(package).path = ''
        ### test ###
        self.assertEqual([], self.plugin._get_rtcd_pid(package, 'language'))

    @mock.patch('os.remove')
    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test__get_rtcd_pid_2(self, mock_join, mock_isdir, mock_listdir, mock_remove):
        """_get_rtcd_pid normal case
        os.path.isdir = True
        autoremove = False
        """
        ### setting ###
        mock_join.return_value = 'piddir'
        mock_isdir.return_value = True
        package = MagicMock()
        type(package).path = ''
        mock_listdir.return_value = ['hoge', 'rtcd_language_1234']
        ### test ###
        self.assertEqual([1234], self.plugin._get_rtcd_pid(package, 'language'))
        mock_remove.assert_not_called()

    @mock.patch('os.remove')
    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test__get_rtcd_pid_3(self, mock_join, mock_isdir, mock_listdir, mock_remove):
        """_get_rtcd_pid normal case
        os.path.isdir = True
        autoremove = True
        """
        ### setting ###
        mock_join.return_value = 'piddir'
        mock_isdir.return_value = True
        package = MagicMock()
        type(package).path = ''
        mock_listdir.return_value = ['hoge', 'rtcd_language_1234']
        ### test ###
        self.assertEqual([1234], self.plugin._get_rtcd_pid(package, 'language', autoremove=True))
        mock_remove.assert_called_once()

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin._get_rtcd_pid')
    def test_is_rtcd_launched_1(self, mock_rtcd_pid, mock_process_iter):
        """is_rtcd_launched normal case
        proc.pid = pid
        """
        ### setting ###
        mock_rtcd_pid.return_value = ['pid']
        proc = MagicMock()
        type(proc).pid = 'pid'
        mock_process_iter.return_value = [proc]
        ### test ###
        self.assertEqual(True, self.plugin.is_rtcd_launched('package', 'language'))

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin._get_rtcd_pid')
    def test_is_rtcd_launched_2(self, mock_rtcd_pid, mock_process_iter):
        """is_rtcd_launched normal case
        proc.pid != pid
        """
        ### setting ###
        mock_rtcd_pid.return_value = ['pid']
        proc = MagicMock()
        type(proc).pid = 'hoge'
        mock_process_iter.return_value = [proc]
        ### test ###
        self.assertEqual(False, self.plugin.is_rtcd_launched('package', 'language'))

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_standalone_rtc_launched')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_rtcd_launched')
    def test_is_launched_1(self, mock_rtcd_launched, mock_rtc_launched):
        """is_launched normal case
        is_rtcd_launched = False
        is_standalone_rtc_launched = False
        """
        ### setting ###
        package = MagicMock()
        type(package).standalone_rtc_commands = ['command']
        mock_rtcd_launched.return_value = False
        mock_rtc_launched.return_value = False
        ### test ###
        self.assertEqual(False, self.plugin.is_launched(package))
        self.assertEqual(3, mock_rtcd_launched.call_count)
        self.assertEqual(1, mock_rtc_launched.call_count)

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_standalone_rtc_launched')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_rtcd_launched')
    def test_is_launched_2(self, mock_rtcd_launched, mock_rtc_launched):
        """is_launched normal case
        is_rtcd_launched = True
        is_standalone_rtc_launched = False
        """
        ### setting ###
        package = MagicMock()
        type(package).standalone_rtc_commands = ['command']
        mock_rtcd_launched.side_effect = [False, True]
        mock_rtc_launched.return_value = False
        ### test ###
        self.assertEqual(True, self.plugin.is_launched(package))
        self.assertEqual(2, mock_rtcd_launched.call_count)
        self.assertEqual(0, mock_rtc_launched.call_count)

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_standalone_rtc_launched')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_rtcd_launched')
    def test_is_launched_3(self, mock_rtcd_launched, mock_rtc_launched):
        """is_launched normal case
        is_rtcd_launched = False
        is_standalone_rtc_launched = True
        """
        ### setting ###
        package = MagicMock()
        type(package).standalone_rtc_commands = ['command']
        mock_rtcd_launched.return_value = False
        mock_rtc_launched.return_value = True
        ### test ###
        self.assertEqual(True, self.plugin.is_launched(package))
        self.assertEqual(3, mock_rtcd_launched.call_count)
        self.assertEqual(1, mock_rtc_launched.call_count)

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin._get_rtcd_pid')
    @mock.patch('sys.stdout.write')
    def test_terminate_rtcd_1(self, mock_write, mock_rtcd_pid, mock_process_iter):
        """terminate_rtcd normal case
        verbose = False
        proc.pid != pid
        """
        ### setting ###
        mock_rtcd_pid.return_value = ['pid']
        proc = MagicMock(spec=['kill'])
        type(proc).pid = 'hoge'
        mock_process_iter.return_value = [proc]
        package = MagicMock()
        ### test ###
        self.assertEqual(0, self.plugin.terminate_rtcd(package, 'language'))
        proc.kill.assert_not_called()
        mock_write.assert_not_called()

    @mock.patch('psutil.process_iter')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin._get_rtcd_pid')
    @mock.patch('sys.stdout.write')
    def test_terminate_rtcd_2(self, mock_write, mock_rtcd_pid, mock_process_iter):
        """terminate_rtcd normal case
        verbose = True
        proc.pid = pid
        """
        ### setting ###
        mock_rtcd_pid.return_value = [1234]
        proc = MagicMock(spec=['kill'])
        type(proc).pid = 1234
        mock_process_iter.return_value = [proc]
        package = MagicMock()
        ### test ###
        self.assertEqual(0, self.plugin.terminate_rtcd(package, 'language', verbose=True))
        proc.kill.assert_called_once()
        self.assertEqual(2, mock_write.call_count)

    @mock.patch('builtins.open')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_rtcd_launched')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_rtcd_1(self, mock_join, mock_isdir, mock_mkdir, mock_write, mock_rtcd_launched, mock_terminate_rtcd, mock_open):
        """launch_standalone_rtc normal case
        os.path.isdir = True
        is_rtcd_launched = False        
        verbose = False
        len(installed_rtcs) <= 0
        """
        ### setting ###
        mock_isdir.return_value = True
        mock_rtcd_launched.return_value = False
        package = MagicMock()
        self.admin_mock.systeminstaller.get_installed_rtc_names.return_value = ''
        ### test ###
        self.assertEqual(None, self.plugin.launch_rtcd(package, 'language', verbose=False))
        self.assertEqual(0, mock_terminate_rtcd.call_count)

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.start_rtcd')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_rtcd_launched')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_rtcd_2(self, mock_join, mock_isdir, mock_mkdir, mock_write, mock_rtcd_launched, mock_terminate_rtcd, mock_open, mock_start_rtcd):
        """launch_standalone_rtc normal case
        os.path.isdir = True
        is_rtcd_launched = False        
        verbose = True
        len(installed_rtcs) <= 0
        """
        ### setting ###
        mock_isdir.return_value = True
        mock_rtcd_launched.return_value = False
        package = MagicMock()
        self.admin_mock.systeminstaller.get_installed_rtc_names.return_value = 'installed_rtcs'
        process = MagicMock()
        type(process).pid = 'test_pid'
        mock_start_rtcd.return_value = process
        ### test ###
        self.assertEqual(process, self.plugin.launch_rtcd(package, 'language', verbose=True))
        self.assertEqual(0, mock_terminate_rtcd.call_count)
        self.assertEqual(3, mock_write.call_count)

    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.start_rtcd')
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.terminate_rtcd')
    @mock.patch('wasanbon.core.plugins.admin.systemlauncher_plugin.Plugin.is_rtcd_launched')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.mkdir')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.join')
    def test_launch_rtcd_3(self, mock_join, mock_isdir, mock_mkdir, mock_write, mock_rtcd_launched, mock_terminate_rtcd, mock_open, mock_start_rtcd):
        """launch_standalone_rtc normal case
        os.path.isdir = True
        is_rtcd_launched = False        
        verbose = False
        len(installed_rtcs) <= 0
        """
        ### setting ###
        mock_isdir.return_value = True
        mock_rtcd_launched.return_value = False
        package = MagicMock()
        self.admin_mock.systeminstaller.get_installed_rtc_names.return_value = 'installed_rtcs'
        process = MagicMock()
        type(process).pid = 'test_pid'
        mock_start_rtcd.return_value = process
        ### test ###
        self.assertEqual(process, self.plugin.launch_rtcd(package, 'language', verbose=False))
        self.assertEqual(0, mock_terminate_rtcd.call_count)
        self.assertEqual(0, mock_write.call_count)

    @mock.patch('traceback.print_exc')
    @mock.patch('rtshell.rtmgr.get_manager')
    @mock.patch('rtshell.path.cmd_path_to_full_path', return_value='full_path')
    @mock.patch('sys.stdout.write')
    def test_exit_all_rtcs_1(self, mock_write, mock_full_path, mock_get_manager, mock_print_exc):
        """exit_all_rtcs normal case
        verbose = False
        get_manager except ZombieObjectError
        """
        ### setting ###
        package = MagicMock()
        type(package).name = 'pac_name'
        mgr_addrs = {'C++': ['cpp_adr'], 'Java': ['/java_adr'], 'Python': ['python_adr']}
        self.admin_mock.systeminstaller.get_rtcd_manager_addresses.return_value = mgr_addrs
        from rtshell import rts_exceptions
        mock_get_manager.side_effect = rts_exceptions.ZombieObjectError('')
        ### test ###
        self.assertEqual(-1, self.plugin.exit_all_rtcs(package, verbose=False))
        self.assertEqual(1, mock_print_exc.call_count)
        self.assertEqual(5, mock_get_manager.call_count)
        #mock_full_path.assert_has_calls([call('/cpp_adr'), call('/java_adr'), call('/python_adr')])

    @mock.patch('traceback.print_exc')
    @mock.patch('rtshell.rtmgr.get_manager')
    @mock.patch('rtshell.path.cmd_path_to_full_path', return_value='full_path')
    @mock.patch('sys.stdout.write')
    def test_exit_all_rtcs_2(self, mock_write, mock_full_path, mock_get_manager, mock_print_exc):
        """exit_all_rtcs normal case
        verbose = False
        get_manager except NoSuchObjectError
        """
        ### setting ###
        package = MagicMock()
        type(package).name = 'pac_name'
        mgr_addrs = {'C++': ['cpp_adr'], 'Java': ['/java_adr'], 'Python': ['python_adr']}
        self.admin_mock.systeminstaller.get_rtcd_manager_addresses.return_value = mgr_addrs
        from rtshell import rts_exceptions
        mock_get_manager.side_effect = rts_exceptions.NoSuchObjectError('')
        ### test ###
        self.assertEqual(0, self.plugin.exit_all_rtcs(package, verbose=False))
        self.assertEqual(3, mock_get_manager.call_count)
        mock_full_path.assert_has_calls([call('/cpp_adr'), call('/java_adr'), call('/python_adr')])
        self.assertEqual(4, mock_write.call_count)

    @mock.patch('traceback.print_exc')
    @mock.patch('rtshell.rtmgr.get_manager')
    @mock.patch('rtshell.path.cmd_path_to_full_path', return_value='full_path')
    @mock.patch('sys.stdout.write')
    def test_exit_all_rtcs_3(self, mock_write, mock_full_path, mock_get_manager, mock_print_exc):
        """exit_all_rtcs normal case
        verbose = True
        get_manager except NoSuchObjectError
        """
        ### setting ###
        package = MagicMock()
        type(package).name = 'pac_name'
        mgr_addrs = {'C++': ['cpp_adr'], 'Java': ['/java_adr'], 'Python': ['python_adr']}
        self.admin_mock.systeminstaller.get_rtcd_manager_addresses.return_value = mgr_addrs
        from rtshell import rts_exceptions
        mock_get_manager.side_effect = rts_exceptions.NoSuchObjectError('')
        ### test ###
        self.assertEqual(0, self.plugin.exit_all_rtcs(package, verbose=True))
        self.assertEqual(3, mock_get_manager.call_count)
        mock_full_path.assert_has_calls([call('/cpp_adr'), call('/java_adr'), call('/python_adr')])
        self.assertEqual(12, mock_write.call_count)

    @mock.patch('traceback.print_exc')
    @mock.patch('rtshell.rtmgr.get_manager')
    @mock.patch('rtshell.path.cmd_path_to_full_path', return_value='full_path')
    @mock.patch('sys.stdout.write')
    def test_exit_all_rtcs_4(self, mock_write, mock_full_path, mock_get_manager, mock_print_exc):
        """exit_all_rtcs normal case
        verbose = False
        get_manager not raise exception
        len(mgr.components) == 0:
        """
        ### setting ###
        package = MagicMock()
        type(package).name = 'pac_name'
        mgr_addrs = {'C++': ['cpp_adr'], 'Java': ['/java_adr'], 'Python': ['python_adr']}
        self.admin_mock.systeminstaller.get_rtcd_manager_addresses.return_value = mgr_addrs
        from rtshell import rts_exceptions
        mgr = MagicMock()
        type(mgr).components = []
        mock_get_manager.return_value = 'tree', mgr
        ### test ###
        self.assertEqual(0, self.plugin.exit_all_rtcs(package, verbose=False))
        self.assertEqual(3, mock_get_manager.call_count)
        mock_full_path.assert_has_calls([call('/cpp_adr'), call('/java_adr'), call('/python_adr')])
        self.assertEqual(4, mock_write.call_count)

    @mock.patch('traceback.print_exc')
    @mock.patch('rtshell.rtmgr.get_manager')
    @mock.patch('rtshell.path.cmd_path_to_full_path', return_value='full_path')
    @mock.patch('sys.stdout.write')
    def test_exit_all_rtcs_5(self, mock_write, mock_full_path, mock_get_manager, mock_print_exc):
        """exit_all_rtcs normal case
        verbose = True
        get_manager not raise exception
        len(mgr.components) == 0:
        """
        ### setting ###
        package = MagicMock()
        type(package).name = 'pac_name'
        mgr_addrs = {'C++': ['cpp_adr'], 'Java': ['/java_adr'], 'Python': ['python_adr']}
        self.admin_mock.systeminstaller.get_rtcd_manager_addresses.return_value = mgr_addrs
        from rtshell import rts_exceptions
        mgr = MagicMock()
        type(mgr).components = []
        mock_get_manager.return_value = 'tree', mgr
        ### test ###
        self.assertEqual(0, self.plugin.exit_all_rtcs(package, verbose=True))
        self.assertEqual(3, mock_get_manager.call_count)
        mock_full_path.assert_has_calls([call('/cpp_adr'), call('/java_adr'), call('/python_adr')])
        self.assertEqual(12, mock_write.call_count)

    @mock.patch('time.sleep')
    @mock.patch('traceback.print_exc')
    @mock.patch('rtshell.rtmgr.get_manager')
    @mock.patch('rtshell.path.cmd_path_to_full_path', return_value='full_path')
    @mock.patch('sys.stdout.write')
    def test_exit_all_rtcs_6(self, mock_write, mock_full_path, mock_get_manager, mock_print_exc, mock_sleep):
        """exit_all_rtcs normal case
        verbose = False
        get_manager not raise exception
        len(mgr.components) != 0
        try_count = 1
        """
        ### setting ###
        package = MagicMock()
        type(package).name = 'pac_name'
        mgr_addrs = {'C++': ['cpp_adr'], 'Java': ['/java_adr'], 'Python': ['python_adr']}
        self.admin_mock.systeminstaller.get_rtcd_manager_addresses.return_value = mgr_addrs
        from rtshell import rts_exceptions
        mgr = MagicMock()
        r = MagicMock(spec=['exit'])
        type(r).instance_name = PropertyMock(return_value='instance_name')
        type(mgr).components = [r]
        mock_get_manager.return_value = 'tree', mgr
        ### test ###
        self.assertEqual(0, self.plugin.exit_all_rtcs(package, verbose=True, try_count=1))
        self.assertEqual(6, mock_get_manager.call_count)
        mock_full_path.assert_has_calls([call('/cpp_adr'), call('/java_adr'), call('/python_adr')])
        self.assertEqual(18, mock_write.call_count)
        self.assertEqual(3, r.exit.call_count)


if __name__ == '__main__':
    unittest.main()
