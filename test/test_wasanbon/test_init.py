# test for wasanbon/__init__.py

import os
import tempfile
import yaml

import unittest
from unittest import mock
from unittest.mock import call

import wasanbon


class TestPlugin(unittest.TestCase):

    @mock.patch('sys.platform', new='win32')
    @mock.patch('builtins.print')
    def test_get_bin_file_ext_win(self, print_mock):
        """test for get_bin_file_ext win32"""
        ret = wasanbon.get_bin_file_ext()
        self.assertEqual(ret, '.dll')
        print_mock.assert_not_called()

    @mock.patch('sys.platform', new='linux')
    @mock.patch('builtins.print')
    def test_get_bin_file_ext_linux(self, print_mock):
        """test for get_bin_file_ext linux"""
        ret = wasanbon.get_bin_file_ext()
        self.assertEqual(ret, '.so')
        print_mock.assert_not_called()

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('builtins.print')
    def test_get_bin_file_ext_darwin(self, print_mock):
        """test for get_bin_file_ext darwin"""
        ret = wasanbon.get_bin_file_ext()
        self.assertEqual(ret, '.dylib')
        print_mock.assert_not_called()

    @mock.patch('sys.platform', new='aaaa')
    @mock.patch('builtins.print')
    def test_get_bin_file_ext_else(self, print_mock):
        """test for get_bin_file_ext else"""
        with self.assertRaises(wasanbon.UnsupportedPlatformException):
            wasanbon.get_bin_file_ext()
        print_mock.assert_called_once_with(
            '---Unsupported System (%s)' % 'aaaa')

    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('getpass.getpass')
    @mock.patch('builtins.input')
    def test_user_pass(self, input_mock, get_pass_mock, isfile_mock, sys_stdout_write):
        """test for user_pass """
        # mock settings
        test_user = 'aaa'
        test_pass = 'bbb'
        test_token = 'ccc'
        input_mock.side_effect = (test_user, test_token)
        get_pass_mock.return_value = test_pass
        yaml_dict = {'github.com': {
            'username': None,
            'password': None,
            'token': None},
        }
        # make temp file to read in module
        with tempfile.TemporaryDirectory() as tmp:
            test_yaml_path = os.path.join(tmp, 'regsiter.yaml')
            with open(test_yaml_path, 'w') as f:
                yaml.dump(yaml_dict, f)
            wasanbon.register_file = test_yaml_path
            # test
            ret = wasanbon.user_pass()
        self.assertEqual(ret, (test_user, test_pass, test_token))
        sys_calls = [
            call('username:'),
            call('token:'),
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('datetime.datetime')
    def test_timestampstr(self, datetime_mock):
        """test for timestampstr"""
        # mock settings
        test_return = 'test1'
        datetime_mock.now().strftime.return_value = test_return
        ret = wasanbon.timestampstr()
        self.assertEqual(ret, test_return)

    @mock.patch('sys.platform', new='win32')
    @mock.patch('builtins.print')
    def test_get_home_path_win(self, print_mock):
        """test for get_home_path win32"""
        # mock settings
        mock_home = 'test1'
        mock_homedrive = 'test2'
        mock_homepath = 'test3'
        env_dict = {
            'HOME': mock_home,
            'HOMEDRIVE': mock_homedrive,
            'HOMEPATH': mock_homepath,
        }
        with mock.patch.dict(os.environ, env_dict, clear=True):
            ret = wasanbon.get_home_path()
        self.assertEqual(ret, os.path.join(mock_homedrive, mock_homepath))
        print_mock.assert_not_called()

    @mock.patch('sys.platform', new='darwin')
    @mock.patch('builtins.print')
    def test_get_home_path_darwin(self, print_mock):
        """test for get_home_path darwin"""
        # mock settings
        mock_home = 'test1'
        mock_homedrive = 'test2'
        mock_homepath = 'test3'
        env_dict = {
            'HOME': mock_home,
            'HOMEDRIVE': mock_homedrive,
            'HOMEPATH': mock_homepath,
        }
        with mock.patch.dict(os.environ, env_dict, clear=True):
            ret = wasanbon.get_home_path()
        self.assertEqual(ret, mock_home)
        print_mock.assert_not_called()

    @mock.patch('sys.platform', new='linux')
    @mock.patch('builtins.print')
    def test_get_home_path_linux(self, print_mock):
        """test for get_home_path linux"""
        # mock settings
        mock_home = 'test1'
        mock_homedrive = 'test2'
        mock_homepath = 'test3'
        env_dict = {
            'HOME': mock_home,
            'HOMEDRIVE': mock_homedrive,
            'HOMEPATH': mock_homepath,
        }
        with mock.patch.dict(os.environ, env_dict, clear=True):
            ret = wasanbon.get_home_path()
        self.assertEqual(ret, mock_home)
        print_mock.assert_not_called()

    @mock.patch('sys.platform', new='aaaa')
    @mock.patch('builtins.print')
    def test_get_home_path_else(self, print_mock):
        """test for get_home_path else"""
        # mock settings
        mock_home = 'test1'
        mock_homedrive = 'test2'
        mock_homepath = 'test3'
        env_dict = {
            'HOME': mock_home,
            'HOMEDRIVE': mock_homedrive,
            'HOMEPATH': mock_homepath,
        }
        with mock.patch.dict(os.environ, env_dict, clear=True):
            ret = wasanbon.get_home_path()
        self.assertEqual(ret, '')
        print_mock.assert_called_once_with('Unsupported System %s' % 'aaaa')

    def test_get_wasanbon_home(self):
        """test for get_wasanbon_home"""
        # test (in env)
        mock_home = 'test1'
        env_dict = {
            wasanbon.WASANBON_HOME_ENVKEY: mock_home,
        }
        with mock.patch.dict(os.environ, env_dict, clear=True):
            self.assertEqual(wasanbon.get_wasanbon_home(), mock_home)
        # test (no key in env)
        env_dict = {}
        with mock.patch.dict(os.environ, env_dict, clear=True):
            self.assertEqual(wasanbon.get_wasanbon_home(),
                             wasanbon.WASANBON_HOME_DEFAULT)

    @mock.patch('sys.platform', new='win32')
    @mock.patch('wasanbon.core.plugins.admin.environment_plugin')
    def test_load_settings(self, env_plugin_mock):
        """test for load_settings"""
        path_dict = {'key1': 'test1'}
        setting = {'path': path_dict}
        # make temp file to read in module
        with tempfile.TemporaryDirectory() as tmp:
            os.mkdir(os.path.join(tmp, 'settings'))
            test_yaml_path = os.path.join(tmp, 'settings', 'common.yaml')
            with open(test_yaml_path, 'w') as f:
                yaml.dump(setting, f)
            # mock settings
            env_plugin_mock.__path__ = [tmp]
            # test
            ret = wasanbon.load_settings()
        self.assertEqual(ret, {'common': setting})
        self.assertEqual(len(wasanbon.tagdict), 2)

    @mock.patch('sys.platform', new='win32')
    def test_platform_win(self):
        """test for platform win32"""
        ret = wasanbon.platform()
        self.assertEqual(ret, 'windows')

    @mock.patch('sys.platform', new='darwin')
    def test_platform_darwin(self):
        """test for platform darwin"""
        ret = wasanbon.platform()
        self.assertEqual(ret, 'macos')

    @mock.patch('sys.platform', new='linux')
    @mock.patch('distro.linux_distribution', return_value=['Ubuntu'])
    def test_platform_linux_ubuntu(self, _):
        """test for platform linux ubuntu"""
        ret = wasanbon.platform()
        self.assertEqual(ret, 'ubuntu')

    @mock.patch('sys.platform', new='linux')
    @mock.patch('distro.linux_distribution', return_value=['debian'])
    def test_platform_linux_debian(self, _):
        """test for platform linux debian"""
        ret = wasanbon.platform()
        self.assertEqual(ret, 'debian')

    @mock.patch('sys.stdout.write')
    def test_sleep(self, sys_stdout_write):
        """test for sleep"""
        test_interval = 0.2
        wasanbon.sleep(test_interval)
        sys_calls = [
            call('\r# [' + '#' * 1 + ' ' * (29) + ']'),
            call('\n')
        ]
        sys_stdout_write.assert_has_calls(sys_calls)

    @mock.patch('os.path.isfile', return_value=True)
    def test_get_rtm_root(self, _):
        """test for get_rtm_root"""
        # test (have RTM_ROOT)
        mock_rtmroot = 'test1'
        env_dict = {
            'RTM_ROOT': mock_rtmroot,
        }
        with mock.patch.dict(os.environ, env_dict, clear=True):
            ret = wasanbon.get_rtm_root()
        self.assertEqual(ret, mock_rtmroot)
        # test (hit in hints)
        mock_rtmroot = 'test2'
        env_dict = {}
        wasanbon.rtm_root_hints = [mock_rtmroot]
        with mock.patch.dict(os.environ, env_dict, clear=True):
            ret = wasanbon.get_rtm_root()
        self.assertEqual(ret, mock_rtmroot)

    @mock.patch('os.path.isfile', return_value=False)
    def test_get_rtm_root_not_found(self, _):
        """test for get_rtm_root not found"""
        # test
        mock_rtmroot = 'test2'
        env_dict = {}
        wasanbon.rtm_root_hints = [mock_rtmroot]
        with mock.patch.dict(os.environ, env_dict, clear=True):
            ret = wasanbon.get_rtm_root()
        self.assertEqual(ret, '')


if __name__ == '__main__':
    unittest.main()
