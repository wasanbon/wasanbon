# test for wasanbon/core/plugins/admin/environment_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    class FunctionList():
        pass

    def setUp(self):
        import wasanbon.core.plugins.admin.environment_plugin as m
        self.plugin = m.Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init_(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.environment_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin.path', new={'a': 1, 'b': 2, 'c': 3})
    def test_status(self, mock_write):
        """status normal case"""
        ### test ###
        calls = [
            call('# Showing the status of wasanbon environment initialization...\n'),
            call('%s : %s\n' % ('a', 1)),
            call('%s : %s\n' % ('b', 2)),
            call('%s : %s\n' % ('c', 3))
        ]
        self.assertEqual(0, self.plugin.status([]))
        mock_write.assert_has_calls(calls)

    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin._update_path')
    def test_update_path(self, mock_update_path):
        """update_path normal case"""
        ### test ###
        self.assertEqual(0, self.plugin.update_path([]))
        mock_update_path.assert_any_call(verbose=True)

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin._update_path')
    def test_init(self, mock_update_path, mock_write):
        """init normal case"""
        ### test ###
        self.assertEqual(0, self.plugin.update_path([]))
        mock_update_path.assert_any_call(verbose=True)

    @mock.patch('yaml.dump', return_value='')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux or darwin'))
    @mock.patch('wasanbon.user_pass')
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_register_1(self, mock_parse_args, mock_isfile, mock_open, mock_write, mock_user_pass, mock_platform, mock_yaml_dump):
        """register normal case
        os.path.isfile == True
        sys.platform != win32
        """
        ### setting ###
        options = MagicMock()
        open_ret = MagicMock(spec=['close', 'write'])
        mock_parse_args.return_value = options, None
        mock_isfile.return_value = True
        mock_open.return_value = open_ret
        mock_user_pass.return_value = 'user', 'passwd', 'token'
        ### test ###
        self.assertEqual(0, self.plugin.register([]))
        self.assertEqual(3, mock_write.call_count)
        self.assertEqual(2, mock_open.call_count)

    @mock.patch('yaml.dump', return_value='')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux or darwin'))
    @mock.patch('wasanbon.user_pass')
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_register_2(self, mock_parse_args, mock_isfile, mock_open, mock_write, mock_user_pass, mock_platform, mock_yaml_dump):
        """register normal case
        os.path.isfile == False
        sys.platform != win32
        """
        ### setting ###
        options = MagicMock()
        open_ret = MagicMock(spec=['close', 'write'])
        mock_isfile.return_value = False
        mock_parse_args.return_value = options, None
        mock_open.return_value = open_ret
        mock_user_pass.return_value = 'user', 'passwd', 'token'
        ### test ###
        self.assertEqual(0, self.plugin.register([]))
        self.assertEqual(3, mock_write.call_count)
        self.assertEqual(1, mock_open.call_count)

    @mock.patch('builtins.input')
    @mock.patch('yaml.dump', return_value='')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('wasanbon.user_pass')
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_register_3(self, mock_parse_args, mock_isfile, mock_open, mock_write, mock_user_pass, mock_platform, mock_yaml_dump, mock_input):
        """register normal case
        os.path.isfile == False
        sys.platform == win32
        len(options.compiler)==0
        """
        ### setting ###
        options = MagicMock()
        type(options).compiler = ''
        open_ret = MagicMock(spec=['close', 'write'])
        mock_isfile.return_value = False
        mock_parse_args.return_value = options, None
        mock_open.return_value = open_ret
        mock_user_pass.return_value = 'user', 'passwd', 'token'
        ### test ###
        self.assertEqual(0, self.plugin.register([]))
        self.assertEqual(4, mock_write.call_count)
        self.assertEqual(1, mock_open.call_count)
        mock_input.assert_called_once()

    @mock.patch('yaml.dump', return_value='')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('wasanbon.user_pass')
    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_register_4(self, mock_parse_args, mock_isfile, mock_open, mock_write, mock_user_pass, mock_platform, mock_yaml_dump):
        """register normal case
        os.path.isfile == False
        sys.platform == win32
        len(options.compiler)!=0
        """
        ### setting ###
        options = MagicMock()
        type(options).compiler = 'hoge'
        open_ret = MagicMock(spec=['close', 'write'])
        mock_isfile.return_value = False
        mock_parse_args.return_value = options, None
        mock_open.return_value = open_ret
        mock_user_pass.return_value = 'user', 'passwd', 'token'
        ### test ###
        self.assertEqual(0, self.plugin.register([]))
        self.assertEqual(3, mock_write.call_count)
        self.assertEqual(1, mock_open.call_count)

    @mock.patch('sys.stdout.write')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile')
    @mock.patch('wasanbon.core.plugins.PluginFunction.parse_args')
    def test_register_except(self, mock_parse_args, mock_isfile, mock_open, mock_write):
        """register except case
        os.path.isfile == True
        open Exception
        """
        ### setting ###
        mock_parse_args.return_value = None, None
        mock_isfile.return_value = True
        mock_open.side_effect = Exception()
        ### test ###
        self.assertEqual(-1, self.plugin.register([]))
        mock_write.assert_called_once()

    @mock.patch('os.path.join')
    @mock.patch('os.path.isdir')
    def test_setting_path(self, os_path_isdir, os_path_join):
        """setting_path normal case"""
        os_path_join.return_value = 'test'
        os_path_isdir.return_value = True
        self.assertEqual('test', self.plugin.setting_path)

    @mock.patch('sys.stdout.write')
    @mock.patch('os.path.join')
    @mock.patch('os.path.isdir')
    def test_setting_path_err(self, os_path_isdir, os_path_join, mock_write):
        """setting_path error case"""
        os_path_join.return_value = 'test'
        os_path_isdir.return_value = False
        with self.assertRaises(wasanbon.UnsupportedPlatformException):
            self.plugin.setting_path

    def test_getIDE(self):
        """getIDE normal case"""
        self.assertEqual(wasanbon.IDE, self.plugin.getIDE())

    @mock.patch('builtins.open', return_value='')
    @mock.patch('yaml.safe_load')
    def test_path(self, mock_load, mock_open):
        """path normal case"""
        mock_load.return_value = 'test'
        #plugin = Plugin()
        res = self.plugin.path
        self.assertEqual('test', res)

    @mock.patch('os.path.isfile')
    def test_path_err(self, mock_isfile):
        """path error case"""
        mock_isfile.return_value = False
        #plugin = Plugin()
        res = self.plugin.path
        self.assertEqual({}, res)

    @mock.patch('builtins.open', return_value='')
    @mock.patch('yaml.safe_load')
    def test_path_except(self, yaml_safe_load, mock_open):
        """path except case"""
        #plugin = Plugin()
        yaml_safe_load.side_effect = ImportError
        res = self.plugin.path
        self.assertEqual({}, res)

    @mock.patch('os.rename')
    @mock.patch('os.remove')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.platform', return_value='platform')
    @mock.patch('wasanbon.get_home_path', return_value='home_path')
    @mock.patch('os.path.join', return_value='target')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    def test_setup_bashrc_1(self, mock_sys_platform, mock_join, mock_get_home_path, mock_platform, mock_open, mock_isfile, mock_remove, mock_rename):
        """setup_bashrc normal case
        sys.platform == darwin
        os.path.isfile == True
        """
        ### setting ###
        test_file = MagicMock(spec=['__iter__', 'close'])
        test_file.__iter__.return_value = ['hoge', '#-- Starting Setup Script of wasanbon --#',
                                           'hoge', '#-- Ending Setup Script of wasanbon --#', 'hoge']
        fout1 = MagicMock(spec=['write', 'close'])
        fout2 = MagicMock(spec=['write', 'close'])
        mock_open.side_effect = [MagicMock(), test_file, fout1, fout2]
        ### test ###
        self.assertEqual(0, self.plugin.setup_bashrc())
        self.assertEqual(2, fout1.write.call_count)
        self.assertEqual(1, fout1.close.call_count)
        self.assertEqual(3, fout2.write.call_count)
        self.assertEqual(1, fout2.close.call_count)
        mock_remove.assert_called_once()
        mock_rename.assert_called_once()
        mock_join.assert_any_call('home_path', '.bash_profile')

    @mock.patch('sys.stdout.write')
    @mock.patch('os.rename')
    @mock.patch('os.remove')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('builtins.open')
    @mock.patch('wasanbon.platform', return_value='platform')
    @mock.patch('wasanbon.get_home_path', return_value='home_path')
    @mock.patch('os.path.join', return_value='target')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    def test_setup_bashrc_2(self, mock_sys_platform, mock_join, mock_get_home_path, mock_platform, mock_open, mock_isfile, mock_remove, mock_rename, mock_write):
        """setup_bashrc normal case
        sys.platform == linux
        os.path.isfile == True
        verbose = True
        """
        ### setting ###
        test_file = MagicMock(spec=['__iter__', 'close'])
        test_file.__iter__.return_value = ['hoge', '#-- Starting Setup Script of wasanbon --#',
                                           'hoge', '#-- Ending Setup Script of wasanbon --#', 'hoge']
        fout1 = MagicMock(spec=['write', 'close'])
        fout2 = MagicMock(spec=['write', 'close'])
        mock_open.side_effect = [MagicMock(), test_file, fout1, fout2]
        ### test ###
        self.assertEqual(0, self.plugin.setup_bashrc(verbose=True))
        self.assertEqual(2, fout1.write.call_count)
        self.assertEqual(1, fout1.close.call_count)
        self.assertEqual(3, fout2.write.call_count)
        self.assertEqual(1, fout2.close.call_count)
        mock_remove.assert_called_once()
        mock_rename.assert_called_once()
        mock_join.assert_any_call('home_path', '.bashrc')
        mock_write.assert_called_once()

    @mock.patch('sys.platform', return_value='win32')
    def test_setup_bashrc_3(self, mock_write):
        """setup_bashrc normal case
        sys.platform != (darwin or linux)
        """
        ### test ###
        self.assertEqual(-1, self.plugin.setup_bashrc())

    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin.setting_path', return_value='setting_path')
    @mock.patch('yaml.dump')
    @mock.patch('os.path.isdir')
    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.setup.search_command', return_value='new_path')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open', return_value='open_file')
    @mock.patch('yaml.safe_load')
    @mock.patch('os.path.join', return_value='path_filename')
    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin._copy_path_yaml_from_setting_dir')
    def test__update_path_1(self, mock_copy_path, mock_join, mock_safe_load, mock_open, mock_mkdir, mock_search_command, mock_isdir, mock_dump, mock_setting_path):
        """_update_path normal case
        os.path.isdir.return_value = True
        """
        ### setting ###
        test_dir = {'key': 'value', 'eclipse': 'eclipse'}
        test_hints = {'key': ['$HOME'], 'eclipse': ['eclipse']}
        mock_safe_load.side_effect = [test_dir, test_hints]
        mock_isdir.return_value = True
        ### test ###
        self.plugin._update_path()
        self.assertEqual(2, mock_search_command.call_count)
        self.assertEqual(1, mock_isdir.call_count)
        self.assertEqual(0, mock_mkdir.call_count)
        mock_dump.assert_called_once_with(
            {'key': 'new_path', 'eclipse': 'new_path'},
            'open_file',
            encoding='utf8',
            allow_unicode=True,
            default_flow_style=False
        )

    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin.setting_path', return_value='setting_path')
    @mock.patch('yaml.dump')
    @mock.patch('os.path.isdir')
    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.setup.search_command', return_value='new_path')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open', return_value='open_file')
    @mock.patch('yaml.safe_load')
    @mock.patch('os.path.join', return_value='path_filename')
    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin._copy_path_yaml_from_setting_dir')
    def test__update_path_2(self, mock_copy_path, mock_join, mock_safe_load, mock_open, mock_mkdir, mock_search_command, mock_isdir, mock_dump, mock_setting_path):
        """_update_path normal case
        os.path.isdir.return_value = False
        """
        ### setting ###
        test_dir = {'key': 'value', 'eclipse': 'eclipse'}
        test_hints = {'key': ['$HOME'], 'eclipse': ['eclipse']}
        mock_safe_load.side_effect = [test_dir, test_hints]
        mock_isdir.return_value = False
        ### test ###
        self.plugin._update_path()
        self.assertEqual(2, mock_search_command.call_count)
        self.assertEqual(1, mock_isdir.call_count)
        self.assertEqual(1, mock_mkdir.call_count)
        mock_dump.assert_called_once_with(
            {'key': 'new_path', 'eclipse': 'new_path'},
            'open_file',
            encoding='utf8',
            allow_unicode=True,
            default_flow_style=False
        )

    @mock.patch('os.path.isfile')
    @mock.patch('shutil.copy2')
    def test_copy_path_yaml_from_setting_dir(self, shutil_copy2, os_path_isfile):
        """_copy_path_yaml_from_setting_dir set"""
        #plugin = Plugin()
        os_path_isfile.return_value = False
        self.plugin._copy_path_yaml_from_setting_dir()
        shutil_copy2.assert_called_once()

    @mock.patch('os.path.isfile')
    @mock.patch('shutil.copy2')
    def test_copy_path_yaml_from_setting_dir_not_set(self, shutil_copy2, os_path_isfile):
        """_copy_path_yaml_from_setting_dir already set"""
        #plugin = Plugin()
        os_path_isfile.return_value = True
        self.plugin._copy_path_yaml_from_setting_dir()
        shutil_copy2.assert_not_called()


if __name__ == '__main__':
    unittest.main()
