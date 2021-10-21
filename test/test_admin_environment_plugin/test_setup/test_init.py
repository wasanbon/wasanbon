# test for wasanbon/core/plugins/admin/environment_plugin/setup/__init__.py

import unittest
from unittest import mock
from unittest.mock import call

import os
os.environ["PYTHONPATH"] = "~/wasanbon"

from wasanbon.core.plugins.admin.environment_plugin import Plugin
import wasanbon

from logging import DEBUG,  basicConfig, getLogger

basicConfig(
    filename='test.log',
    filemode='w',
    level=DEBUG,
    format='[%(asctime)s] %(levelname)s pid:%(process)d:thread:%(thread)d '
            '%(filename)s %(lineno)d %(funcName)s(): %(message)s')
logger = getLogger('unittest')

class TestPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = Plugin()

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init_(self, mock_init):
        """__init__ normal case"""
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    @mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin.path')
    def test_status(self, mock_path, sys_stdout_write):
        """status normal case"""
        mock_path.return_value = {'a':1, 'b':2, 'c':3}
        calls = [
            call('# Showing the status of wasanbon environment initialization...\n'),
            call('%s : %s\n' % ('a', 1)),
            call('%s : %s\n' % ('b', 2)),
            call('%s : %s\n' % ('c', 3))
        ]
        self.plugin.status([])
        sys_stdout_write.assert_has_calls(calls)

    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin._update_path')
    def test_update_path(self, mock_update_path):
        """update_path normal case"""
        self.assertEqual(0, self.plugin.update_path([]))
        mock_update_path.assert_any_call(verbose=True)
        #mock_update_path.assert_called_once()

    #@mock.patch('sys.stdout.write')
    @mock.patch('wasanbon.core.plugins.admin.environment_plugin.Plugin._update_path')
    def test_init(self, mock_update_path):
        """init normal case"""
        self.assertEqual(0, self.plugin.update_path([]))
        mock_update_path.assert_any_call(verbose=True)
        
    @mock.patch('os.path.join')
    @mock.patch('os.path.isdir')
    def test_setting_path(self, os_path_isdir, os_path_join):
        """setting_path normal case"""
        os_path_join.return_value = 'test'
        os_path_isdir.return_value = True
        self.assertEqual('test', self.plugin.setting_path)

    @mock.patch('os.path.join')
    @mock.patch('os.path.isdir')
    def test_setting_path_err(self, os_path_isdir, os_path_join):
        """setting_path error case"""
        os_path_join.return_value = 'test'
        os_path_isdir.return_value = False
        with self.assertRaises(wasanbon.UnsupportedPlatformException):
            self.plugin.setting_path

    def test_getIDE(self):
        """この関数どこで使っている？いらない気がする"""
        #plugin = Plugin()
        self.assertEqual(wasanbon.IDE, self.plugin.getIDE())

    @mock.patch('yaml.safe_load')
    def test_path(self, mock_load):
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

    #@mock.patch('yaml.safe_load', mock.MagicMock(side_effect=Exception()))
    @mock.patch('yaml.safe_load')
    def test_path_except(self, yaml_safe_load):
        """path except case"""
        #plugin = Plugin()
        yaml_safe_load.side_effect = ImportError
        res = self.plugin.path
        self.assertEqual({}, res)

    @mock.patch('sys.stdout.write')
    def test_setup_bashrc(self):
        """platformで分岐する。あとで"""
        import sys

    def test__uodate_path(self):
        """test case 考えてから書く。"""

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestPlugin('test_path_err'))
    return suite
    
if __name__ == '__main__':
    #とにかく全部のテストを実行する場合
    #unittest.main()
    #テストケースを選んで実行する場合
    runner = unittest.TextTestRunner()
    runner.run(suite())
