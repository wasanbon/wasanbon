# test for wasanbon/core/plugins/admin/environment_plugin/setup/path.py

import unittest
from unittest import mock
from unittest.mock import Mock, call
import os

from wasanbon.core.plugins.admin.environment_plugin.setup import path


class TestPlugin(unittest.TestCase):

    @mock.patch('sys.stdout.write')
    def test_search_command_linux_import_python(self, sys_stdout_write):
        """test for search_command (import python module)"""
        test_module = 'test_hoge'
        test_module_path = 'test_hoge_path'
        test_cmd = 'python_test_hoge'
        test_path = 'test_path'
        test_hints = ['h1', 'h2']
        # mock to import by __import__
        mock_modules = Mock(spec=['__path__'])
        mock_modules.__path__ = [test_module_path]
        import sys
        sys.modules[test_module] = mock_modules
        # test
        ret = path.search_command(
            test_cmd, test_path, test_hints, verbose=True)
        sys_out_calls = [
            call('## Searching Command (%s)\n' % test_cmd),
            call('### Hint: %s\n' % test_hints[0]),
            call('### Hint: %s\n' % test_hints[1]),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        self.assertEqual(ret, test_module_path)

    @mock.patch('sys.stdout.write')
    def test_search_command_linux_failed_to_import_python(self, sys_stdout_write):
        """test for search_command (failed to import python module)"""
        test_cmd = 'python_test_hoge'
        test_path = 'test_path'
        test_hints = ['h1', 'h2']
        ret = path.search_command(
            test_cmd, test_path, test_hints, verbose=True)
        sys_out_calls = [
            call('## Searching Command (%s)\n' % test_cmd),
            call('### Hint: %s\n' % test_hints[0]),
            call('### Hint: %s\n' % test_hints[1]),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        self.assertEqual(ret, '')

    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    def test_search_command_cmd_file_found(self, mock_isfile, sys_stdout_write):
        """test for search_command (not python, path endswith cmd)"""
        test_cmd = 'test_cmd'
        test_path = 'test_path_test_cmd'
        test_hints = ['h1', 'h2']
        mock_isfile.return_value = True
        # test
        ret = path.search_command(
            test_cmd, test_path, test_hints, verbose=True)
        sys_out_calls = [
            call('## Searching Command (%s)\n' % test_cmd),
            call('### Hint: %s\n' % test_hints[0]),
            call('### Hint: %s\n' % test_hints[1]),
            call('## Searching %s ... ' % (test_cmd)),
            call(' Found in %s\n' % test_path)
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        self.assertEqual(ret, test_path)

    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    @mock.patch('os.environ', new={'PATH': ''})
    def test_search_command_linux_cmd_not_in_path_notfoud(self, mock_isfile, sys_stdout_write):
        """test for search_command (not python, cmd file not found, darwin & linux)"""
        test_cmd = 'test_cmd'
        test_path = 'test_path_te,st_cmd'
        test_hints = ['h1', 'h2']
        mock_isfile.return_value = False
        # test
        ret = path.search_command(
            test_cmd, test_path, test_hints, verbose=True)
        sys_out_calls = [
            call('## Searching Command (%s)\n' % test_cmd),
            call('### Hint: %s\n' % test_hints[0]),
            call('### Hint: %s\n' % test_hints[1]),
            call('## Searching %s ... ' % (test_cmd)),
            call(' Not found.\n')
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        self.assertEqual(ret, '')

    @mock.patch('sys.platform', new='linux')
    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile')
    @mock.patch('os.environ', new={'PATH': 'hoge:fuga'})
    def test_search_command_linux_cmd_not_in_path_foud(self, mock_isfile, sys_stdout_write):
        """test for search_command (not python, darwin & linux)"""
        test_cmd = 'test_cmd'
        test_path = 'test_path_te,st_cmd'
        test_hints = ['h1', 'h2']
        mock_isfile.return_value = True
        # test
        ret = path.search_command(
            test_cmd, test_path, test_hints, verbose=True)
        sys_out_calls = [
            call('## Searching Command (%s)\n' % test_cmd),
            call('### Hint: %s\n' % test_hints[0]),
            call('### Hint: %s\n' % test_hints[1]),
            call('## Searching %s ... ' % (test_cmd)),
            call('  Found in %s. \n' % os.path.join('hoge', test_cmd))
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        self.assertEqual(ret, os.path.join('hoge', test_cmd))

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('sys.stdout.write')
    def test_search_command_darwin_cmd_is_java(self, sys_stdout_write):
        """test for search_command (cmd = java, darwin)"""
        test_cmd = 'java'
        test_path = 'test_path_te,st_cmd'
        test_hints = ['h1', 'h2']
        test_mock_return = 'test fugafuga'
        # test
        with mock.patch.object(path, 'check_java_path_in_darwin', return_value=test_mock_return):
            ret = path.search_command(
                test_cmd, test_path, test_hints, verbose=True)
        sys_out_calls = [
            call('## Searching Command (%s)\n' % test_cmd),
            call('### Hint: %s\n' % test_hints[0]),
            call('### Hint: %s\n' % test_hints[1]),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        self.assertEqual(ret, test_mock_return)

    @mock.patch('sys.platform', new='unknown')
    @mock.patch('sys.stdout.write')
    def test_search_command_unknown_platform(self, sys_stdout_write):
        """test for search_command (unknown platform)"""
        test_cmd = 'java'
        test_path = 'test_path_te,st_cmd'
        test_hints = ['h1', 'h2']
        # test
        ret = path.search_command(
            test_cmd, test_path, test_hints, verbose=True)
        sys_out_calls = [
            call('## Searching Command (%s)\n' % test_cmd),
            call('### Hint: %s\n' % test_hints[0]),
            call('### Hint: %s\n' % test_hints[1]),
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        self.assertEqual(ret, '')

    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    def test_check_java_path_in_darwin_not_fount(self, mock_subprocess, sys_stdout_write):
        """test for check_java_path_in_darwin (java not found)"""
        test_cmd = 'test cmd'
        from subprocess import PIPE
        mock_p = Mock()
        mock_p.communicate.return_value = ('', ' No Java runtime present')
        mock_subprocess.return_value = mock_p
        # test
        ret = path.check_java_path_in_darwin(test_cmd, verbose=True)
        sys_out_calls = [
            call('## Searching %s ... ' % (test_cmd)),
            call(' No Java runtime present\n')
        ]
        subprocess_calls = [
            call([test_cmd, '-version'], stdout=PIPE, stderr=PIPE),
        ]
        mock_p_calls = [
            call.wait(),
            call.communicate()
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        mock_subprocess.assert_has_calls(subprocess_calls)
        self.assertEqual(ret, '')
        mock_p.assert_has_calls(mock_p_calls)

    @mock.patch('sys.stdout.write')
    @mock.patch('subprocess.Popen')
    def test_check_java_path_in_darwin_found(self, mock_subprocess, sys_stdout_write):
        """test for check_java_path_in_darwin (java found)"""
        test_cmd = 'test cmd'
        from subprocess import PIPE
        mock_p = Mock()
        mock_p.communicate.return_value = ('', ' Java runtime present')
        mock_subprocess.return_value = mock_p
        # test
        ret = path.check_java_path_in_darwin(test_cmd, verbose=True)
        sys_out_calls = [
            call('## Searching %s ... ' % (test_cmd)),
            call(' Java runtime found.\n')
        ]
        subprocess_calls = [
            call([test_cmd, '-version'], stdout=PIPE, stderr=PIPE),
        ]
        mock_p_calls = [
            call.wait(),
            call.communicate()
        ]
        sys_stdout_write.assert_has_calls(sys_out_calls)
        mock_subprocess.assert_has_calls(subprocess_calls)
        self.assertEqual(ret, "/usr/bin/" + test_cmd)
        mock_p.assert_has_calls(mock_p_calls)


if __name__ == '__main__':
    unittest.main()
