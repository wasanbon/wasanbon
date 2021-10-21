# test for wasanbon/core/plugins/admin/selfupdate_plugin/__init__.py

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
        import wasanbon.core.plugins.admin.selfupdate_plugin as m
        self.admin_mock = MagicMock(spec=['git'])
        self.admin_mock.git(spec=['git_command'])
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()

        ### setting parse_args return option ###
        self.options = self.FunctionList()
        flags = ['verbose_flag', 'force_flag']
        for flag in flags:
            ## default: False ##
            setattr(self.options, flag, False)

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.selfupdate_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.git'], self.plugin.depends())

    @mock.patch('builtins.print')
    def test_print_alternatives(self, mock_print):
        """_print_alternatives normal case"""
        self.plugin._print_alternatives('args')
        mock_print.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.call')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux or darwin'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_run(self, mock_parse_args, mock_chdir, mock_isdir, mock_join, mock_platform, mock_subprocess_call, mock_write):
        """run normal case 
        sys.platform != 'win32'
        """
        ### setting ###
        self.options.force_flag = True
        mock_parse_args.return_value = self.options, ['argv']
        mock_join.return_value = 'joined_path'
        mock_isdir.return_value = True
        mock_subprocess_call.return_value = 0
        ### test ###
        self.assertEqual(0, self.plugin.run(['argv']))
        self.admin_mock.git.git_command.assert_called_once_with(['pull', 'origin', 'release'], verbose=True)
        mock_subprocess_call.assert_called_once_with(['python3', 'setup.py', 'install'])

    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.call')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_run_win32(self, mock_parse_args, mock_chdir, mock_isdir, mock_join, mock_platform, mock_subprocess_call, mock_write):
        """run normal case 
        sys.platform = win32
        """
        ### setting ###
        self.options.force_flag = True
        mock_parse_args.return_value = self.options, ['argv']
        mock_join.return_value = 'joined_path'
        mock_isdir.return_value = True
        mock_subprocess_call.return_value = 0
        ### test ###
        self.assertEqual(0, self.plugin.run(['argv']))
        self.admin_mock.git.git_command.assert_called_once_with(['pull', 'origin', 'release'], verbose=True)
        mock_subprocess_call.assert_called_once_with(['python', 'setup.py', 'install'])

    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.call')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_run_error(self, mock_parse_args, mock_chdir, mock_isdir, mock_join, mock_platform, mock_subprocess_call, mock_write):
        """run error case
        subprocess return != 0
        """
        ### setting ###
        self.options.force_flag = True
        mock_parse_args.return_value = self.options, ['argv']
        mock_join.return_value = 'joined_path'
        mock_isdir.return_value = False
        mock_subprocess_call.return_value = -1
        ### test ###
        self.assertEqual(-1, self.plugin.run(['argv']))
        url = 'https://github.com/wasanbon/wasanbon.git'
        self.admin_mock.git.git_command.assert_called_once_with(['clone', '-b', 'release', url], verbose=True)
        mock_subprocess_call.assert_called_once_with(['python', 'setup.py', 'install'])
        mock_write.assert_any_call('# Error in selfupdating....\n')

    @mock.patch('traceback.print_exc')
    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.call')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.join')
    @mock.patch('os.path.isdir')
    @mock.patch('os.chdir')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_run_error_except(self, mock_parse_args, mock_chdir, mock_isdir, mock_join, mock_platform, mock_subprocess_call, mock_write, mock_print_exc):
        """run error case
        try subprocess , but exception occured
        """
        ### setting ###
        self.options.force_flag = True
        mock_parse_args.return_value = self.options, ['argv']
        mock_join.return_value = 'joined_path'
        mock_isdir.return_value = False
        mock_subprocess_call.return_value = -1
        mock_subprocess_call.side_effect = Exception()
        ### test ###
        self.assertEqual(-1, self.plugin.run(['argv']))
        url = 'https://github.com/wasanbon/wasanbon.git'
        self.admin_mock.git.git_command.assert_called_once_with(['clone', '-b', 'release', url], verbose=True)
        mock_subprocess_call.assert_called_once_with(['python', 'setup.py', 'install'])
        mock_write.assert_any_call('# Exception occured in selfupdating....\n')

    @mock.patch('builtins.print')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_run_error_not_force(self, mock_parse_args, mock_print):
        """run error case
        force_flag = False
        """
        mock_parse_args.return_value = self.options, ['argv']
        self.assertEqual(-1, self.plugin.run(['argv']))
        mock_print.assert_called_once()


if __name__ == '__main__':
    unittest.main()
