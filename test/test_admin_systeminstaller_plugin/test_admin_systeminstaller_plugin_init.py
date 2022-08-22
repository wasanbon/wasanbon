# test for wasanbon/core/plugins/admin/systeminstaller_plugin/__init__.py

import unittest
from unittest import mock
from unittest.mock import call
from unittest.mock import MagicMock, PropertyMock

import sys
sys.path.append('../../')

import wasanbon


class TestPlugin(unittest.TestCase):

    def setUp(self):
        import wasanbon.core.plugins.admin.systeminstaller_plugin as m
        self.admin_mock = MagicMock(spec=['rtcconf', 'rtc'])
        #type(self.admin_mock.environment).path = PropertyMock()
        setattr(m, 'admin', self.admin_mock)
        self.plugin = m.Plugin()
        self.Func = m

    @mock.patch('wasanbon.core.plugins.PluginFunction.__init__')
    def test_init(self, mock_init):
        """__init__ normal case"""
        from wasanbon.core.plugins.admin.systeminstaller_plugin import Plugin
        mock_init.return_value = None
        plugin = Plugin()
        mock_init.assert_called_once()

    def test_depends(self):
        """depends normal case"""
        self.assertEqual(['admin.environment', 'admin.rtcconf', 'admin.rtc'], self.plugin.depends())

    # @mock.patch('wasanbon.core.plugins.admin.rtcconf_plugin.RTCConf')
    def test_get_installed_rtc_names(self):
        """get_installed_rtc_names normal case"""
        type(self.admin_mock.rtcconf).RTCConf = MagicMock(return_value={'manager.components.precreate': 'key1,key2'})
        package = MagicMock()
        setattr(package, 'rtcconf', {'C++': 'C++', 'Java': 'Java', 'Python': 'Python'})
        self.assertEqual(['key1', 'key2', 'key1', 'key2', 'key1', 'key2'], self.plugin.get_installed_rtc_names(package))

    def test_get_installed_rtc_names_select_language(self):
        """get_installed_rtc_names normal case
        language = 'C++'
        """
        type(self.admin_mock.rtcconf).RTCConf = MagicMock(return_value={'manager.components.precreate': 'key1,key2'})
        package = MagicMock()
        setattr(package, 'rtcconf', {'C++': 'C++', 'Java': 'Java', 'Python': 'Python'})
        self.assertEqual(['key1', 'key2'], self.plugin.get_installed_rtc_names(package, language='C++'))

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    def test__get_rtc_name_from_standalone_command_1(self, mock_platform):
        """get_rtc_name_from_standalone_command"""
        def get_binpath(fullpath):
            return 'bin'

        def get_rtcpath(fullpath):
            return 'rtc'
        package = MagicMock()
        setattr(package, 'get_binpath', get_binpath)
        setattr(package, 'get_rtcpath', get_rtcpath)
        self.assertEqual('test', self.plugin._Plugin__get_rtc_name_from_standalone_command(package, 'bin/testComp.exe'))

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    def test__get_rtc_name_from_standalone_command_2(self, mock_platform):
        """get_rtc_name_from_standalone_command"""
        def get_binpath(fullpath):
            return 'bin'

        def get_rtcpath(fullpath):
            return 'rtc'
        package = MagicMock()
        setattr(package, 'get_binpath', get_binpath)
        setattr(package, 'get_rtcpath', get_rtcpath)
        self.assertEqual('test', self.plugin._Plugin__get_rtc_name_from_standalone_command(package, 'bin/testComp'))

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    def test__get_rtc_name_from_standalone_command_3(self, mock_platform):
        """get_rtc_name_from_standalone_command normal case"""
        def get_binpath(fullpath):
            return 'bin'

        def get_rtcpath(fullpath):
            return 'rtc'
        package = MagicMock()
        setattr(package, 'get_binpath', get_binpath)
        setattr(package, 'get_rtcpath', get_rtcpath)
        self.assertEqual('test', self.plugin._Plugin__get_rtc_name_from_standalone_command(package, 'rtc/test.py'))

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    def test__get_rtc_name_from_standalone_command_4(self, mock_platform):
        """get_rtc_name_from_standalone_command normal case"""
        def get_binpath(fullpath):
            return 'bin'

        def get_rtcpath(fullpath):
            return 'rtc'
        package = MagicMock()
        setattr(package, 'get_binpath', get_binpath)
        setattr(package, 'get_rtcpath', get_rtcpath)
        self.assertEqual('', self.plugin._Plugin__get_rtc_name_from_standalone_command(package, 'hoge/test.py'))

    def test_get_rtcd_nameservers(self):
        """get_rtcd_nameservers normal case"""
        package = MagicMock()
        setattr(package, 'rtcconf', {'C++': 'C++', 'Python': 'Python', 'Java': 'Java'})
        type(self.admin_mock.rtcconf).RTCConf = MagicMock(return_value={'corba.nameservers': '  key1:,key1:,key2  '})
        self.assertEqual({'C++': ['key1:', 'key2:2809'],
                          'Python': ['key1:', 'key2:2809'],
                          'Java': ['key1:', 'key2:2809']},
                         self.plugin.get_rtcd_nameservers(package))

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.get_rtcd_nameservers', return_value={'C++': ['C++:ns'], 'Python': [], 'Java': ['Java:ns']})
    def test_get_rtcd_namemanager_addresses(self, mock_get_rtcd_nameservers):
        """get_rtcd_manager_addresses normal case"""
        package = MagicMock()
        setattr(package, 'rtcconf', {'C++': 'C++', 'Python': 'Python', 'Java': 'Java'})
        type(self.admin_mock.rtcconf).RTCConf = MagicMock(return_value={'manager.naming_formats': '  Name%n  '})
        self.assertEqual({'C++': ['C++:ns/Namemanager'],
                          'Python': ['localhost:2809/Namemanager'],
                          'Java': ['Java:ns/Namemanager']},
                         self.plugin.get_rtcd_manager_addresses(package))

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin._Plugin__get_rtc_name_from_standalone_command', side_effect=['', 'rtc_name', 'rtc_name2'])
    def test_get_installed_standalone_rtc_names(self, mock_command):
        """get_installed_standalone_rtc_names normal case"""

        package = MagicMock()
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['cmd1', 'cmd2', 'cmd3'])
        type(package).setting = setting

        get_rtc_from_package = MagicMock(side_effect=[wasanbon.RTCNotFoundException(), 'rtc'])
        type(self.admin_mock.rtc).get_rtc_from_package = get_rtc_from_package

        ### test ###
        result = self.plugin.get_installed_standalone_rtc_names(package, verbose=True)
        self.assertEqual(result, ['rtc_name2'])

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.get_installed_rtc_names', return_value=['rtc_name'])
    def test_is_installed_1(self, mock_get_installed_rtc_names):
        """is_installed not standalone case"""

        package = MagicMock()
        rtc = MagicMock()
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(rtcprofile).basicInfo = basicInfo
        type(rtc).rtcprofile = rtcprofile

        ### test ###
        self.assertEqual(True, self.plugin.is_installed(package, rtc, verbose=True, standalone=False))

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.get_installed_standalone_rtc_names', return_value=['rtc_name'])
    def test_is_installed_2(self, mock_get_installed_rtc_names):
        """is_installed standalone case"""

        package = MagicMock()
        rtc = MagicMock()
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(rtcprofile).basicInfo = basicInfo
        type(rtc).rtcprofile = rtcprofile

        ### test ###
        self.assertEqual(True, self.plugin.is_installed(package, rtc, verbose=True, standalone=True))

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=False)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_binary_from_rtc', return_value='')
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_conf_from_rtc', return_value='conf_path')
    @mock.patch('sys.stdout.write')
    def test_install_rtc_in_package_1(self, mock_write, mock_copy_conf_from_rtc, mock_copy_binary_from_rtc, mock_is_installed):
        """install_rtc_in_package not standalone failed case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).get_binpath = MagicMock(return_value='bin')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Python'
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        type(rtcconf).append = MagicMock(return_value=0)
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        ### test ###
        self.assertEqual(-1, self.plugin.install_rtc_in_package(package, rtc, standalone=False, verbose=True))
        rtcconf.append.assert_has_calls([call('manager.modules.load_path', 'bin'),
                                         call('manager.modules.preload', 'rtc_file_path'),
                                         call('manager.components.precreate', 'rtc_name', verbose=True, allow_duplicate=False)])
        mock_write.assert_any_call('# Installing RTC in package package_name\n')
        mock_write.assert_any_call('### Setting manager.modules.load_path:\n')
        mock_write.assert_any_call('### OK.\n')
        mock_write.assert_any_call('### Setting manager.modules.preload:\n')
        mock_write.assert_any_call('### OK.\n')
        mock_write.assert_any_call('### Setting manager.components.precreate:\n')

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=True)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_binary_from_rtc', return_value='target/targetfile')
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_conf_from_rtc', return_value='conf_path')
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('os.environ.copy', return_value={'RTM_JAVA_ROOT': '/'})
    def test_install_rtc_in_package_3(self, mock_env_copy, mock_platform, mock_write, mock_timestampstr, mock_dump, mock_safe_load, mock_open, ock_mkdir, mock_isdir, mock_copy, mock_copy_conf_from_rtc, mock_copy_binary_from_rtc, mock_is_installed):
        """install_rtc_in_package standalone Java ubuntu case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Java'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        type(rtcconf).append = MagicMock(return_value=1)
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        application = {'standalone': []}
        mock_safe_load.return_value = {'application': application}

        ### test ###
        self.assertEqual(0, self.plugin.install_rtc_in_package(package, rtc, standalone=False, verbose=True, rtcconf_filename='rtcconf_filename'))
        rtcconf.append.assert_has_calls([call('category.rtc_name-1.config_file', 'conf_path')])
        mock_open.assert_has_calls([call('package_path/backup/setting.yaml20211001000000', 'r'), call('package_path/setting.yaml', 'w')])
        mock_dump.assert_called_once_with(
            {'application': {'standalone': ['java -cp "target/targetfile:/jar/*" rtc_nameComp -f conf/rtc_rtc_name.conf']}}, default_flow_style=False)
        mock_write.assert_any_call('# Installing RTC in package package_name\n')
        mock_write.assert_any_call('## RTC (rtc_name) is already installed as standalone.\n')
        mock_write.assert_any_call('## Install standalone again.\n')
        mock_write.assert_any_call('## Configuring System. Set (category.rtc_name-1.config_file) to conf_path\n')

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=True)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_binary_from_rtc', return_value='target/targetfile')
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_conf_from_rtc', return_value='conf_path')
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.environ.copy', return_value={'RTM_JAVA_ROOT': '/'})
    def test_install_rtc_in_package_4(self, mock_env_copy, mock_platform, mock_write, mock_timestampstr, mock_dump, mock_safe_load, mock_open, ock_mkdir, mock_isdir, mock_copy, mock_copy_conf_from_rtc, mock_copy_binary_from_rtc, mock_is_installed):
        """install_rtc_in_package standalone Java win32 case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Java'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        type(rtcconf).append = MagicMock(return_value=1)
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        application = {'standalone': []}
        mock_safe_load.return_value = {'application': application}

        ### test ###
        self.assertEqual(0, self.plugin.install_rtc_in_package(package, rtc, standalone=False, verbose=True, rtcconf_filename='rtcconf_filename'))
        rtcconf.append.assert_has_calls([call('category.rtc_name-1.config_file', 'conf_path')])
        mock_open.assert_has_calls([call('package_path/backup/setting.yaml20211001000000', 'r'), call('package_path/setting.yaml', 'w')])
        mock_dump.assert_called_once_with(
            {'application': {'standalone': ['java -cp "target/targetfile;/jar/*" rtc_nameComp -f conf/rtc_rtc_name.conf']}}, default_flow_style=False)
        mock_write.assert_any_call('# Installing RTC in package package_name\n')
        mock_write.assert_any_call('## RTC (rtc_name) is already installed as standalone.\n')
        mock_write.assert_any_call('## Install standalone again.\n')
        mock_write.assert_any_call('## Configuring System. Set (category.rtc_name-1.config_file) to conf_path\n')

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=True)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_binary_from_rtc', return_value='target/targetfile')
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_conf_from_rtc', return_value='conf_path')
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    def test_install_rtc_in_package_5(self, mock_platform, mock_write, mock_timestampstr, mock_dump, mock_safe_load, mock_open, ock_mkdir, mock_isdir, mock_copy, mock_copy_conf_from_rtc, mock_copy_binary_from_rtc, mock_is_installed):
        """install_rtc_in_package standalone Python ubuntu case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Python'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        type(rtcconf).append = MagicMock(return_value=1)
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        application = {'standalone': []}
        mock_safe_load.return_value = {'application': application}

        ### test ###
        self.assertEqual(0, self.plugin.install_rtc_in_package(package, rtc, standalone=False, verbose=True, rtcconf_filename='rtcconf_filename'))
        rtcconf.append.assert_has_calls([call('category.rtc_name-1.config_file', 'conf_path')])
        mock_open.assert_has_calls([call('package_path/backup/setting.yaml20211001000000', 'r'), call('package_path/setting.yaml', 'w')])
        mock_dump.assert_called_once_with(
            {'application': {'standalone': ['python3 target/targetfile -f conf/rtc_rtc_name.conf']}}, default_flow_style=False)
        mock_write.assert_any_call('# Installing RTC in package package_name\n')
        mock_write.assert_any_call('## RTC (rtc_name) is already installed as standalone.\n')
        mock_write.assert_any_call('## Install standalone again.\n')
        mock_write.assert_any_call('## Configuring System. Set (category.rtc_name-1.config_file) to conf_path\n')

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=True)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_binary_from_rtc', return_value='target/targetfile')
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_conf_from_rtc', return_value='conf_path')
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('sys.stdout.write')
    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    def test_install_rtc_in_package_6(self, mock_platform, mock_write, mock_timestampstr, mock_dump, mock_safe_load, mock_open, ock_mkdir, mock_isdir, mock_copy, mock_copy_conf_from_rtc, mock_copy_binary_from_rtc, mock_is_installed):
        """install_rtc_in_package standalone Python win32 case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Python'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        type(rtcconf).append = MagicMock(return_value=1)
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        application = {'standalone': []}
        mock_safe_load.return_value = {'application': application}

        ### test ###
        self.assertEqual(0, self.plugin.install_rtc_in_package(package, rtc, standalone=False, verbose=True, rtcconf_filename='rtcconf_filename'))
        rtcconf.append.assert_has_calls([call('category.rtc_name-1.config_file', 'conf_path')])
        mock_open.assert_has_calls([call('package_path/backup/setting.yaml20211001000000', 'r'), call('package_path/setting.yaml', 'w')])
        mock_dump.assert_called_once_with(
            {'application': {'standalone': ['python target/targetfile -f conf/rtc_rtc_name.conf']}}, default_flow_style=False)
        mock_write.assert_any_call('# Installing RTC in package package_name\n')
        mock_write.assert_any_call('## RTC (rtc_name) is already installed as standalone.\n')
        mock_write.assert_any_call('## Install standalone again.\n')
        mock_write.assert_any_call('## Configuring System. Set (category.rtc_name-1.config_file) to conf_path\n')

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=True)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_binary_from_rtc', return_value='target/targetfile')
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_conf_from_rtc', return_value='conf_path')
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('sys.stdout.write')
    def test_install_rtc_in_package_7(self, mock_write, mock_timestampstr, mock_dump, mock_safe_load, mock_open, ock_mkdir, mock_isdir, mock_copy, mock_copy_conf_from_rtc, mock_copy_binary_from_rtc, mock_is_installed):
        """install_rtc_in_package standalone C++ and select conffile case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        type(rtcconf).append = MagicMock(return_value=1)
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        application = {'standalone': []}
        mock_safe_load.return_value = {'application': application}

        ### test ###
        self.assertEqual(0, self.plugin.install_rtc_in_package(package, rtc, standalone=False,
                         verbose=True, rtcconf_filename='rtcconf_filename', conffile='conffile'))
        rtcconf.append.assert_has_calls([call('category.rtc_name-1.config_file', 'conffile')])
        mock_open.assert_has_calls([call('package_path/backup/setting.yaml20211001000000', 'r'), call('package_path/setting.yaml', 'w')])
        mock_dump.assert_called_once_with({'application': {'standalone': ['target/targetfile -f conf/rtc_rtc_name.conf']}}, default_flow_style=False)
        mock_write.assert_any_call('# Installing RTC in package package_name\n')
        mock_write.assert_any_call('## RTC (rtc_name) is already installed as standalone.\n')
        mock_write.assert_any_call('## Install standalone again.\n')
        mock_write.assert_any_call('## Configuring System. Set (category.rtc_name-1.config_file) to conffile\n')

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=True)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_binary_from_rtc', return_value='target/targetfile')
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.copy_conf_from_rtc', return_value='conf_path')
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('sys.stdout.write')
    def test_install_rtc_in_package_7(self, mock_write, mock_timestampstr, mock_dump, mock_safe_load, mock_open, ock_mkdir, mock_isdir, mock_copy, mock_copy_conf_from_rtc, mock_copy_binary_from_rtc, mock_is_installed):
        """install_rtc_in_package standalone same command case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        type(rtcconf).append = MagicMock(return_value=1)
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        application = {'standalone': ['target/targetfile -f conf/rtc_rtc_name.conf <-same command']}
        mock_safe_load.return_value = {'application': application}

        ### test ###
        self.assertEqual(0, self.plugin.install_rtc_in_package(package, rtc, standalone=False,
                         verbose=True, rtcconf_filename='rtcconf_filename', conffile='conffile'))
        rtcconf.append.assert_has_calls([call('category.rtc_name-1.config_file', 'conffile')])
        mock_open.assert_has_calls([call('package_path/backup/setting.yaml20211001000000', 'r'), call('package_path/setting.yaml', 'w')])
        mock_dump.assert_called_once_with(
            {'application': {'standalone': ['target/targetfile -f conf/rtc_rtc_name.conf <-same command']}}, default_flow_style=False)
        mock_write.assert_any_call('# Installing RTC in package package_name\n')
        mock_write.assert_any_call('## RTC (rtc_name) is already installed as standalone.\n')
        mock_write.assert_any_call('## Install standalone again.\n')
        mock_write.assert_any_call('## Configuring System. Set (category.rtc_name-1.config_file) to conffile\n')

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=True)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.uninstall_standalone_rtc_from_package', return_value=True)
    def test_uninstall_rtc_from_package_1(self, mock_uninstall_standalone_rtc_from_package, mock_is_installed):
        """uninstall_rtc_from_package is_installed case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        ### test ###
        self.assertEqual(True, self.plugin.uninstall_rtc_from_package(package, rtc))

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=False)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.uninstall_standalone_rtc_from_package', return_value=True)
    def test_uninstall_rtc_from_package_2(self, mock_uninstall_standalone_rtc_from_package, mock_is_installed):
        """uninstall_rtc_from_package unknown language case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Ruby'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        ### test ###
        with self.assertRaises(wasanbon.UnsupportedLanguageException):
            self.assertEqual(True, self.plugin.uninstall_rtc_from_package(package, rtc))

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=False)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.uninstall_standalone_rtc_from_package', return_value=True)
    @mock.patch('sys.stdout.write')
    def test_uninstall_rtc_from_package_3(self, mock_write, mock_uninstall_standalone_rtc_from_package, mock_is_installed):
        """uninstall_rtc_from_package C++ case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        remove = MagicMock()
        type(rtcconf).remove = remove
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        ### test ###
        self.plugin.uninstall_rtc_from_package(package, rtc, rtcconf_filename='rtcconf_filename', verbose=True)
        mock_write.assert_any_call('## Uninstall RTC (rtc_name) from package\n')
        remove.assert_has_calls([call('manager.components.precreate', 'rtc_name', verbose=True),
                                 call('manager.components.precreate'),
                                 call('manager.modules.preload', 'rtc_name.so', verbose=True),
                                 call('manager.modules.preload'),
                                 call('manager.modules.load_path'),
                                 call('category.rtc_name.config_file'),
                                 call('category.rtc_name0.config_file'),
                                 call('category.rtc_name1.config_file'),
                                 call('category.rtc_name2.config_file'),
                                 call('category.rtc_name3.config_file'),
                                 call('category.rtc_name4.config_file'),
                                 call('category.rtc_name5.config_file'),
                                 call('category.rtc_name6.config_file'),
                                 call('category.rtc_name7.config_file'),
                                 call('category.rtc_name8.config_file'),
                                 call('category.rtc_name9.config_file'),
                                 call('category.rtc_name10.config_file'),
                                 call('category.rtc_name11.config_file'),
                                 call('category.rtc_name12.config_file'),
                                 call('category.rtc_name13.config_file'),
                                 call('category.rtc_name14.config_file'),
                                 call('category.rtc_name15.config_file')])

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=False)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.uninstall_standalone_rtc_from_package', return_value=True)
    @mock.patch('sys.stdout.write')
    def test_uninstall_rtc_from_package_4(self, mock_write, mock_uninstall_standalone_rtc_from_package, mock_is_installed):
        """uninstall_rtc_from_package Java case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Java'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        remove = MagicMock()
        type(rtcconf).remove = remove
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        ### test ###
        self.plugin.uninstall_rtc_from_package(package, rtc, rtcconf_filename='rtcconf_filename', verbose=True)
        mock_write.assert_any_call('## Uninstall RTC (rtc_name) from package\n')
        remove.assert_has_calls([call('manager.components.precreate', 'rtc_name', verbose=True),
                                 call('manager.components.precreate'),
                                 call('manager.modules.preload', 'rtc_name.jar', verbose=True),
                                 call('manager.modules.preload'),
                                 call('manager.modules.load_path'),
                                 call('category.rtc_name.config_file'),
                                 call('category.rtc_name0.config_file'),
                                 call('category.rtc_name1.config_file'),
                                 call('category.rtc_name2.config_file'),
                                 call('category.rtc_name3.config_file'),
                                 call('category.rtc_name4.config_file'),
                                 call('category.rtc_name5.config_file'),
                                 call('category.rtc_name6.config_file'),
                                 call('category.rtc_name7.config_file'),
                                 call('category.rtc_name8.config_file'),
                                 call('category.rtc_name9.config_file'),
                                 call('category.rtc_name10.config_file'),
                                 call('category.rtc_name11.config_file'),
                                 call('category.rtc_name12.config_file'),
                                 call('category.rtc_name13.config_file'),
                                 call('category.rtc_name14.config_file'),
                                 call('category.rtc_name15.config_file')])

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.is_installed', return_value=False)
    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin.uninstall_standalone_rtc_from_package', return_value=True)
    @mock.patch('sys.stdout.write')
    def test_uninstall_rtc_from_package_5(self, mock_write, mock_uninstall_standalone_rtc_from_package, mock_is_installed):
        """uninstall_rtc_from_package Python case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Python'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        remove = MagicMock()
        type(rtcconf).remove = remove
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        ### test ###
        self.plugin.uninstall_rtc_from_package(package, rtc, rtcconf_filename='rtcconf_filename', verbose=True)
        mock_write.assert_any_call('## Uninstall RTC (rtc_name) from package\n')
        remove.assert_has_calls([call('manager.components.precreate', 'rtc_name', verbose=True),
                                 call('manager.components.precreate'),
                                 call('manager.modules.preload', 'rtc_name.py', verbose=True),
                                 call('manager.modules.preload'),
                                 call('manager.modules.load_path'),
                                 call('category.rtc_name.config_file'),
                                 call('category.rtc_name0.config_file'),
                                 call('category.rtc_name1.config_file'),
                                 call('category.rtc_name2.config_file'),
                                 call('category.rtc_name3.config_file'),
                                 call('category.rtc_name4.config_file'),
                                 call('category.rtc_name5.config_file'),
                                 call('category.rtc_name6.config_file'),
                                 call('category.rtc_name7.config_file'),
                                 call('category.rtc_name8.config_file'),
                                 call('category.rtc_name9.config_file'),
                                 call('category.rtc_name10.config_file'),
                                 call('category.rtc_name11.config_file'),
                                 call('category.rtc_name12.config_file'),
                                 call('category.rtc_name13.config_file'),
                                 call('category.rtc_name14.config_file'),
                                 call('category.rtc_name15.config_file')])

    @mock.patch('sys.stdout.write')
    def test_uninstall_all_rtc_from_package_1(self, mock_write):
        """uninstall_all_rtc_from_package normal case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Python'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        remove = MagicMock()
        type(rtcconf).remove = remove
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        ### test ###
        self.plugin.uninstall_all_rtc_from_package(package, rtcconf_filename='rtcconf_filename', verbose=True)
        remove.assert_has_calls([call('manager.components.precreate'),
                                 call('manager.modules.preload'),
                                 call('manager.modules.load_path')])

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin._Plugin__get_rtc_name_from_standalone_command', return_value='rtc_name')
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('sys.stdout.write')
    def test_uninstall_standalone_rtc_from_package_1(self, mock_write, mock_timestampstr, mock_dump, mock_safe_load, mock_open, mock_mkdir, mock_isdir, mock_copy, mock_get_rtc_name_from_standalone_command):
        """uninstall_all_rtc_from_package delete all command case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        type(rtcconf).append = MagicMock(return_value=1)
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        application = {'standalone': ['target/targetfile -f conf/rtc_rtc_name.conf']}
        mock_safe_load.return_value = {'application': application}

        ### test ###
        self.assertEqual(0, self.plugin.uninstall_standalone_rtc_from_package(package, rtc, verbose=True))
        mock_open.assert_has_calls([call('package_path/backup/setting.yaml20211001000000', 'r'), call('package_path/setting.yaml', 'w')])
        mock_dump.assert_called_once_with({'application': {}}, default_flow_style=False)

    @mock.patch('wasanbon.core.plugins.admin.systeminstaller_plugin.Plugin._Plugin__get_rtc_name_from_standalone_command', return_value='rtc_name')
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isdir')
    @mock.patch('os.mkdir')
    @mock.patch('builtins.open')
    @mock.patch('yaml.safe_load')
    @mock.patch('yaml.dump')
    @mock.patch('wasanbon.timestampstr', return_value='20211001000000')
    @mock.patch('sys.stdout.write')
    def test_uninstall_standalone_rtc_from_package_2(self, mock_write, mock_timestampstr, mock_dump, mock_safe_load, mock_open, mock_mkdir, mock_isdir, mock_copy, mock_get_rtc_name_from_standalone_command):
        """uninstall_all_rtc_from_package delete one command case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile

        rtcconf = MagicMock()
        type(rtcconf).append = MagicMock(return_value=1)
        RTCConf = MagicMock(return_value=rtcconf)
        type(self.admin_mock.rtcconf).RTCConf = RTCConf

        application = {'standalone': ['target/targetfile -f conf/rtc_rtc_name.conf', 'target/nottargetfile -f conf/rtc_rtc_name.conf']}
        mock_safe_load.return_value = {'application': application}

        ### test ###
        self.assertEqual(0, self.plugin.uninstall_standalone_rtc_from_package(package, rtc, verbose=True))
        mock_open.assert_has_calls([call('package_path/backup/setting.yaml20211001000000', 'r'), call('package_path/setting.yaml', 'w')])
        mock_dump.assert_called_once_with(
            {'application': {'standalone': ['target/nottargetfile -f conf/rtc_rtc_name.conf']}}, default_flow_style=False)

    @mock.patch('sys.stdout.write')
    def test_copy_binary_from_rtc_1(self, mock_write):
        """copy_binary_from_rtc not standalone python"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'Python'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile
        type(rtc).get_rtc_executable_file_path = MagicMock(return_value='./executable_file_path')
        type(rtc).get_rtc_file_path = MagicMock(return_value='./file_path')

        ### test ###
        self.assertEqual('file_path', self.Func.copy_binary_from_rtc(package, rtc, verbose=True, standalone=False))

    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.mkdir')
    @mock.patch('shutil.copy')
    @mock.patch('sys.stdout.write')
    def test_copy_binary_from_rtc_2(self, mock_write, mock_copy, mock_mkdir, mock_isdir):
        """copy_binary_from_rtc standalone C++"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile
        type(rtc).get_rtc_executable_file_path = MagicMock(return_value='./executable_file_path')
        type(rtc).get_rtc_file_path = MagicMock(return_value='./file_path')

        ### test ###
        self.assertEqual('bin/executable_file_path', self.Func.copy_binary_from_rtc(package, rtc, verbose=True, standalone=True))
        mock_copy.assert_called_once_with('./executable_file_path', 'bin/executable_file_path')

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='linux'))
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.mkdir')
    @mock.patch('shutil.copy')
    @mock.patch('os.listdir', return_value=['file_path.so'])
    @mock.patch('sys.stdout.write')
    def test_copy_binary_from_rtc_3(self, mock_listdir, mock_write, mock_copy, mock_mkdir, mock_isdir, mock_platform):
        """copy_binary_from_rtc not standalone C++ linux"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile
        type(rtc).get_rtc_executable_file_path = MagicMock(return_value='./executable_file_path')
        type(rtc).get_rtc_file_path = MagicMock(return_value='./file_path.aaa')

        ### test ###
        self.assertEqual('bin/file_path.aaa', self.Func.copy_binary_from_rtc(package, rtc, verbose=True, standalone=False))
        mock_copy.assert_has_calls([call('./file_path.aaa', 'bin/file_path.aaa'),
                                    call('./file_path.aaa', 'bin/file_path.so')])

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.mkdir')
    @mock.patch('shutil.copy')
    @mock.patch('os.listdir', return_value=['file_path.dll'])
    @mock.patch('sys.stdout.write')
    def test_copy_binary_from_rtc_4(self, mock_listdir, mock_write, mock_copy, mock_mkdir, mock_isdir, mock_platform):
        """copy_binary_from_rtc not standalone C++ win32"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile
        type(rtc).get_rtc_executable_file_path = MagicMock(return_value='./executable_file_path')
        type(rtc).get_rtc_file_path = MagicMock(return_value='./file_path.aaa')

        ### test ###
        self.assertEqual('bin/file_path.aaa', self.Func.copy_binary_from_rtc(package, rtc, verbose=True, standalone=False))
        mock_copy.assert_has_calls([call('./file_path.aaa', 'bin/file_path.aaa'),
                                    call('./file_path.aaa', 'bin/file_path.dll')])

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.mkdir')
    @mock.patch('shutil.copy')
    @mock.patch('os.listdir', return_value=['file_path.dylib'])
    @mock.patch('sys.stdout.write')
    def test_copy_binary_from_rtc_5(self, mock_listdir, mock_write, mock_copy, mock_mkdir, mock_isdir, mock_platform):
        """copy_binary_from_rtc not standalone C++ darwin"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile
        type(rtc).get_rtc_executable_file_path = MagicMock(return_value='./executable_file_path')
        type(rtc).get_rtc_file_path = MagicMock(return_value='./file_path.aaa')

        ### test ###
        self.assertEqual('bin/file_path.aaa', self.Func.copy_binary_from_rtc(package, rtc, verbose=True, standalone=False))
        mock_copy.assert_has_calls([call('./file_path.aaa', 'bin/file_path.aaa'),
                                    call('./file_path.aaa', 'bin/file_path.dylib')])

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    @mock.patch('os.path.isdir', return_value=True)
    @mock.patch('os.mkdir')
    @mock.patch('shutil.copy')
    @mock.patch('os.listdir', return_value=['file_path.dylib'])
    @mock.patch('sys.stdout.write')
    def test_copy_binary_from_rtc_6(self, mock_listdir, mock_write, mock_copy, mock_mkdir, mock_isdir, mock_platform):
        """copy_binary_from_rtc not file"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile
        type(rtc).get_rtc_executable_file_path = MagicMock(return_value='')
        type(rtc).get_rtc_file_path = MagicMock(return_value='')

        ### test ###
        self.assertEqual('', self.Func.copy_binary_from_rtc(package, rtc, verbose=True, standalone=False))

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='darwin'))
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('sys.stdout.write')
    def test_copy_conf_from_rtc_1(self, mock_write, mock_isfile, mock_copy, mock_platform):
        """copy_conf_from_rtc not force case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile
        type(rtc).get_rtc_conf_path = MagicMock(return_value='rtc_conf_path')

        ### test ###
        self.assertEqual('conf/rtc_conf0.conf', self.Func.copy_conf_from_rtc(package, rtc, verbose=True, force=False))
        mock_write.assert_any_call('## Do not copy.\n')

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('sys.stdout.write')
    def test_copy_conf_from_rtc_2(self, mock_write, mock_isfile, mock_copy, mock_platform):
        """copy_conf_from_rtc aforce case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile
        type(rtc).get_rtc_conf_path = MagicMock(return_value='rtc_conf_path')

        ### test ###
        self.assertEqual('conf/rtc_conf0.conf', self.Func.copy_conf_from_rtc(package, rtc, verbose=True, force=True))
        mock_copy.assert_called_once_with('rtc_conf_path', 'package_path/conf/rtc_conf0.conf')
        mock_write.assert_any_call('## Force Copying Config (rtc_conf_path -> package_path/conf/rtc_conf0.conf)\n')

    @mock.patch('sys.platform', new_callable=PropertyMock(return_value='win32'))
    @mock.patch('shutil.copy')
    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('sys.stdout.write')
    def test_copy_conf_from_rtc_3(self, mock_write, mock_isfile, mock_copy, mock_platform):
        """copy_conf_from_rtc not confile case"""

        package = MagicMock()
        type(package).name = 'package_name'
        type(package).path = 'package_path'
        type(package).get_binpath = MagicMock(return_value='bin')
        type(package).get_confpath = MagicMock(return_value='conf')
        setting = MagicMock()
        type(setting).get = MagicMock(return_value=['target/targetfile -f conf/rtc_rtc_name.conf'])
        type(package).setting = setting
        rtc = MagicMock()
        type(rtc).name = 'rtc_name'
        type(rtc).get_rtc_file_path = MagicMock(return_value='rtc_file_path')
        rtcprofile = MagicMock()
        basicInfo = MagicMock()
        type(basicInfo).name = 'rtc_name'
        type(basicInfo).category = 'category'
        type(rtcprofile).basicInfo = basicInfo
        language = MagicMock()
        type(language).kind = 'C++'
        type(rtcprofile).language = language
        type(rtc).rtcprofile = rtcprofile
        type(rtc).get_rtc_conf_path = MagicMock(return_value='')

        ### test ###
        self.assertEqual([], self.Func.copy_conf_from_rtc(package, rtc, verbose=True, force=True))
        mock_write.assert_called_once_with('## No configuration file for RTC (rtc_name) is found.\n')


if __name__ == '__main__':
    unittest.main()
