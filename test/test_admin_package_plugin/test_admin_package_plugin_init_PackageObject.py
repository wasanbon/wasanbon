# test for wasanbon/core/plugins/admin/idlcompiler_plugin/dart_converter.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

from wasanbon.core.plugins.admin.package_plugin import PackageObject

import wasanbon

def mock_join_func( *args ):
    ret = ""
    for val in args:
        ret = ret + str(val) + '/'
    return ret.rstrip('/')

class TestPlugin(unittest.TestCase):

    def get_setting(self):
        console_bind = ['C++', 'Java', 'Python']
        nameservers = ['localhost:2809']
        application = {'name': 'test_project01', 'BIN_DIR': 'bin', 'RTC_DIR': 'rtc', 'RTS_DIR': 'system', 'CONF_DIR': 'conf',
                       'conf.C++': 'rtc_cpp.conf', 'conf.Python': 'rtc_py.conf', 'conf.Java': 'rtc_java.conf', 'system': 'DefaultSystem.xml',
                       'console_bind': console_bind,
                       'nameservers': nameservers}
        setting = {'application': application}
        return setting

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('yaml.safe_load')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile', return_value=True)
    def test_PackageObject_properties_1(self, mock_isfile, mock_open, mock_safe_load, mock_join):
        """PackageObject properties with name, path"""

        mock_safe_load.return_value = self.get_setting()

        ### test ###
        pObj = PackageObject(name='test_project01', path='/path/to/test_project01')
        self.assertEqual('test_project01', pObj.name)
        self.assertEqual('/path/to/test_project01', pObj.path)
        self.assertEqual('/path/to/test_project01/setting.yaml', pObj.setting_file_path)
        self.assertEqual('""', pObj.description)
        self.assertEqual(self.get_setting()['application'], pObj.setting)
        self.assertEqual('bin', pObj.get_binpath(fullpath=False))
        self.assertEqual('/path/to/test_project01/bin', pObj.get_binpath(fullpath=True))
        self.assertEqual('system', pObj.get_systempath(fullpath=False))
        self.assertEqual('/path/to/test_project01/system', pObj.get_systempath(fullpath=True))
        self.assertEqual('conf', pObj.get_confpath(fullpath=False))
        self.assertEqual('/path/to/test_project01/conf', pObj.get_confpath(fullpath=True))
        self.assertEqual('rtc', pObj.get_rtcpath(fullpath=False))
        self.assertEqual('/path/to/test_project01/rtc', pObj.get_rtcpath(fullpath=True))
        self.assertEqual('/path/to/test_project01/rtc/repository.yaml', pObj.rtc_repository_file)
        self.assertEqual([], pObj.standalone_rtc_commands)

        mock_open.assert_called_once_with('/path/to/test_project01/setting.yaml', 'r')

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('yaml.safe_load')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile', return_value=True)
    def test_PackageObject_properties_2(self, mock_isfile, mock_open, mock_safe_load, mock_join):
        """PackageObject properties with path"""

        mock_safe_load.return_value = self.get_setting()

        ### test ###
        pObj = PackageObject(path='/path/to/test_project01')
        self.assertEqual('test_project01', pObj.name)
        self.assertEqual('/path/to/test_project01', pObj.path)
        self.assertEqual('/path/to/test_project01/setting.yaml', pObj.setting_file_path)
        self.assertEqual('""', pObj.description)
        self.assertEqual(self.get_setting()['application'], pObj.setting)
        self.assertEqual('bin', pObj.get_binpath(fullpath=False))
        self.assertEqual('/path/to/test_project01/bin', pObj.get_binpath(fullpath=True))
        self.assertEqual('system', pObj.get_systempath(fullpath=False))
        self.assertEqual('/path/to/test_project01/system', pObj.get_systempath(fullpath=True))
        self.assertEqual('conf', pObj.get_confpath(fullpath=False))
        self.assertEqual('/path/to/test_project01/conf', pObj.get_confpath(fullpath=True))
        self.assertEqual('rtc', pObj.get_rtcpath(fullpath=False))
        self.assertEqual('/path/to/test_project01/rtc', pObj.get_rtcpath(fullpath=True))
        self.assertEqual('/path/to/test_project01/rtc/repository.yaml', pObj.rtc_repository_file)
        self.assertEqual([], pObj.standalone_rtc_commands)

        mock_open.assert_called_once_with('/path/to/test_project01/setting.yaml', 'r')

    @mock.patch('yaml.safe_load')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile', side_effect=[True, False])
    def test_default_system_filepath_1(self, mock_isfile, mock_open, mock_safe_load):
        """default_system_filepath normal case"""

        mock_safe_load.return_value = self.get_setting()

        ### test ###
        pObj = PackageObject(path='/path/to/test_project01')
        import os
        self.assertEqual(os.path.join('/path/to/test_project01',os.path.join('/path/to/test_project01','system'),'DefaultSystem.xml'), pObj.default_system_filepath)

    @mock.patch('yaml.safe_load')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile', side_effect=[True, True])
    @mock.patch('sys.stdout.write')
    def test_default_system_filepath_2(self, mock_write, mock_isfile, mock_open, mock_safe_load):
        """default_system_filepath old case"""

        mock_safe_load.return_value = self.get_setting()

        ### test ###
        pObj = PackageObject(path='/path/to/test_project01')
        import os
        self.assertEqual(os.path.join('/path/to/test_project01','DefaultSystem.xml'), pObj.default_system_filepath)
        mock_write.assert_called_once_with('# This package contains old manner system description\n')

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('yaml.safe_load')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile', side_effect=[True, False, True, False, True, False, True])
    def test_rtcconf_1(self, mock_isfile, mock_open, mock_safe_load, mock_join):
        """rtcconf normal case"""

        mock_safe_load.return_value = self.get_setting()

        expect = {'C++': '/path/to/test_project01/conf/rtc_cpp.conf',
                  'Java': '/path/to/test_project01/conf/rtc_java.conf',
                  'Python': '/path/to/test_project01/conf/rtc_py.conf'}

        ### test ###
        pObj = PackageObject(path='/path/to/test_project01')
        self.assertEqual(expect, pObj.rtcconf)

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('yaml.safe_load')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile', side_effect=[True, True, True, True, True, True, True])
    @mock.patch('sys.stdout.write')
    def test_rtcconf_2(self, mock_write, mock_isfile, mock_open, mock_safe_load, mock_join):
        """rtcconf old case"""

        mock_safe_load.return_value = self.get_setting()

        expect = {'C++': '/path/to/test_project01/rtc_cpp.conf',
                  'Java': '/path/to/test_project01/rtc_java.conf',
                  'Python': '/path/to/test_project01/rtc_py.conf'}

        ### test ###
        pObj = PackageObject(path='/path/to/test_project01')
        self.assertEqual(expect, pObj.rtcconf)
        mock_write.assert_any_call('# conf.C++ must be filename, and path of conffile must be writtein in CONF_DIR\n'),
        mock_write.assert_any_call('# conf.Java must be filename, and path of conffile must be writtein in CONF_DIR\n'),
        mock_write.assert_any_call('# conf.Python must be filename, and path of conffile must be writtein in CONF_DIR\n')

    @mock.patch('os.path.join', side_effect=mock_join_func)
    @mock.patch('yaml.safe_load')
    @mock.patch('builtins.open')
    @mock.patch('os.path.isfile', side_effect=[True, False, False, False, False, False, False])
    @mock.patch('sys.stdout.write')
    def test_rtcconf_3(self, mock_write, mock_isfile, mock_open, mock_safe_load, mock_join):
        """rtcconf file not found case"""

        mock_safe_load.return_value = self.get_setting()

        expect = {}

        import os
        os.sep = '/'

        ### test ###
        pObj = PackageObject(path='/path/to/test_project01')
        self.assertEqual(expect, pObj.rtcconf)
        mock_write.assert_any_call('# Config file /path/to/test_project01/conf/rtc_cpp.conf is not found.\n'),
        mock_write.assert_any_call('# Config file /path/to/test_project01/conf/rtc_java.conf is not found.\n'),
        mock_write.assert_any_call('# Config file /path/to/test_project01/conf/rtc_py.conf is not found.\n')


if __name__ == '__main__':
    unittest.main()
