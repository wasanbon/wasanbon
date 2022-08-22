# test for wasanbon/core/plugins/admin/git_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')


class TestPlugin(unittest.TestCase):

    def setUp(self):
        import wasanbon.core.plugins.admin.git_plugin as m
        self.admin_mock = MagicMock(spec=['environment'])
        type(self.admin_mock.environment).path = {}
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        ### setting ###
        from wasanbon.core.plugins.admin.git_plugin import Plugin
        mock_init.return_value = None
        ### test ###
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        ### test ###
        self.assertEqual(['admin.environment'], self.plugin.depends())

    @mock.patch('wasanbon.core.plugins.admin.git_plugin.git_command')
    def test_git_command(self, mock_git_command):
        """git_command normal case"""
        ### setting ###
        mock_git_command.return_value = 'test'
        ### test ###
        self.assertEqual('test', self.plugin.git_command('test_command'))
        mock_git_command.assert_called_once()

    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('wasanbon.get_home_path')
    @mock.patch('os.environ.copy')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd', return_value='cur_dir')
    def test_git_command_1(self, mock_getcwd, mock_chdir, mock_env_copy, mock_get_home_path, mock_PIPE, mock_Popen):
        """git_command normal case
        gitenv['HOME'] exist
        verbose = False
        interractive = False
        pipe = False
        """
        ### setting ###
        mock_env_copy.return_value = {'HOME': 'home'}
        mock_get_home_path.return_value = 'home_path'
        self.admin_mock.environment.path['git'] = 'git'
        p = MagicMock(spec=['wait'])
        mock_Popen.return_value = p
        ### test ###
        from wasanbon.core.plugins.admin.git_plugin import git_command
        self.assertEqual(p, git_command(['cmd']))
        mock_Popen.assert_called_once_with(['git', 'cmd'], env={'HOME': 'home'}, stdout='PIPE', stderr='PIPE')
        p.wait.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    @mock.patch('subprocess.PIPE', new_callable=PropertyMock(return_value='PIPE'))
    @mock.patch('wasanbon.get_home_path')
    @mock.patch('os.environ.copy')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd', return_value='cur_dir')
    def test_git_command_2(self, mock_getcwd, mock_chdir, mock_env_copy, mock_get_home_path, mock_PIPE, mock_Popen, mock_write):
        """git_command normal case
        gitenv['HOME'] not exist
        verbose = True
        interractive = True
        pipe = True
        """
        ### setting ###
        mock_env_copy.return_value = {}
        mock_get_home_path.return_value = 'home_path'
        self.admin_mock.environment.path['git'] = 'git'
        p = MagicMock(spec=['wait'])
        mock_Popen.return_value = p
        ### test ###
        from wasanbon.core.plugins.admin.git_plugin import git_command
        self.assertEqual(p, git_command(['cmd'], verbose=True, pipe=True, interactive=True))
        mock_Popen.assert_called_once_with(['git', 'cmd'], env={'HOME': 'home_path'}, stdout=None, stderr=None)
        p.wait.assert_not_called()
        self.assertEqual(5, mock_write.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('os.environ.copy')
    @mock.patch('os.chdir')
    @mock.patch('os.getcwd', return_value='cur_dir')
    def test_git_command_3(self, mock_getcwd, mock_chdir, mock_env_copy, mock_write):
        """git_command error case
        len(admin.environment.path['git']) == 0
        """
        ### setting ###
        mock_env_copy.return_value = {'HOME': 'home'}
        self.admin_mock.environment.path['git'] = ''
        ### test ###
        from wasanbon.core.plugins.admin.git_plugin import git_command
        self.assertEqual(False, git_command(['cmd']))
        mock_write.assert_called_once()


if __name__ == '__main__':
    unittest.main()
